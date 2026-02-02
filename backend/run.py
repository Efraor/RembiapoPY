from app import create_app

<<<<<<< HEAD

# Creamos la instancia de Flask ya configurada (con blueprints registrados, etc.)
app = create_app()

if __name__ == "__main__":
    app.run()
=======
app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
>>>>>>> diego/main
