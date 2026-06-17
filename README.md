# Password Manager

Secure desktop password manager with encryption, built with Python and CustomTkinter.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features

- **AES-256 encryption** — all passwords encrypted with Fernet + PBKDF2 (480,000 iterations)
- **Master password** — single password to access all credentials
- **Password generator** — configurable length (4–64), character sets (A-Z, a-z, 0-9, symbols)
- **CRUD operations** — add, edit, delete entries with duplicate detection
- **Search** — instant filter by service or login name
- **Export / Import** — JSON backup encrypted with your master password
- **Restore from backup** — recover all passwords on a new computer
- **Themes** — Light, Dark, System (auto)
- **Localization** — English and Russian
- **Hotkeys** — Ctrl+C/V/X/A for fields, Ctrl+C for table rows
- **Context menus** — right-click copy for login, password, or service
- **Auto-close** — optional inactivity timer (configurable in settings)

## Screenshots

<p align="center">
  <img src="https://img.shields.io/badge/Dark%20Theme-1e1e2e?style=for-the-badge&labelColor=7c3aed" alt="Dark Theme">
  <img src="https://img.shields.io/badge/Light%20Theme-f0f0f0?style=for-the-badge&labelColor=3b82f6" alt="Light Theme">
</p>

## Installation

### Windows (Pre-built)

1. Download `PasswordManager.exe` from [Releases](https://github.com/Astapov-source/PasswordManager/releases)
2. Run the executable — no installation required
3. Data is stored in `%APPDATA%/PasswordManager/`

### Windows / Linux (From source)

```bash
# Clone the repository
git clone https://github.com/Astapov-source/PasswordManager.git
cd PasswordManager

# Install dependencies
pip install customtkinter cryptography

# Run the application
python main.py
```

### Build executable yourself

```bash
pip install pyinstaller
python build.py
# Output: dist/PasswordManager.exe
```

## Requirements

| Dependency | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Runtime |
| customtkinter | 5.2+ | Modern GUI |
| cryptography | 41.0+ | Fernet encryption + PBKDF2 |
| PyInstaller | 6.0+ | Building .exe (optional) |

### System requirements

- **Windows**: 10 or later (x64)
- **Linux**: any distro with Python 3.10+ and tkinter
- **RAM**: ~50 MB
- **Disk**: ~20 MB (app) + minimal (database)

## How it works

### Encryption

All passwords are encrypted at rest using **Fernet symmetric encryption** (AES-128-CBC). The encryption key is derived from your master password via **PBKDF2-HMAC-SHA256** with 480,000 iterations and a random 16-byte salt. The salt is stored alongside the database — without the master password, data is unrecoverable.

```
Master Password → PBKDF2 (480k iterations) → Fernet Key → Encrypt/Decrypt
```

### Data storage

| OS | Location |
|----|----------|
| Windows | `%APPDATA%/PasswordManager/` |
| Linux | `~/.password-manager/` |

Files:
- `passwords.db` — SQLite database with encrypted passwords
- `passwords.db.salt` — PBKDF2 salt (required for decryption)
- `settings.json` — preferences (language, theme)

### Backup & Restore

**Export**: Creates a JSON file with all entries encrypted with your current master password.

**Restore on new computer**:
1. Run the app → choose **"Restore from Backup"**
2. Select the exported JSON file
3. Enter your master password
4. All entries are decrypted and re-encrypted with a new key

## Usage

1. **First launch** — choose "Create New Account" or "Restore from Backup"
2. **Add entry** — fill Service, Login, Password fields → click "Add"
3. **Generate password** — adjust length/character sets → click "Generate"
4. **Edit** — double-click a row → modify fields → click "Save"
5. **Delete** — select row → click "Delete" → confirm
6. **Search** — type in the search bar to filter by service name
7. **Copy** — right-click row → "Copy Login" / "Copy Password" / "Copy Service"
8. **Settings** — click ⚙ to change theme, master password, export/import

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Copy selected text or table row |
| `Ctrl+V` | Paste from clipboard |
| `Ctrl+X` | Cut selected text |
| `Ctrl+A` | Select all text |
| `F11` | Toggle fullscreen |
| `Escape` | Exit fullscreen |

## Project structure

```
PasswordManager/
├── main.py                    # CustomTkinter application (entry point)
├── password_manager.py        # Legacy Tkinter version (backup)
├── test_core.py               # Unit tests (15 tests)
├── build.py                   # PyInstaller build script
├── PasswordManager.bat        # Windows launcher
├── AGENTS.md                  # Developer notes
├── .gitignore                 # Git ignore rules
└── README.md
```

## For developers

```bash
# Run tests
python test_core.py

# Build exe (Windows)
python build.py

# Dependencies
pip install customtkinter cryptography pyinstaller
```

## License

MIT License — free to use, modify, and distribute.

---

<p align="center">
  <sub>Built with Python + CustomTkinter</sub>
</p>
