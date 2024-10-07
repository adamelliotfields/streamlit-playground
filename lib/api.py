import base64
import io
import time

import httpx
import streamlit as st
from openai import APIError, OpenAI
from PIL import Image

from .config import config


def txt2txt_generate(api_key, service, model, parameters, **kwargs):
    base_url = config.services[service]
    if service == "Hugging Face":
        base_url = f"{base_url}/{model}/v1"
    client = OpenAI(api_key=api_key, base_url=base_url)

    try:
        stream = client.chat.completions.create(stream=True, model=model, **parameters, **kwargs)
        return st.write_stream(stream)
    except APIError as e:
        # OpenAI uses this message for streaming errors and attaches response.error to error.body
        # https://github.com/openai/openai-python/blob/v1.0.0/src/openai/_streaming.py#L59
        return e.body if e.message == "An error occurred during streaming" else e.message
    except Exception as e:
        return str(e)


def txt2img_generate(api_key, service, model, inputs, parameters, **kwargs):
    headers = {}
    if service == "Black Forest Labs":
        headers["x-key"] = api_key

    if service == "Fal":
        headers["Authorization"] = f"Key {api_key}"

    if service == "Hugging Face":
        headers["Authorization"] = f"Bearer {api_key}"
        headers["X-Wait-For-Model"] = "true"
        headers["X-Use-Cache"] = "false"

    if service == "Together":
        headers["Authorization"] = f"Bearer {api_key}"

    json = {}
    if service == "Black Forest Labs":
        json = {**parameters, **kwargs}
        json["prompt"] = inputs

    if service == "Fal":
        json = {**parameters, **kwargs}
        json["prompt"] = inputs

    if service == "Hugging Face":
        json = {
            "inputs": inputs,
            "parameters": {**parameters, **kwargs},
        }

    if service == "Together":
        json = {**parameters, **kwargs}
        json["prompt"] = inputs

    base_url = config.services[service]

    if service not in ["Together"]:
        base_url = f"{base_url}/{model}"

    try:
        response = httpx.post(base_url, headers=headers, json=json, timeout=config.txt2img.timeout)
        if response.status_code // 100 == 2:  # 2xx
            # BFL is async so we need to poll for result
            # https://api.bfl.ml/docs
            if service == "Black Forest Labs":
                id = response.json()["id"]
                url = f"{config.services[service]}/get_result?id={id}"

                retries = 0
                while retries < config.txt2img.timeout:
                    response = httpx.get(url, timeout=config.txt2img.timeout)
                    if response.status_code // 100 != 2:
                        return f"Error: {response.status_code} {response.text}"

                    if response.json()["status"] == "Ready":
                        image = httpx.get(
                            response.json()["result"]["sample"],
                            headers=headers,
                            timeout=config.txt2img.timeout,
                        )
                        return Image.open(io.BytesIO(image.content))

                    retries += 1
                    time.sleep(1)

                return "Error: API timeout"

            if service == "Fal":
                # Sync mode means wait for image base64 string instead of CDN link
                if parameters.get("sync_mode", True):
                    bytes = base64.b64decode(response.json()["images"][0]["url"].split(",")[-1])
                    return Image.open(io.BytesIO(bytes))
                else:
                    url = response.json()["images"][0]["url"]
                    image = httpx.get(url, headers=headers, timeout=config.txt2img.timeout)
                    return Image.open(io.BytesIO(image.content))

            if service == "Hugging Face":
                return Image.open(io.BytesIO(response.content))

            if service == "Together":
                url = response.json()["data"][0]["url"]
                image = httpx.get(url, headers=headers, timeout=config.txt2img.timeout)
                return Image.open(io.BytesIO(image.content))

        else:
            return f"Error: {response.status_code} {response.text}"
    except Exception as e:
        return str(e)
