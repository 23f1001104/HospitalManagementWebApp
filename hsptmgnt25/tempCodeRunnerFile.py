
#POPULATING START

# INSERT DUMMY PATIENTS INTO USERS START


dummy_patients = [
    ("patient1", "p@1", "patient1", "patient"),
    ("patient2", "p@2", "patient2", "patient"),
    ("patient3", "p@3", "patient3", "patient"),
    ("patient4", "p@4", "patient4", "patient"),
    ("patient5", "p@5", "patient5", "patient"),
    ("patient6", "p@6", "patient6", "patient"),
    ("patient7", "p@7", "patient7", "patient"),
    ("patient8", "p@8", "patient8", "patient"),
    ("patient9", "p@9", "patient9", "patient"),
    ("patient10", "p@10", "patient10", "patient")
]


for p in dummy_patients:
    curr.execute("SELECT id FROM users WHERE email = ?", (p[1],))
    exists = curr.fetchone()
    if not exists:
        curr.execute(
            "INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, ?)",
            (p[0], p[1], p[2], p[3])
        )

# INSERT DUMMY PATIENTS INTO USERS END


# INSERT DUMMY DOCTORS (2 per department) into INTO BOTH DOCTORS AND USER START


dummy_doctors = [
    ("Dr Ortho 1", "ortho1@email", "ortho1", "Orthopedics", "Experience of 12 years"),
    ("Dr Ortho 2", "ortho2@email", "ortho2", "Orthopedics", "Experience of 15 years"),

    ("Dr Neuro 1", "neuro1@email", "neuro1", "Neurology", "Expert in seizures & stroke"),
    ("Dr Neuro 2", "neuro2@email", "neuro2", "Neurology", "10+ years clinical practice"),

    ("Dr ENT 1", "ent1@email", "ent1", "ENT", "Specialist in sinus care"),
    ("Dr ENT 2", "ent2@email", "ent2", "ENT", "Throat & hearing specialist"),

    ("Dr Gyno 1", "gyno1@email", "gyno1", "Gynecology", "Experienced gynecologist"),
    ("Dr Gyno 2", "gyno2@email", "gyno2", "Gynecology", "Maternity specialist"),

    ("Dr Eye 1", "eye1@email", "eye1", "Ophthalmology", "Cataract & Lasik expert"),
    ("Dr Eye 2", "eye2@email", "eye2", "Ophthalmology", "Vision correction specialist")
]   
for d in dummy_doctors:
    curr.execute("SELECT id FROM users WHERE email = ?", (d[1],))
    exists = curr.fetchone()
    if exists:
        continue

    # Insert into users
    curr.execute(
        "INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, 'doctor')",
        (d[0], d[1], d[2])
    )
    doctor_id = curr.lastrowid

    # Insert into doctors table
    curr.execute(
        "INSERT INTO doctors (id, fullname, email, password, department, bio) VALUES (?, ?, ?, ?, ?, ?)",
        (doctor_id, d[0], d[1], d[2], d[3], d[4])
    )



# INSERT DUMMY DOCTORS (2 per department) into INTO BOTH DOCTORS AND USER END



# INSERT DUMMY AVAILABILITY START

all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
shifts = ["morning", "afternoon", "evening", "night"]

curr.execute("SELECT id, fullname FROM doctors")
all_docs = curr.fetchall()

for doc in all_docs:
    doctor_id = doc[0]
    doctor_name = doc[1]

    # Select random number of work days (2–3 days)
    work_days = random.sample(all_days, random.randint(2, 3))	

    for day in work_days:
        # Random shifts (1–2 shifts per selected day)
        chosen_shifts = random.sample(shifts, random.randint(1, 2))

        # Build slot flags
        morning = 1 if "morning" in chosen_shifts else 0
        afternoon = 1 if "afternoon" in chosen_shifts else 0
        evening = 1 if "evening" in chosen_shifts else 0
        night = 1 if "night" in chosen_shifts else 0

        # Insert availability
        curr.execute("""
            INSERT OR IGNORE INTO doctors_availability
            (doctor_id, doctor_name, day, morning, afternoon, evening, night)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (doctor_id, doctor_name, day, morning, afternoon, evening, night))

# INSERT DUMMY AVAILABILITY END     


# ADD DUMMY APPOINTMENTS START


# Get patient IDs and names
curr.execute("SELECT id, fullname FROM users WHERE email IN ('p@1', 'p@2')")
patients = curr.fetchall()

# Get Dr Neuro 1 ID and info
curr.execute("SELECT id, fullname, department FROM doctors WHERE email = 'neuro1@email'")
neuro1 = curr.fetchone()

if neuro1 and len(patients) >= 2:
    # Patient 1
    p1_id = patients[0][0]
    p1_name = patients[0][1]
    
    # Patient 2
    p2_id = patients[1][0]
    p2_name = patients[1][1]
    
    # Dr Neuro 1
    neuro1_id = neuro1[0]
    neuro1_name = neuro1[1]
    neuro1_dept = neuro1[2]
    
    # Dummy appointments
    appointments_data = [
        (neuro1_id, p1_id, neuro1_name, p1_name, neuro1_dept, 'Monday', 'morning'),
        (neuro1_id, p1_id, neuro1_name, p1_name, neuro1_dept, 'Wednesday', 'afternoon'),
        (neuro1_id, p2_id, neuro1_name, p2_name, neuro1_dept, 'Monday', 'evening'),
        (neuro1_id, p2_id, neuro1_name, p2_name, neuro1_dept, 'Friday', 'morning'),
        (neuro1_id, p2_id, neuro1_name, p2_name, neuro1_dept, 'Tuesday', 'night'),
    ]
    
    for apt in appointments_data:
        # Check if appointment already exists to avoid duplicates
        curr.execute("""
            SELECT id FROM appointments 
            WHERE doctor_id = ? AND patient_id = ? AND day = ? AND slot = ?
        """, (apt[0], apt[1], apt[5], apt[6]))
        
        if not curr.fetchone():
            curr.execute("""
                INSERT INTO appointments 
                (doctor_id, patient_id, doctor_name, patient_name, department, day, slot)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, apt)

# ADD DUMMY APPOINTMENTS END

#POPULATING END
