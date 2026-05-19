import os
from supabase import create_client

url = None
key = None
with open(".env", "r") as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            if k == "PUBLIC_SUPABASE_URL":
                url = v
            elif k == "SUPABASE_SERVICE_ROLE_KEY":
                key = v

supabase = create_client(url, key)

# Query all doctors
res_docs = supabase.table('doctors').select('*').execute()
print("=== DOCTORS ===")
for doc in res_docs.data or []:
    print(f"ID: {doc['id']} | Name: Dr. {doc['first_name']} {doc['last_name']} | Specialty: {doc['speciality']}")

# Query all schedules
res_scheds = supabase.table('doctor_schedules').select('*').execute()
print("\n=== DOCTOR SCHEDULES ===")
for sched in res_scheds.data or []:
    # Find doctor name
    doc_name = "Unknown"
    for doc in res_docs.data or []:
        if doc['id'] == sched['doctor_id']:
            doc_name = f"Dr. {doc['first_name']} {doc['last_name']}"
            break
    print(f"ID: {sched['id']} | Doctor: {doc_name} ({sched['doctor_id']}) | Date: {sched['start_date']} to {sched['end_date']} | Time: {sched['start_time']} - {sched['end_time']}")

# Query all appointments
res_appts = supabase.table('appointments').select('*, doctor:doctors(*)').execute()
print("\n=== APPOINTMENTS ===")
for appt in res_appts.data or []:
    doc = appt.get('doctor') or {}
    doc_name = f"Dr. {doc.get('first_name', '')} {doc.get('last_name', '')}"
    print(f"ID: {appt['id']} | Patient ID: {appt['patient_id']} | Doctor: {doc_name} ({appt['doctor_id']}) | Date: {appt['appointment_date']} | Status: {appt['status']} | Schedule ID: {appt['schedule_id']}")
