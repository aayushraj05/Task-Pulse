from flask import Flask, request, jsonify
import pyodbc
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from datetime import datetime
import atexit

app = Flask(__name__)

# Twilio Credentials (Directly hardcoded)
TWILIO_ACCOUNT_SID = 'AC8d429a4fc17ce6ba154e46a0ed168424'  # Replace with your actual account SID
TWILIO_AUTH_TOKEN = '3817fe7fb703ce5b1647ff7ac0afc080'    # Replace with your actual auth token
TWILIO_PHONE_NUMBER = '+15204472353'  # Your Twilio phone number

# Initialize Twilio Client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Database connection function
def create_connection():
    try:
        conn = pyodbc.connect(
            'Driver={ODBC Driver 18 for SQL Server};'
            'Server=taskscheduler-server.database.windows.net;'
            'Database=TaskSchedulerDB;'
            'UID=sqladmin;'
            'PWD=Pratham@18;'  # Ensure this is secure
            'Timeout=30;'
        )
        return conn
    except pyodbc.Error as e:
        return None

# Function to get tasks from the database
def get_tasks():
    conn = create_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tasks")
    tasks = cursor.fetchall()
    conn.close()
    
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task[0],
            'TaskName': task[1],
            'TaskDescription': task[2],
            'DueDate': task[3],
            'ReminderTime': convert_gmt_to_ist(task[4]),  # Convert ReminderTime to IST
            'ContactMethod': task[5],
            'ContactInfo': task[6],
            'ReminderSent': task[7]
        })
    return task_list

# Convert GMT to IST
def convert_gmt_to_ist(gmt_time_input):
    # Check if the input is a datetime object
    if isinstance(gmt_time_input, datetime):
        gmt_time = gmt_time_input
    else:
        # Parse the GMT time string to a datetime object
        gmt_time = datetime.strptime(gmt_time_input, "%a, %d %b %Y %H:%M:%S %Z")

    # Set the timezone to GMT
    gmt_time = gmt_time.replace(tzinfo=pytz.timezone('GMT'))

    # Convert to IST
    ist_time = gmt_time.astimezone(pytz.timezone('Asia/Kolkata'))
    
    return ist_time.strftime("%a, %d %b %Y %H:%M:%S IST")

# Route to handle tasks
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = get_tasks()
        return jsonify(tasks), 200
    elif request.method == 'POST':
        return create_task()

# Create Task
def create_task():
    data = request.json

    task_name = data['TaskName']
    task_description = data['TaskDescription']
    due_date = data['DueDate']
    reminder_time = data['ReminderTime']
    contact_method = data['ContactMethod']
    contact_info = data['ContactInfo']

    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO Tasks (TaskName, TaskDescription, DueDate, ReminderTime, ContactMethod, ContactInfo, ReminderSent)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (task_name, task_description, due_date, reminder_time, contact_method, contact_info, 0))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Task created successfully!'}), 201

# Send Reminder
def send_reminder(task_name, contact_method, contact_info):
    if contact_method == "SMS":
        try:
            message = twilio_client.messages.create(
                body=f"This is a reminder for your task: {task_name}.",
                from_=TWILIO_PHONE_NUMBER,
                to=contact_info
            )
            print(f"Reminder sent: {message.sid}")  # Log the message SID for confirmation
        except Exception as e:
            print(f"Error sending reminder: {e}")

# Check Reminders
def check_reminders():
    conn = create_connection()
    if conn is None:
        print("Failed to connect to database.")
        return

    cursor = conn.cursor()
    # Select tasks where the reminder time is due and reminder has not been sent
    cursor.execute("SELECT * FROM Tasks WHERE ReminderTime <= GETDATE() AND ReminderSent = 0")
    tasks = cursor.fetchall()

    for task in tasks:
        task_id = task[0]
        task_name = task[1]
        contact_method = task[5]
        contact_info = task[6]

        # Attempt to send the reminder
        if send_reminder(task_name, contact_method, contact_info):
            # Only update ReminderSent if sending the reminder was successful
            cursor.execute("UPDATE Tasks SET ReminderSent = 1 WHERE TaskID = ?", (task_id,))
            print(f"Reminder sent for task: {task_name}")
        else:
            print(f"Failed to send reminder for task: {task_name}")

    conn.commit()
    conn.close()

# Initialize Background Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_reminders, 'interval', minutes=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Update Task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json

    task_name = data['TaskName']
    task_description = data['TaskDescription']
    due_date = data['DueDate']
    reminder_time = data['ReminderTime']
    contact_method = data['ContactMethod']
    contact_info = data['ContactInfo']

    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    cursor.execute(""" 
        UPDATE Tasks
        SET TaskName = ?, TaskDescription = ?, DueDate = ?, ReminderTime = ?, ContactMethod = ?, ContactInfo = ?
        WHERE TaskID = ?
    """, (task_name, task_description, due_date, reminder_time, contact_method, contact_info, task_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Task updated successfully!'}), 200

# Delete Task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = create_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM Tasks WHERE TaskID = ?", (task_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Task deleted successfully!'}), 200

# Main execution
if __name__ == '__main__':
    app.run(debug=True)
