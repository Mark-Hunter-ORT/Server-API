# FulboQL - Backend

FulboQL is an application where a user can upload football players, managers, clubs and referees. Then
the user can create matches to represent real-life matches and load the events of the match in real-time.

The kinds of events that cna be loaded are:
* Match Moments (start/ends of times/extra times)
* Restarts (kickoffs, freekicks, etc)
* Fouls (including perpetrator, victim and punishment)
* Highlights (free text input to denote miscellaneous events)
* Injuries
* Substitutions
* On Goals (including goalkeeper, assist, if it ended in a goal and if it was a penalty)

## Backend

The backend is a Flask server with SQLAlchemy for DB integration and using a PostgreSQL DB.

### Instalation

Clone the Git repository and configure the virtualenv

~~~
git clone https://github.com/SebastianMCarreira/fulboQL.git
cd fulboQL
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
~~~

Generate the app/local_settings.py file using the local_settings_example.py temaplate with the required following variables:
* SECRET_KEY (random long string) 
* SQLALCHEMY_DATABASE_URI (connection string for your postgreSQL database including credentials and db)
* INITIAL_USERS (with an admin user and a normal user, inclding starting credentials)

Initialize the database and start the server

~~~
python manage.py init_db
python manage.py runserver
~~~

The server is now available at http://localhost:5000/