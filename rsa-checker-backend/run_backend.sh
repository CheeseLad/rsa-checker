#!/bin/bash

python3 generate_data.py &

gunicorn --bind 127.0.0.1:5000 wsgi:app