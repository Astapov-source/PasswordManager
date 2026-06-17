import subprocess
import sys

cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", "PasswordManager",
    "--clean",
    "main.py",
]

print("Building PasswordManager.exe ...")
subprocess.run(cmd, check=True)
print("Done! exe in dist/ folder")
