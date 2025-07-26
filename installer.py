import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Todos los paquetes han sido instalados correctamente.")
    except subprocess.CalledProcessError:
        print("❌ Hubo un error al instalar los paquetes.")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()
