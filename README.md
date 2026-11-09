# PaletteVault

PaletteVault is a makeup collection manager. It helps you keep track of what is in your
makeup bag, warns you when products pass their **PAO (Period After Opening)** date and
records **pan progress** so you can see how much of each product you have used.

Built with Flask and PostgreSQL using a DevOps approach: GitHub Actions CI, Docker, and
deployment to Render.

**Author:** Leah O Sullivan (R00247730), INFO8021 DevOps Strategy and Automation, MTU

---

## Branches

| Branch | What it contains |
|--------|------------------|
| `main` | Initial website (Home and About Us pages, no database functionality), plus the database scripts and seed data |
| `feature/add-product` | **Functionality 1:** Home page reads the vault from the database, barcode lookup, Add Product form, and live PAO expiry warnings (Fresh / Days Left / Expired) |
| `feature/usage-log` | **Functionality 2:** Usage Log page, log new pan progress for a product, and view its dated usage history |

The feature branches are kept separate and are **not merged** into `main`.

## Database

PostgreSQL 18 database called `palettevault` with four tables:

| Table | Purpose |
|-------|---------|
| `users` | Registered users (passwords stored as hashes) |
| `products` | Makeup in a user's vault, with opened date, PAO months, expiry date, pan progress and status |
| `usage_logs` | Dated pan-progress history for each product |
| `wishlist_items` | Products a user would like to buy |

Relationships: a user owns many products and many wishlist items; a product has many usage logs.
The full schema is in `database/create_tables.sql` and the seed data is in `data/`.

## Getting started (Windows)

1. Install [PostgreSQL 18](https://www.postgresql.org/download/) and make sure the server is running.
   The scripts use `postgres` / `postgres` on `localhost:5432` by default. If your password is
   different, set it first:

   ```cmd
   set DB_PASSWORD=your_password
   ```

2. Create a virtual environment and install the packages:

   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create the database and tables, then load the data:

   ```cmd
   python initialise_db.py
   python populate_db.py
   ```

4. Run the app:

   ```cmd
   set FLASK_APP=palettevault.py
   flask run
   ```

   Open http://127.0.0.1:5000. If `flask run` gives an error, use `python -m flask run`.

To switch to a feature branch: `git checkout feature/add-product` (or `feature/usage-log`),
then run `flask run` again.

## Pages

| URL | Page | Branch |
|-----|------|--------|
| `/` | Home - vault dashboard and barcode scanner | all |
| `/about` | About Us | all |
| `/login`, `/register` | Sign In and Register forms | all |
| `/products/add` | Add Product (with `?barcode=` lookup) | `feature/add-product` |
| `/usage` | Usage Log - choose a product | `feature/usage-log` |
| `/usage/<id>` | Log usage and view history | `feature/usage-log` |

## Project structure

```
PaletteVault/
├── .github/workflows/main.yml   # CI: flake8, create + populate DB, pytest, Docker build
├── app/
│   ├── __init__.py              # creates the Flask app and loads config
│   ├── routes.py                # page routes
│   ├── forms.py                 # Flask-WTF forms
│   ├── pao.py                   # PAO expiry date and status calculations
│   ├── db.py                    # database connection helpers (feature branches)
│   ├── products.py              # product queries (feature/add-product)
│   ├── usage.py                 # usage log queries (feature/usage-log)
│   ├── auth.py, wishlist.py     # placeholders for later milestones
│   ├── static/css/style.css
│   ├── static/js/main.js
│   └── templates/
├── data/                        # seed data CSV files
├── database/create_tables.sql   # tables, keys, relationships and constraints
├── tests/                       # pytest tests
├── initialise_db.py             # creates the database and tables
├── populate_db.py               # loads the CSV data into the tables
├── config.py                    # settings (read from environment variables)
├── palettevault.py              # entry point
├── Dockerfile
├── requirements.txt
└── tech_spec.yaml
```

## Tests and linting

The tests on the feature branches use the database, so run `initialise_db.py` and
`populate_db.py` first.

```cmd
pytest -v
flake8 .
```

GitHub Actions runs the same steps on every push, using a PostgreSQL service container.

## Docker

```cmd
docker build -t palettevault .
docker run -p 5000:5000 -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/palettevault palettevault
```

## Still to build

- Real sign-in with Flask-Login (the vault currently shows demo user 1)
- Wishlist page
- Camera barcode scanning and lookup from an external product database
