import os
import sys
import json
import sqlite3
import string
import traceback
import random
import base64
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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
        "settings": "Settings",
        "settings_title": "Settings",
        "theme": "Theme",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "theme_system": "System",
        "export_json": "Export to JSON",
        "import_json": "Import from JSON",
        "close": "Close",
        "status_ready": "Ready",
        "status_exported": "Exported successfully",
        "status_imported": "Imported successfully",
        "err_export": "Export failed: {err}",
        "err_import": "Import failed: {err}",
        "err_import_file": "Import file not found",
        "err_import_decrypt": "Failed to decrypt import file. Wrong master password?",
        "auto_close": "Auto-close after (min)",
        "auto_close_disabled": "Disabled",
        "full_copy_row": "Copy entire row",
        "welcome_title": "Welcome",
        "welcome_label": "Password Manager",
        "welcome_create": "Create New Account",
        "welcome_restore": "Restore from Backup",
        "welcome_create_desc": "Set up a new master password",
        "welcome_restore_desc": "Import passwords from JSON backup",
        "restore_title": "Restore from Backup",
        "restore_select_file": "Select backup file:",
        "restore_enter_pw": "Enter your old master password:",
        "restore_btn": "Restore",
        "restore_err_decrypt": "Wrong master password or corrupted file",
        "restore_err_format": "Invalid backup file format",
        "restore_success": "Restored {count} passwords",
    },
    "ru": {
        "app_title": "\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440 \u043f\u0430\u0440\u043e\u043b\u0435\u0439",
        "create_title": "\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044c",
        "create_label": "\u0421\u043e\u0437\u0434\u0430\u0439\u0442\u0435 \u043c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044c:",
        "confirm_label": "\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0435 \u043f\u0430\u0440\u043e\u043b\u044c:",
        "create_btn": "\u0421\u043e\u0437\u0434\u0430\u0442\u044c",
        "login_title": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044c",
        "login_label": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0432\u0430\u0448 \u043c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044c:",
        "unlock_btn": "\u0412\u043e\u0439\u0442\u0438",
        "err_empty": "\u041f\u0430\u0440\u043e\u043b\u044c \u043d\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u043f\u0443\u0441\u0442\u044b\u043c",
        "err_short": "\u041f\u0430\u0440\u043e\u043b\u044c \u0434\u043e\u043b\u0436\u0435\u043d \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u0442\u044c \u043c\u0438\u043d\u0438\u043c\u0443\u043c 8 \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432",
        "err_mismatch": "\u041f\u0430\u0440\u043e\u043b\u0438 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442",
        "err_no_salt": "\u0424\u0430\u0439\u043b \u0441\u043e\u043b\u0438 \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d",
        "err_wrong_pw": "\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u043c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044c",
        "credentials": "\u0423\u0447\u0451\u0442\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435",
        "service": "\u0421\u0435\u0440\u0432\u0438\u0441",
        "login": "\u041b\u043e\u0433\u0438\u043d",
        "password": "\u041f\u0430\u0440\u043e\u043b\u044c",
        "length": "\u0414\u043b\u0438\u043d\u0430",
        "add": "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c",
        "edit": "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c",
        "delete": "\u0423\u0434\u0430\u043b\u0438\u0442\u044c",
        "generate": "\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c",
        "clear": "\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c",
        "col_service": "\u0421\u0435\u0440\u0432\u0438\u0441",
        "col_login": "\u041b\u043e\u0433\u0438\u043d",
        "col_password": "\u041f\u0430\u0440\u043e\u043b\u044c",
        "warn_all_fields": "\u0412\u0441\u0435 \u043f\u043e\u043b\u044f \u0434\u043e\u043b\u0436\u043d\u044b \u0431\u044b\u0442\u044c \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u044b",
        "warn_select_edit": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0437\u0430\u043f\u0438\u0441\u044c \u0434\u043b\u044f \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f",
        "warn_select_delete": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0437\u0430\u043f\u0438\u0441\u044c \u0434\u043b\u044f \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f",
        "warn_duplicate": "\u0421\u0435\u0440\u0432\u0438\u0441 '{service}' \u0443\u0436\u0435 \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u0435\u0442",
        "confirm_delete": "\u0423\u0434\u0430\u043b\u0438\u0442\u044c '{service}'?",
        "success_add": "\u0417\u0430\u043f\u0438\u0441\u044c \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0430",
        "success_edit": "\u0417\u0430\u043f\u0438\u0441\u044c \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0430",
        "success_delete": "\u0417\u0430\u043f\u0438\u0441\u044c \u0443\u0434\u0430\u043b\u0435\u043d\u0430",
        "err_load": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438: {err}",
        "err_add": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f: {err}",
        "err_edit": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f: {err}",
        "err_delete": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f: {err}",
        "language": "\u042f\u0437\u044b\u043a",
        "fullscreen": "\u041f\u043e\u043b\u043d\u044b\u0439 \u044d\u043a\u0440\u0430\u043d",
        "search": "\u041f\u043e\u0438\u0441\u043a...",
        "change_master_pw": "\u0421\u043c\u0435\u043d\u0438\u0442\u044c \u043c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044c",
        "change_master_title": "\u0421\u043c\u0435\u043d\u0430 \u043c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044f",
        "current_password": "\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u043f\u0430\u0440\u043e\u043b\u044c:",
        "new_password": "\u041d\u043e\u0432\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c:",
        "confirm_new_password": "\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0435 \u043d\u043e\u0432\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c:",
        "err_current_empty": "\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u043f\u0430\u0440\u043e\u043b\u044c \u043d\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u043f\u0443\u0441\u0442\u044b\u043c",
        "err_new_empty": "\u041d\u043e\u0432\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c \u043d\u0435 \u043c\u043e\u0436\u0435\u0442 \u0431\u044b\u0442\u044c \u043f\u0443\u0441\u0442\u044b\u043c",
        "err_new_short": "\u041d\u043e\u0432\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c \u0434\u043e\u043b\u0436\u0435\u043d \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u0442\u044c \u043c\u0438\u043d\u0438\u043c\u0443\u043c 8 \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432",
        "err_new_mismatch": "\u041d\u043e\u0432\u044b\u0435 \u043f\u0430\u0440\u043e\u043b\u0438 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u044e\u0442",
        "err_current_wrong": "\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u0442\u0435\u043a\u0443\u0449\u0438\u0439 \u043f\u0430\u0440\u043e\u043b\u044c",
        "success_master_pw": "\u041c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044c \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u0438\u0437\u043c\u0435\u043d\u0451\u043d",
        "ctx_copy": "\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c",
        "ctx_copy_login": "\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043b\u043e\u0433\u0438\u043d",
        "ctx_copy_password": "\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043f\u0430\u0440\u043e\u043b\u044c",
        "ctx_copy_service": "\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441\u0435\u0440\u0432\u0438\u0441",
        "ctx_cut": "\u0412\u044b\u0440\u0435\u0437\u0430\u0442\u044c",
        "ctx_paste": "\u0412\u0441\u0442\u0430\u0432\u0438\u0442\u044c",
        "ctx_select_all": "\u0412\u044b\u0434\u0435\u043b\u0438\u0442\u044c \u0432\u0441\u0451",
        "gen_uppercase": "A-Z",
        "gen_lowercase": "a-z",
        "gen_digits": "0-9",
        "gen_symbols": "!@#",
        "err_gen_no_chars": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0445\u043e\u0442\u044f \u0431\u044b \u043e\u0434\u0438\u043d \u0442\u0438\u043f \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432",
        "settings": "\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438",
        "settings_title": "\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438",
        "theme": "\u0422\u0435\u043c\u0430",
        "theme_light": "\u0421\u0432\u0435\u0442\u043b\u0430\u044f",
        "theme_dark": "\u0422\u0451\u043c\u043d\u0430\u044f",
        "theme_system": "\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u0430\u044f",
        "export_json": "\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u0432 JSON",
        "import_json": "\u0418\u043c\u043f\u043e\u0440\u0442 \u0438\u0437 JSON",
        "close": "\u0417\u0430\u043a\u0440\u044b\u0442\u044c",
        "status_ready": "\u0413\u043e\u0442\u043e\u0432\u043e",
        "status_exported": "\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d \u0443\u0441\u043f\u0435\u0448\u043d\u043e",
        "status_imported": "\u0418\u043c\u043f\u043e\u0440\u0442 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d \u0443\u0441\u043f\u0435\u0448\u043d\u043e",
        "err_export": "\u041e\u0448\u0438\u0431\u043a\u0430 \u044d\u043a\u0441\u043f\u043e\u0440\u0442\u0430: {err}",
        "err_import": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0438\u043c\u043f\u043e\u0440\u0442\u0430: {err}",
        "err_import_file": "\u0424\u0430\u0439\u043b \u0438\u043c\u043f\u043e\u0440\u0442\u0430 \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d",
        "err_import_decrypt": "\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u0440\u0430\u0441\u0448\u0438\u0444\u0440\u043e\u0432\u0430\u0442\u044c. \u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u043c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044c?",
        "auto_close": "\u0410\u0432\u0442\u043e\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0447\u0435\u0440\u0435\u0437 (\u043c\u0438\u043d)",
        "auto_close_disabled": "\u0412\u044b\u043a\u043b\u044e\u0447\u0435\u043d\u043e",
        "full_copy_row": "\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0432\u0441\u044e \u0441\u0442\u0440\u043e\u043a\u0443",
        "welcome_title": "\u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c",
        "welcome_label": "\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440 \u043f\u0430\u0440\u043e\u043b\u0435\u0439",
        "welcome_create": "\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043d\u043e\u0432\u044b\u0439 \u0430\u043a\u043a\u0430\u0443\u043d\u0442",
        "welcome_restore": "\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0438\u0437 \u0431\u044d\u043a\u0430\u043f\u0430",
        "welcome_create_desc": "\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043d\u043e\u0432\u044b\u0439 \u043c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044c",
        "welcome_restore_desc": "\u0418\u043c\u043f\u043e\u0440\u0442 \u043f\u0430\u0440\u043e\u043b\u0435\u0439 \u0438\u0437 JSON-\u0431\u044d\u043a\u0430\u043f\u0430",
        "restore_title": "\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u0438\u0437 \u0431\u044d\u043a\u0430\u043f\u0430",
        "restore_select_file": "\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0444\u0430\u0439\u043b \u0431\u044d\u043a\u0430\u043f\u0430:",
        "restore_enter_pw": "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0441\u0442\u0430\u0440\u044b\u0439 \u043c\u0430\u0441\u0442\u0435\u0440-\u043f\u0430\u0440\u043e\u043b\u044c:",
        "restore_btn": "\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c",
        "restore_err_decrypt": "\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c \u0438\u043b\u0438 \u043f\u043e\u0432\u0440\u0435\u0436\u0434\u0451\u043d\u043d\u044b\u0439 \u0444\u0430\u0439\u043b",
        "restore_err_format": "\u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u0444\u043e\u0440\u043c\u0430\u0442 \u0444\u0430\u0439\u043b\u0430 \u0431\u044d\u043a\u0430\u043f\u0430",
        "restore_success": "\u0412\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043e {count} \u043f\u0430\u0440\u043e\u043b\u0435\u0439",
    },
}


def get_data_dir():
    app_name = "PasswordManager"
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
        app_name = ".password-manager"
    data_dir = os.path.join(base, app_name)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def derive_key(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt


class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.data_dir = get_data_dir()
        self.db_path = os.path.join(self.data_dir, "passwords.db")
        self.settings_path = os.path.join(self.data_dir, "settings.json")
        self.master_key = None
        self.fernet = None
        self.settings = self._load_settings()
        self.lang_code = self.settings.get("language", "en")
        self.text = LANG[self.lang_code]
        self._editing_service = None
        self._all_entries = []
        self._active_entries = []
        self._auto_close_minutes = self.settings.get("auto_close_minutes", 0)
        self._auto_close_timer = None

        self.title(self.text["app_title"])
        self.geometry("950x680")
        self.minsize(800, 600)

        saved_theme = self.settings.get("theme", "dark")
        if saved_theme in ("light", "dark", "system"):
            ctk.set_appearance_mode(saved_theme)

        self.service_var = tk.StringVar()
        self.login_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=12)
        self.gen_upper_var = tk.BooleanVar(value=True)
        self.gen_lower_var = tk.BooleanVar(value=True)
        self.gen_digit_var = tk.BooleanVar(value=True)
        self.gen_symbol_var = tk.BooleanVar(value=True)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter_tree())

        self.after(200, self._on_startup)

    def _on_startup(self):
        try:
            self.withdraw()
            self.after(100, self._show_auth_dialog)
        except Exception:
            tb = traceback.format_exc()
            log_path = os.path.join(get_data_dir(), "startup.log")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"\n_on_startup EXCEPTION:\n{tb}")
            messagebox.showerror("Startup Error", tb)

    def _show_auth_dialog(self):
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._exit_fullscreen)
        self.bind("<Control-c>", self._hotkey_copy)
        self.bind("<Control-v>", self._hotkey_paste)
        self.bind("<Control-x>", self._hotkey_cut)
        self.bind("<Control-a>", self._hotkey_select_all)
        self.bind("<Key>", lambda e: self._reset_auto_close())
        self.bind("<Button-1>", lambda e: self._reset_auto_close())

        if self._db_exists():
            self._show_login_dialog()
        else:
            self._show_welcome_dialog()

    def _load_settings(self):
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"language": "en", "theme": "dark", "auto_close_minutes": 0}

    def _save_settings(self):
        self.settings["language"] = self.lang_code
        self.settings["auto_close_minutes"] = self._auto_close_minutes
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False)
        except Exception:
            pass

    def _db_exists(self):
        return os.path.exists(self.db_path)

    def _derive_key(self, password, salt=None):
        return derive_key(password, salt)

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

    def _toggle_fullscreen(self, event=None):
        state = not self.attributes("-fullscreen")
        self.attributes("-fullscreen", state)

    def _exit_fullscreen(self, event=None):
        if self.attributes("-fullscreen"):
            self.attributes("-fullscreen", False)

    def _reset_auto_close(self):
        if self._auto_close_minutes > 0:
            if self._auto_close_timer:
                self.after_cancel(self._auto_close_timer)
            self._auto_close_timer = self.after(
                self._auto_close_minutes * 60 * 1000, self._auto_close_app
            )

    def _auto_close_app(self):
        self.destroy()

    def _get_focused_entry(self):
        widget = self.focus_get()
        if isinstance(widget, (ctk.CTkEntry, ctk.CTkTextbox)):
            return widget
        return None

    def _bind_copy_paste(self, widget):
        def copy_text(e):
            try:
                root = widget.winfo_toplevel()
                root.clipboard_clear()
                root.clipboard_append(widget.selection_get())
            except tk.TclError:
                pass
            return "break"

        def paste_text(e):
            try:
                widget.insert("insert", widget.winfo_toplevel().clipboard_get())
            except tk.TclError:
                pass
            return "break"

        def cut_text(e):
            try:
                root = widget.winfo_toplevel()
                root.clipboard_clear()
                root.clipboard_append(widget.selection_get())
                widget.delete("sel.first", "sel.last")
            except tk.TclError:
                pass
            return "break"

        def select_all(e):
            try:
                widget.select_range(0, "end")
            except tk.TclError:
                pass
            return "break"

        widget.bind("<Control-c>", copy_text)
        widget.bind("<Control-C>", copy_text)
        widget.bind("<Control-v>", paste_text)
        widget.bind("<Control-V>", paste_text)
        widget.bind("<Control-x>", cut_text)
        widget.bind("<Control-X>", cut_text)
        widget.bind("<Control-a>", select_all)
        widget.bind("<Control-A>", select_all)

    def _hotkey_copy(self, event=None):
        entry = self._get_focused_entry()
        if entry:
            if isinstance(entry, ctk.CTkTextbox):
                try:
                    text = entry.get("sel.first", "sel.last")
                except Exception:
                    text = entry.get("1.0", "end-1c")
            else:
                sel = entry.selection_range()
                if sel:
                    text = entry.get()[sel[0]:sel[1]]
                else:
                    text = entry.get()
            if text:
                self.clipboard_clear()
                self.clipboard_append(text)
        elif hasattr(self, "tree"):
            selected = self.tree.selection()
            if selected:
                values = self.tree.item(selected[0])["values"]
                text = " | ".join(str(v) for v in values)
                self.clipboard_clear()
                self.clipboard_append(text)
        return "break"

    def _hotkey_paste(self, event=None):
        entry = self._get_focused_entry()
        if entry:
            try:
                text = self.clipboard_get()
                if isinstance(entry, ctk.CTkTextbox):
                    try:
                        entry.delete("sel.first", "sel.last")
                    except Exception:
                        pass
                    entry.insert("insert", text)
                else:
                    sel = entry.selection_range()
                    if sel and sel[0] is not None:
                        entry.delete(sel[0], sel[1])
                    entry.insert("insert", text)
            except Exception:
                pass
        return "break"

    def _hotkey_cut(self, event=None):
        entry = self._get_focused_entry()
        if entry:
            if isinstance(entry, ctk.CTkTextbox):
                try:
                    text = entry.get("sel.first", "sel.last")
                    self.clipboard_clear()
                    self.clipboard_append(text)
                    entry.delete("sel.first", "sel.last")
                except Exception:
                    pass
            else:
                sel = entry.selection_range()
                if sel:
                    text = entry.get()[sel[0]:sel[1]]
                    self.clipboard_clear()
                    self.clipboard_append(text)
                    entry.delete(sel[0], sel[1])
        return "break"

    def _hotkey_select_all(self, event=None):
        entry = self._get_focused_entry()
        if entry:
            if isinstance(entry, ctk.CTkTextbox):
                entry.tag_add("sel", "1.0", "end-1c")
            else:
                entry.select_range(0, "end")
        return "break"

    def _show_entry_context_menu(self, event, widget):
        menu = tk.Menu(self, tearoff=0,
                       bg="#2b2b3d", fg="#e0e0e0",
                       activebackground="#7c3aed",
                       activeforeground="#ffffff",
                       font=("Segoe UI", 10))
        has_selection = False
        if isinstance(widget, ctk.CTkTextbox):
            try:
                widget.get("sel.first", "sel.last")
                has_selection = True
            except Exception:
                pass
        else:
            sel = widget.selection_range()
            has_selection = bool(sel and sel[0] is not None)

        def do_copy():
            if isinstance(widget, ctk.CTkTextbox):
                try:
                    text = widget.get("sel.first", "sel.last")
                except Exception:
                    text = widget.get("1.0", "end-1c")
            else:
                sel = widget.selection_range()
                if sel:
                    text = widget.get()[sel[0]:sel[1]]
                else:
                    text = widget.get()
            if text:
                self.clipboard_clear()
                self.clipboard_append(text)

        def do_cut():
            if isinstance(widget, ctk.CTkTextbox):
                try:
                    text = widget.get("sel.first", "sel.last")
                    self.clipboard_clear()
                    self.clipboard_append(text)
                    widget.delete("sel.first", "sel.last")
                except Exception:
                    pass
            else:
                sel = widget.selection_range()
                if sel:
                    text = widget.get()[sel[0]:sel[1]]
                    self.clipboard_clear()
                    self.clipboard_append(text)
                    widget.delete(sel[0], sel[1])

        def do_paste():
            try:
                text = self.clipboard_get()
                if isinstance(widget, ctk.CTkTextbox):
                    try:
                        widget.delete("sel.first", "sel.last")
                    except Exception:
                        pass
                    widget.insert("insert", text)
                else:
                    sel = widget.selection_range()
                    if sel and sel[0] is not None:
                        widget.delete(sel[0], sel[1])
                    widget.insert("insert", text)
            except Exception:
                pass

        def do_select_all():
            if isinstance(widget, ctk.CTkTextbox):
                widget.tag_add("sel", "1.0", "end-1c")
            else:
                widget.select_range(0, "end")

        menu.add_command(label=self._t("ctx_copy"), command=do_copy,
                         state="normal" if has_selection else "disabled")
        menu.add_command(label=self._t("ctx_cut"), command=do_cut,
                         state="normal" if has_selection else "disabled")
        menu.add_command(label=self._t("ctx_paste"), command=do_paste)
        menu.add_separator()
        menu.add_command(label=self._t("ctx_select_all"), command=do_select_all)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _show_tree_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0,
                       bg="#2b2b3d", fg="#e0e0e0",
                       activebackground="#7c3aed",
                       activeforeground="#ffffff",
                       font=("Segoe UI", 10))
        selected = self.tree.selection()

        def do_copy():
            if selected:
                values = self.tree.item(selected[0])["values"]
                text = " | ".join(str(v) for v in values)
                self.clipboard_clear()
                self.clipboard_append(text)

        def do_copy_login():
            if selected:
                values = self.tree.item(selected[0])["values"]
                self.clipboard_clear()
                self.clipboard_append(str(values[1]))

        def do_copy_password():
            if selected:
                values = self.tree.item(selected[0])["values"]
                self.clipboard_clear()
                self.clipboard_append(str(values[2]))

        def do_copy_service():
            if selected:
                values = self.tree.item(selected[0])["values"]
                self.clipboard_clear()
                self.clipboard_append(str(values[0]))

        menu.add_command(label=self._t("full_copy_row"), command=do_copy,
                         state="normal" if selected else "disabled")
        menu.add_separator()
        menu.add_command(label=self._t("ctx_copy_login"), command=do_copy_login,
                         state="normal" if selected else "disabled")
        menu.add_command(label=self._t("ctx_copy_password"), command=do_copy_password,
                         state="normal" if selected else "disabled")
        menu.add_command(label=self._t("ctx_copy_service"), command=do_copy_service,
                         state="normal" if selected else "disabled")

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _show_toast(self, text, toast_type="info", duration=2000):
        self.status_label.configure(text=text)
        self.after(duration, lambda: self.status_label.configure(text=self._t("status_ready")))

    def _show_login_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(self._t("login_title"))
        dialog.geometry("400x260")
        dialog.resizable(False, False)
        dialog.protocol("WM_DELETE_WINDOW", self.destroy)
        dialog.after(10, lambda: dialog.lift())
        dialog.after(20, lambda: dialog.focus_force())

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 400) // 2
        y = (sh - 260) // 2
        dialog.geometry(f"400x260+{x}+{y}")

        ctk.CTkLabel(dialog, text=self._t("login_label"),
                     font=("Segoe UI", 13)).pack(pady=(30, 8))

        pw_entry = ctk.CTkEntry(dialog, show="*", width=280, font=("Segoe UI", 13))
        pw_entry.pack(pady=8)
        pw_entry.focus_set()

        def login():
            pw = pw_entry.get()
            if not pw:
                messagebox.showwarning("Warning", self._t("err_empty"))
                return
            salt_file = self.db_path + ".salt"
            if not os.path.exists(salt_file):
                messagebox.showerror("Error", self._t("err_no_salt"))
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
                self.deiconify()
                self._setup_ui()
                self._load_data()
                self._reset_auto_close()
            except Exception:
                messagebox.showerror("Error", self._t("err_wrong_pw"))

        ctk.CTkButton(dialog, text=self._t("unlock_btn"), command=login,
                      width=200, font=("Segoe UI", 13, "bold")).pack(pady=15)
        dialog.bind("<Return>", lambda e: login())

    def _show_welcome_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(self._t("welcome_title"))
        dialog.geometry("420x340")
        dialog.resizable(False, False)
        dialog.protocol("WM_DELETE_WINDOW", self.destroy)
        dialog.after(10, lambda: dialog.lift())
        dialog.after(20, lambda: dialog.focus_force())

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 420) // 2
        y = (sh - 340) // 2
        dialog.geometry(f"420x340+{x}+{y}")

        ctk.CTkLabel(dialog, text=self._t("welcome_label"),
                     font=("Segoe UI", 20, "bold")).pack(pady=(30, 25))

        def go_create():
            dialog.destroy()
            self._show_create_dialog()

        def go_restore():
            dialog.destroy()
            self._show_restore_dialog()

        ctk.CTkButton(dialog, text=self._t("welcome_create"),
                      command=go_create, width=300, height=40,
                      font=("Segoe UI", 13, "bold")).pack(pady=8)
        ctk.CTkLabel(dialog, text=self._t("welcome_create_desc"),
                     font=("Segoe UI", 10), text_color="gray60").pack()

        ctk.CTkButton(dialog, text=self._t("welcome_restore"),
                      command=go_restore, width=300, height=40,
                      font=("Segoe UI", 13, "bold"),
                      fg_color="gray40", hover_color="gray50").pack(pady=(20, 8))
        ctk.CTkLabel(dialog, text=self._t("welcome_restore_desc"),
                     font=("Segoe UI", 10), text_color="gray60").pack()

    def _show_restore_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(self._t("restore_title"))
        dialog.geometry("460x320")
        dialog.resizable(False, False)
        dialog.protocol("WM_DELETE_WINDOW", self.destroy)
        dialog.after(10, lambda: dialog.lift())
        dialog.after(20, lambda: dialog.focus_force())

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 460) // 2
        y = (sh - 320) // 2
        dialog.geometry(f"460x320+{x}+{y}")

        ctk.CTkLabel(dialog, text=self._t("restore_select_file"),
                     font=("Segoe UI", 12)).pack(pady=(25, 5))

        file_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        file_frame.pack(fill="x", padx=30, pady=5)
        file_var = tk.StringVar()
        file_entry = ctk.CTkEntry(file_frame, textvariable=file_var,
                                  width=280, font=("Segoe UI", 11))
        file_entry.pack(side="left", fill="x", expand=True)

        def browse():
            path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json")])
            if path:
                file_var.set(path)

        ctk.CTkButton(file_frame, text="...", width=40,
                      command=browse).pack(side="left", padx=(5, 0))

        ctk.CTkLabel(dialog, text=self._t("restore_enter_pw"),
                     font=("Segoe UI", 12)).pack(pady=(15, 5))
        pw_entry = ctk.CTkEntry(dialog, show="*", width=300,
                                font=("Segoe UI", 12))
        pw_entry.pack(pady=5)
        pw_entry.focus_set()

        def do_restore():
            file_path = file_var.get().strip()
            master_pw = pw_entry.get()
            if not file_path:
                messagebox.showwarning("Warning", self._t("err_import_file"))
                return
            if not os.path.exists(file_path):
                messagebox.showwarning("Warning", self._t("err_import_file"))
                return
            if not master_pw:
                messagebox.showwarning("Warning", self._t("err_empty"))
                return

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    import_data = json.load(f)
                if not isinstance(import_data, list) or len(import_data) == 0:
                    messagebox.showerror("Error", self._t("restore_err_format"))
                    return
            except Exception:
                messagebox.showerror("Error", self._t("restore_err_format"))
                return

            test_key, _ = self._derive_key(master_pw)
            test_fernet = Fernet(test_key)
            verified = 0
            for entry in import_data:
                try:
                    test_fernet.decrypt(entry["password"].encode())
                    verified += 1
                except Exception:
                    pass

            if verified == 0:
                messagebox.showerror("Error", self._t("restore_err_decrypt"))
                return

            key, salt = self._derive_key(master_pw)
            self.master_key = key
            self.fernet = Fernet(key)
            salt_b64 = base64.urlsafe_b64encode(salt).decode()
            with open(self.db_path + ".salt", "w") as f:
                f.write(salt_b64)
            self._init_db()

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            imported = 0
            for entry in import_data:
                try:
                    dec_pw = self._decrypt(entry["password"])
                    re_encrypted = self._encrypt(dec_pw)
                    cursor.execute(
                        "INSERT INTO passwords (service, login, password) VALUES (?, ?, ?)",
                        (entry.get("service", ""), entry.get("login", ""), re_encrypted))
                    imported += 1
                except Exception:
                    continue
            conn.commit()
            conn.close()

            dialog.destroy()
            self.deiconify()
            self._setup_ui()
            self._load_data()
            self._reset_auto_close()

        ctk.CTkButton(dialog, text=self._t("restore_btn"),
                      command=do_restore, width=200,
                      font=("Segoe UI", 13, "bold")).pack(pady=20)
        dialog.bind("<Return>", lambda e: do_restore())

    def _show_create_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(self._t("create_title"))
        dialog.geometry("400x320")
        dialog.resizable(False, False)
        dialog.protocol("WM_DELETE_WINDOW", self.destroy)
        dialog.after(10, lambda: dialog.lift())
        dialog.after(20, lambda: dialog.focus_force())

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 400) // 2
        y = (sh - 320) // 2
        dialog.geometry(f"400x320+{x}+{y}")

        ctk.CTkLabel(dialog, text=self._t("create_label"),
                     font=("Segoe UI", 13)).pack(pady=(25, 8))

        pw_entry = ctk.CTkEntry(dialog, show="*", width=280, font=("Segoe UI", 13))
        pw_entry.pack(pady=8)
        pw_entry.focus_set()

        ctk.CTkLabel(dialog, text=self._t("confirm_label"),
                     font=("Segoe UI", 13)).pack(pady=(10, 8))

        confirm_entry = ctk.CTkEntry(dialog, show="*", width=280, font=("Segoe UI", 13))
        confirm_entry.pack(pady=8)

        def create():
            pw = pw_entry.get()
            confirm = confirm_entry.get()
            if not pw:
                messagebox.showwarning("Warning", self._t("err_empty"))
                return
            if len(pw) < 8:
                messagebox.showwarning("Warning", self._t("err_short"))
                return
            if pw != confirm:
                messagebox.showwarning("Warning", self._t("err_mismatch"))
                return
            key, salt = self._derive_key(pw)
            self.master_key = key
            self.fernet = Fernet(key)
            salt_b64 = base64.urlsafe_b64encode(salt).decode()
            with open(self.db_path + ".salt", "w") as f:
                f.write(salt_b64)
            self._init_db()
            dialog.destroy()
            self.deiconify()
            self._setup_ui()
            self._load_data()
            self._reset_auto_close()

        ctk.CTkButton(dialog, text=self._t("create_btn"), command=create,
                      width=200, font=("Segoe UI", 13, "bold")).pack(pady=15)
        dialog.bind("<Return>", lambda e: create())

    def _setup_ui(self):
        self.title(self.text["app_title"])
        for widget in self.winfo_children():
            widget.destroy()
        self._active_entries.clear()

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=15)

        top_bar = ctk.CTkFrame(container, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 12))

        settings_btn = ctk.CTkButton(top_bar, text="\u2699 " + self._t("settings"),
                                      command=self._open_settings,
                                      width=120, height=32,
                                      font=("Segoe UI", 11))
        settings_btn.pack(side="left")

        ctk.CTkLabel(top_bar, text=self.text["app_title"],
                     font=("Segoe UI", 20, "bold")).pack(side="left", padx=(12, 0))

        lang_combo = ctk.CTkComboBox(top_bar, values=["en", "ru"], width=60,
                                      command=lambda v: self._switch_language(v))
        lang_combo.set(self.lang_code)
        lang_combo.pack(side="right")

        ctk.CTkLabel(top_bar, text=self._t("language") + ":",
                     font=("Segoe UI", 11)).pack(side="right", padx=(0, 6))

        input_card = ctk.CTkFrame(container, corner_radius=10)
        input_card.pack(fill="x", pady=(0, 12))

        card_inner = ctk.CTkFrame(input_card, fg_color="transparent")
        card_inner.pack(fill="x", padx=15, pady=12)

        fields = [
            (self._t("service"), self.service_var),
            (self._t("login"), self.login_var),
        ]

        for i, (label, var) in enumerate(fields):
            f = ctk.CTkFrame(card_inner, fg_color="transparent")
            f.grid(row=i, column=0, columnspan=4, sticky="ew", pady=3)
            ctk.CTkLabel(f, text=label, width=70, anchor="w",
                         font=("Segoe UI", 12)).pack(side="left")
            entry = ctk.CTkEntry(f, textvariable=var, font=("Segoe UI", 12))
            entry.pack(side="left", fill="x", expand=True, padx=(8, 0))
            self._active_entries.append(entry)
            self._bind_copy_paste(entry)

        pw_f = ctk.CTkFrame(card_inner, fg_color="transparent")
        pw_f.grid(row=2, column=0, columnspan=4, sticky="ew", pady=3)
        ctk.CTkLabel(pw_f, text=self._t("password"), width=70, anchor="w",
                     font=("Segoe UI", 12)).pack(side="left")
        pw_entry = ctk.CTkEntry(pw_f, textvariable=self.password_var,
                                font=("Segoe UI", 12))
        pw_entry.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self._active_entries.append(pw_entry)
        self._bind_copy_paste(pw_entry)

        gen_frame = ctk.CTkFrame(card_inner, fg_color="transparent")
        gen_frame.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(8, 0))

        ctk.CTkLabel(gen_frame, text=self._t("length") + ":",
                     font=("Segoe UI", 12)).pack(side="left")
        length_slider = ctk.CTkSlider(gen_frame, from_=4, to=64,
                                       number_of_steps=60,
                                       variable=self.length_var,
                                       width=200)
        length_slider.pack(side="left", padx=(10, 0))

        length_label = ctk.CTkLabel(gen_frame, textvariable=self.length_var,
                                    width=30, font=("Segoe UI", 12))
        length_label.pack(side="left", padx=(4, 15))

        for text, var in [
            (self._t("gen_uppercase"), self.gen_upper_var),
            (self._t("gen_lowercase"), self.gen_lower_var),
            (self._t("gen_digits"), self.gen_digit_var),
            (self._t("gen_symbols"), self.gen_symbol_var),
        ]:
            ctk.CTkCheckBox(gen_frame, text=text, variable=var,
                            font=("Segoe UI", 11)).pack(side="left", padx=(6, 0))

        btn_row = ctk.CTkFrame(card_inner, fg_color="transparent")
        btn_row.grid(row=4, column=0, columnspan=4, pady=(12, 0))

        ctk.CTkButton(btn_row, text=self._t("generate"),
                      command=self._generate_password,
                      width=110, font=("Segoe UI", 12, "bold")).pack(side="left", padx=3)
        ctk.CTkButton(btn_row, text=self._t("add"),
                      command=self._add_entry,
                      width=90, font=("Segoe UI", 12, "bold")).pack(side="left", padx=3)
        ctk.CTkButton(btn_row, text=self._t("edit"),
                      command=self._edit_entry,
                      width=90, font=("Segoe UI", 12, "bold"),
                      fg_color="gray40", hover_color="gray50").pack(side="left", padx=3)
        ctk.CTkButton(btn_row, text=self._t("delete"),
                      command=self._delete_entry,
                      width=90, font=("Segoe UI", 12, "bold"),
                      fg_color="#dc2626", hover_color="#b91c1c").pack(side="left", padx=3)
        ctk.CTkButton(btn_row, text=self._t("clear"),
                      command=self._clear_fields,
                      width=80, font=("Segoe UI", 12),
                      fg_color="gray40", hover_color="gray50").pack(side="left", padx=3)

        search_frame = ctk.CTkFrame(container, corner_radius=10)
        search_frame.pack(fill="x", pady=(0, 4))
        search_inner = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_inner.pack(fill="x", padx=10, pady=6)
        ctk.CTkLabel(search_inner, text="\U0001F50D", font=("Segoe UI", 13)).pack(side="left")
        search_entry = ctk.CTkEntry(search_inner, textvariable=self.search_var,
                                    placeholder_text=self._t("search"),
                                    font=("Segoe UI", 12))
        search_entry.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self._bind_copy_paste(search_entry)

        table_frame = ctk.CTkFrame(container, corner_radius=10)
        table_frame.pack(fill="both", expand=True)

        columns = ("service", "login", "password")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        self.tree.heading("service", text=self._t("col_service"))
        self.tree.heading("login", text=self._t("col_login"))
        self.tree.heading("password", text=self._t("col_password"))

        self.tree.column("service", width=280, minwidth=120)
        self.tree.column("login", width=280, minwidth=120)
        self.tree.column("password", width=280, minwidth=120)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2b2b3d",
                        foreground="#e0e0e0",
                        fieldbackground="#2b2b3d",
                        borderwidth=0,
                        font=("Segoe UI", 10),
                        rowheight=30)
        style.configure("Treeview.Heading",
                        background="#3b3b5c",
                        foreground="#c0c0c0",
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0, relief="flat")
        style.map("Treeview",
                   background=[("selected", "#7c3aed")],
                   foreground=[("selected", "#ffffff")])

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=(1, 1))
        scrollbar.pack(side="right", fill="y", pady=(1, 1))

        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Button-3>", self._show_tree_context_menu)

        def tree_copy(e):
            selected = self.tree.selection()
            if selected:
                values = self.tree.item(selected[0])["values"]
                text = " | ".join(str(v) for v in values)
                self.clipboard_clear()
                self.clipboard_append(text)
            return "break"

        self.tree.bind("<Control-c>", tree_copy)
        self.tree.bind("<Control-C>", tree_copy)

        status_frame = ctk.CTkFrame(self, height=30, corner_radius=0)
        status_frame.pack(fill="x", side="bottom")
        self.status_label = ctk.CTkLabel(status_frame, text=self._t("status_ready"),
                                         font=("Segoe UI", 10), anchor="w")
        self.status_label.pack(side="left", padx=10)

    def _open_settings(self):
        settings_win = ctk.CTkToplevel(self)
        settings_win.title(self._t("settings_title"))
        settings_win.geometry("500x450")
        settings_win.resizable(True, True)

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 500) // 2
        y = (sh - 450) // 2
        settings_win.geometry(f"500x450+{x}+{y}")
        settings_win.attributes("-topmost", True)
        settings_win.after(200, lambda: settings_win.attributes("-topmost", False))
        settings_win.lift()
        settings_win.focus_force()

        scroll = ctk.CTkScrollableFrame(settings_win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(scroll, text=self._t("settings_title"),
                     font=("Segoe UI", 18, "bold")).pack(pady=(0, 20))

        theme_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        theme_frame.pack(fill="x", pady=8)
        ctk.CTkLabel(theme_frame, text=self._t("theme") + ":",
                     font=("Segoe UI", 13)).pack(side="left")
        theme_combo = ctk.CTkComboBox(
            theme_frame,
            values=[self._t("theme_light"), self._t("theme_dark"), self._t("theme_system")],
            width=150,
            command=self._on_theme_change
        )
        current_theme = self.settings.get("theme", "dark")
        theme_map = {"light": self._t("theme_light"),
                     "dark": self._t("theme_dark"),
                     "system": self._t("theme_system")}
        theme_combo.set(theme_map.get(current_theme, self._t("theme_dark")))
        theme_combo.pack(side="right")

        ctk.CTkButton(scroll, text=self._t("change_master_pw"),
                      command=self._change_master_password,
                      width=250, font=("Segoe UI", 12)).pack(pady=15)

        ctk.CTkButton(scroll, text=self._t("export_json"),
                      command=self._export_json,
                      width=250, font=("Segoe UI", 12)).pack(pady=8)

        ctk.CTkButton(scroll, text=self._t("import_json"),
                      command=self._import_json,
                      width=250, font=("Segoe UI", 12)).pack(pady=8)

        auto_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        auto_frame.pack(fill="x", pady=15)
        ctk.CTkLabel(auto_frame, text=self._t("auto_close") + ":",
                     font=("Segoe UI", 12)).pack(side="left")
        auto_slider = ctk.CTkSlider(auto_frame, from_=0, to=30,
                                     number_of_steps=31,
                                     width=200)
        auto_slider.set(self._auto_close_minutes)
        auto_slider.pack(side="left", padx=(10, 0))
        auto_label = ctk.CTkLabel(auto_frame, text=str(self._auto_close_minutes),
                                  width=40, font=("Segoe UI", 12))
        auto_label.pack(side="left", padx=(4, 0))

        def on_auto_close_change(val):
            minutes = int(val)
            self._auto_close_minutes = minutes
            auto_label.configure(text=str(minutes) if minutes > 0 else self._t("auto_close_disabled"))
            self._save_settings()
            self._reset_auto_close()

        auto_slider.configure(command=on_auto_close_change)

        ctk.CTkButton(scroll, text=self._t("close"),
                      command=settings_win.destroy,
                      width=200, font=("Segoe UI", 12),
                      fg_color="gray40", hover_color="gray50").pack(pady=20)

    def _on_theme_change(self, choice):
        theme_map = {self._t("theme_light"): "light",
                     self._t("theme_dark"): "dark",
                     self._t("theme_system"): "system"}
        theme = theme_map.get(choice, "dark")
        self.settings["theme"] = theme
        ctk.set_appearance_mode(theme)
        self._save_settings()

    def _change_master_password(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(self._t("change_master_title"))
        dialog.geometry("420x360")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 420) // 2
        y = (sh - 360) // 2
        dialog.geometry(f"420x360+{x}+{y}")

        ctk.CTkLabel(dialog, text=self._t("current_password"),
                     font=("Segoe UI", 13)).pack(pady=(20, 8))
        old_entry = ctk.CTkEntry(dialog, show="*", width=280, font=("Segoe UI", 13))
        old_entry.pack(pady=5)
        old_entry.focus_set()

        ctk.CTkLabel(dialog, text=self._t("new_password"),
                     font=("Segoe UI", 13)).pack(pady=(10, 8))
        new_entry = ctk.CTkEntry(dialog, show="*", width=280, font=("Segoe UI", 13))
        new_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text=self._t("confirm_new_password"),
                     font=("Segoe UI", 13)).pack(pady=(10, 8))
        confirm_entry = ctk.CTkEntry(dialog, show="*", width=280, font=("Segoe UI", 13))
        confirm_entry.pack(pady=5)

        def do_change():
            old_pw = old_entry.get()
            new_pw = new_entry.get()
            confirm_pw = confirm_entry.get()
            if not old_pw:
                messagebox.showwarning("Warning", self._t("err_current_empty"))
                return
            if not new_pw:
                messagebox.showwarning("Warning", self._t("err_new_empty"))
                return
            if len(new_pw) < 8:
                messagebox.showwarning("Warning", self._t("err_new_short"))
                return
            if new_pw != confirm_pw:
                messagebox.showwarning("Warning", self._t("err_new_mismatch"))
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
                messagebox.showerror("Error", self._t("err_current_wrong"))
                try:
                    conn.close()
                except Exception:
                    pass
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

        ctk.CTkButton(dialog, text=self._t("change_master_pw"),
                      command=do_change, width=200,
                      font=("Segoe UI", 13, "bold")).pack(pady=15)
        dialog.bind("<Return>", lambda e: do_change())

    def _export_json(self):
        try:
            folder = filedialog.askdirectory()
            if not folder:
                return
            export_data = []
            for service, login, decrypted_pw in self._all_entries:
                enc_pw = self._encrypt(decrypted_pw)
                export_data.append({
                    "service": service,
                    "login": login,
                    "password": enc_pw
                })
            file_path = os.path.join(folder, "passwords_export.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            self._show_toast(self._t("status_exported"), "success")
        except Exception as e:
            self._show_toast(self._t("err_export", err=str(e)), "error")

    def _import_json(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json")])
            if not file_path:
                return
            if not os.path.exists(file_path):
                self._show_toast(self._t("err_import_file"), "error")
                return
            with open(file_path, "r", encoding="utf-8") as f:
                import_data = json.load(f)

            if not isinstance(import_data, list):
                self._show_toast(self._t("err_import"), "error")
                return

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            imported = 0
            skipped = 0
            for entry in import_data:
                try:
                    service = entry.get("service", "")
                    login = entry.get("login", "")
                    raw_pw = entry.get("password", "")
                    if not service or not raw_pw:
                        skipped += 1
                        continue

                    try:
                        dec_pw = self._decrypt(raw_pw)
                    except Exception:
                        dec_pw = raw_pw

                    cursor.execute(
                        "SELECT id FROM passwords WHERE service = ?",
                        (service,))
                    if not cursor.fetchone():
                        re_encrypted = self._encrypt(dec_pw)
                        cursor.execute(
                            "INSERT INTO passwords (service, login, password) VALUES (?, ?, ?)",
                            (service, login, re_encrypted))
                        imported += 1
                    else:
                        skipped += 1
                except Exception:
                    skipped += 1
                    continue
            conn.commit()
            conn.close()
            self._load_data()
            msg = self._t("status_imported") + f" ({imported})"
            if skipped:
                msg += f", skipped ({skipped})"
            self._show_toast(msg, "success" if imported else "warning")
        except Exception as e:
            self._show_toast(self._t("err_import", err=str(e)), "error")

    def _filter_tree(self):
        if not hasattr(self, "tree"):
            return
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for service, login, decrypted_pw in self._all_entries:
            if query in service.lower() or query in login.lower():
                self.tree.insert("", "end", values=(service, login, decrypted_pw))

    def _switch_language(self, lang_code):
        self.lang_code = lang_code
        self.text = LANG[lang_code]
        self._save_settings()
        if self.fernet:
            self._setup_ui()
            self._load_data()

    def _load_data(self):
        if not hasattr(self, "tree"):
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._all_entries = []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT service, login, password FROM passwords ORDER BY service")
            for row in cursor.fetchall():
                service, login, encrypted_pw = row
                decrypted_pw = self._decrypt(encrypted_pw)
                self._all_entries.append((service, login, decrypted_pw))
                self.tree.insert("", "end", values=(service, login, decrypted_pw))
            conn.close()
        except Exception as e:
            self._show_toast(self._t("err_load", err=str(e)), "error")

    def _add_entry(self):
        service = self.service_var.get().strip()
        login = self.login_var.get().strip()
        password = self.password_var.get().strip()
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
        password = self.password_var.get().strip()
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

        if messagebox.askyesno("Confirm", self._t("confirm_delete", service=service)):
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
        self.password_var.set("".join(password[:length]))

    def _clear_fields(self):
        self.service_var.set("")
        self.login_var.set("")
        self.password_var.set("")
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
            self.password_var.set(values[2])

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    import traceback

    _log_path = os.path.join(get_data_dir(), "startup.log")
    _log_lines = []
    try:
        _log_lines.append(f"Python: {sys.version}")
        _log_lines.append(f"CWD: {os.getcwd()}")
        _log_lines.append(f"Script: {os.path.abspath(__file__)}")
        _log_lines.append(f"Data dir: {get_data_dir()}")
        _log_lines.append("Creating app...")
        app = PasswordManagerApp()
        _log_lines.append("App created. Starting mainloop...")
        with open(_log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(_log_lines))
        app.run()
    except Exception:
        tb = traceback.format_exc()
        _log_lines.append(f"\nEXCEPTION:\n{tb}")
        with open(_log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(_log_lines))
        err_path = os.path.join(get_data_dir(), "crash.log")
        with open(err_path, "w", encoding="utf-8") as f:
            f.write(tb)
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"App crashed.\n\n{tb}\n\nSee: {err_path}")
            root.destroy()
        except Exception:
            print(tb)
