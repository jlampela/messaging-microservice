from app import create_app, db

app = create_app("development")

@app.before_first_request
def create_db_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run()