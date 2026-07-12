from ollama import Client


class LLMClient:
    """
    Handles communication with a local Ollama server.
    """

    def __init__(
        self,
        model: str = "qwen3:8b",
        host: str = "http://localhost:11434",
    ):

        self.model = model
        self.client = Client(host=host)

    def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.2,
    ) -> str:
        """
        Generate a response from the local LLM.
        """

        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            system=system,
            options={
                "temperature": temperature,
                "num_gpu": 0,
            },
        )

        return response["response"]

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.2,
    ) -> str:
        """
        Chat API (better for multi-turn conversations).
        """

        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature,
            },
        )

        return response["message"]["content"]

    def change_model(self, model: str):

        self.model = model

    def list_models(self):

        return self.client.list()

    def ping(self) -> bool:

        try:
            self.client.list()
            return True
        except Exception:
            return False