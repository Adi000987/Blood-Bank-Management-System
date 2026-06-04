Blood Bank Management System

Blood Bank Management System is a desktop application developed using Python, Tkinter, and MySQL. The project helps manage blood donors and blood requests through a simple graphical user interface.

The system allows users to register as blood donors, request blood, search for donors by blood group, and provides an admin panel for managing donor and request records.

## Features

- Admin login system
- Donor registration
- Blood request submission
- Search donors by blood group
- View registered donors
- View blood requests
- Delete donor records
- Delete blood request records
- Password hashing for login security
- User-friendly dark-themed interface

Technologies Used

- Python
- Tkinter
- MySQL
- MySQL Connector
- hashlib (MD5)

Database Tables

The project uses the following tables:

- `tbladmin`
- `tblblooddonars`
- `tblbloodgroup`
- `tblbloodrequirer`

## Installation

1. Install the required package:

```bash
pip install mysql-connector-python
```

2. Create a MySQL database named:

```sql
CREATE DATABASE admin;
```

3. Create the required tables or import the provided SQL file.

4. Update the database connection details in the Python file:

```python
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='YOUR_PASSWORD',
        database='admin'
    )
```

5. Run the application:

```bash
python blood_bank.py
```

Admin Login

Default credentials:

```text
Username: admin
Password: Admin@1
```

These credentials can be changed directly from the database.

## Project Modules

Admin Panel

- Login authentication
- View donor records
- View blood requests
- Delete donors
- Delete requests
- Logout functionality

Register Donor

Stores donor information such as:

- Name
- Mobile Number
- Email
- Gender
- Age
- Blood Group
- Address
- Message

Request Blood

Allows users to submit blood requests along with contact details and required blood group.

### Search Donor

Users can search for available donors based on blood group. If no donor is available, an appropriate message is displayed.

Screenshots

The screenshots folder contains images of:

- Admin Login Page
- Donor Registration Page
- Blood Request Page
- Search Donor Page
- Admin Dashboard

Future Improvements

Some features that can be added in future versions:

- Blood stock management
- Email notifications
- SMS alerts
- Hospital integration
- Better password encryption
- Web-based version of the application

Author

Aditya Gupta

B.Tech Computer Science Engineering

SRM Institute of Science and Technology

License

This project was developed for academic and learning purposes.
