1.About Projects

# 🏋️‍♀️ Fitness Studio API

A simple Django backend to manage fitness classes and client bookings. This project allows users to create, view, and book fitness classes, with timezone support, logging, and unit testing.

---

## Features

-  Add and retrieve fitness classes
-  Book a class with automatic slot deduction
-  View bookings by user email
-  Timezone-aware responses (default: `Asia/Kolkata`)
-  Logging of booking activity
-  Unit test for booking logic

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** Django
- **Database:** SQLite (default)
- **API Format:** JSON (REST-style)
- **Timezone Handling:** `pytz`
- **Logging:** Python's built-in `logging` module

---

## 🔧 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/fitness-studio.git
   cd fitness-studio

2.Create and activate a virtual environment

python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate


3.Install dependencies

pip install -r requirements.txt


4.Apply migrations

python manage.py makemigrations
python manage.py migrate


5.Run the development server

python manage.py runserver



6.API Endpoints

| Method | Endpoint            | Description                       |
| ------ | ------------------- | --------------------------------- |
| GET    | `/classes/`         | Get list of all fitness classes   |
| POST   | `/book/`            | Book a class (by class ID)        |
| GET    | `/bookings/`        | Retrieve bookings by client email ,here email pass on body in json format |


7. Example JSON Payloads




7.Running Tests
Run the unit tests using:
python manage.py test

   
