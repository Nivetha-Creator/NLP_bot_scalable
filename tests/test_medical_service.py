from nlp_bot_scalable.services.medical_service import MedicalService

def test_symptom_checker():
    service = MedicalService()

    result = service.symptom_checker("I have fever and cough")

    assert result is not None