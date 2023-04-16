from app import create_app, db
from app.queue.models import Queue, UserQueue
from app.auth.models import User


application = create_app()

if __name__ == "__main__":
    application.run('0.0.0.0')

    @app.shell_context_processor
    def make_shell_context():
        create_app()
        return {'db': db, 'User': User, 'Queue': Queue, 'UserQueue': UserQueue}
