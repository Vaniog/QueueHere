#!/bin/bash

flask db upgrade
gunicorn -w 4 'queue_app:create_app()' -b 0.0.0.0
