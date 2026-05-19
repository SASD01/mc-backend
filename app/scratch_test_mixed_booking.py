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

# Let's try to book an appointment with:
# doctor_id = Dr. Daniela Mejía (6135b28a-df4a-4326-83e3-489721cea23c)
# BUT schedule_id = Dr. Alejandro Vega's schedule (397a815f-7144-4b50-9c04-2708bcd3a5d0)

patient_id = "fe5662a4-a855-43f2-af08-b3c9db237ba5"
doctor_id = "6135b28a-df4a-4326-83e3-489721cea23c"
schedule_id = "397a815f-7144-4b50-9c04-2708bcd3a5d0"
appointment_date = "2026-05-24T10:00:00Z"

data = {
    "patient_id": patient_id,
    "doctor_id": doctor_id,
    "schedule_id": schedule_id,
    "appointment_date": appointment_date,
    "status": "pending"
}

try:
    print("Inserting mixed appointment...")
    res = supabase.table('appointments').insert(data).execute()
    print("Insertion Result:")
    print(res.data)
except Exception as e:
    print(f"Error/Constraint triggered: {e}")
