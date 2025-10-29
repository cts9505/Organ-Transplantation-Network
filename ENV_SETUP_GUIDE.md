# 🔧 Environment Setup Guide

## Overview
This project now uses environment variables to securely manage database credentials and Flask configuration. This prevents sensitive information from being hardcoded in the source code.

---

## 📁 Files Created

### 1. `.env` (Your actual credentials - DO NOT COMMIT)
Contains your actual database credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=DBMS_PROJECT

FLASK_SECRET_KEY=sec key
FLASK_DEBUG=True
```

### 2. `.env.example` (Template for others)
A template file that shows what variables are needed:
```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=DBMS_PROJECT

FLASK_SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True
```

### 3. `.gitignore` (Prevents .env from being committed)
Ensures `.env` file is never committed to version control.

---

## 🚀 Quick Setup

### Step 1: Install python-dotenv
```bash
pip3 install --break-system-packages python-dotenv
```

Or using a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install python-dotenv
```

### Step 2: Configure Your Environment
The `.env` file is already created with default values. Update it if your MySQL credentials are different:

```bash
nano .env  # or use any text editor
```

Change these values:
- `DB_PASSWORD`: Your MySQL root password
- `FLASK_SECRET_KEY`: A random secret key (use `python3 -c "import secrets; print(secrets.token_hex(32))"` to generate)

### Step 3: Run the Application
```bash
python3 main.py
```

You should see:
```
✅ Successfully connected to MySQL database: DBMS_PROJECT
 * Running on http://127.0.0.1:5000
```

---

## 🔒 Security Benefits

### Before (Hardcoded):
```python
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # ⚠️ Exposed in code!
    database="DBMS_PROJECT"
)
```

### After (Environment Variables):
```python
from dotenv import load_dotenv
load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),  # ✅ Secure!
    database=os.getenv('DB_NAME')
)
```

---

## 📝 Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DB_HOST` | MySQL server hostname | `localhost` | Yes |
| `DB_USER` | MySQL username | `root` | Yes |
| `DB_PASSWORD` | MySQL password | `root` | Yes |
| `DB_NAME` | Database name | `DBMS_PROJECT` | Yes |
| `FLASK_SECRET_KEY` | Flask session encryption key | `sec key` | Yes |
| `FLASK_DEBUG` | Enable debug mode | `True` | No |

---

## 🛠 Troubleshooting

### Error: "Unable to connect to MySQL database"
1. Check if MySQL is running:
   ```bash
   mysql -u root -p
   ```

2. Verify `.env` file exists and has correct credentials

3. Ensure database exists:
   ```sql
   CREATE DATABASE IF NOT EXISTS DBMS_PROJECT;
   ```

### Error: "No module named 'dotenv'"
Install python-dotenv:
```bash
pip3 install --break-system-packages python-dotenv
```

### Want to use different credentials temporarily?
Set environment variables in your terminal (they override `.env`):
```bash
export DB_PASSWORD='my_different_password'
python3 main.py
```

---

## 🌐 Production Deployment

For production servers (Heroku, AWS, etc.), set environment variables through the platform's dashboard instead of using a `.env` file:

**Heroku:**
```bash
heroku config:set DB_HOST=your_host
heroku config:set DB_PASSWORD=your_password
```

**AWS/Linux:**
```bash
export DB_HOST=your_host
export DB_PASSWORD=your_password
```

---

## ✅ Checklist

- [x] `.env` file created with your credentials
- [x] `.env.example` file created as template
- [x] `.gitignore` includes `.env`
- [x] `python-dotenv` installed
- [x] `main.py` updated to use environment variables
- [x] README.md updated with setup instructions

---

## 🔐 Best Practices

1. **Never commit `.env`** - It's in `.gitignore` for a reason
2. **Use strong secret keys** - Generate with `secrets.token_hex(32)`
3. **Different credentials per environment** - Dev, staging, production should have separate databases
4. **Rotate credentials regularly** - Update passwords periodically
5. **Use read-only users** - For features that only need to read data

---

**Security Note:** The `.env` file contains sensitive credentials. Keep it secure and never share it publicly!
