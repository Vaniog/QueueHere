from app import create_app, db

application = create_app()

if __name__ == "__main__":
    application.run('0.0.0.0')
