import os
from supabase import create_client
from app.services.appointment_service import AppointmentService

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

service = AppointmentService()
docs = service.get_doctors_by_specialty("Ortopedia")
print("Doctors returned for Ortopedia:")
for doc in docs:
    print(f"ID: {doc['id']} | Name: Dr. {doc['first_name']} {doc['last_name']} | Specialty: {doc['speciality']}")
