from typing import List

from app.core.security import get_current_user
from app.schemas.appointment import (
    AppointmentResponse,
    BookAppointmentRequest,
    DaySlotsResponse,
    DoctorSchema,
    SpecialtyResponse,
    UpcomingAppointmentResponse,
)
from app.services.appointment_service import AppointmentService
from fastapi import APIRouter, Depends, HTTPException, Query, status

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
    service: AppointmentService = Depends(get_appointment_service),
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
    service: AppointmentService = Depends(get_appointment_service),
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
    service: AppointmentService = Depends(get_appointment_service),
):
    try:
        appointment_date_iso = request.appointment_date.isoformat()

        appointment = service.book_appointment(
            patient_id=patient_id,
            doctor_id=request.doctor_id,
            schedule_id=request.schedule_id,
            appointment_date=appointment_date_iso,
        )
        if not appointment:
            raise HTTPException(status_code=400, detail="Could not book appointment.")
        return appointment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/appointments/upcoming", response_model=List[UpcomingAppointmentResponse])
def get_upcoming_appointment(
    patient_id: str = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    try:
        appointments = service.get_upcoming_appointment(patient_id=patient_id)
        return appointments
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
