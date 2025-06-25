import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime as dt
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
# import faker
import random
from typing import List

# Initialize Faker for generating fake data
# fake = faker.Faker()
# from config import generate_natural_response
app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


# Database initialization
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# def init_db():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     # cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#     #     id INTEGER PRIMARY KEY,
#     #     name TEXT,
#     #     title TEXT,s
#     #     time_off_balance INTEGER,
#     #     address TEXT,
#     #     requested_time_off INTEGER DEFAULT 0
#     # )''')
#     # conn.commit()
#     required_columns = {"id", "name", "time_off_balance", "title", "address","requested_time_off"}

#     # Get existing table schema
#     cursor.execute("PRAGMA table_info(users)")
#     existing_columns = {row[1] for row in cursor.fetchall()}  # Extract column names

#     # Check if any required column is missing
#     if not required_columns.issubset(existing_columns):
#         print("Table structure is incorrect. Recreating the users table...")
        
#         cursor.execute("DROP TABLE IF EXISTS users")  # Remove old table

#         # Create the new table with correct schema
#         cursor.execute("""
#             CREATE TABLE users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 time_off_balance REAL NOT NULL DEFAULT 0,
#                 title TEXT NOT NULL,
#                 address TEXT NOT NULL,
#                 requested_time_off INTEGER DEFAULT 0     
#             )
#         """)
#         conn.commit()
#     conn.close()
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            time_off_balance REAL NOT NULL DEFAULT 0,
            title TEXT NOT NULL,
            address TEXT NOT NULL,
            requested_time_off INTEGER DEFAULT 0
        )
    ''')

    # Generate 50 dummy user records
    file_path = 'users_data.xlsx'
    df = pd.read_excel(file_path)

    # Convert data to list of tuples
    dummy_users = [
        (
            row['Name'],
            round(row['TimeOffBalance'], 2),
            row['Job'],
            row['Address'].replace('\n', ', '),  # Clean up newlines in addresses
            int(row['RequestedTimeOff'])
        )
        for _, row in df.iterrows()
    ]

    # Insert records into the users table
    cursor.executemany('''
        INSERT INTO users (name, time_off_balance, title, address, requested_time_off)
        VALUES (?, ?, ?, ?, ?)
    ''', dummy_users)

    conn.commit()
    conn.close()
    print("Database initialized and inserted 50 dummy user records.")

init_db()

# Request models
class TimeOffRequest(BaseModel):
    name: str
    from_date: str
    to_date: str

class UpdateTitleRequest(BaseModel):
    name: str
    new_title: str

class UpdateAddressRequest(BaseModel):
    name: str
    new_address: str

class CreateUserRequest(BaseModel):
    name: str
    time_off_balance: int
    title: str
    address: str

class ExpenseEntry(BaseModel):
    transaction_id: str | None
    supplier: str
    transaction_date: str
    transaction_amount: float 
    receipt_file: str
    transaction_type: str
    payment_method: str

class ExpenseClaimRequest(BaseModel):
    name: str
    sustainable_travel_incentive: bool
    expense_report: str

@app.get("/export-users/")
def export_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    if not users:
        return {"message": "No data available to export"}

    # Convert to DataFrame for Excel export
    df = pd.DataFrame(users)

    file_path = "users_data.xlsx"
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename="users_data.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.delete("/clear-users/")
def clear_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete all records from the users table
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()

    return {"message": "All user data has been cleared."}

class NameBasedRequest(BaseModel):
    name: str

@app.post("/user_profile_details")
def get_user_profile(request: NameBasedRequest):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(name) = LOWER(?)", (request.name,)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(dict(user))
    response = dict(user)
    return response

@app.post("/get_emails")
def get_emails(request: NameBasedRequest):
    name = request.name
    all_emails = [{
        "Subject": "Flight Receipt - Singapore Airlines",
        "Content": "Dear Victoria Baker, Thank you for flying with Singapore Airlines. Your receipt for your flight from KL to Singapore is attached.",
        "Name": "Victoria Baker",
        "Sender": "no-reply@singaporeair.com",
        "Recipient": "victoria.baker@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[flight_receipt_KL_SG.pdf](https://ibm.box.com/shared/static/gh0zj63dwpx2u3u9xyolygcx1hxytsgx.pdf)"],
        "Timestamp": "2025-04-05T10:00:00Z"
    },
    {
        "Subject": "Hotel Receipt - Crowne Plaza Singapore",
        "Content": "Dear Victoria Baker, Thank you for staying with us at Crowne Plaza Singapore. Your receipt for your stay is attached.",
        "Name": "Victoria Baker",
        "Sender": "reservations@crowneplaza.com",
        "Recipient": "victoria.baker@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[hotel_receipt_Crowne_Plaza.pdf](https://ibm.box.com/shared/static/92g5lp8un10bgqa26w69lzl7gk3u1gow.pdf)"],
        "Timestamp": "2025-04-05T12:00:00Z"
    },
    {
        "Subject": "Food Receipt - Din Tai Fung",
        "Content": "Dear Victoria Baker, Thank you for dining with us at Din Tai Fung. Your receipt is attached.",
        "Name": "Victoria Baker",
        "Sender": "no-reply@dintaifung.com",
        "Recipient": "victoria.baker@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[food_receipt_Din_Tai_Fung.pdf](https://ibm.box.com/shared/static/3otaia1w3093y3uzinpce8luvjtfrsw9.pdf)"],
        "Timestamp": "2025-04-05T18:00:00Z"
    },
    {
        "Subject": "Grab Ride Receipt",
        "Content": "Dear Victoria Baker, Thank you for using Grab. Your ride receipt is attached.",
        "Name": "Victoria Baker",
        "Sender": "no-reply@grab.com",
        "Recipient": "victoria.baker@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[grab_ride_receipt.pdf](https://ibm.box.com/shared/static/cfrvmhe45od60wnn1ea9cytrugt9iewb.pdf)"],
        "Timestamp": "2025-04-06T20:00:00Z"
    },
    {
        "Subject": "Food Receipt - Jumbo Seafood",
        "Content": "Dear Victoria Baker, Thank you for dining with us at Jumbo Seafood. Your receipt is attached.",
        "Name": "Victoria Baker",
        "Sender": "no-reply@jumboseafood.com",
        "Recipient": "victoria.baker@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[food_receipt_Jumbo_Seafood.pdf](https://ibm.box.com/shared/static/s94p43jsjf53gihs25kuold49bh5k6ys.pdf)"],
        "Timestamp": "2025-04-06T12:00:00Z"
    },
    {
        "Subject": "Food Receipt - Newton Food Centre",
        "Content": "Dear Victoria Baker, Thank you for dining with us at Newton Food Centre. Your receipt is attached.",
        "Name": "Victoria Baker",
        "Sender": "no-reply@newtonfoodcentre.com",
        "Recipient": "victoria.baker@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[food_receipt_Newton_Food_Centre.pdf](https://ibm.box.com/shared/static/67d8khvsmhp49e43r6g62iz8l9r79okd.pdf)"],
        "Timestamp": "2025-04-06T18:00:00Z"
    },
    {
        "Subject": "Food Receipt - Tiong Bahru Market",
        "Content": "Dear Victoria Baker, Thank you for dining with us at Tiong Bahru Market. Your receipt is attached.",
        "Name": "Victoria Baker",
        "Sender": "no-reply@tiongbahrumarket.com",
        "Recipient": "victoria.baker@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[food_receipt_Tiong_Bahru_Market.pdf](https://ibm.box.com/shared/static/i36bdcwu6oxsu5342cyllk5hwub8umf1.pdf)"],
        "Timestamp": "2025-04-07T12:00:00Z"
    },
    {
        "Subject": "Meeting Reminder",
        "Content": "Dear Daniel Anderson, This is a reminder for our upcoming meeting on Monday at 10 AM.",
        "Name": "Daniel Anderson",
        "Sender": "meeting-reminder@example.com",
        "Recipient": "daniel.anderson@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": [],
        "Timestamp": "2025-04-08T09:00:00Z"
    },
    {
        "Subject": "Project Update",
        "Content": "Dear William Frazier, Please find the latest project update attached.",
        "Name": "William Frazier",
        "Sender": "project-update@example.com",
        "Recipient": "william.frazier@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[project_update.pdf](https://ibm.box.com/shared/static/i8m2xdgi8ez7kn1fwhve3qavyiktrgq7.pdf)"],
        "Timestamp": "2025-04-08T10:00:00Z"
    },
    {
        "Subject": "Invoice",
        "Content": "Dear Danielle Hall, Please find the attached invoice for your recent purchase.",
        "Name": "Danielle Hall",
        "Sender": "invoices@example.com",
        "Recipient": "danielle.hall@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[invoice_12345.pdf](https://ibm.box.com/shared/static/5kyw2w8d7nsherej34nrhxxad457mp23.pdf)"],
        "Timestamp": "2025-04-08T11:00:00Z"
    },
    {
        "Subject": "Newsletter",
        "Content": "Dear Diane Conrad, Here is your monthly newsletter with the latest updates and news.",
        "Name": "Diane Conrad",
        "Sender": "newsletter@example.com",
        "Recipient": "diane.conrad@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": [],
        "Timestamp": "2025-04-08T12:00:00Z"
    },
    {
        "Subject": "Training Schedule",
        "Content": "Dear Maria Mcdowell, Please find the attached training schedule for the upcoming week.",
        "Name": "Maria Mcdowell",
        "Sender": "training@example.com",
        "Recipient": "maria.mcdowell@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[training_schedule.pdf](https://ibm.box.com/shared/static/wykfqfcogqooqshb1qny1pel3pmb3xln.pdf)"],
        "Timestamp": "2025-04-08T13:00:00Z"
    },
    {
        "Subject": "Meeting Minutes",
        "Content": "Dear Mrs. Karina Williamson, Please find the attached meeting minutes from our last meeting.",
        "Name": "Mrs. Karina Williamson",
        "Sender": "meeting-minutes@example.com",
        "Recipient": "karina.williamson@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[meeting_minutes.pdf](https://ibm.box.com/shared/static/x7r0jlgpzsemjtoikugsjb2ztfambukg.pdf)"],
        "Timestamp": "2025-04-08T14:00:00Z"
    },
    {
        "Subject": "Task Assignment",
        "Content": "Dear Jacob Graham, Please find the attached task assignment for the upcoming project.",
        "Name": "Jacob Graham",
        "Sender": "task-assignment@example.com",
        "Recipient": "jacob.graham@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[task_assignment.pdf](https://ibm.box.com/shared/static/6t8sp29q0eisc7mzwt4s4m3gtvzhnkyi.pdf)"],
        "Timestamp": "2025-04-08T15:00:00Z"
    },
    {
        "Subject": "Performance Review",
        "Content": "Dear Jessica West, Please find the attached performance review for the last quarter.",
        "Name": "Jessica West",
        "Sender": "performance-review@example.com",
        "Recipient": "jessica.west@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[performance_review.pdf](https://ibm.box.com/shared/static/abhhlg8p0njats0fff8juuxvfddgwpde.pdf)"],
        "Timestamp": "2025-04-08T16:00:00Z"
    },
    {
        "Subject": "Event Invitation",
        "Content": "Dear Rebekah Valdez, You are invited to our upcoming event. Please find the details attached.",
        "Name": "Rebekah Valdez",
        "Sender": "event-invitation@example.com",
        "Recipient": "rebekah.valdez@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[event_invitation.pdf](https://ibm.box.com/shared/static/8t2et95bukuet5rlw1p07p300nkvm7ew.pdf)"],
        "Timestamp": "2025-04-08T17:00:00Z"
    },
    {
        "Subject": "Survey Request",
        "Content": "Dear Yvonne Clark, Please take a moment to complete our survey. Your feedback is important to us.",
        "Name": "Yvonne Clark",
        "Sender": "survey-request@example.com",
        "Recipient": "yvonne.clark@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": [],
        "Timestamp": "2025-04-08T18:00:00Z"
    },
    {
        "Subject": "Meeting Agenda",
        "Content": "Dear James Harding, Please find the attached meeting agenda for our upcoming meeting.",
        "Name": "James Harding",
        "Sender": "meeting-agenda@example.com",
        "Recipient": "james.harding@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[meeting_agenda.pdf](https://ibm.box.com/shared/static/tkwl52jzjywcola3wylfhs7hay7bjtht.pdf)"],
        "Timestamp": "2025-04-08T19:00:00Z"
    },
    {
        "Subject": "Project Report",
        "Content": "Dear Thomas Anderson, Please find the attached project report for your review.",
        "Name": "Thomas Anderson",
        "Sender": "project-report@example.com",
        "Recipient": "thomas.anderson@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[project_report.pdf](https://ibm.box.com/shared/static/9xcxbvu65mmdlqabwok68r2n9g4b0js9.pdf)"],
        "Timestamp": "2025-04-08T20:00:00Z"
    },
    {
        "Subject": "Training Materials",
        "Content": "Dear Jennifer Rivers, Please find the attached training materials for the upcoming training session.",
        "Name": "Jennifer Rivers",
        "Sender": "training-materials@example.com",
        "Recipient": "jennifer.rivers@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[training_materials.pdf](https://ibm.box.com/shared/static/319hb7712h8bxgngun3qvj7zxbbqi2ak.pdf)"],
        "Timestamp": "2025-04-08T21:00:00Z"
    },
    {
        "Subject": "Meeting Notes",
        "Content": "Dear Sarah Boyle, Please find the attached meeting notes from our last meeting.",
        "Name": "Sarah Boyle",
        "Sender": "meeting-notes@example.com",
        "Recipient": "sarah.boyle@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[meeting_notes.pdf](https://ibm.box.com/shared/static/o4t8jc1j85h5nnil61gmy59f65yuwsnx.pdf)"],
        "Timestamp": "2025-04-08T22:00:00Z"
    },
    {
        "Subject": "Task Update",
        "Content": "Dear Mary Pruitt, Please find the attached task update for your review.",
        "Name": "Mary Pruitt",
        "Sender": "task-update@example.com",
        "Recipient": "mary.pruitt@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[task_update.pdf](https://ibm.box.com/shared/static/zycxldyrk0sc7xdueduivrn6vacy9mu5.pdf)"],
        "Timestamp": "2025-04-08T23:00:00Z"
    },
    {
        "Subject": "Event Reminder",
        "Content": "Dear Laura Escobar, This is a reminder for our upcoming event on Friday at 5 PM.",
        "Name": "Laura Escobar",
        "Sender": "event-reminder@example.com",
        "Recipient": "laura.escobar@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": [],
        "Timestamp": "2025-04-09T00:00:00Z"
    },
    {
        "Subject": "Project Timeline",
        "Content": "Dear Becky Simmons, Please find the attached project timeline for your review.",
        "Name": "Becky Simmons",
        "Sender": "project-timeline@example.com",
        "Recipient": "becky.simmons@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[project_timeline.pdf](https://ibm.box.com/shared/static/j7ut4xqlii5dkb38kk5t46wj31m5x5ke.pdf)"],
        "Timestamp": "2025-04-09T01:00:00Z"
    },
    {
        "Subject": "Meeting Summary",
        "Content": "Dear Tracey Brown, Please find the attached meeting summary from our last meeting.",
        "Name": "Tracey Brown",
        "Sender": "meeting-summary@example.com",
        "Recipient": "tracey.brown@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[meeting_summary.pdf](https://ibm.box.com/shared/static/ft5v6v7qrmsq1kk9mme98h7lfyopo38i.pdf)"],
        "Timestamp": "2025-04-09T02:00:00Z"
    },
    {
        "Subject": "Task Assignment",
        "Content": "Dear Sean Lang, Please find the attached task assignment for the upcoming project.",
        "Name": "Sean Lang",
        "Sender": "task-assignment@example.com",
        "Recipient": "sean.lang@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[task_assignment.pdf](https://ibm.box.com/shared/static/6t8sp29q0eisc7mzwt4s4m3gtvzhnkyi.pdf)"],
        "Timestamp": "2025-04-09T03:00:00Z"
    },
    {
        "Subject": "Performance Review",
        "Content": "Dear Michael Miller, Please find the attached performance review for the last quarter.",
        "Name": "Michael Miller",
        "Sender": "performance-review@example.com",
        "Recipient": "michael.miller@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[performance_review.pdf](https://ibm.box.com/shared/static/abhhlg8p0njats0fff8juuxvfddgwpde.pdf)"],
        "Timestamp": "2025-04-09T04:00:00Z"
    },
    {
        "Subject": "Event Invitation",
        "Content": "Dear Victor Vincent, You are invited to our upcoming event. Please find the details attached.",
        "Name": "Victor Vincent",
        "Sender": "event-invitation@example.com",
        "Recipient": "victor.vincent@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[event_invitation.pdf](https://ibm.box.com/shared/static/8t2et95bukuet5rlw1p07p300nkvm7ew.pdf)"],
        "Timestamp": "2025-04-09T05:00:00Z"
    },
    {
        "Subject": "Survey Request",
        "Content": "Dear Anthony Underwood, Please take a moment to complete our survey. Your feedback is important to us.",
        "Name": "Anthony Underwood",
        "Sender": "survey-request@example.com",
        "Recipient": "anthony.underwood@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": [],
        "Timestamp": "2025-04-09T06:00:00Z"
    },
    {
        "Subject": "Meeting Agenda",
        "Content": "Dear Kathleen Fowler, Please find the attached meeting agenda for our upcoming meeting.",
        "Name": "Kathleen Fowler",
        "Sender": "meeting-agenda@example.com",
        "Recipient": "kathleen.fowler@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[meeting_agenda.pdf](https://ibm.box.com/shared/static/tkwl52jzjywcola3wylfhs7hay7bjtht.pdf)"],
        "Timestamp": "2025-04-09T07:00:00Z"
    },
    {
        "Subject": "Project Report",
        "Content": "Dear John Garcia, Please find the attached project report for your review.",
        "Name": "John Garcia",
        "Sender": "project-report@example.com",
        "Recipient": "john.garcia@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[project_report.pdf](https://ibm.box.com/shared/static/9xcxbvu65mmdlqabwok68r2n9g4b0js9.pdf)"],
        "Timestamp": "2025-04-09T08:00:00Z"
    },
    {
        "Subject": "Training Materials",
        "Content": "Dear Tracy Melton, Please find the attached training materials for the upcoming training session.",
        "Name": "Tracy Melton",
        "Sender": "training-materials@example.com",
        "Recipient": "tracy.melton@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[training_materials.pdf](https://ibm.box.com/shared/static/319hb7712h8bxgngun3qvj7zxbbqi2ak.pdf)"],
        "Timestamp": "2025-04-09T09:00:00Z"
    },
    {
        "Subject": "Meeting Notes",
        "Content": "Dear Allison Stevens, Please find the attached meeting notes from our last meeting.",
        "Name": "Allison Stevens",
        "Sender": "meeting-notes@example.com",
        "Recipient": "allison.stevens@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[meeting_notes.pdf](https://ibm.box.com/shared/static/o4t8jc1j85h5nnil61gmy59f65yuwsnx.pdf)"],
        "Timestamp": "2025-04-09T10:00:00Z"
    },
    {
        "Subject": "Task Update",
        "Content": "Dear Robert Martin, Please find the attached task update for your review.",
        "Name": "Robert Martin",
        "Sender": "task-update@example.com",
        "Recipient": "robert.martin@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[task_update.pdf](https://ibm.box.com/shared/static/zycxldyrk0sc7xdueduivrn6vacy9mu5.pdf)"],
        "Timestamp": "2025-04-09T11:00:00Z"
    },
    {
        "Subject": "Event Reminder",
        "Content": "Dear John Smith, This is a reminder for our upcoming event on Friday at 5 PM.",
        "Name": "John Smith",
        "Sender": "event-reminder@example.com",
        "Recipient": "john.smith@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": [],
        "Timestamp": "2025-04-09T12:00:00Z"
    },
    {
        "Subject": "Project Timeline",
        "Content": "Dear Curtis Hunter, Please find the attached project timeline for your review.",
        "Name": "Curtis Hunter",
        "Sender": "project-timeline@example.com",
        "Recipient": "curtis.hunter@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[project_timeline.pdf](https://ibm.box.com/shared/static/j7ut4xqlii5dkb38kk5t46wj31m5x5ke.pdf)"],
        "Timestamp": "2025-04-09T13:00:00Z"
    },
    {
        "Subject": "Meeting Summary",
        "Content": "Dear Roy Andrews, Please find the attached meeting summary from our last meeting.",
        "Name": "Roy Andrews",
        "Sender": "meeting-summary@example.com",
        "Recipient": "roy.andrews@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[meeting_summary.pdf](https://ibm.box.com/shared/static/ft5v6v7qrmsq1kk9mme98h7lfyopo38i.pdf)"],
        "Timestamp": "2025-04-09T14:00:00Z"
    },
    {
        "Subject": "Task Assignment",
        "Content": "Dear Frank Melendez, Please find the attached task assignment for the upcoming project.",
        "Name": "Frank Melendez",
        "Sender": "task-assignment@example.com",
        "Recipient": "frank.melendez@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[task_assignment.pdf](https://ibm.box.com/shared/static/6t8sp29q0eisc7mzwt4s4m3gtvzhnkyi.pdf)"],
        "Timestamp": "2025-04-09T15:00:00Z"
    },
    {
        "Subject": "Performance Review",
        "Content": "Dear James Davies, Please find the attached performance review for the last quarter.",
        "Name": "James Davies",
        "Sender": "performance-review@example.com",
        "Recipient": "james.davies@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[performance_review.pdf](https://ibm.box.com/shared/static/abhhlg8p0njats0fff8juuxvfddgwpde.pdf)"],
        "Timestamp": "2025-04-09T16:00:00Z"
    },
    {
        "Subject": "Event Invitation",
        "Content": "Dear Jessica Cole, You are invited to our upcoming event. Please find the details attached.",
        "Name": "Jessica Cole",
        "Sender": "event-invitation@example.com",
        "Recipient": "jessica.cole@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[event_invitation.pdf](https://ibm.box.com/shared/static/8t2et95bukuet5rlw1p07p300nkvm7ew.pdf)"],
        "Timestamp": "2025-04-09T17:00:00Z"
    },
    {
        "Subject": "Survey Request",
        "Content": "Dear Gerald Pollard, Please take a moment to complete our survey. Your feedback is important to us.",
        "Name": "Gerald Pollard",
        "Sender": "survey-request@example.com",
        "Recipient": "gerald.pollard@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": [],
        "Timestamp": "2025-04-09T18:00:00Z"
    },
    {
        "Subject": "Meeting Agenda",
        "Content": "Dear Tony Tanner, Please find the attached meeting agenda for our upcoming meeting.",
        "Name": "Tony Tanner",
        "Sender": "meeting-agenda@example.com",
        "Recipient": "tony.tanner@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[meeting_agenda.pdf](https://ibm.box.com/shared/static/tkwl52jzjywcola3wylfhs7hay7bjtht.pdf)"],
        "Timestamp": "2025-04-09T19:00:00Z"
    },
    {
        "Subject": "Project Report",
        "Content": "Dear Erin Anderson, Please find the attached project report for your review.",
        "Name": "Erin Anderson",
        "Sender": "project-report@example.com",
        "Recipient": "erin.anderson@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[project_report.pdf](https://ibm.box.com/shared/static/9xcxbvu65mmdlqabwok68r2n9g4b0js9.pdf)"],
        "Timestamp": "2025-04-09T20:00:00Z"
    },
    {
        "Subject": "Training Materials",
        "Content": "Dear Blake Hernandez, Please find the attached training materials for the upcoming training session.",
        "Name": "Blake Hernandez",
        "Sender": "training-materials@example.com",
        "Recipient": "blake.hernandez@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[training_materials.pdf](https://ibm.box.com/shared/static/319hb7712h8bxgngun3qvj7zxbbqi2ak.pdf)"],
        "Timestamp": "2025-04-09T21:00:00Z"
    },
    {
        "Subject": "Meeting Notes",
        "Content": "Dear Bethany Nichols, Please find the attached meeting notes from our last meeting.",
        "Name": "Bethany Nichols",
        "Sender": "meeting-notes@example.com",
        "Recipient": "bethany.nichols@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[meeting_notes.pdf](https://ibm.box.com/shared/static/o4t8jc1j85h5nnil61gmy59f65yuwsnx.pdf)"],
        "Timestamp": "2025-04-09T22:00:00Z"
    },
    {
        "Subject": "Task Update",
        "Content": "Dear Renee Doyle, Please find the attached task update for your review.",
        "Name": "Renee Doyle",
        "Sender": "task-update@example.com",
        "Recipient": "renee.doyle@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[task_update.pdf](https://ibm.box.com/shared/static/zycxldyrk0sc7xdueduivrn6vacy9mu5.pdf)"],
        "Timestamp": "2025-04-09T23:00:00Z"
    },
    {
        "Subject": "Event Reminder",
        "Content": "Dear Michael Dominguez, This is a reminder for our upcoming event on Friday at 5 PM.",
        "Name": "Michael Dominguez",
        "Sender": "event-reminder@example.com",
        "Recipient": "michael.dominguez@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": [],
        "Timestamp": "2025-04-10T00:00:00Z"
    },
    {
        "Subject": "Project Timeline",
        "Content": "Dear Veronica Harrell, Please find the attached project timeline for your review.",
        "Name": "Veronica Harrell",
        "Sender": "project-timeline@example.com",
        "Recipient": "veronica.harrell@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[project_timeline.pdf](https://ibm.box.com/shared/static/j7ut4xqlii5dkb38kk5t46wj31m5x5ke.pdf)"],
        "Timestamp": "2025-04-10T01:00:00Z"
    },
    {
        "Subject": "Meeting Summary",
        "Content": "Dear Laura Richard, Please find the attached meeting summary from our last meeting.",
        "Name": "Laura Richard",
        "Sender": "meeting-summary@example.com",
        "Recipient": "laura.richard@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[meeting_summary.pdf](https://ibm.box.com/shared/static/ft5v6v7qrmsq1kk9mme98h7lfyopo38i.pdf)"],
        "Timestamp": "2025-04-10T02:00:00Z"
    },
    {
        "Subject": "Task Assignment",
        "Content": "Dear Deborah Bryant, Please find the attached task assignment for the upcoming project.",
        "Name": "Deborah Bryant",
        "Sender": "task-assignment@example.com",
        "Recipient": "deborah.bryant@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[task_assignment.pdf](https://ibm.box.com/shared/static/6t8sp29q0eisc7mzwt4s4m3gtvzhnkyi.pdf)"],
        "Timestamp": "2025-04-10T03:00:00Z"
    },
    {
        "Subject": "Performance Review",
        "Content": "Dear Kevin Kelley, Please find the attached performance review for the last quarter.",
        "Name": "Kevin Kelley",
        "Sender": "performance-review@example.com",
        "Recipient": "kevin.kelley@example.com",
        "Thread_ID": "1",
        "Thread_Index": "1",
        "Attachments": ["[performance_review.pdf](https://ibm.box.com/shared/static/abhhlg8p0njats0fff8juuxvfddgwpde.pdf)"],
        "Timestamp": "2025-04-10T04:00:00Z"
    }]
    return [i for i in all_emails if i["Name"] == name]

@app.post("/get_corporate_card_transactions")
def get_corporate_card_transactions(request: NameBasedRequest):
    name = request.name
    all_transactions = [
        {
            "Expense Type": "Flights", 
            "Supplier Details": "Singapore Airlines", 
            "Date": "2025-04-05",
            "Amount": "1200.00", 
            "Employee Name": "Victoria Baker", 
            "Transaction ID": 30238
        }, 
        {
            "Expense Type": "Hotel", 
            "Supplier Details": "Crowne Plaza", 
            "Date": "2025-04-05",
            "Amount": "3000.00", 
            "Employee Name": "Victoria Baker", 
            "Transaction ID": 30245
        }, 
        {
            "Expense Type": "Ridesharing", 
            "Supplier Details": "Grab Malaysia EC", 
            "Date": "2025-04-05",
            "Amount": "70.00", 
            "Employee Name": "Victoria Baker",
            "Transaction ID": 12388
        }
    ]

    return  [i for i in all_transactions if i["Employee Name"] == name]

# @app.post("/submit_expense_claim",operation_id="submitExpenseClaim")
# def request_time_off(request: ExpenseClaim):
#     conn = get_db_connection()
#     user = conn.execute("SELECT * FROM users WHERE LOWER(name) =  LOWER(?)", (request.name,)).fetchone()
#     if not user:
#         conn.close()
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # from_date = dt.strptime(request.from_date, "%d-%b-%Y")
#     # to_date = dt.strptime(request.to_date, "%d-%b-%Y")
#     from_date = dt.strptime(request.from_date, "%Y-%m-%d")
#     to_date = dt.strptime(request.to_date, "%Y-%m-%d")


#     days_difference = (to_date - from_date).days
    
#     if days_difference > user["time_off_balance"]:
#         conn.close()
#         raise HTTPException(status_code=200, detail="Not enough time off balance")
    
#     conn.execute("UPDATE users SET requested_time_off = ? WHERE LOWER(name) =  LOWER(?)", (days_difference, request.name))
#     conn.commit()
#     conn.close()
#     data = {"message": "Time off request submitted.", "requested_time_off": days_difference}

#     # llm_res = generate_natural_response(data)
#     # data["llm_response"] = llm_res
#     # llm_res = llm_res.replace('"',"")
#     # # print(data)
#     # if "Great news!" in llm_res:
#     #    llm_res = llm_res.replace("Great news!","") 
#     return f"{days_difference} days"



# @app.get("/time-off-balance/{name}",operation_id="getTimeOffBalance")
# def get_time_off_balance(name: str):
#     conn = get_db_connection()
#     user = conn.execute("SELECT name, time_off_balance FROM users WHERE LOWER(name) = LOWER(?)", (name,)).fetchone()
#     conn.close()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     data = dict(user)

#     llm_res = generate_natural_response(data)
#     data["llm_response"] = llm_res
#     llm_res = llm_res.replace('"',"")
#     # print(data)
#     if "Great news!" in llm_res:
#        llm_res = llm_res.replace("Great news!","") 
#     return llm_res.strip()

# @app.post("/request-time-off",operation_id="requestTimeOffBalance")
# def request_time_off(request: TimeOffRequest):
#     conn = get_db_connection()
#     user = conn.execute("SELECT * FROM users WHERE LOWER(name) =  LOWER(?)", (request.name,)).fetchone()
#     if not user:
#         conn.close()
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # from_date = dt.strptime(request.from_date, "%d-%b-%Y")
#     # to_date = dt.strptime(request.to_date, "%d-%b-%Y")
#     from_date = dt.strptime(request.from_date, "%Y-%m-%d")
#     to_date = dt.strptime(request.to_date, "%Y-%m-%d")


#     days_difference = (to_date - from_date).days
    
#     if days_difference > user["time_off_balance"]:
#         conn.close()
#         raise HTTPException(status_code=200, detail="Not enough time off balance")
    
#     conn.execute("UPDATE users SET requested_time_off = ? WHERE LOWER(name) =  LOWER(?)", (days_difference, request.name))
#     conn.commit()
#     conn.close()
#     data = {"message": "Time off request submitted.", "requested_time_off": days_difference}

#     llm_res = generate_natural_response(data)
#     data["llm_response"] = llm_res
#     llm_res = llm_res.replace('"',"")
#     # print(data)
#     if "Great news!" in llm_res:
#        llm_res = llm_res.replace("Great news!","") 
#     return llm_res.strip()

# @app.put("/update-title",operation_id="updateTitle")
# def update_title(request: UpdateTitleRequest):
#     conn = get_db_connection()
#     result = conn.execute("UPDATE users SET title = ? WHERE LOWER(name) =  LOWER(?)", (request.new_title, request.name))
#     conn.commit()
#     conn.close()
    
#     if result.rowcount == 0:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     data = {"message": "Title updated successfully", "new_title": request.new_title}

#     llm_res = generate_natural_response(data)
#     data["llm_response"] = llm_res
#     llm_res = llm_res.replace('"',"")
#     # print(data)
#     if "Great news!" in llm_res:
#        llm_res = llm_res.replace("Great news!","") 
#     return llm_res.strip()


# @app.put("/update-address",operation_id="updateAddress")
# def update_address(request: UpdateAddressRequest):
#     conn = get_db_connection()
#     result = conn.execute("UPDATE users SET address = ? WHERE LOWER(name) =  LOWER(?)", (request.new_address, request.name))
#     conn.commit()
#     conn.close()
    
#     if result.rowcount == 0:
#         raise HTTPException(status_code=404, detail="User not found")
        
#     data = {"message": "Address updated successfully", "new_address": request.new_address}

#     llm_res = generate_natural_response(data)
#     data["llm_response"] = llm_res
#     llm_res = llm_res.replace('"',"")
#     if "Great news!" in llm_res:
#        llm_res = llm_res.replace("Great news!","") 
#     return llm_res.strip()


@app.post("/create-user",operation_id="createUser")
def create_user(request: CreateUserRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define required columns
    required_columns = {"id", "name", "time_off_balance", "title", "address","requested_time_off"}

    # Get existing table schema
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = {row[1] for row in cursor.fetchall()}  # Extract column names

    # Check if any required column is missing
    if not required_columns.issubset(existing_columns):
        print("Table structure is incorrect. Recreating the users table...")
        
        cursor.execute("DROP TABLE IF EXISTS users")  # Remove old table

        # Create the new table with correct schema
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                time_off_balance REAL NOT NULL DEFAULT 0,
                title TEXT NOT NULL,
                address TEXT NOT NULL,
                requested_time_off INTEGER DEFAULT 0     
            )
        """)
        conn.commit()

    # Insert the new user
    cursor.execute(
        "INSERT INTO users (name, time_off_balance, title, address) VALUES (?, ?, ?, ?)", 
        (request.name, request.time_off_balance, request.title, request.address)
    )
    
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return {"message": "User created successfully", "user_id": user_id}


@app.post("/time-off-balance")
def get_time_off_balance(request: NameBasedRequest):
    name = request.name
    conn = get_db_connection()
    user = conn.execute("SELECT name, time_off_balance FROM users WHERE LOWER(name) = LOWER(?)", (name,)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    data = dict(user)

    # llm_res = generate_natural_response(data)
    # data["llm_response"] = llm_res
    # llm_res = llm_res.replace('"',"")
    # # print(data)
    # if "Great news!" in llm_res:
    #    llm_res = llm_res.replace("Great news!","") 
    return data["time_off_balance"]

@app.post("/request-time-off",operation_id="requestTimeOffBalance")
def request_time_off(request: TimeOffRequest):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(name) =  LOWER(?)", (request.name,)).fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    # from_date = dt.strptime(request.from_date, "%d-%b-%Y")
    # to_date = dt.strptime(request.to_date, "%d-%b-%Y")
    from_date = dt.strptime(request.from_date, "%Y-%m-%d")
    to_date = dt.strptime(request.to_date, "%Y-%m-%d")


    days_difference = (to_date - from_date).days + 1
    
    if days_difference > user["time_off_balance"]:
        conn.close()
        raise HTTPException(status_code=200, detail="Not enough time off balance")
    
    conn.execute("UPDATE users SET requested_time_off = ? WHERE LOWER(name) =  LOWER(?)", (days_difference, request.name))
    conn.commit()
    conn.close()
    data = {"message": "Time off request submitted.", "requested_time_off": days_difference}
    return f"{days_difference} days"

@app.post("/create-expense-claim")
def create_expense_claim(request: ExpenseClaimRequest):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(name) =  LOWER(?)", (request.name,)).fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    data = request
    return data

@app.put("/update-title",operation_id="updateTitle")
def update_title(request: UpdateTitleRequest):
    conn = get_db_connection()
    result = conn.execute("UPDATE users SET title = ? WHERE LOWER(name) =  LOWER(?)", (request.new_title, request.name))
    conn.commit()
    conn.close()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    data = {"message": "Title updated successfully", "new_title": request.new_title}

    # llm_res = generate_natural_response(data)
    # data["llm_response"] = llm_res
    # llm_res = llm_res.replace('"',"")
    # # print(data)
    # if "Great news!" in llm_res:
    #    llm_res = llm_res.replace("Great news!","") 
    return request.new_title


@app.put("/update-address",operation_id="updateAddress")
def update_address(request: UpdateAddressRequest):
    conn = get_db_connection()
    result = conn.execute("UPDATE users SET address = ? WHERE LOWER(name) =  LOWER(?)", (request.new_address, request.name))
    conn.commit()
    conn.close()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
        
    data = {"message": "Address updated successfully", "new_address": request.new_address}

    # llm_res = generate_natural_response(data)
    # data["llm_response"] = llm_res
    # llm_res = llm_res.replace('"',"")
    # if "Great news!" in llm_res:
    #    llm_res = llm_res.replace("Great news!","") 
    return request.new_address
