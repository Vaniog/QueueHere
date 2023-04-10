import threading
from asyncio import sleep


class TaskBot:
    def run(self):
        print(1)
        sleep(100)


class TaskBotThread(threading.Thread):
    def run(self) -> None:
        bot = TaskBot()
        bot.run()
