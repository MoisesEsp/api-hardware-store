import requests

url_base = 'http://127.0.0.1:5000/api/productos'
url_login = 'http://127.0.0.1:5000/api/login'

credenciales = {
    "username": "admin",
    "password": "admin123"
}

print("1. Solicitando token de acceso...")
respuesta_login = requests.post(url_login, json=credenciales)

if respuesta_login.status_code == 200:
    # Extraemos el token del diccionario JSON
    token = respuesta_login.json().get('token')
    print("✅ Token obtenido exitosamente.\n")

    # Preparamos la cabecera de autorización exigida por el estándar JWT
    cabeceras = {
        "Authorization": f"Bearer {token}"
    }

    print("2. Intentando crear un producto protegido por token...")
    nuevo_hardware = {
        "nombre": "Tarjeta Gráfica RTX 4060",
        "especificaciones": "8GB GDDR6, DLSS 3",
        "precio": 320.00,
        "stock": 4,
        "categoria_id": 2 # Asumiendo que 2 es "Componentes Internos"
    }

    # Hacemos la petición POST enviando los datos Y las cabeceras de seguridad
    respuesta_post = requests.post(url_base, json=nuevo_hardware, headers=cabeceras)
    
    print(f"Estado POST: {respuesta_post.status_code}")
    print(f"Respuesta: {respuesta_post.json()}")

else:
    print(f"❌ Fallo el login. Estado: {respuesta_login.status_code}")