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

# Task Reminder Application Flow (Using Flask and Twilio SMS)

## 1. Overview of the Application

This application allows users to manage their tasks by creating, updating, deleting, and viewing them. Each task has a due date and a reminder time. When the reminder time is reached, an SMS notification is sent to the user via **Twilio**. The backend is built using **Flask**, and the task data is stored in a database (e.g., SQLite or Azure SQL).

---

## 2. Components Involved

- **Flask Framework**: Flask handles the backend logic of the application, including receiving user requests to manage tasks (create, update, delete, and get tasks).
  
- **Twilio SMS API**: Twilio is used to send SMS notifications when the reminder time for a task is triggered.

- **Database**: A database (e.g., SQLite or Azure SQL) stores task details such as the task name, due date, reminder time, and the user’s phone number.

---

## 3. Flow of the Application

### Step 1: **Task Creation**
- The user sends a **POST** request to the Flask API to create a new task.
- The task includes details such as:
  - Task name
  - Due date
  - Reminder time
  - User’s phone number for receiving reminders
- The task is stored in the database, and a response is sent back to the user confirming the task creation.

### Step 2: **Task Reminder Scheduling**
- Once a task is created, the application calculates the time remaining until the reminder.
- A background job (using a scheduler like `APScheduler` or similar) is set up to trigger an SMS when the reminder time arrives.
  
### Step 3: **Sending SMS via Twilio**
- When the scheduled reminder time is reached:
  - The Flask app uses Twilio’s SMS API to send an SMS to the user’s phone number.
  - The message includes details of the task, such as the task name and due date.
  
### Step 4: **Task Update**
- The user can update an existing task by sending a **PUT** request to the API.
- The updated task details (e.g., new reminder time or task name) are saved in the database.
- If the reminder time is updated, the existing reminder is canceled, and a new one is scheduled.

### Step 5: **Task Deletion**
- The user sends a **DELETE** request to remove a task.
- The task is deleted from the database, and any scheduled reminder associated with that task is also canceled.

### Step 6: **View Tasks**
- The user can view all tasks by sending a **GET** request to the API.
- The API fetches the tasks from the database and returns them to the user.

---

## 4. Error Handling
- The application handles scenarios where Twilio SMS fails (e.g., invalid phone numbers) by logging errors and sending appropriate responses to the user.
- Database-related errors, such as failed task creation or updates, are also handled, ensuring the user receives meaningful error messages.

---

## 5. Summary
This task reminder application allows users to manage their tasks with automated SMS reminders using Twilio. Flask powers the backend, and all task-related data is stored in a database. The application ensures that reminders are sent at the right time, and users can easily manage their tasks through create, update, and delete functionality.
