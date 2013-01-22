#!/bin/bash
rm gustosity/default.db
rm -rf gustosity/media/photos
rm -rf gustosity/media/cache
python manage.py syncdb --noinput
python manage.py migrate
python manage.py loaddata fixtures/init_data_sites.json
python manage.py loaddata fixtures/init_data_users.json
python manage.py loaddata fixtures/init_data_food.json
python manage.py loaddata fixtures/init_flatpages.json
python manage.py fakeusers
python manage.py fakeprofiles
python manage.py fakestream
python manage.py runserver
