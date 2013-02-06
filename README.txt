workon gustosity
./manage.py syncdb --settings=gustosity.settings.prod
./manage.py collectstatic --settings=gustosity.settings.prod
./apache2/bin/restart
