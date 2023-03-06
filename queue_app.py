from app import create_app, db
from app.models import User, Post

app = create_app()


@app.shell_context_processor
def make_shell_context():
    create_app()
    return {'db': db, 'User': User, 'Post': Post}
