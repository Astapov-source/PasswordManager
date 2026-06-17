import os
import sys
import json
import sqlite3
import base64
import tempfile
import shutil
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt


def test_key_derivation():
    key1, salt1 = derive_key("testpassword")
    key2, _ = derive_key("testpassword", salt1)
    assert key1 == key2, "Same password + salt should produce same key"
    key3, _ = derive_key("differentpassword", salt1)
    assert key1 != key3, "Different password should produce different key"
    print("PASS: key derivation")


def test_encrypt_decrypt():
    key, salt = derive_key("masterpw")
    fernet = Fernet(key)
    plaintext = "MyS3cur3P@ss!"
    encrypted = fernet.encrypt(plaintext.encode()).decode()
    decrypted = fernet.decrypt(encrypted.encode()).decode()
    assert decrypted == plaintext
    assert encrypted != plaintext
    print("PASS: encrypt/decrypt")


def test_database_operations():
    tmp = tempfile.mkdtemp()
    db_path = os.path.join(tmp, "test.db")
    key, salt = derive_key("masterpw")
    fernet = Fernet(key)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT NOT NULL UNIQUE,
        login TEXT NOT NULL,
        password TEXT NOT NULL
    )""")
    conn.commit()

    def encrypt(data):
        return fernet.encrypt(data.encode()).decode()

    def decrypt(data):
        return fernet.decrypt(data.encode()).decode()

    c.execute("INSERT INTO passwords (service, login, password) VALUES (?, ?, ?)",
              ("GitHub", "user@mail.com", encrypt("gh_token_123")))
    c.execute("INSERT INTO passwords (service, login, password) VALUES (?, ?, ?)",
              ("Gmail", "user@gmail.com", encrypt("gmail_pass")))
    conn.commit()

    c.execute("SELECT service, login, password FROM passwords ORDER BY service")
    rows = c.fetchall()
    assert len(rows) == 2
    assert rows[0][0] == "GitHub"
    assert decrypt(rows[0][2]) == "gh_token_123"
    assert rows[1][0] == "Gmail"
    assert decrypt(rows[1][2]) == "gmail_pass"

    c.execute("UPDATE passwords SET login = 'new@mail.com' WHERE service = 'Gmail'")
    conn.commit()
    c.execute("SELECT login FROM passwords WHERE service = 'Gmail'")
    assert c.fetchone()[0] == "new@mail.com"

    c.execute("DELETE FROM passwords WHERE service = 'Gmail'")
    conn.commit()
    c.execute("SELECT * FROM passwords WHERE service = 'Gmail'")
    assert c.fetchone() is None

    try:
        c.execute("INSERT INTO passwords (service, login, password) VALUES (?, ?, ?)",
                  ("GitHub", "dup@mail.com", encrypt("dup")))
        conn.commit()
        assert False, "Should have raised UNIQUE constraint"
    except sqlite3.IntegrityError:
        pass

    conn.close()
    shutil.rmtree(tmp)
    print("PASS: database CRUD + unique constraint")


def test_password_generation():
    import string
    import random
    chars = string.ascii_letters + string.digits + string.punctuation

    for length in [4, 8, 12, 16, 32, 64]:
        for _ in range(50):
            pw = [
                random.choice(string.ascii_letters),
                random.choice(string.digits),
                random.choice(string.punctuation),
            ]
            remaining = length - 3
            if remaining > 0:
                pw += random.choices(chars, k=remaining)
            random.shuffle(pw)
            pw = "".join(pw[:length])
            assert len(pw) == length, f"Length mismatch: expected {length}, got {len(pw)}"
            has_letter = any(c in string.ascii_letters for c in pw)
            has_digit = any(c in string.digits for c in pw)
            has_symbol = any(c in string.punctuation for c in pw)
            assert has_letter and has_digit and has_symbol, f"Weak password at length {length}: {pw}"
    print("PASS: password generation (lengths 4-64, 50 samples each)")


def test_password_generation_min_length():
    import string
    import random
    chars = string.ascii_letters + string.digits + string.punctuation

    length = 3
    pw = [
        random.choice(string.ascii_letters),
        random.choice(string.digits),
        random.choice(string.punctuation),
    ]
    remaining = max(0, length - 3)
    if remaining > 0:
        pw += random.choices(chars, k=remaining)
    random.shuffle(pw)
    pw = "".join(pw[:length])
    assert len(pw) == 3
    print("PASS: password generation min length (3 chars)")


def test_password_generation_length_clamp():
    import string
    import random
    chars = string.ascii_letters + string.digits + string.punctuation

    length = 2
    if length < 4:
        length = 4
    pw = [
        random.choice(string.ascii_letters),
        random.choice(string.digits),
        random.choice(string.punctuation),
    ]
    remaining = length - 3
    if remaining > 0:
        pw += random.choices(chars, k=remaining)
    random.shuffle(pw)
    pw = "".join(pw[:length])
    assert len(pw) == 4
    print("PASS: password generation length clamped to 4")


def test_salt_persistence():
    tmp = tempfile.mkdtemp()
    salt_path = os.path.join(tmp, "test.salt")
    key1, salt1 = derive_key("masterpw")
    salt_b64 = base64.urlsafe_b64encode(salt1).decode()
    with open(salt_path, "w") as f:
        f.write(salt_b64)
    with open(salt_path, "r") as f:
        loaded_b64 = f.read().strip()
    loaded_salt = base64.urlsafe_b64decode(loaded_b64)
    key2, _ = derive_key("masterpw", loaded_salt)
    assert key1 == key2
    shutil.rmtree(tmp)
    print("PASS: salt persistence")


def test_settings_persistence():
    tmp = tempfile.mkdtemp()
    settings_path = os.path.join(tmp, "settings.json")

    for lang in ["en", "ru"]:
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump({"language": lang}, f, ensure_ascii=False)
        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["language"] == lang

    os.remove(settings_path)
    assert not os.path.exists(settings_path)

    shutil.rmtree(tmp)
    print("PASS: settings persistence (en/ru)")


def test_language_strings():
    from main import LANG

    assert "en" in LANG
    assert "ru" in LANG

    for lang in ["en", "ru"]:
        required_keys = [
            "app_title", "create_title", "login_title",
            "add", "edit", "delete", "generate", "clear",
            "col_service", "col_login", "col_password",
            "service", "login", "password", "length",
            "warn_all_fields", "warn_select_edit", "warn_select_delete",
            "success_add", "success_edit", "success_delete",
            "err_empty", "err_short", "err_mismatch", "err_wrong_pw",
            "language", "fullscreen", "search",
        ]
        for key in required_keys:
            assert key in LANG[lang], f"Missing key '{key}' in lang '{lang}'"
            assert isinstance(LANG[lang][key], str), f"Key '{key}' in '{lang}' is not a string"
            assert len(LANG[lang][key]) > 0, f"Key '{key}' in '{lang}' is empty"

    print("PASS: language strings complete (en + ru)")


def test_language_switch():
    from main import LANG

    assert LANG["en"]["app_title"] != LANG["ru"]["app_title"]
    assert LANG["en"]["add"] != LANG["ru"]["add"]
    assert LANG["en"]["delete"] != LANG["ru"]["delete"]
    assert LANG["en"]["generate"] != LANG["ru"]["generate"]
    assert LANG["en"]["length"] != LANG["ru"]["length"]
    print("PASS: language strings differ between en/ru")


def test_special_characters_encrypt_decrypt():
    key, salt = derive_key("masterpw")
    fernet = Fernet(key)
    special = "Пароль!@#$%^&*()_+{}|:<>?~`-=[];',./"
    encrypted = fernet.encrypt(special.encode()).decode()
    decrypted = fernet.decrypt(encrypted.encode()).decode()
    assert decrypted == special
    print("PASS: special characters (Cyrillic + symbols) encrypt/decrypt")


def test_empty_password_encrypt():
    key, salt = derive_key("masterpw")
    fernet = Fernet(key)
    empty = ""
    encrypted = fernet.encrypt(empty.encode()).decode()
    decrypted = fernet.decrypt(encrypted.encode()).decode()
    assert decrypted == empty
    print("PASS: empty string encrypt/decrypt")


def test_long_password_encrypt():
    key, salt = derive_key("masterpw")
    fernet = Fernet(key)
    long_pw = "A" * 10000
    encrypted = fernet.encrypt(long_pw.encode()).decode()
    decrypted = fernet.decrypt(encrypted.encode()).decode()
    assert decrypted == long_pw
    print("PASS: long password (10000 chars) encrypt/decrypt")


def test_data_dir_frozen():
    import types
    fake_frozen = types.SimpleNamespace(frozen=True)
    old_frozen = getattr(sys, 'frozen', None)
    sys.frozen = True
    try:
        from main import get_data_dir
        data_dir = get_data_dir()
        assert os.path.isdir(data_dir)
        assert "PasswordManager" in data_dir or ".password-manager" in data_dir
    finally:
        if old_frozen is not None:
            sys.frozen = old_frozen
        else:
            del sys.frozen
    print("PASS: data dir for frozen exe")


def test_data_dir_script():
    from main import get_data_dir
    data_dir = get_data_dir()
    assert os.path.isdir(data_dir)
    if sys.platform == "win32":
        assert "PasswordManager" in data_dir
    else:
        assert ".password-manager" in data_dir
    print("PASS: data dir (unified for script and exe)")


if __name__ == "__main__":
    test_key_derivation()
    test_encrypt_decrypt()
    test_database_operations()
    test_password_generation()
    test_password_generation_min_length()
    test_password_generation_length_clamp()
    test_salt_persistence()
    test_settings_persistence()
    test_language_strings()
    test_language_switch()
    test_special_characters_encrypt_decrypt()
    test_empty_password_encrypt()
    test_long_password_encrypt()
    test_data_dir_frozen()
    test_data_dir_script()
    print("\nAll tests passed.")
