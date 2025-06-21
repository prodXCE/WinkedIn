# WinkedIn: Your AI-Powered Career Assistant

**Status: Phase 1 Complete**

WinkedIn is a Python-based automation tool designed to streamline and enhance your job search and networking efforts on LinkedIn. By leveraging browser automation and artificial intelligence, this assistant helps you find relevant job opportunities and craft personalized connection requests to key people, such as recruiters and hiring managers.

This project is currently in active development. This README reflects the features and functionality completed in Phase 1.

---

## Features (Phase 1)

* **Secure Login:** Safely logs into your LinkedIn account without storing your password in plain text.
* **Dynamic Job Search:** Search for job listings on LinkedIn using keywords (e.g., "Software Engineer") and location.
* **Contact Discovery:** After selecting a job, search for relevant contacts (e.g., "Recruiter") within that specific company.
* **AI-Powered Message Generation:** Utilizes the Gemini API to generate professional, context-aware connection messages tailored to the job and company you're targeting.
* **Interactive Message Editor:** Review, edit, or regenerate the AI-crafted message before it gets sent.
* **Automated Connection Request:** Sends the connection request along with your custom message to the selected person.
* **Command-Line Interface:** A user-friendly, menu-driven interface to guide you through the process.

---

## Technology Stack

* **Python 3:** The core programming language.
* **Selenium:** For browser automation and web scraping.
* **webdriver-manager:** To automatically manage the browser driver, removing manual setup.
* **Requests:** For making efficient API calls to the AI model.
* **Google Gemini:** The AI model used for generating personalized messages.

---

## Setup and Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

* Python 3.8 or newer.
* Google Chrome browser installed.

### 1. Clone the Repository

First, clone the project repository from GitHub to your local machine.

```bash
git clone https://github.com/prodXCE/WinkedIn.git
cd WinkedIn
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Your Email (Optional)

You can pre-fill your LinkedIn email address for convenience.
1.  Open the `config.py` file.
2.  Change the `LINKEDIN_EMAIL` variable to your email:
    ```python
    LINKEDIN_EMAIL = "your.email@example.com"
    ```
If you leave it blank, the script will prompt you for your email every time it runs.

---

## How to Run the Application

Once you have completed the setup, you can run the application with a single command from the project's root directory.

```bash
python main.py
```

The script will launch, and you can follow the interactive menu prompts in your terminal. A Chrome browser window will open to perform the automation tasks.

---

## ⚠️ Disclaimer

This tool is intended for personal use to assist with the job application process. Automating actions on social media platforms can be against their Terms of Service. Use this tool responsibly and ethically. Overuse may lead to your LinkedIn account being flagged or restricted. The developers of this project are not responsible for any consequences of its use.

---

## Future Work (Upcoming Phases)

* **Phase 2: Deep Personalization:** Add features to "warm up" contacts by liking their posts and further personalizing messages based on their profile content.
* **Phase 3: Organization & Follow-Up:** Implement a job application tracker and an automated follow-up system.
* **Phase 4: Advanced Analysis & GUI:** Build a job-to-skill matching engine and a full graphical user interface (GUI).
