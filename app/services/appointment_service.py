from datetime import datetime, timedelta, time
from app.repositories.clinic_repository import ClinicRepository

class AppointmentService:
    def __init__(self):
        self.repo = ClinicRepository()

    def get_specialties(self):
        return self.repo.get_specialties()

    def get_doctors_by_specialty(self, specialty: str):
        return self.repo.get_doctors_by_specialty(specialty)

    def get_available_slots(self, doctor_id: str, target_date: str):
        schedules = self.repo.get_doctor_schedules(doctor_id, target_date)
        
        # Obtenemos citas reservadas y extraemos las horas
        booked_appointments = self.repo.get_booked_appointments(doctor_id, target_date)
        booked_times = []
        for appt in booked_appointments:
            # appointment_date viene como timestamptz string (ej: "2023-10-24T10:00:00Z")
            dt = datetime.fromisoformat(appt['appointment_date'].replace('Z', '+00:00'))
            booked_times.append(dt.time())
            
        morning_slots = []
        afternoon_slots = []
        
        # Iterar sobre cada horario válido del doctor
        for sched in schedules:
            start_t = time.fromisoformat(sched['start_time'])
            end_t = time.fromisoformat(sched['end_time'])
            
            # Generar bloques de 30 mins
            current_dt = datetime.combine(datetime.min, start_t)
            end_dt = datetime.combine(datetime.min, end_t)
            
            while current_dt < end_dt:
                current_time = current_dt.time()
                is_available = current_time not in booked_times
                
                slot = {"time": current_time, "is_available": is_available, "schedule_id": sched['id']}
                
                if current_time.hour < 12:
                    morning_slots.append(slot)
                else:
                    afternoon_slots.append(slot)
                    
                current_dt += timedelta(minutes=30)

        morning_slots.sort(key=lambda x: x['time'])
        afternoon_slots.sort(key=lambda x: x['time'])
        
        return {
            "morning": morning_slots,
            "afternoon": afternoon_slots
        }

    def book_appointment(self, patient_id: str, doctor_id: str, schedule_id: str, appointment_date: str):
        return self.repo.book_appointment(patient_id, doctor_id, schedule_id, appointment_date)

    def get_upcoming_appointment(self, patient_id: str):
        return self.repo.get_upcoming_appointment(patient_id)
