from __future__ import annotations

import httpx

from app.config import Settings, settings


class LocalLLMClient:
    def __init__(self, config: Settings = settings) -> None:
        self.config = config

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        url = f"{self.config.llm_base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.llm_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.config.llm_model,
            "messages": messages,
            "temperature": self.config.llm_temperature
            if temperature is None
            else temperature,
            "max_tokens": self.config.llm_max_tokens
            if max_tokens is None
            else max_tokens,
        }

        with httpx.Client(timeout=self.config.llm_timeout_seconds) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def health(self) -> bool:
        url = f"{self.config.llm_base_url.rstrip('/')}/models"
        headers = {"Authorization": f"Bearer {self.config.llm_api_key}"}
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
        except httpx.HTTPError:
            return False
        return True
