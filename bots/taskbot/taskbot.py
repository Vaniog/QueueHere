import threading
import time
from app.extensions import db
from app.queue.models import QueueTask


class TaskBotThread(threading.Thread):
    def __init__(self, current_app):
        self.current_app = current_app
        threading.Thread.__init__(self)
        self.daemon = True

    UPDATE_FREQUENCY = 1  # in seconds

    def run(self):
        with self.current_app.app_context():
            while True:
                nearest = QueueTask.get_nearest()
                if nearest is not None and nearest.execute_if_need():
                    db.session.commit()
                time.sleep(self.UPDATE_FREQUENCY)
