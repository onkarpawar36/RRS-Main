# Room Rental System

A Django-based web application for managing room rentals with features like user authentication, room listings, chat functionality, and more.

## Features

- User registration and authentication
- Room listing and management
- Image upload for rooms
- Real-time chat between users and room owners
- Bookmark/favorite rooms
- Room reporting system
- Responsive design with Bootstrap

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Run development server:
   ```bash
   python manage.py runserver
   ```

## Deployment to Render

This application is configured for deployment on Render.com:

1. Push your code to GitHub
2. Connect your GitHub repository to Render
3. Create a new Web Service on Render
4. Select your repository
5. Use the following settings:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn rental_system_project.wsgi:application`
   - **Environment**: `Python 3.11.5`

### Environment Variables

Set these environment variables in Render:
- `SECRET_KEY`: A secure random string for Django
- `DEBUG`: Set to `false` for production
- `DATABASE_URL`: Will be automatically provided by Render's PostgreSQL

## Technology Stack

- **Backend**: Django 5.2.6
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **File Storage**: Local storage
- **Deployment**: Render.com