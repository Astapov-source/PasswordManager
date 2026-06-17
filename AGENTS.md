# Password Manager

## Quick Start
```bash
pip install pyinstaller cryptography
python password_manager.py
python build.py  # produces single .exe
```

## Architecture
- Single-file app: `password_manager.py`
- Encryption: Fernet + PBKDF2 (from `cryptography`)
- Storage: SQLite with encrypted passwords
- GUI: Tkinter with dark theme (custom colors, no external deps)
- Settings: `settings.json` (persists language choice)
- Localization: English (`en`) and Russian (`ru`)

## Data Location (important)
- **Always**: DB/settings stored in `%APPDATA%/PasswordManager/` (Windows) or `~/.password-manager/` (Linux)
- Same location for both script mode and exe mode
- This means the exe can be moved anywhere without losing data

## Conventions
- Passwords: configurable 4–64 chars, guaranteed letters+digits+symbols
- Duplicate service names rejected on add
- Deletion requires confirmation
- Cross-platform: Windows + Linux identical behavior
- Double-click table row → loads into edit fields
- Language switch via dropdown in top-right corner
- Dark purple/gray theme with accent-colored buttons