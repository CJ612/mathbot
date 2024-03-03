from openai import OpenAI
from config import TOKEN_OPENAI

client = OpenAI(api_key = TOKEN_OPENAI)

class TestAi():
    def __init__(self, prompt: str) -> None:
        self.prompt = prompt

    def generate_ai_image(self) -> str:
        img = client.images.generate(
            model="dall-e-3",
            prompt=self.prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return img.data[0].url 