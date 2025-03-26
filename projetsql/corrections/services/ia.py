import requests
from django.conf import settings

class DeepSeekService:
    @staticmethod
    def generate_feedback(prompt: str) -> dict:
        headers = {"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"}
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            headers=headers
        )
        return response.json()

class OllamaService:
    @staticmethod
    def generate_feedback(prompt: str, model: str = "llama3") -> dict:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()