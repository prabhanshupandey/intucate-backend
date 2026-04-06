import requests
from app.config import OPENROUTER_API_KEY

def get_ai_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",   # required
        "X-Title": "My Flask App"
    }

    data = {
        "model": "openrouter/auto",   # 🔥 SAME AS YOUR WORKING NODE CODE
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    print("FULL RESPONSE:", result)

    if "choices" not in result:
        return f"API Error: {result}"

    return result["choices"][0]["message"]["content"]