# Mechanic Scheduler

A simple Flask + PostgreSQL app for managing appointments, customers, and mechanics.

## Features

- View/add mechanics and customers
- Create, update, and delete appointments
- REST API backend with basic frontend

## Setup

1. **Clone repo & install dependencies**

```bash
git clone https://github.com/your-username/mechanic-scheduler.git
cd mechanic-scheduler
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt  # or install manually
```
2. **Create ```.env```**
```bash
DB_HOST=localhost
DB_NAME=mechanic_scheduler
DB_USER=your_user
DB_PASS=your_password
DB_PORT=5432
```
3. **Set up PostgreSQL**
Full SQL schema is in ```schema.sql```
4. Start the app
```bash
python app.py
```
Visit http://localhost:5000
