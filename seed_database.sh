#!/bin/bash

rm db.sqlite3
rm -rf ./QuestScribeapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations QuestScribeapi
python3 manage.py migrate QuestScribeapi


