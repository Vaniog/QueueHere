#!/bin/bash

gunicorn -w 4 'queue_app:create_app()' -b 0.0.0.0