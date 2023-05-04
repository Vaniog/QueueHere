import enum

from app import db


class StatsEnum(enum.Enum):
    users_registered = "users_registered"
    queues_created = "queues_created"
    queues_entries = "queues_entries"
    likes_given = "likes_given"

    def __str__(self):
        return self.name


class Stats(db.Model):
    name = db.Column(db.String(30), primary_key=True)
    count = db.Column(db.Integer, nullable=False, default=0)

    @staticmethod
    def get_or_create(name):
        stat = Stats.query.filter_by(name=name).first()
        if stat is None:
            stat = Stats(name=name, count=0)
            db.session.add(stat)
            db.session.commit()
        return stat

    @staticmethod
    def increase(name):
        Stats.get_or_create(name).count += 1

    @staticmethod
    def decrease(name):
        Stats.get_or_create(name).count -= 1

    @staticmethod
    def get_count_of(name):
        if name == StatsEnum.queues_created:
            return Queue.query.count()
        return Stats.get_or_create(name).count


from app.queue.models import Queue
