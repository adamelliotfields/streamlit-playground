import base64
import io

import httpx
import streamlit as st
from openai import APIError, OpenAI
from PIL import Image

from .config import Config


def txt2txt_generate(api_key, service, model, parameters, **kwargs):
    base_url = Config.SERVICES[service]
    if service == "Hugging Face":
        base_url = f"{base_url}/{model}/v1"
    client = OpenAI(api_key=api_key, base_url=base_url)

    try:
        stream = client.chat.completions.create(stream=True, model=model, **parameters, **kwargs)
        return st.write_stream(stream)
    except APIError as e:
        # OpenAI uses this message for streaming errors and attaches response.error to error.body
        return e.body if e.message == "An error occurred during streaming" else e.message
    except Exception as e:
        return str(e)


def txt2img_generate(api_key, service, model, inputs, parameters, **kwargs):
    headers = {}
    if service == "Hugging Face":
        headers["Authorization"] = f"Bearer {api_key}"
        headers["X-Wait-For-Model"] = "true"
        headers["X-Use-Cache"] = "false"
    if service == "Fal":
        headers["Authorization"] = f"Key {api_key}"

    json = {}
    if service == "Hugging Face":
        json = {
            "inputs": inputs,
            "parameters": {**parameters, **kwargs},
        }
    if service == "Fal":
        json = {**parameters, **kwargs}
        json["prompt"] = inputs

    base_url = f"{Config.SERVICES[service]}/{model}"

    try:
        response = httpx.post(base_url, headers=headers, json=json, timeout=Config.TXT2IMG_TIMEOUT)
        if response.status_code // 100 == 2:  # 2xx
            if service == "Hugging Face":
                return Image.open(io.BytesIO(response.content))
            if service == "Fal":
                # sync_mode means wait for image base64 instead of CDN link
                if parameters.get("sync_mode", True):
                    bytes = base64.b64decode(response.json()["images"][0]["url"].split(",")[-1])
                    return Image.open(io.BytesIO(bytes))
                else:
                    url = response.json()["images"][0]["url"]
                    image = httpx.get(url, headers=headers, timeout=Config.TXT2IMG_TIMEOUT)
                    return Image.open(io.BytesIO(image.content))
        else:
            return f"Error: {response.status_code} {response.text}"
    except Exception as e:
        return str(e)
