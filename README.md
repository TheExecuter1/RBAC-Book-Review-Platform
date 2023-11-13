
# My Flask App

## Description
[Provide a brief description of what your app does.]

## Requirements
- Python 3.x
- PostgreSQL

## Installation

### Setting Up a Python Environment
1. Clone the repository: `git clone [https://github.com/TheExecuter1/RBAC-Book-Review-Platform/tree/main]`
2. Navigate to the project directory: `cd [project-directory]`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On Unix or MacOS: `source venv/bin/activate`
5. Install required packages: `pip install -r requirements.txt`

### Configuring PostgreSQL
1. Install PostgreSQL: [https://www.postgresql.org/download/]
2. Create a new PostgreSQL database for the app.
3. Update the app's configuration to connect to your PostgreSQL database:
   - Open `app/__init__.py` 
   - Set the `SQLALCHEMY_DATABASE_URI` to your database URI: 
     ```
     SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'
     ```

## Database Migrations

### Setting Up Migrations
If you haven't already set up migrations, you'll need to initialize a migration directory:

```bash
flask db init
```

This command will add a `migrations` folder to your application, which will track all database migrations.

Open the migrations folder and go to alembic.ini
Below the [alembic] put this line 'sqlalchemy.url = postgresql://username:password@localhost/dbname'

### Running Migrations

If you have existing migration scripts:

1. If you make changes to your database models, generate new migration scripts:
   ```bash
   flask db migrate -m "Description of changes"
   ```

2. Again, apply the new migrations to the database:
   ```bash
   flask db upgrade
   ```

## Environment Variables

Your application uses environment variables for configuration. To set these up:

1. Create a `.env` file in the root directory of the project.
2. Add the following environment variables to the `.env` file:
   ```
   SECRET_KEY=your_secret_key_here
   JWT_SECRET_KEY=your_jwt_secret_key_here
   ```
3. Replace `your_secret_key_here` and `your_jwt_secret_key_here` with your own secret keys.

### Generating Secret Keys
For security, it's important to generate your own secret keys. Here's how you can generate a secret key in Python:

```python
import os
print(os.urandom(16))
```

Run this script in a Python environment to generate a secure secret key.

### Running the App
1. Run the Flask application: `flask run.py`
3. Access the app in your web browser at `http://127.0.0.1:5000/`

