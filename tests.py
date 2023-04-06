import unittest
from app import db, create_app
from app.queue.models import Queue, UserQueue
from app.auth.models import User
from app.config import Config


class UserModelCase(unittest.TestCase):
    def setUp(self):
        config_obj = Config()
        config_obj.SQLALCHEMY_DATABASE_URI = 'sqlite://'
        app = create_app(config_obj)

        db.session.remove()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_queue(self):
        u1 = User(username='u1', email='u1@gmail.com')
        u2 = User(username='u2', email='u2@gmail.com')
        u3 = User(username='u3', email='u3@gmail.com')

        q1 = Queue(name="q")
        q2 = Queue(name="q")

        q1.add_member(u1, 'u1 printed')
        q1.add_member(u2, 'u2 printed')

        db.session.add_all([u1, u2, u3, q1, q2])
        db.session.commit()

        self.assertEqual(2, len(q1.members))
        self.assertTrue(q1.contains(u1))
        self.assertFalse(q1.contains(u3))

        q1.remove_member(u1)
        db.session.commit()

        self.assertEqual(1, len(q1.members))
        self.assertFalse(q1.contains(u1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
