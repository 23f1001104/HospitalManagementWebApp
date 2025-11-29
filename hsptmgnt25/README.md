# Hospital Management System (Flask + SQLite)

A hospital management web application built using Flask and SQLite that allows Admins, Doctors, and Patients to manage users, appointments, availability, and patient records.

------------------------------------------------------------

FEATURES

USER ROLES

ADMIN
- Add, edit and delete doctors
- Edit and delete patients
- Blacklist / unblacklist doctors and patients
- View all doctors, patients, and appointments
- Search doctors, patients, and appointments
- Manage system data from one dashboard

DOCTOR
- View assigned appointments
- Set weekly availability
- Update patient medical history
- Mark appointments as completed or cancelled

PATIENT
- Register and login
- Book appointments
- Cancel appointments
- View appointment history
- Edit personal details

------------------------------------------------------------

TECH STACK

- Backend : Flask (Python)
- Database : SQLite
- Frontend : HTML, Jinja2 Templates
- Session management using Flask sessions
- No cloud database or third party services used

------------------------------------------------------------

## PROJECT STRUCTURE

```text
project/
│
├── app.py
├── hospital.db
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── admin.html
│   ├── doctor.html
│   ├── user.html
│   ├── doctoradd.html
│   ├── department.html
│   ├── doctorinfo.html
│   ├── doctor_availability.html
│   ├── updatepatient.html
│   ├── patienthistory.html
│   ├── edit_doctor_info.html
│   ├── edit_patient_info.html
│   ├── doctor_selecing_slots.html
│   ├── remove_doctor_confirm.html
│   ├── remove_patient_confirm.html
│   ├── slotsfull.html
│   ├── blacklisted.html
│   └── changes_by_patient.html
│
└── static/
```

------------------------------------------------------------

HOW TO RUN

1. Install Python (3.8 or higher)

2. Install Flask
pip install flask

3. Run the app
python app.py

4. Open browser and go to
http://127.0.0.1:5000

------------------------------------------------------------

DEFAULT ADMIN LOGIN

Email    : admin@email
Password : root

------------------------------------------------------------

DATABASE TABLES

USERS
- id
- fullname
- email
- password
- role (admin / doctor / patient)
- status (active / blacklisted)

DOCTORS
- id
- fullname
- email
- department
- bio
- status

DOCTOR_AVAILABILITY
- doctor_id
- day
- morning
- afternoon
- evening
- night

APPOINTMENTS
- doctor_id
- patient_id
- department
- day
- slot
- status

PATIENT_HISTORY
- appointment_id
- diagnosis
- medicines
- prescription
- doctor_response

------------------------------------------------------------

APPOINTMENT RULES

- Only 8 bookings allowed per doctor per time slot
- A patient cannot double-book the same doctor at the same time
- Appointment statuses maintained:
  - booked
  - completed
  - cancelled
  - cancelled by patient

------------------------------------------------------------

IMPORTANT NOTES

- Passwords are stored in plain text (not secure)
- No authentication middleware
- No role protection in URLs
- No form validation
- No CSRF protection
- This project is NOT production ready
- For educational and academic purposes only

------------------------------------------------------------

PURPOSE

This project is designed for:
- Learning Flask
- Understanding CRUD operations
- Building role-based systems
- Learning SQLite integration
- College project usage

------------------------------------------------------------

LICENSE

Free to use for educational and personal learning purposes.

------------------------------------------------------------

