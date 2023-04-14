import enum

from app import db

import shortuuid
from datetime import datetime


class UserQueue(db.Model):
    member_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), primary_key=True)
    queue_id = db.Column(db.String(10), db.ForeignKey('queue.id', ondelete="CASCADE"), primary_key=True)
    name_printed = db.Column(db.String(30), nullable=False)

    index_in_queue = db.Column(db.Integer, primary_key=True)
    arrive_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    is_visible = db.Column(db.Boolean, default=True, nullable=False)

    member = db.relationship("User", back_populates="queues", passive_deletes=True)
    queue = db.relationship("Queue", back_populates="members", passive_deletes=True)

    def update_arrive_time(self):
        self.arrive_time = datetime.utcnow()


def generate_queue_id():
    try_times = 5

    def try_to_generate_from(alphabet):
        for i in range(try_times):
            new_id = shortuuid.ShortUUID(alphabet=alphabet).random(length=5)
            if Queue.query.filter_by(id=new_id).first() is None:
                return new_id
        return None

    return try_to_generate_from('0123456789') or \
        try_to_generate_from('ABCDEFGHIJKLMNOPQRSTUVWXYZ') or \
        try_to_generate_from('abcdefghijklmnopqrstuvwxyz') or \
        try_to_generate_from('0123456789ABCDEFGHJKLMNPQRSTUVWXYZ') or \
        try_to_generate_from('0123456789abcdefghijklmnopqrstuvwxyz') or \
        try_to_generate_from('23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')


class Queue(db.Model):
    id = db.Column(db.String(10), primary_key=True, default=generate_queue_id)
    name = db.Column(db.String(100), nullable=False)
    members = db.relationship('UserQueue', back_populates='queue', cascade='all, delete, merge, save-update')
    tasks = db.relationship('QueueTask', back_populates='queue', cascade='all, delete, merge, save-update')
    last_index = db.Column(db.Integer, nullable=False, default=0)

    is_open = db.Column(db.Boolean, nullable=False, default=True)

    admin_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    admin = db.relationship('User', back_populates='owned_queues')

    def __repr__(self):
        return '<Queue {}>'.format(self.name)

    def close(self):
        self.is_open = False

    def open(self):
        self.is_open = True

    def list(self):
        return UserQueue.query \
            .filter_by(queue_id=self.id, is_visible=True) \
            .order_by(UserQueue.index_in_queue)

    def tasks_sorted(self):
        return sorted(self.tasks, key=lambda task: task.execute_time)

    def next_clearing(self):
        return next(x for x in self.tasks_sorted() if x.action == TaskEnum.clear)

    def next_opening(self):
        return next(x for x in self.tasks_sorted() if x.action == TaskEnum.open)

    def next_closing(self):
        return next(x for x in self.tasks_sorted() if x.action == TaskEnum.close)

    def get_user_queue(self, user):
        return UserQueue.query.filter_by(queue_id=self.id, member_id=user.id).first()

    def was_in_queue(self, user):
        return self.get_user_queue(user) is not None

    def contains(self, user):
        return self.was_in_queue(user) and self.get_user_queue(user).is_visible

    def add_member(self, user, name_printed):
        if self.contains(user):
            return
        self.last_index += 1
        if self.was_in_queue(user):
            was_user = self.get_user_queue(user)
            was_user.name_printed = name_printed
            was_user.index_in_queue = self.last_index
            was_user.is_visible = True
            was_user.update_arrive_time()
            return
        uq = UserQueue(name_printed=name_printed,
                       index_in_queue=self.last_index,
                       arrive_time=datetime.utcnow())
        uq.member = user
        self.members.append(uq)

    def clear(self):
        for member in self.members:
            self.leave_member(member.member)

    def leave_member(self, user):
        UserQueue.query.filter_by(member_id=user.id, queue_id=self.id).first().is_visible = False

    def remove_member(self, user):
        UserQueue.query.filter_by(member_id=user.id, queue_id=self.id).delete()


class TaskEnum(enum.Enum):
    clear = 1
    close = 2
    open = 3

    def __str__(self):
        return self.name


class QueueTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    queue_id = db.Column(db.String(10), db.ForeignKey('queue.id', ondelete="CASCADE"), nullable=False)
    queue = db.relationship("Queue", back_populates="tasks", passive_deletes=True)

    action = db.Column(db.Enum(TaskEnum), nullable=False)  # clear, close, open
    execute_time = db.Column(db.DateTime, nullable=False, index=True)

    def __repr__(self):
        return "<QueueTask {}: {}>".format(self.action, self.execute_time)

    @staticmethod
    def get_nearest():
        return QueueTask.query.order_by(QueueTask.execute_time).first()

    def execute_if_needed(self):
        if self.execute_time <= datetime.utcnow():
            self.execute()
            db.session.delete(self)
            return True
        return False

    def execute(self):
        if self.action == TaskEnum.clear:
            self.queue.clear()
        elif self.action == TaskEnum.close:
            self.queue.close()
        elif self.action == TaskEnum.open:
            self.queue.open()
