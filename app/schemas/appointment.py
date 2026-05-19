from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time, datetime

class DoctorSchema(BaseModel):
    id: str
    first_name: str
    last_name: str
    speciality: str
    status: Optional[str] = None
    
class SpecialtyResponse(BaseModel):
    specialties: List[str]

class TimeSlot(BaseModel):
    time: time
    is_available: bool
    schedule_id: str

class DaySlotsResponse(BaseModel):
    morning: List[TimeSlot]
    afternoon: List[TimeSlot]

class BookAppointmentRequest(BaseModel):
    doctor_id: str
    schedule_id: str
    appointment_date: datetime
    
class AppointmentResponse(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    schedule_id: str
    appointment_date: datetime
    status: str

class UpcomingAppointmentResponse(BaseModel):
    id: str
    patient_id: str
    appointment_date: datetime
    status: str
    doctor: DoctorSchema
