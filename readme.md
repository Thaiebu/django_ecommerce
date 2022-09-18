#Create a virtual environment to install dependencies in and activate it:

$ python3 -m venv env
$ source env/bin/activate
#Then install the dependencies:

(env)$ pip install -r requirements.txt
Note the (env) in front of the prompt.

Once pip has finished downloading the dependencies:

(env)$ cd django_ecommerce
(env)$ python manage.py runserver
And navigate to http://127.0.0.1:8000/.