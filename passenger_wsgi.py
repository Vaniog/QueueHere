import sys

import os

INTERP = os.path.expanduser("/home/forva/FlaskPlayground/QueueSite/venv/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from queue_app import application

if __name__ == '__main__':
    application.run()
