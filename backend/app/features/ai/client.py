import asyncio

from google import genai
from google.genai import types

from app.features.ai.prompts import SYSTEM_INSTRUCTION


class GeminiClient:
    def __init__(
        self,
        api_key: str,
        model: str,
        timeout_seconds: float = 5.0
    ):
        if not api_key or api_key == "YOUR_API_KEY":
            raise ValueError("Gemini API key is missing.")

        if timeout_seconds <= 0:
            raise ValueError("Timeout must be positive.")

        self.api_key = api_key
        self.model = model
        self.timeout_seconds = timeout_seconds

    async def generate(self, prompt: str) -> str:
        return await asyncio.wait_for(
            self._generate_content(prompt),
            timeout=self.timeout_seconds
        )

    async def _generate_content(self, prompt: str) -> str:
        async with genai.Client(
            api_key=self.api_key,
            http_options=types.HttpOptions(
                timeout=max(10000, int(self.timeout_seconds * 1000))
            )
        ).aio as client:

            response = await client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.2,
                    max_output_tokens=512
                )
            )

            if not response.candidates:
                raise RuntimeError("Gemini returned no candidates.")

            if response.candidates[0].finish_reason != (types.FinishReason.STOP):
                raise RuntimeError("Gemini returned an incomplete response.")

            text = (response.text or "").strip()

            if not text:
                raise RuntimeError("Gemini returned an empty response.")

            return text
