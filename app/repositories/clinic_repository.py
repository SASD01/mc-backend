from app.core.database import get_supabase

class ClinicRepository:
    def __init__(self):
        self.client = get_supabase()

    def get_specialties(self):
        try:
            response = self.client.table('doctors').select('speciality').neq('speciality', None).execute()
            specialties = set()
            if response.data:
                for doc in response.data:
                    specialties.add(doc['speciality'])
            return sorted(list(specialties))
        except Exception as e:
            print(f"Error fetching specialties: {e}")
            return []

    def get_doctors_by_specialty(self, specialty: str):
        try:
            response = self.client.table('doctors').select('*').eq('speciality', specialty).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching doctors by specialty: {e}")
            return []

    def get_doctor_schedules(self, doctor_id: str, target_date: str):
        try:
            response = self.client.table('doctor_schedules')\
                .select('*')\
                .eq('doctor_id', doctor_id)\
                .lte('start_date', target_date)\
                .gte('end_date', target_date)\
                .eq('is_available', True)\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error fetching schedules: {e}")
            return []

    def get_booked_appointments(self, doctor_id: str, target_date: str):
        try:
            response = self.client.table('appointments')\
                .select('*')\
                .eq('doctor_id', doctor_id)\
                .gte('appointment_date', f"{target_date}T00:00:00")\
                .lte('appointment_date', f"{target_date}T23:59:59")\
                .neq('status', 'cancelled')\
                .execute()
            return response.data
        except Exception as e:
            print(f"Error fetching booked appointments: {e}")
            return []

    def book_appointment(self, patient_id: str, doctor_id: str, schedule_id: str, appointment_date: str):
        # Validar que el turno pertenezca al médico seleccionado
        if schedule_id and schedule_id != "00000000-0000-0000-0000-000000000000":
            try:
                sched_res = self.client.table('doctor_schedules').select('doctor_id').eq('id', schedule_id).execute()
                if sched_res.data and sched_res.data[0]['doctor_id'] != doctor_id:
                    print(f"Error: Mismatch de médico. Turno pertenece a {sched_res.data[0]['doctor_id']} pero se pidió para {doctor_id}")
                    return None
            except Exception as e:
                print(f"Error al validar el turno: {e}")

        if not schedule_id or schedule_id == "00000000-0000-0000-0000-000000000000":
            # Extract YYYY-MM-DD from ISO timestamp (e.g. 2026-05-24T10:00:00Z)
            date_str = appointment_date.split('T')[0]
            schedules = self.get_doctor_schedules(doctor_id, date_str)
            if schedules:
                schedule_id = schedules[0]['id']
            else:
                # If no schedule matches for that date, fallback to any schedule of the doctor to avoid FK error
                try:
                    res = self.client.table('doctor_schedules').select('id').eq('doctor_id', doctor_id).limit(1).execute()
                    if res.data:
                        schedule_id = res.data[0]['id']
                except Exception as e:
                    print(f"Error falling back to general schedule: {e}")

        data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "schedule_id": schedule_id,
            "appointment_date": appointment_date,
            "status": "pending"
        }
        response = self.client.table('appointments').insert(data).execute()
        return response.data[0] if response.data else None

    def get_upcoming_appointment(self, patient_id: str):
        from datetime import datetime
        now = datetime.utcnow().isoformat()
        try:
            response = self.client.table('appointments')\
                .select('*, doctor:doctors(*)')\
                .eq('patient_id', patient_id)\
                .neq('status', 'cancelled')\
                .gte('appointment_date', now)\
                .order('appointment_date')\
                .limit(1)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching upcoming appointment: {e}")
            return None

