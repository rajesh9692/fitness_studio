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
.venv\Scripts\activate

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


7. API work's
🔧 How It Works (Step-by-Step)
✅ Step 1: POST Data to /classes_view/ (Create a New Fitness Class)
Endpoint: GET http://127.0.0.1:8000/classes/
Body (raw JSON):
This endpoint handles POST requests to create a new fitness class.

Sample JSON to post in Postman:
{
  "name": "Zumba",
  "date_time": "2025-06-15T10:00:00",
  "instructor": "Mr Alexa",
  "available_slots": 10
}
If everything is correct, the response will be like:

{
  "id": 1,
  "name": "Zumba",
  "date_time": "2025-06-15T10:00:00",
  "instructor": "MR Alexa",
  "available_slots": 10
}
Note: That "id": 1 is the class_id you'll use in the next step.



✅ Step 2: POST to /book/ (Book a Spot in a Class)
Endpoint: GET http://127.0.0.1:8000/book/
Body (raw JSON):
Now you can use the class ID (1 from above) to book a slot in the class using your booking API.

POST body:
{
  "class_id": 1,
  "client_name": "Amit",
  "client_email": "amit2000@example.com"
}
Expected Response:

{
  "message": "Booking successful",
  "remaining_slots": 9,
  "posted_data": {
    "class_id": 1,
    "client_name": "Amit",
    "client_email": "amit2000@gmail.com"
  }
}
   

✅ Step 3: GET to /get_bookings/ (get all booking taking client_email on body)
Endpoint: GET http://127.0.0.1:8000/bookings/
Body (raw JSON):

{
  "email": "amit@example.com"
}

✅ Expected Response (if bookings exist)
{
  "bookings": [
    {
      "class_name": "Zumba",
      "date_time": "2025-06-15T10:30:15",
      "instructor": "MR Alexa",
      "client_name": "Amit",
      "client_email": "amit2000@gmail.com"
    }
  ]
}


If no bookings exist for the email:

{
  "message": "No bookings found for this email"
}


8.Running Tests
Run the unit tests using:
python manage.py test
