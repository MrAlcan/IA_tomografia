from app import create_app, db, iniciar_datos

app = create_app()
with app.app_context():
    db.create_all()
    iniciar_datos()

if __name__ == "__main__":
    app.run(debug=True)
