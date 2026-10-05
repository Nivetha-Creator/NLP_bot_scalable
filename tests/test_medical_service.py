from nlp_bot_scalable.services.medical_service import MedicalService


def test_symptom_checker():
    service = MedicalService()

    result = service.symptom_checker("I have fever and cough")

    assert result is not None
    assert result["emergency"] is False
    assert "Common cold or flu" in result["possible_conditions"]


def test_symptom_checker_emergency():
    service = MedicalService()

    result = service.symptom_checker("severe chest pain")

    assert result["emergency"] is True
    assert result["possible_conditions"] == []


def test_medicine_information_known_drug():
    service = MedicalService()

    result = service.medicine_information("paracetamol")

    assert result["medicine"] == "paracetamol"
    assert "uses" in result


def test_medicine_information_unknown_drug():
    service = MedicalService()

    result = service.medicine_information("unknown-drug")

    assert "message" in result


def test_medical_knowledge_known_topic():
    service = MedicalService()

    result = service.medical_knowledge("diabetes")

    assert result["topic"] == "diabetes"
    assert "definition" in result


def test_medical_knowledge_unknown_topic():
    service = MedicalService()

    result = service.medical_knowledge("unknown-topic")

    assert "message" in result
