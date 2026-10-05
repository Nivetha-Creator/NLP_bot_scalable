from fastapi import APIRouter
from pydantic import BaseModel, Field

from nlp_bot_scalable.services.medical_service import MedicalService

router = APIRouter(
    prefix="/medical",
    tags=["Medical Services"],
)

medical_service = MedicalService()


class SymptomsRequest(BaseModel):
    symptoms: str = Field(..., min_length=1)


class MedicineRequest(BaseModel):
    medicine: str = Field(..., min_length=1)


class HospitalsRequest(BaseModel):
    city: str = Field(..., min_length=1)


class KnowledgeRequest(BaseModel):
    topic: str = Field(..., min_length=1)


@router.post("/symptoms")
def symptom_checker(request: SymptomsRequest):
    return medical_service.symptom_checker(request.symptoms)


@router.post("/medicine")
def medicine_information(request: MedicineRequest):
    return medical_service.medicine_information(request.medicine)


@router.post("/hospitals")
def find_hospitals(request: HospitalsRequest):
    return medical_service.find_hospitals(request.city)


@router.post("/knowledge")
def medical_knowledge(request: KnowledgeRequest):
    return medical_service.medical_knowledge(request.topic)
