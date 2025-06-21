import os
import requests

def generate_referral_message(job_title, company_name):
    """
    Generates a personalized referral message using the Gemini AI model.

    Args:
        job_title (str): The title of the job the user is intereseted in
        company_name (str): The name of the company

    Returns:
        str: A personalized, AI-generated message.
    """

    print(f"\n Generating a personalized referral request for a '{job_title}' role at '{company_name}'...")

    api_key = os.getenv("API_KEY", "")

    if not api_key:
        print("Warning: API Key not found. Using a default template.")
        return(f"Hi! I'm very interested in the {job_title} position at {company_name}."
               "I saw that you work there and would be grateful for the opportunity to connect. Thank you!")

    api_url =  f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    prompt = (f"Write a short, professional, and friendly LinkedIn connection request message. "
                  f"The goal is to ask for a referral for a '{job_title}' position at '{company_name}'. "
                  f"Keep it concise (under 300 characters), professional, and approachable. "
                  f"Do not use placeholders like '[Your Name]' or '[Their Name]'.")

    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()

        response_json = response.json()

        if (response_json.get("candidates") and
            response_json["candidates"][0].get("content") and
            response_json["candidates"][0]["content"].get("parts")):

            generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            print("✅ AI message generated successfully.")
            return generated_text.strip()
        else:
            print("❌ AI response was not in the expected format. Using default message.")
            return (f"Hi! I am very interested in the {job_title} position at {company_name}. "
                            "I would be grateful for the opportunity to connect. Thank you!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error calling AI model: {e}")
        print("Falling back to a default message.")
        return (f"Hi! I am very interested in the {job_title} position at {company_name}. "
                "I would be grateful for the opportunity to connect. Thank you!")
