xs2xps
======

XS2XPS is the server that is behind the screen in the office. Its mostly an experimental project.
It uses a connection to the XPSsystem but also some motion detector data to show on screen ticket information and Mr JJ's movements.
It periodically checks for new data in our XPS system and stores the data in REDIS.
It serves the ticket information using a JSON api.

Installation
------------

1. install Postgres and create the necessary users/databases in it (find passwords and database names in settings)
2. install Redis
3. create a python virtual environment for python2.7
4. activate virtualenvironment
5. pip install -r requirements/local.txt
6. python manage.py migrate
7. create a superuser
8. python manage.py runserver

Tasks
-----

1. Solve any problems during installation (use google!)
2. Solve code problems that show up
3. Use postman to check all endpoints
4. Add a new endpoint /apiratings which will serve the ratings of the latest month (check existing ones)
5. Create a single page (separate from the project) that makes an ajax call to your local installation of the server and requests the /apiratings
6. Run the background task by creating a celeryworker, starting celerybeat and registering a periodic task on your /admin interface (GOOGLE!!!)
7. If you 're done try to connect the raspberry pi with the motion detector to your local installation (ngrok might be helpful),
 also you need to boot the raspberry and edit the python script that controls the motion detector

General
-------

Don't hesitate to ask Stavros for anything, the tasks are not clear enough,
just try to be precise in your questions, after you investigated yourself.
