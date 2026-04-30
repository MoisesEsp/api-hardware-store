# API RESTful - Gestión de Inventario de Hardware

Una API robusta desarrollada en Python y Flask para la administración de un inventario de tienda de hardware y periféricos. Implementa seguridad mediante JSON Web Tokens (JWT) y operaciones CRUD completas sobre una base de datos relacional.

## Arquitectura y Tecnologías
*   **Backend:** Python 3, Flask, SQLAlchemy (ORM)
*   **Base de Datos:** PostgreSQL (Alojada en Neon - Serverless)
*   **Autenticación:** JWT (Flask-JWT-Extended)
*   **Despliegue:** Render (Gunicorn WSGI)

## URL Base (Producción)
https://TU-SERVICIO.onrender.com/api

## Endpoints

### 1. Autenticación
Protege las rutas de modificación exigiendo un token de acceso.

*   **Endpoint:** `POST /login`
*   **Cuerpo (JSON):**
    ```json
    {
      "username": "admin",
      "password": "tu_password"
    }
    ```
*   **Respuesta Exitosa (200 OK):** Devuelve el token JWT.

### 2. Catálogo Público
Obtiene la lista completa de productos disponibles junto con sus categorías (Resolución relacional).

*   **Endpoint:** `GET /productos`
*   **Acceso:** Público
*   **Respuesta Exitosa (200 OK):** Lista de objetos JSON con el inventario.

### 3. Modificación de Inventario (Rutas Protegidas)
Todas las siguientes rutas requieren la cabecera HTTP: `Authorization: Bearer <tu_token>`

#### Añadir Producto
*   **Endpoint:** `POST /productos`
*   **Cuerpo (JSON):** `nombre`, `precio`, `categoria_id` (obligatorios). `especificaciones`, `stock` (opcionales).
*   **Respuesta Exitosa (201 Created):** Confirma la creación y devuelve el ID.

#### Actualizar Producto (Precio/Stock)
*   **Endpoint:** `PUT /productos/<id>`
*   **Cuerpo (JSON):** Enviar solo los campos a modificar (`precio` y/o `stock`).
*   **Respuesta Exitosa (200 OK).**

#### Eliminar Producto
*   **Endpoint:** `DELETE /productos/<id>`
*   **Respuesta Exitosa (200 OK).**

## Despliegue Local
1. Clonar el repositorio.
2. Crear un entorno virtual: `python -m venv .venv`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Crear archivo `.env` con `DATABASE_URL` y `JWT_SECRET_KEY`.
5. Ejecutar servidor: `python run.py`