# Contact Book

Flask + SQLite contact manager with add, search, edit and delete.

## Render settings
Build command: `pip install -r requirements.txt`
Start command: `gunicorn app:app`

Keep `index.html` inside the `templates` folder.

## Local run
`pip install -r requirements.txt` then `python app.py`, and open http://127.0.0.1:5000.

## Data persistence on Render
Render's normal filesystem is temporary. To keep contacts across deploys, attach a Persistent Disk mounted at `/var/data` and set `DATABASE_PATH=/var/data/contacts.db`.
