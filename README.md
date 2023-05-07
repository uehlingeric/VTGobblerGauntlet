# VT Gobbler Gauntlet

This is a Django project that displays the stats for the Gobbler Gauntlet tournament, which is a Virginia Tech Club. The project is currently live at www.vtgobblergauntlet.com and uses a PostgreSQL database. It is hosted on an Amazon EC2 instance with a connected RDS database, and is run via Gunicorn and Nginx.

## Getting Started

Follow the instructions below to run the project on your local machine.

### Requirements

- asgiref==3.6.0
- Django==4.1.7
- django-tables2==2.5.3
- numpy==1.24.2
- pandas==1.5.3
- psycopg2==2.9.5
- psycopg2-binary==2.9.5
- python-dateutil==2.8.2
- python-dotenv==1.0.0
- pytz==2023.3
- six==1.16.0
- sqlparse==0.4.4
- tzdata==2023.3
- whitenoise==5.3.0


### Installation

1. Clone the repository:

```bash
git clone https://github.com/uehlingeric/VTGobblerGauntlet.git
cd VTGobblerGauntlet
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Configure the .env file with your database settings and any other environment variables:

```bash
DB_NAME=your-DB-Name
DB_USER=your-username
DB_PASSWORD=your-password
DB_HOST=your-host
DB_PORT=your-port
```

5. Use the scripts in `VTGobblerGauntlet/playerdata/scripts/` to add data:

```bash
python insert_matches.py
python insert_players.py
python insert_teams.py
```

6. Run database migrations:

```bash
python manage.py migrate
```

6. Collect static files:

```bash
python manage.py collectstatic
```

## Usage

To run the development server, execute:

```bash
python manage.py runserver
```
Then, open your web browser and navigate to http://127.0.0.1:8000/.

## Project Structure

Below is an overview of the main project structure:

<pre>
GGSpring2023/
│
├── .env                        # Environment variables
├── .gitignore                  # Files and folders to be ignored by Git
├── manage.py                   # Django management script
├── README.md                   # Project documentation
└── requirements.txt            # Python package dependencies
│
├── GGSpring2023/               # Main Django app
│   ├── asgi.py                 # ASGI config for deployment
│   ├── settings.py             # Django project settings
│   ├── urls.py                 # Project-level URL configuration
│   ├── wsgi.py                 # WSGI config for deployment
│   └── __init__.py             # Package initialization
│
└── playerdata/                 # App containing the main logic
    ├── admin.py                # Admin panel configuration
    ├── apps.py                 # App configuration
    ├── models.py               # Database models
    ├── tests.py                # Test cases
    ├── urls.py                 # App-level URL configuration
    ├── views.py                # Views and logic for rendering pages
    ├── __init__.py             # Package initialization
    │
    ├── migrations/             # Database migration files
    │   └── ...
    │
    ├── scripts/                # Data insertion and processing scripts
    │   └── ...
    │
    ├── static/                 # Static files (CSS, JavaScript, images)
    │   └── playerdata/
    │       └── css/
    │           ├── styles.css
    │           └── vtstyles.css
    │
    ├── templates/              # HTML templates
    │   └── playerdata/
    │       ├── champ_stats.html
    │       ├── index.html
    │       ├── match_list.html
    │       ├── player_detail.html
    │       ├── player_list.html
    │       ├── role_stats.html
    │       ├── team_detail.html
    │       └── team_list.html
    │
    └── templatetags/           # Custom template tags and filters
        ├── custom_filters.py
        └── __init__.py
</pre>

This structure organizes the main application components, such as the Django project settings, app configurations, database models, views, templates, and static files.

## Author

- Eric Uehling