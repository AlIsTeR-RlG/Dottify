# Dottify

Dottify is a music cataloguing web application built with Django, where users can create albums, add songs to them, build playlists, and browse other users' profiles and contributions. It includes a REST API (built with Django REST Framework) alongside the standard web views, supporting albums, songs, playlists, and aggregate statistics.

This project was built as part of a university software engineering module, with a focus on applying Django fundamentals: models, class-based views, REST API design, authentication, and database migrations.

## Features

- Browse, search, create, update, and delete albums and songs
- Build and manage playlists
- User profile pages showing a user's albums and activity
- A REST API exposing albums, songs, playlists, and nested song-within-album endpoints
- A statistics endpoint summarising data across the platform

## Tech stack

- **Backend:** Django, Django REST Framework, drf-nested-routers
- **Database:** SQLite (default Django setup)
- **Frontend:** Django templates

## Getting started

1. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/AlIsTeR-RlG/Dottify.git
   cd Dottify
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Run the initial setup commands:
   ```bash
   python3 manage.py compilemessages
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py bootstrap
   ```

5. Start the development server:
   ```bash
   python3 manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000/` in your browser.

## Creating an admin account

If you'd like to add data through Django's built-in admin panel rather than the web app's forms, you can create a superuser account:

```bash
python3 manage.py createsuperuser
```

Follow the prompts to set a username, email, and password. Once the server is running, log in at `http://127.0.0.1:8000/admin/` with those credentials to access the admin panel, where you can directly add, edit, or delete albums, songs, playlists, and other data.

## A note on data

This repository doesn't ship with any sample albums, songs, or playlists — the database starts empty aside from any base setup created by the `bootstrap` command (e.g. permission groups). To see the app in action, sign up for an account through the web interface and start adding albums and songs yourself.

## URL reference

### Web pages

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/albums/<id>/` | Album detail page |
| `/albums/<id>/<slug>/` | Album detail page (slug variant) |
| `/albums/search/` | Search albums |
| `/albums/new/` | Create a new album |
| `/albums/<id>/edit/` | Edit an album |
| `/albums/<id>/delete/` | Delete an album |
| `/songs/<id>/` | Song detail page |
| `/songs/new/` | Create a new song |
| `/songs/<id>/edit/` | Edit a song |
| `/songs/<id>/delete/` | Delete a song |
| `/users/<id>/` | User profile page |
| `/users/<id>/<slug>/` | User profile page (slug variant) |

### REST API

| URL | Description |
|-----|-------------|
| `/api/albums/` | List / create albums |
| `/api/albums/<id>/` | Retrieve, update, or delete an album |
| `/api/albums/<id>/songs/` | List songs belonging to a specific album |
| `/api/songs/` | List / create songs |
| `/api/songs/<id>/` | Retrieve, update, or delete a song |
| `/api/playlists/` | List / create playlists |
| `/api/playlists/<id>/` | Retrieve, update, or delete a playlist |
| `/api/statistics/` | Platform-wide statistics |
| `/admin/` | Django admin panel |


## Project status

Dottify was developed as a timeboxed university coursework project, so the feature set reflects what was achievable within that scope rather than a fully polished product. Some areas (UI styling, edge-case handling, test coverage) are functional but not exhaustive, and there's plenty of room for further development. Feedback and suggestions are welcome.
