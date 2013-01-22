#!/bin/bash
rm -rf gustosity/media/photos
rm -rf gustosity/media/cache
python manage.py syncdb --noinput --settings=gustosity.settings.prod
python manage.py migrate --settings=gustosity.settings.prod
python manage.py loaddata fixtures/init_data_sites.json --settings=gustosity.settings.prod
python manage.py loaddata fixtures/init_data_users.json --settings=gustosity.settings.prod
python manage.py loaddata fixtures/init_data_food.json --settings=gustosity.settings.prod
python manage.py loaddata fixtures/init_flatpages.json --settings=gustosity.settings.prod
python manage.py fakeusers --settings=gustosity.settings.prod
python manage.py fakeprofiles --settings=gustosity.settings.prod
python manage.py fakestream --settings=gustosity.settings.prod

