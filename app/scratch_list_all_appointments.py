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

res = supabase.table('appointments').select('*, doctor:doctors(*)').order('created_at', desc=True).execute()
print("=== All appointments (Newest first) ===")
for appt in res.data or []:
    doc = appt.get('doctor') or {}
    print(f"ID: {appt['id']} | Patient ID: {appt['patient_id']} | Date: {appt['appointment_date']} | Doctor: Dr. {doc.get('first_name', '')} {doc.get('last_name', '')} ({appt['doctor_id']}) | Status: {appt['status']} | Created At: {appt['created_at']}")
