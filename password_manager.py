import os
import sys
import json
import sqlite3
import string
import random
import base64
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

COLORS = {
    "bg": "#1e1e2e",
    "surface": "#282840",
    "input": "#313150",
    "accent": "#7c3aed",
    "accent_hover": "#6d28d9",
    "accent_active": "#5b21b6",
    "danger": "#ef4444",
    "danger_hover": "#dc2626",
    "success": "#22c55e",
    "success_bg": "#166534",
    "warning": "#eab308",
    "warning_bg": "#854d0e",
    "error": "#ef4444",
    "error_bg": "#991b1b",
    "info": "#3b82f6",
    "info_bg": "#1e3a5f",
    "text": "#e2e8f0",
    "text_dim": "#94a3b8",
    "border": "#3b3b5c",
    "tree_bg": "#282840",
    "tree_select": "#7c3aed",
    "tree_fg": "#e2e8f0",
    "entry_bg": "#313150",
    "entry_fg": "#e2e8f0",
    "entry_insert": "#e2e8f0",
    "tooltip_bg": "#3b3b5c",
    "tooltip_fg": "#e2e8f0",
    "spinbox_fg": "#e2e8f0",
}

LANG = {
    "en": {
        "app_title": "Password Manager",
        "create_title": "Create Master Password",
        "create_label": "Create a master password:",
        "confirm_label": "Confirm password:",
        "create_btn": "Create",
        "login_title": "Enter Master Password",
        "login_label": "Enter your master password:",
        "unlock_btn": "Unlock",
        "err_empty": "Password cannot be empty",
        "err_short": "Password must be at least 8 characters",
        "err_mismatch": "Passwords do not match",
        "err_no_salt": "Salt file not found",
        "err_wrong_pw": "Incorrect master password",
        "credentials": "Credentials",
        "service": "Service",
        "login": "Login",
        "password": "Password",
        "length": "Length",
        "add": "Add",
        "edit": "Save",
        "delete": "Delete",
        "generate": "Generate",
        "clear": "Clear",
        "col_service": "Service",
        "col_login": "Login",
        "col_password": "Password",
        "warn_all_fields": "All fields must be filled",
        "warn_select_edit": "Select an entry to edit",
        "warn_select_delete": "Select an entry to delete",
        "warn_duplicate": "Service '{service}' already exists",
        "confirm_delete": "Delete '{service}'?",
        "success_add": "Entry added",
        "success_edit": "Entry updated",
        "success_delete": "Entry deleted",
        "err_load": "Failed to load data: {err}",
        "err_add": "Failed to add: {err}",
        "err_edit": "Failed to edit: {err}",
        "err_delete": "Failed to delete: {err}",
        "language": "Language",
        "fullscreen": "Fullscreen",
        "search": "Search...",
        "change_master_pw": "Change Master Password",
        "change_master_title": "Change Master Password",
        "current_password": "Current password:",
        "new_password": "New password:",
        "confirm_new_password": "Confirm new password:",
        "err_current_empty": "Current password cannot be empty",
        "err_new_empty": "New password cannot be empty",
        "err_new_short": "New password must be at least 8 characters",
        "err_new_mismatch": "New passwords do not match",
        "err_current_wrong": "Current password is incorrect",
        "success_master_pw": "Master password changed successfully",
        "ctx_copy": "Copy",
        "ctx_copy_login": "Copy Login",
        "ctx_copy_password": "Copy Password",
        "ctx_copy_service": "Copy Service",
        "ctx_cut": "Cut",
        "ctx_paste": "Paste",
        "ctx_select_all": "Select All",
        "gen_uppercase": "A-Z",
        "gen_lowercase": "a-z",
        "gen_digits": "0-9",
        "gen_symbols": "!@#",
        "err_gen_no_chars": "Select at least one character type",
    },
    "ru": {
        "app_title": "Менеджер паролей",
        "create_title": "Создать мастер-пароль",
        "create_label": "Создайте мастер-пароль:",
        "confirm_label": "Подтвердите пароль:",
        "create_btn": "Создать",
        "login_title": "Введите мастер-пароль",
        "login_label": "Введите ваш мастер-пароль:",
        "unlock_btn": "Войти",
        "err_empty": "Пароль не может быть пустым",
        "err_short": "Пароль должен содержать минимум 8 символов",
        "err_mismatch": "Пароли не совпадают",
        "err_no_salt": "Файл соли не найден",
        "err_wrong_pw": "Неверный мастер-пароль",
        "credentials": "Учётные данные",
        "service": "Сервис",
        "login": "Логин",
        "password": "Пароль",
        "length": "Длина",
        "add": "Добавить",
        "edit": "Сохранить",
        "delete": "Удалить",
        "generate": "Сгенерировать",
        "clear": "Очистить",
        "col_service": "Сервис",
        "col_login": "Логин",
        "col_password": "Пароль",
        "warn_all_fields": "Все поля должны быть заполнены",
        "warn_select_edit": "Выберите запись для редактирования",
        "warn_select_delete": "Выберите запись для удаления",
        "warn_duplicate": "Сервис '{service}' уже существует",
        "confirm_delete": "Удалить '{service}'?",
        "success_add": "Запись добавлена",
        "success_edit": "Запись обновлена",
        "success_delete": "Запись удалена",
        "err_load": "Ошибка загрузки: {err}",
        "err_add": "Ошибка добавления: {err}",
        "err_edit": "Ошибка редактирования: {err}",
        "err_delete": "Ошибка удаления: {err}",
        "language": "Язык",
        "fullscreen": "Полный экран",
        "search": "Поиск...",
        "change_master_pw": "Сменить мастер-пароль",
        "change_master_title": "Смена мастер-пароля",
        "current_password": "Текущий пароль:",
        "new_password": "Новый пароль:",
        "confirm_new_password": "Подтвердите новый пароль:",
        "err_current_empty": "Текущий пароль не может быть пустым",
        "err_new_empty": "Новый пароль не может быть пустым",
        "err_new_short": "Новый пароль должен содержать минимум 8 символов",
        "err_new_mismatch": "Новые пароли не совпадают",
        "err_current_wrong": "Неверный текущий пароль",
        "success_master_pw": "Мастер-пароль успешно изменён",
        "ctx_copy": "Копировать",
        "ctx_copy_login": "Копировать логин",
        "ctx_copy_password": "Копировать пароль",
        "ctx_copy_service": "Копировать сервис",
        "ctx_cut": "Вырезать",
        "ctx_paste": "Вставить",
        "ctx_select_all": "Выделить всё",
        "gen_uppercase": "A-Z",
        "gen_lowercase": "a-z",
        "gen_digits": "0-9",
        "gen_symbols": "!@#",
        "err_gen_no_chars": "Выберите хотя бы один тип символов",
    },
}


def get_data_dir():
    if getattr(sys, 'frozen', False):
        app_name = "PasswordManager"
        if sys.platform == "win32":
            base = os.environ.get("APPDATA", os.path.expanduser("~"))
        else:
            base = os.path.expanduser("~")
            app_name = ".password-manager"
        data_dir = os.path.join(base, app_name)
    else:
        data_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


class Toast:
    def __init__(self, parent, text, toast_type="info", duration=2000):
        self.parent = parent
        self.win = tk.Toplevel(parent)
        self.win.wm_overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.configure(bg=COLORS["bg"])

        colors = {
            "success": (COLORS["success"], COLORS["success_bg"]),
            "error": (COLORS["error"], COLORS["error_bg"]),
            "warning": (COLORS["warning"], COLORS["warning_bg"]),
            "info": (COLORS["info"], COLORS["info_bg"]),
        }
        fg, bg = colors.get(toast_type, colors["info"])

        icons = {"success": "\u2714", "error": "\u2718", "warning": "\u26A0", "info": "\u2139"}
        icon = icons.get(toast_type, "")

        frame = tk.Frame(self.win, bg=bg, highlightbackground=fg, highlightthickness=2)
        frame.pack(fill=tk.BOTH, expand=True)

        content = tk.Frame(frame, bg=bg)
        content.pack(fill=tk.BOTH, expand=True, padx=16, pady=10)

        tk.Label(content, text=icon, bg=bg, fg=fg, font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(content, text=text, bg=bg, fg=COLORS["text"], font=("Segoe UI", 11),
                 wraplength=400, justify=tk.LEFT).pack(side=tk.LEFT, fill=tk.X, expand=True)

        parent.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()

        self.win.update_idletasks()
        tw = self.win.winfo_width()
        th = self.win.winfo_height()

        x = px + (pw - tw) // 2
        y = py + (ph - th) // 2

        self.win.wm_geometry(f"+{x}+{y}")
        self.win.after(duration, self._close)

    def _close(self):
        self.win.destroy()


class Tooltip:
    def __init__(self, widget, text, bg=None, fg=None):
        self.widget = widget
        self.text = text
        self.bg = bg or COLORS["tooltip_bg"]
        self.fg = fg or COLORS["tooltip_fg"]
        self.tip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tip, text=self.text, bg=self.bg, fg=self.fg,
                         font=("Segoe UI", 9), padx=8, pady=4,
                         highlightbackground=COLORS["border"], highlightthickness=1)
        label.pack()

    def hide(self, event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None

    def update_text(self, text):
        self.text = text


class PasswordManager:
    def __init__(self):
        self.data_dir = get_data_dir()
        self.db_path = os.path.join(self.data_dir, "passwords.db")
        self.settings_path = os.path.join(self.data_dir, "settings.json")
        self.master_key = None
        self.fernet = None
        self.settings = self._load_settings()
        self.lang_code = self.settings.get("language", "en")
        self.is_fullscreen = self.settings.get("fullscreen", False)
        self.text = LANG[self.lang_code]
        self._editing_service = None
        self._active_entries = []
        self._all_entries = []

        self.root = tk.Tk()
        self.root.title(self.text["app_title"])
        self.root.geometry("900x620")
        self.root.minsize(700, 500)
        self.root.configure(bg=COLORS["bg"])

        self.service_var = tk.StringVar()
        self.login_var = tk.StringVar()
        self.password_text = None
        self._pw_scrollbar_visible = False
        self.length_var = tk.IntVar(value=12)
        self.gen_upper_var = tk.BooleanVar(value=True)
        self.gen_lower_var = tk.BooleanVar(value=True)
        self.gen_digit_var = tk.BooleanVar(value=True)
        self.gen_symbol_var = tk.BooleanVar(value=True)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter_tree())

        self._setup_styles()

        self.root.bind("<F11>", self._toggle_fullscreen)
        self.root.bind("<Escape>", self._exit_fullscreen)
        self.root.bind("<Control-c>", self._hotkey_copy)
        self.root.bind("<Control-v>", self._hotkey_paste)
        self.root.bind("<Control-x>", self._hotkey_cut)
        self.root.bind("<Control-a>", self._hotkey_select_all)

        if self.is_fullscreen:
            self.root.after(100, lambda: self.root.attributes("-fullscreen", True))

        if self._db_exists():
            self._show_login_dialog()
        else:
            self._show_create_dialog()

    def _load_settings(self):
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"language": "en", "fullscreen": False}

    def _save_settings(self):
        self.settings["language"] = self.lang_code
        self.settings["fullscreen"] = self.is_fullscreen
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False)
        except Exception:
            pass

    def _db_exists(self):
        return os.path.exists(self.db_path)

    def _derive_key(self, password, salt=None):
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL UNIQUE,
                login TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def _encrypt(self, data):
        return self.fernet.encrypt(data.encode()).decode()

    def _decrypt(self, data):
        return self.fernet.decrypt(data.encode()).decode()

    def _t(self, key, **kwargs):
        s = self.text[key]
        return s.format(**kwargs) if kwargs else s

    def _show_toast(self, text, toast_type="info", duration=2000):
        Toast(self.root, text, toast_type, duration)

    def _get_password(self):
        if self.password_text:
            return self.password_text.get("1.0", "end-1c")
        return ""

    def _set_password(self, text):
        if self.password_text:
            self.password_text.delete("1.0", "end")
            self.password_text.insert("1.0", text)
            self.password_text.see("end")
            self._update_pw_scrollbar()

    def _update_pw_scrollbar(self, event=None):
        if not self.password_text:
            return
        first, last = self.password_text.xview()
        should_show = first > 0.0 or last < 1.0
        if should_show and not self._pw_scrollbar_visible:
            self.pw_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            self._pw_scrollbar_visible = True
        elif not should_show and self._pw_scrollbar_visible:
            self.pw_scrollbar.pack_forget()
            self._pw_scrollbar_visible = False

    def _toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        self._save_settings()

    def _exit_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes("-fullscreen", False)
            self._save_settings()

    def _get_focused_entry(self):
        widget = self.root.focus_get()
        if isinstance(widget, (tk.Entry, tk.Text)) and widget in self._active_entries:
            return widget
        return None

    def _hotkey_copy(self, event=None):
        entry = self._get_focused_entry()
        if entry:
            if isinstance(entry, tk.Text):
                try:
                    text = entry.get("sel.first", "sel.last")
                except tk.TclError:
                    text = entry.get("1.0", "end-1c")
            else:
                sel = entry.selection_range()
                if sel:
                    text = entry.get()[sel[0]:sel[1]]
                else:
                    text = entry.get()
            if text:
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
        elif hasattr(self, "tree"):
            selected = self.tree.selection()
            if selected:
                values = self.tree.item(selected[0])["values"]
                text = " | ".join(str(v) for v in values)
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
        return "break"

    def _hotkey_paste(self, event=None):
        entry = self._get_focused_entry()
        if entry:
            try:
                text = self.root.clipboard_get()
                if isinstance(entry, tk.Text):
                    try:
                        entry.delete("sel.first", "sel.last")
                    except tk.TclError:
                        pass
                    entry.insert(tk.INSERT, text)
                else:
                    sel = entry.selection_range()
                    if sel and sel[0] is not None:
                        entry.delete(sel[0], sel[1])
                    entry.insert(tk.INSERT, text)
            except tk.TclError:
                pass
        return "break"

    def _hotkey_cut(self, event=None):
        entry = self._get_focused_entry()
        if entry:
            if isinstance(entry, tk.Text):
                try:
                    text = entry.get("sel.first", "sel.last")
                    self.root.clipboard_clear()
                    self.root.clipboard_append(text)
                    entry.delete("sel.first", "sel.last")
                except tk.TclError:
                    pass
            else:
                sel = entry.selection_range()
                if sel:
                    text = entry.get()[sel[0]:sel[1]]
                    self.root.clipboard_clear()
                    self.root.clipboard_append(text)
                    entry.delete(sel[0], sel[1])
        return "break"

    def _show_entry_context_menu(self, event, widget):
        menu = tk.Menu(self.root, tearoff=0,
                       bg=COLORS["surface"], fg=COLORS["text"],
                       activebackground=COLORS["accent"],
                       activeforeground=COLORS["text"],
                       font=("Segoe UI", 10))
        has_selection = False
        if isinstance(widget, tk.Text):
            try:
                widget.get("sel.first", "sel.last")
                has_selection = True
            except tk.TclError:
                pass
        else:
            sel = widget.selection_range()
            has_selection = bool(sel and sel[0] is not None)

        def do_copy():
            if isinstance(widget, tk.Text):
                try:
                    text = widget.get("sel.first", "sel.last")
                except tk.TclError:
                    text = widget.get("1.0", "end-1c")
            else:
                sel = widget.selection_range()
                if sel:
                    text = widget.get()[sel[0]:sel[1]]
                else:
                    text = widget.get()
            if text:
                self.root.clipboard_clear()
                self.root.clipboard_append(text)

        def do_cut():
            if isinstance(widget, tk.Text):
                try:
                    text = widget.get("sel.first", "sel.last")
                    self.root.clipboard_clear()
                    self.root.clipboard_append(text)
                    widget.delete("sel.first", "sel.last")
                except tk.TclError:
                    pass
            else:
                sel = widget.selection_range()
                if sel:
                    text = widget.get()[sel[0]:sel[1]]
                    self.root.clipboard_clear()
                    self.root.clipboard_append(text)
                    widget.delete(sel[0], sel[1])

        def do_paste():
            try:
                text = self.root.clipboard_get()
                if isinstance(widget, tk.Text):
                    try:
                        widget.delete("sel.first", "sel.last")
                    except tk.TclError:
                        pass
                    widget.insert(tk.INSERT, text)
                else:
                    sel = widget.selection_range()
                    if sel and sel[0] is not None:
                        widget.delete(sel[0], sel[1])
                    widget.insert(tk.INSERT, text)
            except tk.TclError:
                pass

        def do_select_all():
            if isinstance(widget, tk.Text):
                widget.tag_add("sel", "1.0", "end-1c")
            else:
                widget.select_range(0, tk.END)

        menu.add_command(label=self._t("ctx_copy"), command=do_copy,
                         state=tk.NORMAL if has_selection else tk.DISABLED)
        menu.add_command(label=self._t("ctx_cut"), command=do_cut,
                         state=tk.NORMAL if has_selection else tk.DISABLED)
        menu.add_command(label=self._t("ctx_paste"), command=do_paste)
        menu.add_separator()
        menu.add_command(label=self._t("ctx_select_all"), command=do_select_all)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _show_tree_context_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0,
                       bg=COLORS["surface"], fg=COLORS["text"],
                       activebackground=COLORS["accent"],
                       activeforeground=COLORS["text"],
                       font=("Segoe UI", 10))

        selected = self.tree.selection()

        def do_copy():
            if selected:
                values = self.tree.item(selected[0])["values"]
                text = " | ".join(str(v) for v in values)
                self.root.clipboard_clear()
                self.root.clipboard_append(text)

        def do_copy_login():
            if selected:
                values = self.tree.item(selected[0])["values"]
                self.root.clipboard_clear()
                self.root.clipboard_append(str(values[1]))

        def do_copy_password():
            if selected:
                values = self.tree.item(selected[0])["values"]
                self.root.clipboard_clear()
                self.root.clipboard_append(str(values[2]))

        def do_copy_service():
            if selected:
                values = self.tree.item(selected[0])["values"]
                self.root.clipboard_clear()
                self.root.clipboard_append(str(values[0]))

        menu.add_command(label=self._t("ctx_copy"), command=do_copy,
                         state=tk.NORMAL if selected else tk.DISABLED)
        menu.add_separator()
        menu.add_command(label=self._t("ctx_copy_login"), command=do_copy_login,
                         state=tk.NORMAL if selected else tk.DISABLED)
        menu.add_command(label=self._t("ctx_copy_password"), command=do_copy_password,
                         state=tk.NORMAL if selected else tk.DISABLED)
        menu.add_command(label=self._t("ctx_copy_service"), command=do_copy_service,
                         state=tk.NORMAL if selected else tk.DISABLED)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _hotkey_select_all(self, event=None):
        entry = self._get_focused_entry()
        if entry:
            if isinstance(entry, tk.Text):
                entry.tag_add("sel", "1.0", "end-1c")
            else:
                entry.select_range(0, tk.END)
        return "break"

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background=COLORS["bg"], foreground=COLORS["text"],
                        borderwidth=0, focuscolor=COLORS["accent"])
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"],
                        font=("Segoe UI", 10))
        style.configure("Dim.TLabel", background=COLORS["bg"], foreground=COLORS["text_dim"],
                        font=("Segoe UI", 9))
        style.configure("Title.TLabel", background=COLORS["bg"], foreground=COLORS["text"],
                        font=("Segoe UI", 16, "bold"))

        style.configure("Accent.TButton", background=COLORS["accent"], foreground=COLORS["text"],
                        font=("Segoe UI", 10, "bold"), padding=(12, 6), borderwidth=0)
        style.map("Accent.TButton",
                   background=[("active", COLORS["accent_hover"]), ("pressed", COLORS["accent_active"])])

        style.configure("Danger.TButton", background=COLORS["danger"], foreground=COLORS["text"],
                        font=("Segoe UI", 10, "bold"), padding=(12, 6), borderwidth=0)
        style.map("Danger.TButton",
                   background=[("active", COLORS["danger_hover"])])

        style.configure("Ghost.TButton", background=COLORS["surface"], foreground=COLORS["text_dim"],
                        font=("Segoe UI", 10), padding=(12, 6), borderwidth=0)
        style.map("Ghost.TButton",
                   background=[("active", COLORS["input"])])

        style.configure("Treeview",
                        background=COLORS["tree_bg"],
                        foreground=COLORS["tree_fg"],
                        fieldbackground=COLORS["tree_bg"],
                        borderwidth=0,
                        font=("Segoe UI", 10),
                        rowheight=30)
        style.configure("Treeview.Heading",
                        background=COLORS["surface"],
                        foreground=COLORS["text_dim"],
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0, relief="flat")
        style.map("Treeview",
                   background=[("selected", COLORS["tree_select"])],
                   foreground=[("selected", "#ffffff")])
        style.map("Treeview.Heading",
                   background=[("active", COLORS["input"])])

        style.configure("TSpinbox",
                        fieldbackground=COLORS["input"],
                        background=COLORS["surface"],
                        foreground=COLORS["spinbox_fg"],
                        arrowcolor=COLORS["text"],
                        borderwidth=0,
                        font=("Segoe UI", 11))
        style.map("TSpinbox",
                   foreground=[("focus", COLORS["text"])])

    def _make_entry(self, parent, textvariable, show=None):
        entry = tk.Entry(parent, textvariable=textvariable, show=show,
                         bg=COLORS["entry_bg"], fg=COLORS["entry_fg"],
                         insertbackground=COLORS["entry_insert"],
                         font=("Segoe UI", 11),
                         relief="flat", bd=0, highlightthickness=1,
                         highlightbackground=COLORS["border"],
                         highlightcolor=COLORS["accent"])
        entry.bind("<Button-3>", lambda e: self._show_entry_context_menu(e, entry))
        self._active_entries.append(entry)
        return entry

    def _show_create_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self._t("create_title"))
        dialog.geometry("400x320")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=COLORS["bg"])

        tk.Label(dialog, text=self._t("create_label"), bg=COLORS["bg"],
                 fg=COLORS["text"], font=("Segoe UI", 11)).pack(pady=(30, 5))

        pw_entry = self._make_entry(dialog, tk.StringVar(), show="*")
        pw_entry.configure(width=32, font=("Segoe UI", 12))
        pw_entry.pack(pady=8)
        pw_entry.focus_set()

        tk.Label(dialog, text=self._t("confirm_label"), bg=COLORS["bg"],
                 fg=COLORS["text"], font=("Segoe UI", 11)).pack(pady=(10, 5))

        confirm_entry = self._make_entry(dialog, tk.StringVar(), show="*")
        confirm_entry.configure(width=32, font=("Segoe UI", 12))
        confirm_entry.pack(pady=8)

        def create():
            pw = pw_entry.get()
            confirm = confirm_entry.get()
            if not pw:
                self._show_toast(self._t("err_empty"), "error")
                return
            if len(pw) < 8:
                self._show_toast(self._t("err_short"), "error")
                return
            if pw != confirm:
                self._show_toast(self._t("err_mismatch"), "error")
                return
            key, salt = self._derive_key(pw)
            self.master_key = key
            self.fernet = Fernet(key)
            salt_b64 = base64.urlsafe_b64encode(salt).decode()
            with open(self.db_path + ".salt", "w") as f:
                f.write(salt_b64)
            self._init_db()
            dialog.destroy()
            self._setup_ui()
            self._load_data()

        ttk.Button(dialog, text=self._t("create_btn"), command=create, style="Accent.TButton").pack(pady=15)
        dialog.bind("<Return>", lambda e: create())

    def _show_login_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self._t("login_title"))
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=COLORS["bg"])

        tk.Label(dialog, text=self._t("login_label"), bg=COLORS["bg"],
                 fg=COLORS["text"], font=("Segoe UI", 11)).pack(pady=(35, 5))

        pw_entry = self._make_entry(dialog, tk.StringVar(), show="*")
        pw_entry.configure(width=32, font=("Segoe UI", 12))
        pw_entry.pack(pady=10)
        pw_entry.focus_set()

        def login():
            pw = pw_entry.get()
            if not pw:
                self._show_toast(self._t("err_empty"), "error")
                return
            salt_file = self.db_path + ".salt"
            if not os.path.exists(salt_file):
                self._show_toast(self._t("err_no_salt"), "error")
                return
            with open(salt_file, "r") as f:
                salt_b64 = f.read().strip()
            salt = base64.urlsafe_b64decode(salt_b64)
            key, _ = self._derive_key(pw, salt)
            try:
                test_conn = sqlite3.connect(self.db_path)
                test_cursor = test_conn.cursor()
                test_cursor.execute("SELECT password FROM passwords LIMIT 1")
                result = test_cursor.fetchone()
                test_conn.close()
                if result:
                    test_fernet = Fernet(key)
                    test_fernet.decrypt(result[0].encode())
                self.master_key = key
                self.fernet = Fernet(key)
                dialog.destroy()
                self._setup_ui()
                self._load_data()
            except Exception:
                self._show_toast(self._t("err_wrong_pw"), "error")

        ttk.Button(dialog, text=self._t("unlock_btn"), command=login, style="Accent.TButton").pack(pady=15)
        dialog.bind("<Return>", lambda e: login())

    def _setup_ui(self):
        self.root.title(self.text["app_title"])
        for widget in self.root.winfo_children():
            widget.destroy()
        self._active_entries.clear()

        container = tk.Frame(self.root, bg=COLORS["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        top_bar = tk.Frame(container, bg=COLORS["bg"])
        top_bar.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(top_bar, text=self.text["app_title"], style="Title.TLabel").pack(side=tk.LEFT)

        settings_frame = tk.Frame(top_bar, bg=COLORS["bg"])
        settings_frame.pack(side=tk.RIGHT)

        ttk.Label(settings_frame, text=self._t("language") + ":", style="Dim.TLabel").pack(side=tk.LEFT, padx=(0, 4))
        lang_combo = ttk.Combobox(settings_frame, values=["en", "ru"], width=3, state="readonly")
        lang_combo.set(self.lang_code)
        lang_combo.pack(side=tk.LEFT, padx=(0, 10))
        lang_combo.bind("<<ComboboxSelected>>", lambda e: self._switch_language(lang_combo.get()))

        fs_var = tk.BooleanVar(value=self.is_fullscreen)
        fs_check = tk.Checkbutton(settings_frame, text=self._t("fullscreen"), variable=fs_var,
                                  bg=COLORS["bg"], fg=COLORS["text_dim"],
                                  selectcolor=COLORS["input"], activebackground=COLORS["bg"],
                                  activeforeground=COLORS["text"], font=("Segoe UI", 9),
                                  command=lambda: self._set_fullscreen(fs_var.get()))
        fs_check.pack(side=tk.LEFT)

        ttk.Button(settings_frame, text=self._t("change_master_pw"),
                   command=self._change_master_password, style="Accent.TButton").pack(side=tk.LEFT, padx=(10, 0))

        input_card = tk.Frame(container, bg=COLORS["surface"],
                              highlightbackground=COLORS["border"], highlightthickness=1)
        input_card.pack(fill=tk.X, pady=(0, 12))

        card_inner = tk.Frame(input_card, bg=COLORS["surface"])
        card_inner.pack(fill=tk.X, padx=15, pady=12)

        fields = [
            (self._t("service"), self.service_var),
            (self._t("login"), self.login_var),
        ]

        for i, (label, var) in enumerate(fields):
            f = tk.Frame(card_inner, bg=COLORS["surface"])
            f.grid(row=i, column=0, columnspan=3, sticky=tk.EW, pady=3)
            f.columnconfigure(1, weight=1)

            ttk.Label(f, text=label, style="Dim.TLabel", width=8).grid(row=0, column=0, sticky=tk.W)
            entry = self._make_entry(f, var)
            entry.grid(row=0, column=1, sticky=tk.EW, padx=(8, 0))

        pw_f = tk.Frame(card_inner, bg=COLORS["surface"])
        pw_f.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=3)
        pw_f.columnconfigure(1, weight=1)

        ttk.Label(pw_f, text=self._t("password"), style="Dim.TLabel", width=8).grid(row=0, column=0, sticky=tk.W)

        pw_text_frame = tk.Frame(pw_f, bg=COLORS["surface"])
        pw_text_frame.grid(row=0, column=1, sticky=tk.EW, padx=(8, 0))

        self.password_text = tk.Text(pw_text_frame, height=1, wrap="none",
                                      bg=COLORS["entry_bg"], fg=COLORS["entry_fg"],
                                      insertbackground=COLORS["entry_insert"],
                                      font=("Segoe UI", 11),
                                      relief="flat", bd=0, highlightthickness=1,
                                      highlightbackground=COLORS["border"],
                                      highlightcolor=COLORS["accent"],
                                      padx=5, pady=3)
        self.password_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._active_entries.append(self.password_text)

        self.pw_scrollbar = ttk.Scrollbar(pw_text_frame, orient=tk.HORIZONTAL,
                                           command=self.password_text.xview)
        self.password_text.configure(xscrollcommand=self.pw_scrollbar.set)

        def _on_pw_key(event=None):
            self.password_text.see("end")
            self._update_pw_scrollbar()

        self.password_text.bind("<KeyRelease>", _on_pw_key)
        self.password_text.bind("<Configure>", self._update_pw_scrollbar)
        self.password_text.bind("<Button-3>", lambda e: self._show_entry_context_menu(e, self.password_text))

        len_frame = tk.Frame(card_inner, bg=COLORS["surface"])
        len_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(8, 0))

        ttk.Label(len_frame, text=self._t("length") + ":", style="Dim.TLabel").pack(side=tk.LEFT)
        length_spin = tk.Spinbox(len_frame, from_=4, to=64, textvariable=self.length_var,
                                 width=5, font=("Segoe UI", 11),
                                 bg=COLORS["input"], fg=COLORS["spinbox_fg"],
                                 buttonbackground=COLORS["surface"],
                                 insertbackground=COLORS["entry_insert"],
                                 relief="flat", bd=0, highlightthickness=1,
                                 highlightbackground=COLORS["border"],
                                 highlightcolor=COLORS["accent"])
        length_spin.pack(side=tk.LEFT, padx=(10, 0))

        checks_frame = tk.Frame(len_frame, bg=COLORS["surface"])
        checks_frame.pack(side=tk.LEFT, padx=(15, 0))

        for text, var in [
            (self._t("gen_uppercase"), self.gen_upper_var),
            (self._t("gen_lowercase"), self.gen_lower_var),
            (self._t("gen_digits"), self.gen_digit_var),
            (self._t("gen_symbols"), self.gen_symbol_var),
        ]:
            tk.Checkbutton(checks_frame, text=text, variable=var,
                           bg=COLORS["surface"], fg=COLORS["text_dim"],
                           selectcolor=COLORS["input"], activebackground=COLORS["surface"],
                           activeforeground=COLORS["text"], font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(6, 0))

        btn_row = tk.Frame(card_inner, bg=COLORS["surface"])
        btn_row.grid(row=4, column=0, columnspan=3, pady=(12, 0))

        ttk.Button(btn_row, text=self._t("generate"), command=self._generate_password,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row, text=self._t("add"), command=self._add_entry,
                   style="Accent.TButton").pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row, text=self._t("edit"), command=self._edit_entry,
                   style="Ghost.TButton").pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row, text=self._t("delete"), command=self._delete_entry,
                   style="Danger.TButton").pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_row, text=self._t("clear"), command=self._clear_fields,
                   style="Ghost.TButton").pack(side=tk.LEFT, padx=3)

        search_frame = tk.Frame(container, bg=COLORS["surface"],
                                highlightbackground=COLORS["border"], highlightthickness=1)
        search_frame.pack(fill=tk.X, pady=(0, 4))
        search_inner = tk.Frame(search_frame, bg=COLORS["surface"])
        search_inner.pack(fill=tk.X, padx=10, pady=6)
        ttk.Label(search_inner, text="\U0001F50D", style="Dim.TLabel").pack(side=tk.LEFT)
        search_entry = tk.Entry(search_inner, textvariable=self.search_var,
                                bg=COLORS["entry_bg"], fg=COLORS["entry_fg"],
                                insertbackground=COLORS["entry_insert"],
                                font=("Segoe UI", 11), relief="flat", bd=0,
                                highlightthickness=1,
                                highlightbackground=COLORS["border"],
                                highlightcolor=COLORS["accent"])
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))
        search_entry.insert(0, self._t("search"))
        search_entry.bind("<FocusIn>", lambda e: self._on_search_focus_in(search_entry))
        search_entry.bind("<FocusOut>", lambda e: self._on_search_focus_out(search_entry))

        table_frame = tk.Frame(container, bg=COLORS["surface"],
                               highlightbackground=COLORS["border"], highlightthickness=1)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("service", "login", "password")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        self.tree.heading("service", text=self._t("col_service"))
        self.tree.heading("login", text=self._t("col_login"))
        self.tree.heading("password", text=self._t("col_password"))

        self.tree.column("service", width=250, minwidth=100)
        self.tree.column("login", width=250, minwidth=100)
        self.tree.column("password", width=250, minwidth=100)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(1, 0), pady=(1, 1))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(1, 1))

        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Button-3>", self._show_tree_context_menu)

        self._password_tooltips = {}

    def _set_fullscreen(self, value):
        self.is_fullscreen = value
        self.root.attributes("-fullscreen", value)
        self._save_settings()

    def _change_master_password(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self._t("change_master_title"))
        dialog.geometry("420x340")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=COLORS["bg"])

        tk.Label(dialog, text=self._t("current_password"), bg=COLORS["bg"],
                 fg=COLORS["text"], font=("Segoe UI", 11)).pack(pady=(20, 5))

        old_entry = self._make_entry(dialog, tk.StringVar(), show="*")
        old_entry.configure(width=32, font=("Segoe UI", 12))
        old_entry.pack(pady=5)
        old_entry.focus_set()

        tk.Label(dialog, text=self._t("new_password"), bg=COLORS["bg"],
                 fg=COLORS["text"], font=("Segoe UI", 11)).pack(pady=(10, 5))

        new_entry = self._make_entry(dialog, tk.StringVar(), show="*")
        new_entry.configure(width=32, font=("Segoe UI", 12))
        new_entry.pack(pady=5)

        tk.Label(dialog, text=self._t("confirm_new_password"), bg=COLORS["bg"],
                 fg=COLORS["text"], font=("Segoe UI", 11)).pack(pady=(10, 5))

        confirm_entry = self._make_entry(dialog, tk.StringVar(), show="*")
        confirm_entry.configure(width=32, font=("Segoe UI", 12))
        confirm_entry.pack(pady=5)

        def do_change():
            old_pw = old_entry.get()
            new_pw = new_entry.get()
            confirm_pw = confirm_entry.get()

            if not old_pw:
                self._show_toast(self._t("err_current_empty"), "error")
                return
            if not new_pw:
                self._show_toast(self._t("err_new_empty"), "error")
                return
            if len(new_pw) < 8:
                self._show_toast(self._t("err_new_short"), "error")
                return
            if new_pw != confirm_pw:
                self._show_toast(self._t("err_new_mismatch"), "error")
                return

            salt_file = self.db_path + ".salt"
            with open(salt_file, "r") as f:
                salt = base64.urlsafe_b64decode(f.read().strip())
            old_key, _ = self._derive_key(old_pw, salt)
            try:
                test_fernet = Fernet(old_key)
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT id, password FROM passwords")
                rows = cursor.fetchall()
                if rows:
                    test_fernet.decrypt(rows[0][1].encode())
            except Exception:
                self._show_toast(self._t("err_current_wrong"), "error")
                conn.close()
                return

            new_key, new_salt = self._derive_key(new_pw)
            new_fernet = Fernet(new_key)

            cursor.execute("SELECT id, password FROM passwords")
            rows = cursor.fetchall()
            for row_id, enc_pw in rows:
                dec_pw = test_fernet.decrypt(enc_pw.encode())
                new_enc_pw = new_fernet.encrypt(dec_pw).decode()
                cursor.execute("UPDATE passwords SET password = ? WHERE id = ?",
                               (new_enc_pw, row_id))
            conn.commit()
            conn.close()

            new_salt_b64 = base64.urlsafe_b64encode(new_salt).decode()
            with open(salt_file, "w") as f:
                f.write(new_salt_b64)

            self.master_key = new_key
            self.fernet = new_fernet

            dialog.destroy()
            self._show_toast(self._t("success_master_pw"), "success")

        ttk.Button(dialog, text=self._t("change_master_pw"), command=do_change,
                   style="Accent.TButton").pack(pady=12)
        dialog.bind("<Return>", lambda e: do_change())

    def _on_search_focus_in(self, entry):
        if entry.get() == self._t("search"):
            entry.delete(0, tk.END)
            entry.configure(fg=COLORS["entry_fg"])

    def _on_search_focus_out(self, entry):
        if not entry.get():
            entry.insert(0, self._t("search"))
            entry.configure(fg=COLORS["text_dim"])

    def _filter_tree(self):
        if not hasattr(self, "tree"):
            return
        query = self.search_var.get().lower()
        if query == self._t("search").lower():
            query = ""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._password_tooltips.clear()
        for service, login, decrypted_pw in self._all_entries:
            if query in service.lower():
                item_id = self.tree.insert("", tk.END, values=(service, login, decrypted_pw))
                tip = Tooltip(self.tree, decrypted_pw)
                self._password_tooltips[item_id] = tip

    def _switch_language(self, lang_code):
        self.lang_code = lang_code
        self.text = LANG[lang_code]
        self._save_settings()
        if self.fernet:
            self._setup_ui()
            self._load_data()

    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._password_tooltips.clear()
        self._all_entries = []

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT service, login, password FROM passwords ORDER BY service")
            for row in cursor.fetchall():
                service, login, encrypted_pw = row
                decrypted_pw = self._decrypt(encrypted_pw)
                self._all_entries.append((service, login, decrypted_pw))
                item_id = self.tree.insert("", tk.END, values=(service, login, decrypted_pw))
                tip = Tooltip(self.tree, decrypted_pw)
                self._password_tooltips[item_id] = tip
            conn.close()
        except Exception as e:
            self._show_toast(self._t("err_load", err=str(e)), "error")

    def _add_entry(self):
        service = self.service_var.get().strip()
        login = self.login_var.get().strip()
        password = self._get_password().strip()
        if not service or not login or not password:
            self._show_toast(self._t("warn_all_fields"), "warning")
            return
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM passwords WHERE service = ?", (service,))
            if cursor.fetchone():
                self._show_toast(self._t("warn_duplicate", service=service), "warning")
                conn.close()
                return
            encrypted_pw = self._encrypt(password)
            cursor.execute("INSERT INTO passwords (service, login, password) VALUES (?, ?, ?)",
                           (service, login, encrypted_pw))
            conn.commit()
            conn.close()
            self._load_data()
            self._clear_fields()
            self._show_toast(self._t("success_add"), "success")
        except Exception as e:
            self._show_toast(self._t("err_add", err=str(e)), "error")

    def _edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            self._show_toast(self._t("warn_select_edit"), "warning")
            return
        service = self.service_var.get().strip()
        login = self.login_var.get().strip()
        password = self._get_password().strip()
        if not service or not login or not password:
            self._show_toast(self._t("warn_all_fields"), "warning")
            return
        old_values = self.tree.item(selected[0])["values"]
        old_service = old_values[0]
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if old_service != service:
                cursor.execute("SELECT id FROM passwords WHERE service = ?", (service,))
                if cursor.fetchone():
                    self._show_toast(self._t("warn_duplicate", service=service), "warning")
                    conn.close()
                    return
            encrypted_pw = self._encrypt(password)
            cursor.execute("UPDATE passwords SET service = ?, login = ?, password = ? WHERE service = ?",
                           (service, login, encrypted_pw, old_service))
            conn.commit()
            conn.close()
            self._load_data()
            self._clear_fields()
            self._show_toast(self._t("success_edit"), "success")
        except Exception as e:
            self._show_toast(self._t("err_edit", err=str(e)), "error")

    def _delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            self._show_toast(self._t("warn_select_delete"), "warning")
            return
        values = self.tree.item(selected[0])["values"]
        service = values[0]

        confirm_win = tk.Toplevel(self.root)
        confirm_win.title("")
        confirm_win.geometry("350x150")
        confirm_win.resizable(False, False)
        confirm_win.transient(self.root)
        confirm_win.grab_set()
        confirm_win.configure(bg=COLORS["bg"])

        tk.Label(confirm_win, text=self._t("confirm_delete", service=service),
                 bg=COLORS["bg"], fg=COLORS["text"], font=("Segoe UI", 11),
                 wraplength=300).pack(pady=(25, 15))

        btn_frame = tk.Frame(confirm_win, bg=COLORS["bg"])
        btn_frame.pack()

        def confirm():
            confirm_win.grab_release()
            confirm_win.destroy()
            def do_delete():
                try:
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM passwords WHERE service = ?", (service,))
                    conn.commit()
                    conn.close()
                    self._load_data()
                    self._clear_fields()
                    self._show_toast(self._t("success_delete"), "success")
                except Exception as e:
                    self._show_toast(self._t("err_delete", err=str(e)), "error")
            self.root.after(50, do_delete)

        ttk.Button(btn_frame, text=self._t("delete"), command=confirm,
                   style="Danger.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._t("clear"), command=confirm_win.destroy,
                   style="Ghost.TButton").pack(side=tk.LEFT, padx=5)

    def _generate_password(self):
        length = self.length_var.get()
        if length < 4:
            length = 4
            self.length_var.set(4)
        pools = []
        if self.gen_upper_var.get():
            pools.append(string.ascii_uppercase)
        if self.gen_lower_var.get():
            pools.append(string.ascii_lowercase)
        if self.gen_digit_var.get():
            pools.append(string.digits)
        if self.gen_symbol_var.get():
            pools.append(string.punctuation)
        if not pools:
            self._show_toast(self._t("err_gen_no_chars"), "error")
            return
        all_chars = "".join(pools)
        password = [random.choice(pool) for pool in pools]
        remaining = length - len(password)
        if remaining > 0:
            password += random.choices(all_chars, k=remaining)
        random.shuffle(password)
        self._set_password("".join(password[:length]))

    def _clear_fields(self):
        self.service_var.set("")
        self.login_var.set("")
        self._set_password("")
        self._editing_service = None

    def _on_double_click(self, event):
        self._load_selected_to_fields()

    def _on_select(self, event):
        self._load_selected_to_fields()

    def _load_selected_to_fields(self):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            self.service_var.set(values[0])
            self.login_var.set(values[1])
            self._set_password(values[2])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PasswordManager()
    app.run()
