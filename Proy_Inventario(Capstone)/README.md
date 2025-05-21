# 📦 Inventario Personal - Proyecto Flask
Por:
     Eloim N. Borges Millete
     R00572231
     COMP 2052


Este proyecto es una aplicación web para gestionar un inventario personal, con autenticación de usuarios y control de permisos por rol.

## 🚀 Requisitos

- Python 3.10+
- MySQL Server
- Virtualenv (opcional)

## 📁 Estructura

```
/final_project/
├── run.py
├── config.py
├── requirements.txt
├── create_demo_users.py
├── /app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── test_routes.py
│   ├── auth_routes.py
│   └── /templates/
│       ├── cambiar_password.html
│       ├── dashboard.html
│       ├── index.html
│       ├── item_form.html
│       ├── layout.html
│       ├── login.html
│       ├── register.html
│       └── usuarios.html
├── /pruebas/
│   ├── create.rest
│   ├── read.rest
│   ├── read-a-row.rest
│   ├── update.rest
│   └── delete.rest
```

## 👥 Roles y permisos

- **Admin:** Acceso total (CRUD, gestión de usuarios)
- **Supervisor:** Puede ver y gestionar ítems propios
- **Empleado:** Solo visualiza

## ⚙️ Instalación y uso

1. Instala dependencias:
```bash
pip install -r requirements.txt
```

2. Crea base de datos en MySQL llamada `inventario_personal` y ejecuta el script:
```bash
mysql -u root -p < 05_inventario.sql
```

3. Crea usuarios iniciales:
```bash
python create_demo_users.py
```

4. Inicia la aplicación:
```bash
python run.py
```

5. Accede a: `http://localhost:5000`

## 🔐 Usuarios de prueba

| Usuario     | Rol        | Email              | Contraseña  |
|-------------|------------|--------------------|-------------|
| Eloim       | Admin      | Borges@inter.edu   | admin3010   |
| Supervisor  | Supervisor | supervisor@demo.com| super123    |
| Empleado    | Empleado   | empleado@demo.com  | empleado123 |

## 🧪 Pruebas REST

Puedes probar la API usando los archivos `.rest` en la carpeta `/pruebas/` con la extensión **REST Client** en VS Code.

