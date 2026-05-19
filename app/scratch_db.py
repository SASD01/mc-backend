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

# Query appointments for this patient
res = supabase.table('appointments')\
    .select('*, doctor:doctors(*)')\
    .eq('patient_id', 'fe5662a4-a855-43f2-af08-b3c9db237ba5')\
    .execute()

print("Patient appointments:")
for appt in res.data or []:
    print(f"ID: {appt['id']}, Date: {appt['appointment_date']}, Status: {appt['status']}, Doctor: {appt['doctor']['first_name']} {appt['doctor']['last_name']}, Speciality: {appt['doctor']['speciality']}")
