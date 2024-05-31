import subprocess

# Ejecutar el script expect para crear la base de datos en una sesión interactiva de psql
try:
    subprocess.run(['expect', './create_db.exp'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error ejecutando el script: {e}")
except FileNotFoundError as e:
    print(f"Expect no está instalado o el script no se encuentra: {e}")
