# Task-Pulse
Developed a task scheduling and reminder system with email/SMS notifications using Flask, Twilio , and SQL Server.

# Task Reminder Application using Flask and Twilio for SMS

This project is a Flask-based task reminder application that allows users to create, update, delete, and retrieve tasks. The tasks come with reminders that send SMS notifications using Twilio. The application is connected to a database (such as Azure SQL or SQLite) to store the tasks.

## Key Components
1. **Flask**: A lightweight web framework used to build the backend API of the application.
2. **Twilio**: A third-party service used for sending SMS notifications for task reminders.
3. **SQLAlchemy**: An ORM (Object Relational Mapper) to handle the interaction between the application and the database.
4. **RESTful API**: Used to expose endpoints to perform CRUD (Create, Read, Update, Delete) operations on tasks.

---

## Application Flow

### 1. **Setup and Configuration**

- **Twilio Configuration**:
  To send SMS reminders, the application integrates Twilio via its API. The Twilio configuration includes the **account SID**, **auth token**, and a **Twilio phone number** from which the SMS will be sent. These values are stored securely, usually in environment variables.

- **Flask Setup**:
  Flask is initialized, and routes are defined to handle different HTTP methods such as `POST`, `GET`, `PUT`, and `DELETE`.

### 2. **Database and Models**

A `Task` model is defined to store task information and reminder times.

```python
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)  # Twilio will send SMS to this number

