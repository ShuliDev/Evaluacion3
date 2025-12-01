Requisitos

- Python 
- Django 
- Pillow
  

1. Crear y activar un entorno virtual:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
Esto posiblemente solo funcione con Powershell Extension, no el Powershell normal


2. Instalar dependencias:


pip install -r requirements.txt
o también
pip install django pillow


3. Ejecutar el servidor de desarrollo:

python manage.py runserver


Visita `http://127.0.0.1:8000/` para ver la tienda y `http://127.0.0.1:8000/admin/` para el panel de administración.
Usuario: admin
Contraseña: admin
