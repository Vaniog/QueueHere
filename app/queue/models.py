from app import db

import shortuuid


class UserQueue(db.Model):
    member_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), primary_key=True)
    queue_id = db.Column(db.String(10), db.ForeignKey('queue.id', ondelete="CASCADE"), primary_key=True)
    name_printed = db.Column(db.String(30), nullable=False)

    index_in_queue = db.Column(db.Integer, primary_key=True)
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    member = db.relationship("User", back_populates="queues", passive_deletes=True)
    queue = db.relationship("Queue", back_populates="members", passive_deletes=True)


def generate_queue_id():
    new_id = shortuuid.ShortUUID().random(length=5)
    while Queue.query.filter_by(id=new_id).first() is not None:
        new_id = shortuuid.ShortUUID().random(length=5)
    return new_id


class Queue(db.Model):
    id = db.Column(db.String(10), primary_key=True, default=generate_queue_id)
    name = db.Column(db.String(100), nullable=False)
    members = db.relationship('UserQueue', back_populates='queue', cascade='all, delete, merge, save-update')
    last_index = db.Column(db.Integer, nullable=False, default=0)

    admin_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    admin = db.relationship('User', back_populates='owned_queues')

    def __repr__(self):
        return '<Queue {}>'.format(self.name)

    def list(self):
        return UserQueue.query \
            .filter_by(queue_id=self.id, is_visible=True) \
            .order_by(UserQueue.index_in_queue)

    def get_user_queue(self, user):
        return UserQueue.query.filter_by(queue_id=self.id, member_id=user.id).first()

    def was_in_queue(self, user):
        return self.get_user_queue(user) is not None

    def contains(self, user):
        return self.was_in_queue(user) and self.get_user_queue(user).is_visible

    def add_member(self, user, name_printed):
        self.last_index += 1
        if self.was_in_queue(user):
            was_user = self.get_user_queue(user)
            was_user.name_printed = name_printed
            was_user.index_in_queue = self.last_index
            was_user.is_visible = True
            return
        uq = UserQueue(name_printed=name_printed, index_in_queue=self.last_index)
        uq.member = user
        self.members.append(uq)

    def leave_member(self, user):
        UserQueue.query.filter_by(member_id=user.id, queue_id=self.id).first().is_visible = False

    def remove_member(self, user):
        UserQueue.query.filter_by(member_id=user.id, queue_id=self.id).delete()
