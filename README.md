# fitness-studio-
Django project with clean structure, including models, views, URLs, and optional APIs.



# Bookstore API

## Setup Instructions

```bash
# Clone repo
git clone https://github.com/your-username/bookstore.git
cd bookstore

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

