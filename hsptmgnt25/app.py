#IMPORT 
from flask import Flask,request,render_template,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import text
import sqlite3
import random


#INSTANTIATE FLASK
app = Flask(__name__)
app.secret_key = "something_super_secret_and_random"



#MAKING THE DATABASE FILE
conn = sqlite3.connect("hospital.db")

#MAKING CURSOR
curr = conn.cursor()

#MAKING THE USERS TABLE
curr.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'doctor', 'patient')) NOT NULL,
    status TEXT CHECK(status IN ('active', 'blacklisted')) DEFAULT 'active'
);
""")

#MAKING DOCTOR TABLE
curr.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY,
    fullname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, 
    department TEXT CHECK(department IN ('Ophthalmology', 'Gynecology', 'Neurology', 'Orthopedics', 'ENT')) NOT NULL,
    bio TEXT,
    status TEXT CHECK(status IN ('active', 'blacklisted')) DEFAULT 'active',
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);
""")

#MAING DOCTOR AVAILABILITY TABLE
curr.execute("""
CREATE TABLE IF NOT EXISTS doctors_availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    doctor_name TEXT NOT NULL,
    day TEXT CHECK(day IN (
        'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'
    )) NOT NULL,
    morning INTEGER CHECK(morning IN (0,1)) DEFAULT 0,
    afternoon INTEGER CHECK(afternoon IN (0,1)) DEFAULT 0,
    evening INTEGER CHECK(evening IN (0,1)) DEFAULT 0,
    night INTEGER CHECK(night IN (0,1)) DEFAULT 0,
    FOREIGN KEY (doctor_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(doctor_id, day)
);
""")

#CREATING APPOINTMENTS TABLE
curr.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    doctor_name TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    department TEXT NOT NULL CHECK(department IN ('Ophthalmology', 'Gynecology', 'Neurology', 'Orthopedics', 'ENT')),
    day TEXT NOT NULL,
    slot TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'booked',
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    FOREIGN KEY (patient_id) REFERENCES users(id)
);
""")


#CREATING PATIENT HISTORY TABLE
curr.execute("""
CREATE TABLE IF NOT EXISTS patient_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    doctor_name TEXT NOT NULL,
    patient_name TEXT NOT NULL,
    department TEXT NOT NULL CHECK(department IN ('Ophthalmology', 'Gynecology', 'Neurology', 'Orthopedics', 'ENT')),
    doctor_response TEXT CHECK(doctor_response IN ('Cancelled', 'Completed','Yet to be','Cancelled By Patient')) NOT NULL,
    test_done TEXT,
    medicines TEXT,
    diagnosis TEXT,
    prescription TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES users(id) ON DELETE CASCADE
);
""")

#INSERTING ADMIN [CHECK IF ADMIN IS AVAILABLE; IF NOT ADD IT IF YES SKIP IT] INTO USER
curr.execute("SELECT * FROM users WHERE email = ?", ("admin@email",))
admin = curr.fetchone()
if not admin:
    curr.execute("""INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, ?)""", ("Admin", "admin@email", "root", "admin"))	



# #POPULATING START

# # INSERT DUMMY PATIENTS INTO USERS START


# dummy_patients = [
#     ("patient1", "p@1", "patient1", "patient"),
#     ("patient2", "p@2", "patient2", "patient"),
#     ("patient3", "p@3", "patient3", "patient"),
#     ("patient4", "p@4", "patient4", "patient"),
#     ("patient5", "p@5", "patient5", "patient"),
#     ("patient6", "p@6", "patient6", "patient"),
#     ("patient7", "p@7", "patient7", "patient"),
#     ("patient8", "p@8", "patient8", "patient"),
#     ("patient9", "p@9", "patient9", "patient"),
#     ("patient10", "p@10", "patient10", "patient")
# ]


# for p in dummy_patients:
#     curr.execute("SELECT id FROM users WHERE email = ?", (p[1],))
#     exists = curr.fetchone()
#     if not exists:
#         curr.execute(
#             "INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, ?)",
#             (p[0], p[1], p[2], p[3])
#         )

# # INSERT DUMMY PATIENTS INTO USERS END


# # INSERT DUMMY DOCTORS (2 per department) into INTO BOTH DOCTORS AND USER START


# dummy_doctors = [
#     ("Dr Ortho 1", "ortho1@email", "ortho1", "Orthopedics", "Experience of 12 years"),
#     ("Dr Ortho 2", "ortho2@email", "ortho2", "Orthopedics", "Experience of 15 years"),

#     ("Dr Neuro 1", "neuro1@email", "neuro1", "Neurology", "Expert in seizures & stroke"),
#     ("Dr Neuro 2", "neuro2@email", "neuro2", "Neurology", "10+ years clinical practice"),

#     ("Dr ENT 1", "ent1@email", "ent1", "ENT", "Specialist in sinus care"),
#     ("Dr ENT 2", "ent2@email", "ent2", "ENT", "Throat & hearing specialist"),

#     ("Dr Gyno 1", "gyno1@email", "gyno1", "Gynecology", "Experienced gynecologist"),
#     ("Dr Gyno 2", "gyno2@email", "gyno2", "Gynecology", "Maternity specialist"),

#     ("Dr Eye 1", "eye1@email", "eye1", "Ophthalmology", "Cataract & Lasik expert"),
#     ("Dr Eye 2", "eye2@email", "eye2", "Ophthalmology", "Vision correction specialist")
# ]   
# for d in dummy_doctors:
#     curr.execute("SELECT id FROM users WHERE email = ?", (d[1],))
#     exists = curr.fetchone()
#     if exists:
#         continue

#     # Insert into users
#     curr.execute(
#         "INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, 'doctor')",
#         (d[0], d[1], d[2])
#     )
#     doctor_id = curr.lastrowid

#     # Insert into doctors table
#     curr.execute(
#         "INSERT INTO doctors (id, fullname, email, password, department, bio) VALUES (?, ?, ?, ?, ?, ?)",
#         (doctor_id, d[0], d[1], d[2], d[3], d[4])
#     )



# # INSERT DUMMY DOCTORS (2 per department) into INTO BOTH DOCTORS AND USER END



# # INSERT DUMMY AVAILABILITY START

# all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# shifts = ["morning", "afternoon", "evening", "night"]

# curr.execute("SELECT id, fullname FROM doctors")
# all_docs = curr.fetchall()

# for doc in all_docs:
#     doctor_id = doc[0]
#     doctor_name = doc[1]

#     # Select random number of work days (2–3 days)
#     work_days = random.sample(all_days, random.randint(2, 3))	

#     for day in work_days:
#         # Random shifts (1–2 shifts per selected day)
#         chosen_shifts = random.sample(shifts, random.randint(1, 2))

#         # Build slot flags
#         morning = 1 if "morning" in chosen_shifts else 0
#         afternoon = 1 if "afternoon" in chosen_shifts else 0
#         evening = 1 if "evening" in chosen_shifts else 0
#         night = 1 if "night" in chosen_shifts else 0

#         # Insert availability
#         curr.execute("""
#             INSERT OR IGNORE INTO doctors_availability
#             (doctor_id, doctor_name, day, morning, afternoon, evening, night)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (doctor_id, doctor_name, day, morning, afternoon, evening, night))

# # INSERT DUMMY AVAILABILITY END     


# # ADD DUMMY APPOINTMENTS START


# # Get patient IDs and names
# curr.execute("SELECT id, fullname FROM users WHERE email IN ('p@1', 'p@2')")
# patients = curr.fetchall()

# # Get Dr Neuro 1 ID and info
# curr.execute("SELECT id, fullname, department FROM doctors WHERE email = 'neuro1@email'")
# neuro1 = curr.fetchone()

# if neuro1 and len(patients) >= 2:
#     # Patient 1
#     p1_id = patients[0][0]
#     p1_name = patients[0][1]
    
#     # Patient 2
#     p2_id = patients[1][0]
#     p2_name = patients[1][1]
    
#     # Dr Neuro 1
#     neuro1_id = neuro1[0]
#     neuro1_name = neuro1[1]
#     neuro1_dept = neuro1[2]
    
#     # Dummy appointments
#     appointments_data = [
#         (neuro1_id, p1_id, neuro1_name, p1_name, neuro1_dept, 'Monday', 'morning'),
#         (neuro1_id, p1_id, neuro1_name, p1_name, neuro1_dept, 'Wednesday', 'afternoon'),
#         (neuro1_id, p2_id, neuro1_name, p2_name, neuro1_dept, 'Monday', 'evening'),
#         (neuro1_id, p2_id, neuro1_name, p2_name, neuro1_dept, 'Friday', 'morning'),
#         (neuro1_id, p2_id, neuro1_name, p2_name, neuro1_dept, 'Tuesday', 'night'),
#     ]
    
#     for apt in appointments_data:
#         # Check if appointment already exists to avoid duplicates
#         curr.execute("""
#             SELECT id FROM appointments 
#             WHERE doctor_id = ? AND patient_id = ? AND day = ? AND slot = ?
#         """, (apt[0], apt[1], apt[5], apt[6]))
        
#         if not curr.fetchone():
#             curr.execute("""
#                 INSERT INTO appointments 
#                 (doctor_id, patient_id, doctor_name, patient_name, department, day, slot)
#                 VALUES (?, ?, ?, ?, ?, ?, ?)
#             """, apt)

# # ADD DUMMY APPOINTMENTS END

# #POPULATING END


conn.commit()
conn.close()



#HOME OF FLASK
@app.route('/')
def hello_world():
    return 'You are in port 5000. Hit /login or /register'



#MAKING REGISTRATION
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST": 
        
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        
        
        conn = sqlite3.connect("hospital.db")
        curr = conn.cursor()

        curr.execute("""INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, ?)""", (fullname, email, password, 'patient')) 
        
        conn.commit()
        conn.close()


        return render_template("login.html")
        
    return render_template("register.html")


#MAKING LOGIN
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']
        

        conn = sqlite3.connect("hospital.db")
        curr = conn.cursor()

        curr.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = curr.fetchone()
        
        conn.close()
        
        #CHOICE WISE RENDERING
        if user:
            user_id = user[0]
            user_name = user[1]
            user_email = user[2]
            user_password = user[3]
            user_role = user[4]
            user_status = user[5]  # Get status
            
            session['user_id'] = user_id
            #storing user_id into session for our use
            

            if user_status == 'blacklisted':
                return render_template('blacklisted.html', name=user_name, id=user_id)
            

            if user_role == 'patient':
                return redirect(url_for('user',id=user_id))
            if user_role == 'doctor':
                return redirect(url_for('doctor',id=user_id))
            if user_role == 'admin':
                return redirect(url_for('admin'))
        else:
            return "It seems like you are not registered. Please register yourself", 401
        
    return render_template("login.html")





#ADMIN PAGE
@app.route('/admin')
def admin():
    search_query = request.args.get('search', '').strip()
    
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()
    
    if search_query:
        
        search_pattern = f"%{search_query}%"
        
        # Search Patients
        curr.execute("""
            SELECT * FROM users 
            WHERE role = 'patient' 
            AND (fullname LIKE ? OR email LIKE ? OR CAST(id AS TEXT) LIKE ?)
        """, (search_pattern, search_pattern, search_pattern))
        patients = curr.fetchall()
        

        total_patients = len(patients)

        # Search Doctors
        curr.execute("""
            SELECT * FROM doctors 
            WHERE fullname LIKE ? 
            OR email LIKE ? 
            OR department LIKE ?
            OR CAST(id AS TEXT) LIKE ?
        """, (search_pattern, search_pattern, search_pattern, search_pattern))
        doctors = curr.fetchall()
        total_doctors = len(doctors)

        # Search Appointments
        curr.execute("""
            SELECT * FROM appointments 
            WHERE doctor_name LIKE ? 
            OR patient_name LIKE ? 
            OR department LIKE ?
            OR day LIKE ?
            OR CAST(id AS TEXT) LIKE ?
        """, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
        appointments = curr.fetchall()
        total_appointments = len(appointments)

    else:
        # No search - show all
        curr.execute("SELECT * FROM users WHERE role = 'patient'")
        patients = curr.fetchall()
        total_patients = len(patients)

        
        curr.execute('SELECT * FROM doctors')
        doctors = curr.fetchall()
        total_doctors = len(doctors)

        
        curr.execute("SELECT * FROM appointments WHERE status = ?", ("booked",))

        appointments = curr.fetchall()
        total_appointments = len(appointments)
        
    
    conn.close()
    
    return render_template("admin.html",
                         patients=patients,
                         doctors=doctors,
                         appointments=appointments,
                         search_query=search_query, total_doctors = total_doctors, total_patients = total_patients , total_appointments = total_appointments )




#ADDING A DOCTOR
@app.route("/doctoradd",methods=['GET','POST'])
def doctoradd():
    if request.method =="POST":
        fullname = request.form['fullname'] 
        email = request.form['email'] 
        password = request.form['password'] 
        department = request.form['department'] 
        bio = request.form['bio']
        
        
        conn = sqlite3.connect('hospital.db')
        curr = conn.cursor()

        curr.execute("""INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, ?)""", (fullname, email, password, 'doctor')) 
        
        doctor_id = curr.lastrowid
    
        curr.execute("""INSERT INTO doctors (id, fullname, email, password, department, bio) VALUES (?, ?, ?, ?, ?, ?)""", (doctor_id, fullname, email, password, department, bio)) 
        
        # FOR AVAILABILITY
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for day in days:
            day_checked = request.form.get(f'day_{day}')

            if day_checked:  
                slot = request.form.get(f'slot_{day}', '')
                
                
                morning = 1 if slot == 'morning' else 0
                afternoon = 1 if slot == 'afternoon' else 0
                evening = 1 if slot == 'evening' else 0
                night = 1 if slot == 'night' else 0
                
                
                curr.execute("""INSERT INTO doctors_availability (doctor_id, doctor_name, day, morning, afternoon, evening, night) VALUES (?, ?, ?, ?, ?, ?, ?)""", (doctor_id,fullname, day, morning, afternoon, evening, night))
        
        
        conn.commit()
        conn.close()


        return redirect(url_for("admin"))
    return render_template('doctoradd.html')


#USER PAGE [PATIENT PAGE]
@app.route("/user/<int:id>",methods=['GET','POST'])
def user(id):
    conn = sqlite3.connect("hospital.db")
    curr = conn.cursor()

    curr.execute(
        "SELECT * FROM users WHERE id = ?",(id,)
    )
    user = curr.fetchone()

    conn.close()

    patient_id = user[0] 
    user_name = user[1] 

    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()

    curr.execute("""
        SELECT * FROM appointments
        WHERE patient_id = ?
        AND status = 'booked'
    """, (patient_id,))
    appointment = curr.fetchall()


    conn.close()
    
    return render_template("user.html",user_name=user_name,appointment=appointment,user_id=patient_id)


#DOCTOR PAGE
@app.route("/doctor/<int:id>",methods=['GET','POST'])
def doctor(id):
    conn = sqlite3.connect("hospital.db")
    curr = conn.cursor()
    
    curr.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = curr.fetchone()
    doctor_name = user[1]

    curr.execute("""
        SELECT * FROM appointments 
        WHERE doctor_id = ? AND status = 'booked'
        ORDER BY created_at DESC
    """, (id,))
    appointments = curr.fetchall()
    
    
    conn.close()
    return render_template("doctor.html",appointments=appointments,doctor_name=doctor_name, doctor=user)


#DEPARTMENT PAGE
@app.route('/<department>',methods=['GET','POST'])
def department(department):
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()

    curr.execute("SELECT * FROM doctors WHERE department=?",(department,))
    doctors = curr.fetchall()

    conn.close()


    bios = {
        'Ophthalmology': "Our Ophthalmology Department cares for everything related to your eyes and vision. From routine eye checkups to advanced surgeries, we’ve got you covered. We treat cataracts, glaucoma, and a wide range of eye conditions. Our specialists use modern technology to help you see clearly again. Your healthy vision is our top priority—because the world looks better when you can see it well.",
        'Gynecology': "We’re dedicated to supporting women’s health at every stage of life. From regular checkups to maternity care, our team provides compassionate, expert guidance. We handle everything from prenatal care to advanced gynecological treatments. Your comfort, privacy, and trust matter most to us. Here, women’s health and wellbeing always come first.",
        'Neurology': "Our Neurology Department focuses on the brain, spine, and nervous system. We help patients manage headaches, seizures, strokes, and other neurological concerns. Our doctors combine advanced diagnostics with personalized care. Every treatment plan is designed to help you regain strength and balance. We’re here to help you live life with clarity and confidence.",
        'Orthopedics': "Whether it’s a fracture, joint pain, or sports injury, our Orthopedics team is here to help. We specialize in restoring movement and reducing pain through expert care. From physiotherapy to advanced surgery, we offer complete solutions. Our goal is to get you back on your feet—stronger than ever. Because every step you take matters to us.",
        'ENT': "Our ENT specialists care for all your ear, nose, and throat needs. We treat hearing loss, sinus problems, throat infections, and more. Using advanced techniques, we make breathing, hearing, and speaking easier. From kids to adults, we offer gentle, effective care for all ages. Breathe better, hear better, and live better with our ENT team."
    }
    

    return render_template("department.html", department = department, bio=bios[department],doctors = doctors)


#DOCTOR INFO
@app.route('/doctorinfo/<int:id>',methods=['GET','POST'])
def doctorinfo(id):
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()

    curr.execute("SELECT * FROM doctors WHERE id=?",(id,))
    doctor = curr.fetchone()

    conn.close()
    
    
    doctor_id = doctor[0]       
    doctor_name = doctor[1]       
    doctor_email = doctor[2]       
    doctor_department = doctor[4]       
    doctor_bio = doctor[5]       
    
    return render_template('doctorinfo.html',doctor_bio=doctor_bio,doctor_name=doctor_name,doctor_department=doctor_department,doctor_email=doctor_email)




#VIEWING DOCTOR AVAILABILITY
@app.route('/doctor_availability/<int:id>',methods = ['GET','POST'])
def doctor_availability(id):
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()

    curr.execute("SELECT * FROM doctors_availability WHERE doctor_id=?",(id,))
    slots = curr.fetchall()
    
    return render_template('doctor_availability.html',doctors_availability=slots)




#MAKING BOOKING / MAKING APPOINTMENT
@app.route('/booking', methods=['GET','POST'])
def booking():
    user_id = session.get('user_id')       
    # storing doctor id using session for later use    
    doctor_id = request.form.get('doctor_id')     
    day = request.form.get('day')
    slot = request.form.get('slot')     
    
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()
    
    # CHECK EXISTING BOOKINGS FOR THIS DOCTOR, DAY, AND SLOT
    curr.execute("""
        SELECT COUNT(*) FROM appointments 
        WHERE doctor_id = ? AND day = ? AND slot = ? AND status = 'booked'
    """, (doctor_id, day, slot))
    
    current_bookings = curr.fetchone()[0]
    print(current_bookings)
    
    # IF X OR MORE BOOKINGS EXIST, REDIRECT BACK WITH ERROR MESSAGE
    X = 8
    if current_bookings >= X:
        print('rsbg')
        # Get doctor details for error message
        curr.execute("SELECT fullname, department FROM doctors WHERE id = ?", (doctor_id,))
        doctor_info = curr.fetchone()
        department = doctor_info[1]
        
        conn.close()
        
        return render_template('slotsfull.html',day=day,slot=slot)
    
    
    curr.execute("SELECT fullname, department FROM doctors WHERE id = ?", (doctor_id,))
    doctor_info = curr.fetchone()
    doctor_name = doctor_info[0]
    department = doctor_info[1]
    

    curr.execute("SELECT fullname FROM users WHERE id = ?", (user_id,))
    patient_info = curr.fetchone()
    patient_name = patient_info[0]
    

    curr.execute("""
    INSERT INTO appointments (doctor_id, patient_id, doctor_name, patient_name, department, day, slot)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (doctor_id, user_id, doctor_name, patient_name, department, day, slot))

    appointment_id = curr.lastrowid

    # PARALLEL INSERT IN patient_history TABLE  
    curr.execute("""
    INSERT INTO patient_history 
    (appointment_id, doctor_id, patient_id, doctor_name, patient_name, 
     department, doctor_response, test_done, medicines, diagnosis, prescription)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (appointment_id, doctor_id, user_id, doctor_name, patient_name, 
          department, 'Yet to be', 'Yet to be', 'Yet to be', 'Yet to be', 'Yet to be'))
    conn.commit()
    conn.close()
    
    # return render_template('booking.html', doctor_name=doctor_name, day=day, slot=slot, appointment_id=appointment_id)
    return redirect(url_for('user', id=user_id))


# cancel appointment
@app.route('/cancel_appointment',methods = ['GET','POST'])
def cancel_appointment():
    appointment_id = request.form.get('appointment_id')
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()
    
    # FIND THE APPOINTMENT FIRST
    curr.execute("""
        SELECT id, doctor_id, patient_id, doctor_name, patient_name, 
               department, day, slot, created_at, status 
        FROM appointments 
        WHERE id = ?
    """, (appointment_id,))
    appointment = curr.fetchone()
    
    if appointment:
        # Delete the appointment
        # curr.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        patient_id = appointment[2]
        curr.execute("UPDATE appointments SET status = ? WHERE id = ?",("Cancelled By Patient", appointment_id))
        curr.execute("""UPDATE patient_history 
                     SET doctor_response = 'Cancelled By Patient',
        test_done = 'Cancelled By Patient' ,
        medicines = 'Cancelled By Patient' ,
        diagnosis = 'Cancelled By Patient' ,
        prescription = 'Cancelled By Patient'  WHERE appointment_id = ? """, (appointment_id,))
        conn.commit()
        
        # TYPE CONVERSION FROM TUPLE TO DICTIONARY FOR JINJA 2
        appointment_dict = {
            'id': appointment[0],
            'doctor_id': appointment[1],
            'patient_id': appointment[2],
            'doctor_name': appointment[3],
            'patient_name': appointment[4],
            'department': appointment[5],
            'day': appointment[6],
            'slot': appointment[7],
            'created_at': appointment[8],
            'status': appointment[9]
        }
        conn.close()
        return redirect(url_for('user', id=patient_id))
    

#DOCTOR UPDATING PATIENTS INFO
@app.route('/update_patient_history/<int:appointment_id>', methods=['GET', 'POST'])
def update_patient_history(appointment_id):
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()
    
    # FETCH APPOINTMENT DETAILS
    curr.execute("""
        SELECT doctor_id, patient_id, doctor_name, patient_name, department
        FROM appointments 
        WHERE id = ?
    """, (appointment_id,))
    
    appointment = curr.fetchone()
    print(appointment)
    
    doctor_id = appointment[0]
    patient_id = appointment[1]
    doctor_name = appointment[2]
    patient_name = appointment[3]
    department = appointment[4]
    
    if request.method == 'POST':
        doctor_response = request.form.get('doctor_response')
        test_done = request.form.get('test_done')
        medicines = request.form.get('medicines')
        diagnosis = request.form.get('diagnosis')
        prescription = request.form.get('prescription')
        
        # INSERT INTO PATIENT HISTORY
        # curr.execute("""
        #     INSERT INTO patient_history 
        #     (appointment_id, doctor_id, patient_id, doctor_name, patient_name, 
        #      department, doctor_response, test_done, medicines, diagnosis, prescription)
        #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        # """, (appointment_id, doctor_id, patient_id, doctor_name, patient_name, 
        #       department, doctor_response, test_done, medicines, diagnosis, prescription))
        


        # UPDATE APPOINTMENT STATUS
        if doctor_response == 'Completed':
            curr.execute("UPDATE appointments SET status = 'completed' WHERE id = ?", (appointment_id,))
            curr.execute("""
            INSERT INTO patient_history 
            (appointment_id, doctor_id, patient_id, doctor_name, patient_name, 
             department, doctor_response, test_done, medicines, diagnosis, prescription)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (appointment_id, doctor_id, patient_id, doctor_name, patient_name, 
              department, doctor_response, test_done, medicines, diagnosis, prescription))
            
        elif doctor_response == 'Cancelled':
            curr.execute("UPDATE appointments SET status = 'cancelled' WHERE id = ?", (appointment_id,))
            curr.execute("""
            INSERT INTO patient_history 
            (appointment_id, doctor_id, patient_id, doctor_name, patient_name, 
             department, doctor_response, test_done, medicines, diagnosis, prescription)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (appointment_id, doctor_id, patient_id, doctor_name, patient_name, 
              department, 'Cancelled', 'Cancelled', 'Cancelled', 'Cancelled', 'Cancelled'))
        
        conn.commit()
        conn.close()
        
        
        return redirect(url_for('doctor', id=doctor_id))
    
    conn.close()
    return render_template('updatepatient.html', 
                         appointment_id=appointment_id,
                         doctor_name=doctor_name,
                         patient_name=patient_name,
                         department=department)


# SHOWING PATIENT HISTORY -- main view
@app.route('/patient_history/<int:patient_id>',methods = ['GET','POST'])
def showpatienthistory(patient_id):
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()

    curr.execute("SELECT * FROM patient_history WHERE patient_id = ?", (patient_id,))
    history = curr.fetchall()
    conn.close()
    if history:
        return render_template('patienthistory.html',history=history)
    else:
        return "No Records to Show", 401 



# DOCTOR CHOOSE SLOTS
@app.route('/doctor_select_slots/<int:doctor_id>', methods=['GET', 'POST'])
def doctor_select_slots(doctor_id):
    conn = sqlite3.connect("hospital.db")
    curr = conn.cursor()

    # FIND DOCTOR
    curr.execute("SELECT fullname FROM doctors WHERE id = ?", (doctor_id,))
    row = curr.fetchone()
    if not row:
        conn.close()
        return "Doctor not found"
    doctor_name = row[0]

    if request.method == 'POST':

        # 1️ DELETE OLD SLOTS
        curr.execute("DELETE FROM doctors_availability WHERE doctor_id = ?", (doctor_id,))

        days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

        # 2️ INSERT NEW SLOTS
        for day in days:
            checkbox = request.form.get(f"day_{day}")
            slot = request.form.get(f"slot_{day}")

            if not checkbox:
                continue

            morning = afternoon = evening = night = 0

            if slot == "morning":
                morning = 1
            elif slot == "afternoon":
                afternoon = 1
            elif slot == "evening":
                evening = 1
            elif slot == "night":
                night = 1

            curr.execute("""
                INSERT INTO doctors_availability
                (doctor_id, doctor_name, day, morning, afternoon, evening, night)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (doctor_id, doctor_name, day, morning, afternoon, evening, night))

        conn.commit()
        conn.close()

        return redirect(url_for('doctor', id=doctor_id))


    conn.close()
    return render_template(
        "doctor_selecing_slots.html",
        doctor_id=doctor_id,
        doctor_name=doctor_name
    )






#EDIT DOCTOR
@app.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    conn = sqlite3.connect("hospital.db")
    curr = conn.cursor()
    
    # GET DOCTOR DATA
    curr.execute("SELECT email, department, bio, fullname FROM doctors WHERE id = ?", (doctor_id,))
    doctor = curr.fetchone()
    
    if request.method == 'POST':
        new_email = request.form.get("email").strip()
        new_department = request.form.get("department")
        new_bio = request.form.get("bio").strip()
        
        
        email = new_email if new_email else doctor[0]
        department = new_department if new_department and new_department != "Select Department" else doctor[1]
        bio = new_bio if new_bio else doctor[2]
        
        
        # UPDATE DOCTOR TABLE
        curr.execute("""
            UPDATE doctors
            SET email = ?, department = ?, bio = ?
            WHERE id = ?
        """, (email, department, bio, doctor_id))
        

        # UPDATE USERS TABLE
        curr.execute("""
            UPDATE users
            SET email = ?
            WHERE id = ?
        """, (email, doctor_id))


        #UPDATING AVAILABILITY
        
        # 1. CLEAR old availability
        curr.execute("DELETE FROM doctors_availability WHERE doctor_id = ?", (doctor_id,))
        
        # 2. RE-INSERT availability
        days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        doctor_name = doctor[3] 
        
        for day in days:
            day_checked = request.form.get(f"day_{day}")
            slot = request.form.get(f"slot_{day}", "")
            
            if day_checked:
                morning   = 1 if slot == "morning" else 0
                afternoon = 1 if slot == "afternoon" else 0
                evening   = 1 if slot == "evening" else 0
                night     = 1 if slot == "night" else 0
                
                curr.execute("""
                    INSERT INTO doctors_availability
                    (doctor_id, doctor_name, day, morning, afternoon, evening, night)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (doctor_id, doctor_name, day, morning, afternoon, evening, night))
        
        conn.commit()
        conn.close()
        return redirect(url_for("admin"))
    

    curr.execute("SELECT day, morning, afternoon, evening, night FROM doctors_availability WHERE doctor_id = ?", (doctor_id,))
    availability = curr.fetchall()
    
    conn.close()
    return render_template('edit_doctor_info.html', doctor=doctor, availability=availability, doctor_id=doctor_id)



#DELETE DOCTOR
@app.route('/remove_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def remove_doctor(doctor_id):
    if request.method == 'POST':
        choice = request.form.get("choice")

        if choice == "yes":
            conn = sqlite3.connect("hospital.db")
            curr = conn.cursor()

            # DELETE DOCTOR
            curr.execute("DELETE FROM doctors_availability WHERE doctor_id = ?", (doctor_id,))

            # DELETE DOCTOR
            curr.execute("DELETE FROM appointments WHERE doctor_id = ?", (doctor_id,))

            # DELETE DOCTOR
            curr.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))

            # DELETE DOCTOR
            curr.execute("DELETE FROM users WHERE id = ?", (doctor_id,))

            conn.commit()
            conn.close()

            return redirect('/admin')   # back to admin page

        else:
            return redirect('/admin')   # No → return admin

    return render_template('remove_doctor_confirm.html', doctor_id=doctor_id)




# BLACKLIST DOCTOR
@app.route('/blacklist/<int:doctor_id>')
def blacklist_doctor(doctor_id):
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()
    
    
    curr.execute("UPDATE users SET status = 'blacklisted' WHERE id = ?", (doctor_id,))
    

    curr.execute("UPDATE doctors SET status = 'blacklisted' WHERE id = ?", (doctor_id,))
    
    conn.commit()
    conn.close()
    
    return redirect('/admin') 



# UNBLACKLIST DOCTOR
@app.route('/unblacklist/<int:doctor_id>')
def unblacklist_doctor(doctor_id):
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()
    

    curr.execute("UPDATE users SET status = 'active' WHERE id = ?", (doctor_id,))
    

    curr.execute("UPDATE doctors SET status = 'active' WHERE id = ?", (doctor_id,))
    
    conn.commit()
    conn.close()
    
    return redirect('/admin')  # Go back to admin page





#EDIT PATIENT BY ADMIN
@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    if request.method == 'POST':

        new_fullname = request.form.get("fullname").strip()
        new_email = request.form.get("email").strip()
        
        conn = sqlite3.connect("hospital.db")
        curr = conn.cursor()
        

        curr.execute("SELECT fullname, email FROM users WHERE id = ? AND role = 'patient'", (patient_id,))
        current_data = curr.fetchone()
        

        fullname = new_fullname if new_fullname else current_data[0]
        email = new_email if new_email else current_data[1]
        

        # UPDATE patient info
        curr.execute("""
            UPDATE users
            SET fullname = ?, email = ?
            WHERE id = ? AND role = 'patient'
        """, (fullname, email, patient_id))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for("admin"))
    
   
    conn = sqlite3.connect("hospital.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM users WHERE id = ? AND role = 'patient'", (patient_id,))
    patient = curr.fetchone()
    conn.close()
    
    return render_template('edit_patient_info.html', patient=patient)


#REMOVE PATIENT
@app.route('/remove_patient/<int:patient_id>', methods=['GET', 'POST'])
def remove_patient(patient_id):
    if request.method == 'POST':
        choice = request.form.get("choice")

        if choice == "yes":
            conn = sqlite3.connect("hospital.db")
            curr = conn.cursor()

            # DELETE PATIENT
            curr.execute("DELETE FROM patient_history WHERE patient_id = ?", (patient_id,))

            # DELETE PATIENT
            curr.execute("DELETE FROM appointments WHERE patient_id = ?", (patient_id,))

            # DELETE PATIENT
            curr.execute("DELETE FROM users WHERE id = ? AND role = 'patient'", (patient_id,))

            conn.commit()
            conn.close()

            return redirect('/admin')  

        else:
            return redirect('/admin')  

    return render_template('remove_patient_confirm.html', patient_id=patient_id)




# BLACKLIST PATIENT
@app.route('/blacklist_patient/<int:patient_id>')
def blacklist_patient(patient_id):
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()
    
    # BLACKLIST
    curr.execute("UPDATE users SET status = 'blacklisted' WHERE id = ?", (patient_id,))
    
    conn.commit()
    conn.close()
    
    return redirect('/admin')  




# UNBLACKLIST PATIENT
@app.route('/unblacklist_patient/<int:patient_id>')
def unblacklist_patient(patient_id):
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()
    
    # UNBLACKLIST
    curr.execute("UPDATE users SET status = 'active' WHERE id = ?", (patient_id,))
    
    conn.commit()
    conn.close()
    
    return redirect('/admin')




#PATIENT INFO CHANGE BY PATIENTS
@app.route('/editbypatient/<int:id>', methods=['GET', 'POST'])
def editbypatient(id):
    conn = sqlite3.connect("hospital.db")
    curr = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')

        # Get current patient name for cascade update
        curr.execute("SELECT fullname FROM users WHERE id = ?", (id,))
        old_name = curr.fetchone()[0]

        # UPDATE users table
        curr.execute("""
            UPDATE users 
            SET fullname = COALESCE(NULLIF(?, ''), fullname),
                email = COALESCE(NULLIF(?, ''), email),
                password = COALESCE(NULLIF(?, ''), password)
            WHERE id = ?
        """, (name, email, password, id))

        # UPDATE appointments table (patient_name)
        if name:
            curr.execute("""
                UPDATE appointments 
                SET patient_name = ?
                WHERE patient_id = ?
            """, (name, id))

        # UPDATE patient_history table (patient_name)
        if name:
            curr.execute("""
                UPDATE patient_history 
                SET patient_name = ?
                WHERE patient_id = ?
            """, (name, id))

        conn.commit()
        conn.close()

        return redirect(url_for('user', id=id))



    curr.execute("SELECT fullname, email FROM users WHERE id = ?", (id,))
    user = curr.fetchone()
    conn.close()

    return render_template("changes_by_patient.html", user=user, user_id=id)



#VIEW APPOINTMENT
@app.route('/view_appointment/<int:appointment_id>')
def view_appointment(appointment_id):
    conn = sqlite3.connect('hospital.db')
    curr = conn.cursor()
    
    # Get the patient_id from the appointment
    curr.execute("SELECT patient_id FROM appointments WHERE id = ?", (appointment_id,))
    result = curr.fetchone()
    
    conn.close()
    

    patient_id = result[0]
    return redirect(url_for('showpatienthistory', patient_id=patient_id))




if __name__ == '__main__':
    app.run(debug=True) 

