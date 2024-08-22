import io
from abc import ABC, abstractmethod

import requests
from PIL import Image


class Txt2ImgAPI(ABC):
    @abstractmethod
    def generate_image(self, model, prompt, parameters, **kwargs):
        pass


# essentially the same as huggingface_hub's inference client
class HuggingFaceTxt2ImgAPI(Txt2ImgAPI):
    def __init__(self, token):
        self.api_url = "https://api-inference.huggingface.co/models"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "X-Wait-For-Model": "true",
            "X-Use-Cache": "false",
        }

    def generate_image(self, model, prompt, parameters, **kwargs):
        try:
            response = requests.post(
                f"{self.api_url}/{model}",
                headers=self.headers,
                json={
                    "inputs": prompt,
                    "parameters": {**parameters, **kwargs},
                },
            )
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
            else:
                raise Exception(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            return str(e)
