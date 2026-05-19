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

# Test for Dr. Daniela Mejía (6135b28a-df4a-4326-83e3-489721cea23c)
print("=== Slots for Dr. Daniela Mejía on 2026-05-24 ===")
slots_24 = service.get_available_slots("6135b28a-df4a-4326-83e3-489721cea23c", "2026-05-24")
print(slots_24)

print("\n=== Slots for Dr. Daniela Mejía on 2026-05-22 ===")
slots_22 = service.get_available_slots("6135b28a-df4a-4326-83e3-489721cea23c", "2026-05-22")
print(slots_22)
