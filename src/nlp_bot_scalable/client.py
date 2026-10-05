import requests

BASE_URL = "http://127.0.0.1:8000"


def login(email: str, password: str) -> str:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    if not data.get("success"):
        raise ValueError(data.get("message", "Login failed"))

    access_token = data.get("access_token")
    if not access_token:
        raise ValueError("Login response did not include an access token")

    return access_token


def chat():
    print("NLP Chatbot")
    print("Sign in to start chatting.")
    print("-" * 40)

    email = input("Email: ").strip()
    password = input("Password: ").strip()

    try:
        token = login(email, password)
    except (requests.RequestException, ValueError) as error:
        print(f"Authentication failed: {error}")
        return

    print("Authenticated. Type 'exit' to quit.")
    print("-" * 40)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            print("Bot: Goodbye!")
            break

        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": message},
                headers=headers,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            print(f"Bot: {data['response']}")

        except requests.RequestException as error:
            print(f"Error connecting to chatbot: {error}")


if __name__ == "__main__":
    chat()
