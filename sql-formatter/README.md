# SQL Formatter

A tiny web app to format SQL queries using [sqlparse](https://github.com/andialbrecht/sqlparse).

## Features

- Paste SQL or upload a `.sql` file
- Choose keyword case (upper/lower/as-is)
- Light/Dark theme toggle
- Download or copy the formatted SQL

## Setup

```bash
bash setup.sh
source venv/bin/activate  # if not already activated
python app.py
```

Then open <http://localhost:5000> in a browser.

## Tests

```bash
python -m pytest -q
```
