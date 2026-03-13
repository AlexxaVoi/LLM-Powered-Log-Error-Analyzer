import httpx
import json
from app.constants import OLLAMA_URL


async def get_ai_analysis(log_text: str) -> dict:
    prompt = f"""
    Analyze these server error logs and provide a structured report in English.
    Logs content:
    {log_text}

    You must return ONLY a JSON object with exactly these three keys:
    "issue": "short title of the problem",
    "root_cause": "detailed explanation of why this happened",
    "solution": "step-by-step fix for this issue"
    """

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=60.0
            )
            response.raise_for_status()
            result_raw = response.json().get("response")
            return json.loads(result_raw)

        except Exception as e:
            return {
                "issue": "AI Analysis Failed",
                "root_cause": str(e),
                "solution": "Ensure Ollama server is running locally."
            }
