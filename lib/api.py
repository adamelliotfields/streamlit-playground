import io

import requests
import streamlit as st
from openai import APIError, OpenAI
from PIL import Image

from .config import Config


def txt2txt_generate(api_key, service, model, parameters, **kwargs):
    base_url = Config.SERVICES[service]
    if service == "Huggingface":
        base_url = f"{base_url}/{model}/v1"
    client = OpenAI(api_key=api_key, base_url=base_url)

    try:
        stream = client.chat.completions.create(stream=True, model=model, **parameters, **kwargs)
        return st.write_stream(stream)
    except APIError as e:
        return e.message
    except Exception as e:
        return str(e)


def txt2img_generate(api_key, service, model, inputs, parameters, **kwargs):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Wait-For-Model": "true",
        "X-Use-Cache": "false",
    }
    base_url = f"{Config.SERVICES[service]}/{model}"

    try:
        response = requests.post(
            base_url,
            headers=headers,
            json={
                "inputs": inputs,
                "parameters": {**parameters, **kwargs},
            },
        )
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return str(e)
