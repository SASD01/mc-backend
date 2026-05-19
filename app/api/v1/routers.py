from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List

from app.schemas.appointment import (
    SpecialtyResponse, 
    DoctorSchema, 
    DaySlotsResponse, 
    BookAppointmentRequest, 
    AppointmentResponse,
    UpcomingAppointmentResponse
)
from app.services.appointment_service import AppointmentService
from app.core.security import get_current_user

api_router = APIRouter()

def get_appointment_service() -> AppointmentService:
    return AppointmentService()

@api_router.get("/specialties", response_model=SpecialtyResponse)
def get_specialties(service: AppointmentService = Depends(get_appointment_service)):
    try:
        specialties = service.get_specialties()
        return SpecialtyResponse(specialties=specialties)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/doctors", response_model=List[DoctorSchema])
def get_doctors_by_specialty(
    specialty: str = Query(..., description="Specialty to filter doctors"),
    service: AppointmentService = Depends(get_appointment_service)
):
    try:
        doctors = service.get_doctors_by_specialty(specialty)
        return doctors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/appointments/slots", response_model=DaySlotsResponse)
def get_appointment_slots(
    doctor_id: str = Query(...),
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    service: AppointmentService = Depends(get_appointment_service)
):
    try:
        slots = service.get_available_slots(doctor_id, date)
        return slots
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/appointments/book", response_model=AppointmentResponse)
def book_appointment(
    request: BookAppointmentRequest,
    patient_id: str = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service)
):
    try:
        # Convertimos el datetime a ISO 8601 string manejable por Supabase
        appointment_date_iso = request.appointment_date.isoformat()
        
        appointment = service.book_appointment(
            patient_id=patient_id,
            doctor_id=request.doctor_id,
            schedule_id=request.schedule_id,
            appointment_date=appointment_date_iso
        )
        if not appointment:
            raise HTTPException(status_code=400, detail="Could not book appointment.")
        return appointment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/appointments/upcoming", response_model=UpcomingAppointmentResponse)
def get_upcoming_appointment(
    patient_id: str = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service)
):
    try:
        appointment = service.get_upcoming_appointment(patient_id=patient_id)
        if not appointment:
            raise HTTPException(status_code=404, detail="No upcoming appointments found.")
        return appointment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/debug")
def debug_endpoints():
    import traceback
    try:
        from app.core.config import settings
        from app.core.database import get_supabase
        
        # Test settings
        settings_dict = {
            "PUBLIC_SUPABASE_URL": settings.PUBLIC_SUPABASE_URL,
            "PUBLIC_SUPABASE_ANON_KEY": settings.PUBLIC_SUPABASE_ANON_KEY[:10] + "..." if settings.PUBLIC_SUPABASE_ANON_KEY else None,
            "SUPABASE_SERVICE_ROLE_KEY": settings.SUPABASE_SERVICE_ROLE_KEY[:10] + "..." if settings.SUPABASE_SERVICE_ROLE_KEY else None
        }
        
        # Test client initialization
        client = get_supabase()
        
        # Test query
        res = client.table('doctors').select('speciality').neq('speciality', None).execute()
        
        return {
            "status": "success",
            "settings": settings_dict,
            "query_data": res.data
        }
    except Exception as e:
        return {
            "status": "error",
            "error_type": str(type(e)),
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }

