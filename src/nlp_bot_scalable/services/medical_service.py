import httpx


class MedicalService:

    RED_FLAGS = [
        "chest pain",
        "difficulty breathing",
        "trouble breathing",
        "shortness of breath",
        "severe bleeding",
        "unconscious",
        "seizure",
        "stroke",
        "suicidal",
        "severe allergic",
    ]

    def symptom_checker(self, symptoms: str):
        symptoms = symptoms.lower().strip()

        # Emergency check first
        if any(flag in symptoms for flag in self.RED_FLAGS):
            return {
                "symptoms": symptoms,
                "possible_conditions": [],
                "emergency": True,
                "message": (
                    "Some of these symptoms can be serious. Please seek "
                    "emergency medical care or contact local emergency "
                    "services immediately."
                ),
                "disclaimer": (
                    "This information is for educational purposes only "
                    "and is not a medical diagnosis."
                ),
            }

        possible_conditions = []

        if "fever" in symptoms and "cough" in symptoms:
            possible_conditions.append("Common cold or flu")
        elif "fever" in symptoms:
            possible_conditions.append("Fever-related infection")
        elif "cough" in symptoms:
            possible_conditions.append(
                "Common cold, flu, or respiratory irritation"
            )

        if "headache" in symptoms:
            possible_conditions.append("Tension headache or migraine")

        if "stomach pain" in symptoms or "abdominal pain" in symptoms:
            possible_conditions.append("Digestive-related condition")

        if not possible_conditions:
            possible_conditions.append(
                "The symptoms are not specific enough to identify a possible condition."
            )

        return {
            "symptoms": symptoms,
            "possible_conditions": possible_conditions,
            "emergency": False,
            "disclaimer": (
                "This information is for educational purposes only "
                "and is not a medical diagnosis. Please consult a "
                "qualified healthcare professional for medical advice."
            ),
        }

    def medicine_information(self, medicine: str):
        medicine = medicine.lower().strip()

        medicines = {
            "paracetamol": {
                "uses": (
                    "Commonly used to reduce fever and relieve "
                    "mild to moderate pain."
                ),
                "side_effects": (
                    "Possible side effects can include nausea, "
                    "stomach discomfort, or allergic reactions."
                ),
                "precautions": (
                    "Avoid exceeding the recommended dose. People "
                    "with liver disease or other medical conditions "
                    "should consult a healthcare professional."
                ),
            },
            "ibuprofen": {
                "uses": (
                    "Commonly used to relieve pain, reduce fever, "
                    "and reduce inflammation."
                ),
                "side_effects": (
                    "Possible side effects can include stomach "
                    "discomfort, nausea, or indigestion."
                ),
                "precautions": (
                    "People with stomach ulcers, kidney problems, "
                    "certain heart conditions, or other medical "
                    "conditions should consult a healthcare professional "
                    "before using it."
                ),
            },
        }

        information = medicines.get(medicine)

        if information is None:
            return {
                "medicine": medicine,
                "message": (
                    "Medicine information is not available in "
                    "the current medical database."
                ),
                "disclaimer": (
                    "This information is for educational purposes only "
                    "and is not a substitute for professional medical advice."
                ),
            }

        return {
            "medicine": medicine,
            **information,
            "disclaimer": (
                "This information is for educational purposes only "
                "and is not a substitute for professional medical advice. "
                "Do not start, stop, or change medication without consulting "
                "a qualified healthcare professional."
            ),
        }

    def find_hospitals(self, city: str):
        city = city.strip()

        headers = {"User-Agent": "NLP-Medical-Assistant/1.0"}

        try:
            with httpx.Client(timeout=15.0) as client:
                # Step 1: city name -> coordinates
                geocode_response = client.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={"q": city, "format": "json", "limit": 1},
                    headers=headers,
                )
                geocode_response.raise_for_status()
                locations = geocode_response.json()

                if not locations:
                    return {
                        "city": city,
                        "hospitals": [],
                        "message": "Location could not be found.",
                    }

                latitude = float(locations[0]["lat"])
                longitude = float(locations[0]["lon"])

                # Step 2: hospitals within 10 km
                query = f"""
                [out:json][timeout:25];
                (
                  node["amenity"="hospital"](around:10000,{latitude},{longitude});
                  way["amenity"="hospital"](around:10000,{latitude},{longitude});
                  relation["amenity"="hospital"](around:10000,{latitude},{longitude});
                );
                out center tags;
                """

                overpass_response = client.post(
                    "https://overpass-api.de/api/interpreter",
                    data={"data": query},
                    headers=headers,
                )
                overpass_response.raise_for_status()
                data = overpass_response.json()

        except httpx.HTTPError as e:
            return {
                "city": city,
                "hospitals": [],
                "message": f"Could not fetch hospital data: {e}",
            }

        hospitals = []
        for place in data.get("elements", []):
            tags = place.get("tags", {})
            name = tags.get("name")
            if not name:
                continue

            address_parts = [
                tags.get("addr:housenumber"),
                tags.get("addr:street"),
                tags.get("addr:city"),
                tags.get("addr:state"),
            ]
            address = (
                ", ".join(part for part in address_parts if part)
                or "Address not available"
            )

            center = place.get("center", {})
            hospitals.append({
                "name": name,
                "address": address,
                "phone": tags.get("phone"),
                "website": tags.get("website"),
                "latitude": place.get("lat", center.get("lat")),
                "longitude": place.get("lon", center.get("lon")),
            })

            if len(hospitals) >= 10:
                break

        return {
            "city": city,
            "hospitals": hospitals,
            "disclaimer": (
                "Hospital data comes from OpenStreetMap and may be incomplete. "
                "In an emergency, contact local emergency services."
            ),
        }

    def medical_knowledge(self, topic: str):
        topic = topic.lower().strip()

        knowledge = {
            "fever": {
                "definition": "Fever is a temporary increase in body temperature, often associated with an infection or illness.",
                "causes": "Common causes include infections and other inflammatory conditions.",
                "symptoms": "Common symptoms may include increased body temperature, sweating, chills, headache, and weakness.",
                "prevention": "Good hygiene, hand washing, and avoiding close contact with people who are sick can help reduce the spread of some infections.",
            },
            "cold": {
                "definition": "The common cold is a viral infection that mainly affects the nose and throat.",
                "causes": "It is commonly caused by respiratory viruses.",
                "symptoms": "Common symptoms include a runny nose, sneezing, sore throat, cough, and congestion.",
                "prevention": "Regular hand washing and avoiding close contact with people who are sick can help reduce the spread.",
            },
            "diabetes": {
                "definition": "Diabetes is a chronic condition that affects how the body regulates blood glucose.",
                "causes": "Different types of diabetes have different causes, including genetic and environmental factors.",
                "symptoms": "Possible symptoms include increased thirst, frequent urination, tiredness, and blurred vision.",
                "prevention": "For some forms of diabetes, healthy eating, physical activity, and maintaining a healthy weight may reduce risk.",
            },
        }

        information = knowledge.get(topic)

        if information is None:
            return {
                "topic": topic,
                "message": "Medical information is not available for this topic in the current knowledge base.",
                "disclaimer": (
                    "This information is for educational purposes only "
                    "and is not a substitute for professional medical advice."
                ),
            }

        return {
            "topic": topic,
            **information,
            "disclaimer": (
                "This information is for educational purposes only "
                "and is not a substitute for professional medical advice."
            ),
        }