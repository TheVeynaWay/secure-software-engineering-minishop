# MiniShop – Setup Instructions

## Prerequisites

| Tool | Minimum version | Check |
|------|----------------|-------|
| Python | 3.8 | `python --version` |
| pip | bundled with Python | `pip --version` |

No other software is required. SQLite is part of Python's standard library.

---

## 1. Get the Code

If you cloned the repository, skip this step. Otherwise download and unzip the project, then open a terminal in the project root (the folder that contains `app.py`).

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

| Platform | Command |
|----------|---------|
| macOS / Linux | `source venv/bin/activate` |
| Windows (CMD) | `venv\Scripts\activate.bat` |
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` |

Your prompt should now start with `(venv)`.

---

## 3. Install Dependencies

```bash
pip install flask
```

Only Flask (and its sub-dependencies — Werkzeug, Jinja2, etc.) is required.

---

## 4. Run the Application

```bash
python app.py
```

On first startup the script:
- Creates the `instance/` directory and `minishop.db` SQLite database automatically.
- Seeds a default admin account and three sample products.

Expected output:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Open <http://127.0.0.1:5000> in your browser.

---

## 5. Default Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |

Customer accounts are created through the self-registration page at `/register`.

---

## 6. Project Structure

```
secure-software-engineering/
├── app.py            # Flask routes and application entry point
├── models.py         # Database connection and schema initialization
├── templates/        # Jinja2 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── products.html
│   ├── order.html
│   ├── order_history.html
│   └── admin/
│       ├── dashboard.html
│       ├── products.html
│       ├── product_form.html
│       └── orders.html
├── static/
│   └── style.css
├── instance/
│   └── minishop.db   # SQLite database (auto-created on first run)
├── README.md
├── AI_USAGE.md
└── Setup.md          # This file
```

---

## 7. Verifying the Installation

1. Visit <http://127.0.0.1:5000/products> — you should see the product listing without logging in.
2. Go to <http://127.0.0.1:5000/login> and sign in as `admin` / `admin123` — you should be redirected to the Admin Dashboard.
3. Go to <http://127.0.0.1:5000/register> and create a customer account — you should be redirected to the login page.
4. Log in as the new customer and place an order — the order should appear at <http://127.0.0.1:5000/orders>.

---

## 8. Stopping the Server

Press `Ctrl + C` in the terminal running `python app.py`.

---

## 9. Resetting the Database

Delete the database file and restart the server to start fresh:

```bash
rm instance/minishop.db   # macOS/Linux
del instance\minishop.db  # Windows
python app.py
```

The admin account and sample products are re-created automatically.

---

## 10. Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| `ModuleNotFoundError: No module named 'flask'` | Virtual environment not active or Flask not installed | Activate `venv` and run `pip install flask` |
| `Address already in use` | Port 5000 is taken by another process | Kill the other process or run `flask run --port 5001` |
| `PermissionError` on `instance/` | Directory not writable | Check folder permissions or run as a user with write access |
| Templates not found | Running from the wrong directory | Make sure your working directory is the project root (where `app.py` lives) |
