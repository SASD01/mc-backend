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

# Let's try to book an appointment for Dr. Daniela Mejía (6135b28a-df4a-4326-83e3-489721cea23c)
# Schedule ID is from Dr. Daniela Mejía (e.g. 76c8d4ce-29cd-4d91-a11e-ea41abc152f7)
# Patient ID is fe5662a4-a855-43f2-af08-b3c9db237ba5

patient_id = "fe5662a4-a855-43f2-af08-b3c9db237ba5"
doctor_id = "6135b28a-df4a-4326-83e3-489721cea23c"
schedule_id = "76c8d4ce-29cd-4d91-a11e-ea41abc152f7"
appointment_date = "2026-05-22T08:00:00Z"

data = {
    "patient_id": patient_id,
    "doctor_id": doctor_id,
    "schedule_id": schedule_id,
    "appointment_date": appointment_date,
    "status": "pending"
}

try:
    print("Inserting appointment...")
    res = supabase.table('appointments').insert(data).execute()
    print("Insertion Result:")
    print(res.data)
except Exception as e:
    print(f"Error: {e}")
