from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) #reinicio cada vez que se guarda el codigo
# nunca usar debug =true en un proyecto real es un riesgo de seguridad