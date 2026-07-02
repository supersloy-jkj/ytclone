# YTClone - YouTube Clone in Django

A full-featured YouTube clone built with Django and Bootstrap 5.

## Features

- 🎬 Video upload & playback
- 👤 User authentication (register, login, logout)
- 📺 Channel pages with banners & avatars
- 👍 Like / Dislike system
- 💬 Comments & threaded replies
- 🔔 Subscriptions
- 🔍 Search
- 📜 Watch history
- 📂 Categories / filtering
- 🎛️ Admin dashboard
- ✏️ Edit / delete your own videos & comments

## Quick Start

### 1. Clone / unzip and enter the project
```bash
cd youtube_clone
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and set a real SECRET_KEY
```

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (for admin panel)
```bash
python manage.py createsuperuser
```

### 7. (Optional) Add categories via admin
Visit `http://127.0.0.1:8000/admin/` and add some categories (e.g. Gaming, Music, Tech).

### 8. Run the server
```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
youtube_clone/
├── youtube_clone/      # Django project settings
├── videos/             # Videos app (models, views, forms)
├── users/              # Users app (auth, channels, subscriptions)
├── templates/          # All HTML templates
├── static/             # CSS, JS, images
├── media/              # Uploaded files (auto-created)
├── requirements.txt
└── manage.py
```

## Tech Stack

- **Backend:** Django 4.2+
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Database:** SQLite (dev) — swap to PostgreSQL for production
- **Auth:** Django's built-in auth + custom user model

## Production Notes

- Set `DEBUG=False` in `.env`
- Use PostgreSQL instead of SQLite
- Use AWS S3 (via `django-storages`) for media files
- Run `python manage.py collectstatic` before deploying
- Use gunicorn + nginx for serving
