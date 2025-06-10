# fitness-studio-
Django project with clean structure, including models, views, URLs, and optional APIs.



# Bookstore API

## Setup Instructions



# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Load seed data
python manage.py loaddata sample_books.json

# Run server
python manage.py runserver

