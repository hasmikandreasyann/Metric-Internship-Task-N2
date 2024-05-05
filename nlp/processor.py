import spacy
import openai
import os
from dotenv import load_dotenv
import requests


def ask_gpt_chat(prompt, model="gpt-3.5-turbo", max_tokens=150):
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    intro = ("Extract the following information, from the scraped webpage provided below, return company name, "
             "contacts, industries that they invest in, investment rounds that they participated. "
             "Please reply only with one python dictionary with the extracted info.")
    if len(prompt) > 30000:
        prompt = prompt[:30000]
    prompt = intro + "\n" + prompt
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # This will throw an error for non-200 responses
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e}\nResponse: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request exception occurred: {e}"