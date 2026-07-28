import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

PASTAS = [
    BASE_DIR / "data" / "raw",
    BASE_DIR / "data" / "cleaned",
    BASE_DIR / "data" / "processed",
    ]

def criar_pastas():

    for pasta in PASTAS:
        pasta.mkdir(parents=True, exist_ok=True)

def rodar_todos_os_scripts():
    pasta_scripts = BASE_DIR / "scripts"

    scripts = sorted(pasta_scripts.glob("*.py"))

    for script in scripts:
            print(f"\nExecutando: {script.name}")

            resultado = subprocess.run(
            [sys.executable, str(script)], 
            cwd=pasta_scripts, 
            check=False
        )

            if resultado.returncode != 0:
                print(f"Erro ao executar '{script.name}' (Código: {resultado.returncode}).")
                print("Pipeline cancelado.")
                sys.exit(1)
criar_pastas()
rodar_todos_os_scripts()