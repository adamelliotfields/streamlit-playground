import io
from abc import ABC, abstractmethod

import requests
import streamlit as st
from openai import APIError, OpenAI
from PIL import Image


class Txt2TxtAPI(ABC):
    @abstractmethod
    def generate_text(self, model, parameters, **kwargs):
        pass


class Txt2ImgAPI(ABC):
    @abstractmethod
    def generate_image(self, model, prompt, parameters, **kwargs):
        pass


class HuggingFaceTxt2TxtAPI(Txt2TxtAPI):
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_text(self, model, parameters, **kwargs):
        if not self.api_key:
            return "API Key is required."
        client = OpenAI(
            api_key=self.api_key,
            base_url=f"https://api-inference.huggingface.co/models/{model}/v1",
        )
        try:
            stream = client.chat.completions.create(stream=True, model=model, **parameters, **kwargs)
            return st.write_stream(stream)
        except APIError as e:
            return e.message
        except Exception as e:
            return str(e)


class PerplexityTxt2TxtAPI(Txt2TxtAPI):
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_text(self, model, parameters, **kwargs):
        if not self.api_key:
            return "API Key is required."
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.perplexity.ai",
        )
        try:
            stream = client.chat.completions.create(stream=True, model=model, **parameters, **kwargs)
            return st.write_stream(stream)
        except APIError as e:
            return e.message
        except Exception as e:
            return str(e)


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
