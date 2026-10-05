const API_URL = window.location.origin;
let currentUser = null;
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message");
const sendButton = document.getElementById("send-button");


/* =========================
   MEDICAL HOME
========================= */
function showMedicalHome() {
    chatBox.innerHTML = `
        <div class="medical-home">

            <div class="welcome-icon">
                🏥
            </div>

            <h1>Medical Assistant</h1>

            <p class="home-description">
                Your AI-powered medical information assistant
            </p>

            <button class="chat-service-button" onclick="openChat()">
                💬 Chat with Medical Assistant
            </button>

            <p class="medical-disclaimer">
                This assistant provides general medical information only
                and is not a substitute for professional medical advice.
            </p>

        </div>
    `;
}

/* =========================
   OPEN MEDICAL SERVICES
========================= */

function openService(service) {

    if (service === "symptoms") {

        chatBox.innerHTML = `
            <div class="service-page">

                <button class="back-button" onclick="showMedicalHome()">
                    ← Back
                </button>

                <div class="service-page-header">
                    <div class="large-service-icon">🩺</div>

                    <div>
                        <h1>Symptom Checker</h1>
                        <p>
                            Tell me about your symptoms.
                        </p>
                    </div>
                </div>

                <div class="service-form">

                    <label>What symptoms are you experiencing?</label>

                    <textarea
                        id="symptom-input"
                        placeholder="Example: I have fever, headache and sore throat..."
                    ></textarea>

                    <button
                        class="primary-button"
                        onclick="checkSymptoms()">
                        Check Symptoms
                    </button>

                </div>

                <div id="service-result"></div>

                <div class="medical-warning">
                    ⚠️ This information is for educational purposes only
                    and is not a medical diagnosis.
                </div>

            </div>
        `;

    }


    else if (service === "medicine") {

        chatBox.innerHTML = `
            <div class="service-page">

                <button class="back-button" onclick="showMedicalHome()">
                    ← Back
                </button>

                <div class="service-page-header">
                    <div class="large-service-icon">💊</div>

                    <div>
                        <h1>Medicine Information</h1>
                        <p>
                            Search for general information about a medicine.
                        </p>
                    </div>
                </div>

                <div class="service-form">

                    <label>Medicine name</label>

                    <input
                        type="text"
                        id="medicine-input"
                        placeholder="Example: Paracetamol"
                    />

                    <button
                        class="primary-button"
                        onclick="getMedicineInfo()">
                        Search Medicine
                    </button>

                </div>

                <div id="service-result"></div>

                <div class="medical-warning">
                    ⚠️ Medicine information is general educational
                    information. Consult a healthcare professional
                    for personal medical advice.
                </div>

            </div>
        `;

    }


    else if (service === "hospitals") {

        chatBox.innerHTML = `
            <div class="service-page">

                <button class="back-button" onclick="showMedicalHome()">
                    ← Back
                </button>

                <div class="service-page-header">
                    <div class="large-service-icon">🏥</div>

                    <div>
                        <h1>Hospital Finder</h1>
                        <p>
                            Find hospitals based on your city or location.
                        </p>
                    </div>
                </div>

                <div class="service-form">

                    <label>City or location</label>

                    <input
                        type="text"
                        id="hospital-input"
                        placeholder="Example: Chennai"
                    />

                    <button
                        class="primary-button"
                        onclick="findHospitals()">
                        Find Hospitals
                    </button>

                </div>

                <div id="service-result"></div>

            </div>
        `;

    }


    else if (service === "knowledge") {

        chatBox.innerHTML = `
            <div class="service-page">

                <button class="back-button" onclick="showMedicalHome()">
                    ← Back
                </button>

                <div class="service-page-header">
                    <div class="large-service-icon">📚</div>

                    <div>
                        <h1>Medical Knowledge</h1>
                        <p>
                            Learn about diseases, symptoms, causes and prevention.
                        </p>
                    </div>
                </div>

                <div class="service-form">

                    <label>What would you like to learn about?</label>

                    <input
                        type="text"
                        id="knowledge-input"
                        placeholder="Example: Diabetes"
                    />

                    <button
                        class="primary-button"
                        onclick="getMedicalKnowledge()">
                        Learn
                    </button>

                </div>

                <div id="service-result"></div>

            </div>
        `;

    }
}


/* =========================
   TEMPORARY SERVICE TESTS
========================= */

/*
   These are temporary.

   We are NOT connecting the new APIs yet.

   First we are checking that the
   frontend pages work correctly.
*/


async function checkSymptoms() {

    const value = document
        .getElementById("symptom-input")
        .value
        .trim();

    if (!value) {
        alert("Please enter your symptoms.");
        return;
    }

    const resultBox = document.getElementById("service-result");

    resultBox.innerHTML = `
        <div class="result-card">
            <h2>🩺 Analyzing Symptoms...</h2>
            <p>Please wait...</p>
        </div>
    `;

    try {

        const response = await fetch(
            `${API_URL}/medical/symptoms?symptoms=${encodeURIComponent(value)}`,
            {
                method: "POST"
            }
        );

        if (!response.ok) {
            throw new Error("Symptom API request failed");
        }

        const data = await response.json();

        resultBox.innerHTML = `
            <div class="result-card">

                <h2>🩺 Symptom Information</h2>

                <p><strong>Your symptoms:</strong></p>

                <p>${data.symptoms}</p>

                <h3>Possible Conditions</h3>

                <ul>
                    ${data.possible_conditions
                        .map(condition => `<li>${condition}</li>`)
                        .join("")}
                </ul>

                <div class="medical-disclaimer">
                    ⚠️ ${data.disclaimer}
                </div>

            </div>
        `;

    } catch (error) {

        console.error(error);

        resultBox.innerHTML = `
            <div class="result-card">
                <h2>❌ Unable to analyze symptoms</h2>
                <p>
                    The medical service could not be reached.
                    Please try again.
                </p>
            </div>
        `;
    }
}

async function getMedicineInfo() {

    const value = document
        .getElementById("medicine-input")
        .value
        .trim();

    if (!value) {
        alert("Please enter a medicine name.");
        return;
    }

    const resultBox = document.getElementById("service-result");

    resultBox.innerHTML = `
        <div class="result-card">
            <h2>💊 Getting Medicine Information...</h2>
            <p>Please wait...</p>
        </div>
    `;

    try {

        const response = await fetch(
            `${API_URL}/medical/medicine?medicine=${encodeURIComponent(value)}`,
            {
                method: "POST"
            }
        );

        if (!response.ok) {
            throw new Error("Medicine API request failed");
        }

        const data = await response.json();

        resultBox.innerHTML = `
            <div class="result-card">

                <h2>💊 Medicine Information</h2>

                <h3>${data.medicine}</h3>

                ${
                    data.uses
                        ? `<p><strong>Uses:</strong><br>${data.uses}</p>`
                        : ""
                }

                ${
                    data.side_effects
                        ? `<p><strong>Possible Side Effects:</strong><br>${data.side_effects}</p>`
                        : ""
                }

                ${
                    data.precautions
                        ? `<p><strong>Precautions:</strong><br>${data.precautions}</p>`
                        : ""
                }

                ${
                    data.message
                        ? `<p>${data.message}</p>`
                        : ""
                }

                <div class="medical-disclaimer">
                    ⚠️ ${data.disclaimer}
                </div>

            </div>
        `;

    } catch (error) {

        console.error(error);

        resultBox.innerHTML = `
            <div class="result-card">
                <h2>❌ Unable to get medicine information</h2>
                <p>
                    The medicine service could not be reached.
                    Please try again.
                </p>
            </div>
        `;
    }
}


async function findHospitals() {

    const value = document
        .getElementById("hospital-input")
        .value
        .trim();

    if (!value) {
        alert("Please enter a city or location.");
        return;
    }

    const resultBox = document.getElementById("service-result");

    resultBox.innerHTML = `
        <div class="result-card">
            <h2>🏥 Searching Hospitals...</h2>
            <p>Please wait...</p>
        </div>
    `;

    try {

        const response = await fetch(
            `${API_URL}/medical/hospitals?city=${encodeURIComponent(value)}`,
            {
                method: "POST"
            }
        );

        if (!response.ok) {
            throw new Error("Hospital API request failed");
        }

        const data = await response.json();

        if (data.hospitals && data.hospitals.length > 0) {

            resultBox.innerHTML = `
                <div class="result-card">

                    <h2>🏥 Hospitals in ${data.city}</h2>

                    ${data.hospitals.map(hospital => `
                        <div class="hospital-item">
                            <h3>${hospital.name}</h3>
                            <p>📍 ${hospital.address}</p>
                        </div>
                    `).join("")}

                    <div class="medical-disclaimer">
                        ⚠️ ${data.disclaimer}
                    </div>

                </div>
            `;

        } else {

            resultBox.innerHTML = `
                <div class="result-card">

                    <h2>🏥 No Hospitals Found</h2>

                    <p>${data.message}</p>

                </div>
            `;
        }

    } catch (error) {

        console.error(error);

        resultBox.innerHTML = `
            <div class="result-card">

                <h2>❌ Unable to find hospitals</h2>

                <p>
                    The hospital service could not be reached.
                    Please try again.
                </p>

            </div>
        `;
    }
}


async function getMedicalKnowledge() {

    const value = document
        .getElementById("knowledge-input")
        .value
        .trim();

    if (!value) {
        alert("Please enter a medical topic.");
        return;
    }

    const resultBox = document.getElementById("service-result");

    resultBox.innerHTML = `
        <div class="result-card">
            <h2>📚 Loading Medical Knowledge...</h2>
            <p>Please wait...</p>
        </div>
    `;

    try {
        const response = await fetch(
            `${API_URL}/medical/knowledge?topic=${encodeURIComponent(value)}`,
            {
                method: "POST"
            }
        );

        if (!response.ok) {
            throw new Error("Failed to fetch medical knowledge");
        }

        const data = await response.json();

        resultBox.innerHTML = `
            <div class="result-card">
                <h2>📚 Medical Knowledge</h2>

                <p><strong>Topic:</strong> ${data.topic}</p>

                <p><strong>Definition:</strong><br>
                ${data.definition || data.message || "Not available"}
                </p>

                <p><strong>Causes:</strong><br>
                ${data.causes || "Not available"}
                </p>

                <p><strong>Symptoms:</strong><br>
                ${data.symptoms || "Not available"}
                </p>

                <p><strong>Prevention:</strong><br>
                ${data.prevention || "Not available"}
                </p>

                <div class="medical-disclaimer">
                    ⚠️ ${data.disclaimer || ""}
                </div>
            </div>
        `;

    } catch (error) {
        console.error(error);

        resultBox.innerHTML = `
            <div class="result-card">
                <h2>❌ Unable to load medical knowledge</h2>
                <p>The medical knowledge service could not be reached. Please try again.</p>
            </div>
        `;
    }
}


/* =========================
   NORMAL CHAT
========================= */

function showChat() {
    openChat();
}

function showProfile() {

    if (!currentUser) {
        showLogin();
        return;
    }

    chatBox.innerHTML = `
        <div class="settings-container">

            <h2>👤 Profile</h2>

            <div class="settings-item">
                <span>Username</span>
                <span>${currentUser.username}</span>
            </div>

            <div class="settings-item">
                <span>Email</span>
                <span>${currentUser.email}</span>
            </div>

        </div>
    `;
}

function openChat() {

    chatBox.innerHTML = `
        <div class="welcome">

            <div class="welcome-icon">🏥</div>

            <h1>Medical Assistant</h1>

            <p>
                Ask me a medical information question.
            </p>

        </div>
    `;

    input.focus();
}


function addMessage(sender, message) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        sender === "user"
            ? "user-message"
            : "bot-message"
    );

    const avatar = document.createElement("div");

    avatar.classList.add("avatar");

    avatar.textContent =
        sender === "user" ? "👤" : "🏥";

    const content = document.createElement("div");

    content.classList.add("message-content");

    const senderName = document.createElement("span");

    senderName.classList.add("sender");

    senderName.textContent =
        sender === "user"
            ? "You"
            : "Medical Assistant";

    const bubble = document.createElement("div");

    bubble.classList.add("bubble");

    bubble.textContent = message;

    content.appendChild(senderName);

    content.appendChild(bubble);

    messageDiv.appendChild(avatar);

    messageDiv.appendChild(content);

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function showTyping() {

    const typing = document.createElement("div");

    typing.id = "typing";

    typing.classList.add(
        "message",
        "bot-message"
    );

    typing.innerHTML = `
        <div class="avatar">🏥</div>

        <div class="message-content">

            <span class="sender">
                Medical Assistant
            </span>

            <div class="bubble">
                Typing...
            </div>

        </div>
    `;

    chatBox.appendChild(typing);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function removeTyping() {

    const typing =
        document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}


async function sendMessage() {

    const message = input.value.trim();

    if (!message) return;

    if (!currentUser) {
        showLogin();
        return;
    }

    addMessage("user", message);

    input.value = "";

    sendButton.disabled = true;

    showTyping();

    try {

        const response = await fetch(
    `${API_URL}/chat`,
    {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message,
            user_id: currentUser.user_id
        })
    }
);

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        removeTyping();

        addMessage(
            "bot",
            data.response
        );

    }

    catch (error) {

        removeTyping();

        addMessage(
            "bot",
            "Sorry, I couldn't connect to the medical assistant server."
        );

        console.error(error);

    }

    finally {

        sendButton.disabled = false;

        input.focus();

    }
}


/* =========================
   ENTER KEY
========================= */

if (input) {

    input.addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {

                event.preventDefault();

                sendMessage();

            }

        }
    );

}


/* =========================
   NEW CHAT
========================= */

const newChatButton =
    document.getElementById("new-chat");

if (newChatButton) {

    newChatButton.addEventListener(
        "click",
        function() {

            showMedicalHome();

            input.value = "";

        }
    );

}


/* =========================
   START
========================= */

function showLogin() {
    chatBox.innerHTML = `
        <div class="login-container">

            <div class="login-card">

                <div class="login-icon">
                    🏥
                </div>

                <h1 id="auth-title">Welcome Back</h1>

                <p class="login-description" id="auth-description">
                    Sign in to continue to Medical Assistant
                </p>

                <div id="register-fields" style="display: none;">

                    <input
                        type="text"
                        id="register-username"
                        placeholder="Username"
                        autocomplete="username"
                    >

                    <input
                        type="email"
                        id="register-email"
                        placeholder="Email"
                        autocomplete="email"
                    >

                    <input
                        type="password"
                        id="register-password"
                        placeholder="Password"
                        autocomplete="new-password"
                    >

                </div>

                <div id="login-fields">

                    <input
                        type="email"
                        id="login-email"
                        placeholder="Email"
                        autocomplete="email"
                    >

                    <input
                        type="password"
                        id="login-password"
                        placeholder="Password"
                        autocomplete="current-password"
                    >

                </div>

                <button id="auth-button" onclick="loginUser()">
                    Sign In
                </button>

                <p id="login-message"></p>

                <p class="auth-switch">
                    <span id="auth-switch-text">
                        Don't have an account?
                    </span>

                    <button
                        type="button"
                        onclick="toggleAuthMode()"
                        class="auth-switch-button"
                        id="auth-switch-button"
                    >
                        Register
                    </button>
                </p>

            </div>

        </div>
    `;
}
async function loginUser() {

    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    const message = document.getElementById("login-message");

    if (!email || !password) {
        message.textContent = "Please enter your email and password.";
        return;
    }

    try {

        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (data.success) {

            currentUser = data;

            message.textContent = "Login successful!";

            setTimeout(() => {
                showMedicalHome();
            }, 500);

        } else {

            message.textContent = data.message;

        }

    } catch (error) {

        console.error(error);

        message.textContent =
            "Unable to connect to the server.";

    }
}
async function showChatHistory() {

    if (!currentUser) {
        showLogin();
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/chat/history?user_id=${currentUser.user_id}`
        );

        const history = await response.json();

        chatBox.innerHTML = `
            <div class="history-container">

                <h2>🕘 Chat History</h2>

                ${
                    history.length === 0
                    ? `<p class="empty-history">
                        No chat history yet.
                       </p>`
                    : history.map(chat => `
                        <div class="history-item">

                            <div class="history-user">
                                You: ${chat.user_message}
                            </div>

                            <div class="history-bot">
                                Assistant: ${chat.bot_response}
                            </div>

                        </div>
                    `).join("")
                }

            </div>
        `;

    } catch (error) {

        console.error(error);

        chatBox.innerHTML = `
            <div class="history-container">
                <h2>🕘 Chat History</h2>
                <p>Unable to load chat history.</p>
            </div>
        `;
    }
}
function logoutUser() {

    currentUser = null;

    showLogin();
}
function showSettings() {

    chatBox.innerHTML = `
        <div class="settings-container">

            <h2>⚙️ Settings</h2>

            <div class="settings-item">
                <span>🌐 Language</span>
                <span>English</span>
            </div>

            <div class="settings-item">
                <span>🔔 Notifications</span>
                <span>On</span>
            </div>

            <div class="settings-item">
                <span>🏥 Medical Disclaimer</span>
                <span>Enabled</span>
            </div>

        </div>
    `;
}
/* =========================================================
   LIGHT / DARK MODE
========================================================= */

function toggleTheme() {

    document.body.classList.toggle("dark-mode");

    const themeButton = document.querySelector(
        '[onclick="toggleTheme()"]'
    );

    if (document.body.classList.contains("dark-mode")) {

        localStorage.setItem("theme", "dark");

        if (themeButton) {
            themeButton.innerHTML = "☀️ Light Mode";
        }

    } else {

        localStorage.setItem("theme", "light");

        if (themeButton) {
            themeButton.innerHTML = "🌙 Dark Mode";
        }
    }
}


/* Load saved theme */

function loadTheme() {

    const savedTheme = localStorage.getItem("theme");

    const themeButton = document.querySelector(
        '[onclick="toggleTheme()"]'
    );

    if (savedTheme === "dark") {

        document.body.classList.add("dark-mode");

        if (themeButton) {
            themeButton.innerHTML = "☀️ Light Mode";
        }

    } else {

        document.body.classList.remove("dark-mode");

        if (themeButton) {
            themeButton.innerHTML = "🌙 Dark Mode";
        }
    }
}


/* Run when page loads */

document.addEventListener("DOMContentLoaded", () => {
    loadTheme();
    showLogin();
});
function toggleAuthMode() {

    const title = document.getElementById("auth-title");
    const description = document.getElementById("auth-description");

    const loginFields = document.getElementById("login-fields");
    const registerFields = document.getElementById("register-fields");

    const authButton = document.getElementById("auth-button");

    const switchText = document.getElementById("auth-switch-text");
    const switchButton = document.getElementById("auth-switch-button");

    const isRegistering =
        registerFields.style.display === "none";

    if (isRegistering) {

        title.textContent = "Create Account";

        description.textContent =
            "Register to start using Medical Assistant";

        loginFields.style.display = "none";
        registerFields.style.display = "block";

        authButton.textContent = "Register";
        authButton.onclick = registerUser;

        switchText.textContent =
            "Already have an account?";

        switchButton.textContent = "Sign In";

    } else {

        title.textContent = "Welcome Back";

        description.textContent =
            "Sign in to continue to Medical Assistant";

        loginFields.style.display = "block";
        registerFields.style.display = "none";

        authButton.textContent = "Sign In";
        authButton.onclick = loginUser;

        switchText.textContent =
            "Don't have an account?";

        switchButton.textContent = "Register";
    }
}
async function registerUser() {

    const username = document.getElementById("register-username").value.trim();
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value;

    const message = document.getElementById("login-message");

    if (!username || !email || !password) {
        message.textContent = "Please fill in all fields.";
        return;
    }

    try {

        const response = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (data.success) {

            message.textContent = "Registration successful! Please sign in.";

            setTimeout(() => {
                toggleAuthMode();
            }, 1000);

        } else {

            message.textContent = data.message || "Registration failed.";
        }

    } catch (error) {

        console.error(error);

        message.textContent =
            "Unable to connect to the server.";
    }
}