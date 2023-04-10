from app import create_app, db
from app.queue.models import Queue, UserQueue
from app.auth.models import User

if __name__ == "__main__":
    app = create_app()


    @app.shell_context_processor
    def make_shell_context():
        create_app()
        return {'db': db, 'User': User, 'Queue': Queue, 'UserQueue': UserQueue}
