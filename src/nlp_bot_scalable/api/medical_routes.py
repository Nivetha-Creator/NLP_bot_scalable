from fastapi import APIRouter

from nlp_bot_scalable.services.medical_service import MedicalService


router = APIRouter(
    prefix="/medical",
    tags=["Medical Services"]
)

medical_service = MedicalService()


@router.post("/symptoms")
def symptom_checker(symptoms: str):
    return medical_service.symptom_checker(symptoms)


@router.post("/medicine")
def medicine_information(medicine: str):
    return medical_service.medicine_information(medicine)


@router.post("/hospitals")
def find_hospitals(city: str):
    return medical_service.find_hospitals(city)


@router.post("/knowledge")
def medical_knowledge(topic: str):
    return medical_service.medical_knowledge(topic)