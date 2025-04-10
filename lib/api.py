import time
from io import BytesIO

import httpx
import streamlit as st
from anthropic import Anthropic
from anthropic import APIError as AnthropicAPIError
from openai import APIError as OpenAIAPIError
from openai import OpenAI
from PIL import Image

from .config import config
from .util import base64_decode_image_data_url


def txt2txt_generate(api_key, provider, parameters, **kwargs):
    model = parameters.get("model", "")
    base_url = config.providers[provider].url

    if provider == "hf":
        base_url = f"{base_url}/{model}/v1"

    try:
        if provider == "anthropic":
            client = Anthropic(api_key=api_key)
            with client.messages.stream(**parameters, **kwargs) as stream:
                return st.write_stream(stream.text_stream)
        else:
            client = OpenAI(api_key=api_key, base_url=base_url)
            stream = client.chat.completions.create(stream=True, **parameters, **kwargs)
            return st.write_stream(stream)
    except AnthropicAPIError as e:
        return e.message
    except OpenAIAPIError as e:
        # OpenAI uses this message for streaming errors and attaches response.error to error.body
        # https://github.com/openai/openai-python/blob/v1.0.0/src/openai/_streaming.py#L59
        return e.body if e.message == "An error occurred during streaming" else e.message
    except Exception as e:
        return str(e)


def txt2img_generate(api_key, provider, model, inputs, parameters, **kwargs):
    headers = {}
    json = {**parameters, **kwargs}

    if provider == "bfl":
        headers["x-key"] = api_key
        json["prompt"] = inputs

    if provider == "fal":
        headers["Authorization"] = f"Key {api_key}"
        json["prompt"] = inputs

    if provider == "hf":
        headers["Authorization"] = f"Bearer {api_key}"
        headers["X-Wait-For-Model"] = "true"
        headers["X-Use-Cache"] = "false"
        json = {
            "inputs": inputs,
            "parameters": {**parameters, **kwargs},
        }

    if provider == "together":
        headers["Authorization"] = f"Bearer {api_key}"
        json["prompt"] = inputs

    base_url = config.providers[provider].url

    if provider not in ["together"]:
        base_url = f"{base_url}/{model}"

    try:
        timeout = config.timeout
        response = httpx.post(base_url, headers=headers, json=json, timeout=timeout)

        if response.status_code // 100 == 2:  # 2xx
            # BFL is async so we need to poll for result
            # https://api.bfl.ml/docs
            if provider == "bfl":
                id = response.json()["id"]
                url = f"{config.providers[provider].url}/get_result?id={id}"

                retries = 0
                while retries < timeout:
                    response = httpx.get(url, timeout=timeout)
                    if response.status_code // 100 != 2:
                        return f"Error: {response.status_code} {response.text}"

                    if response.json()["status"] == "Ready":
                        image = httpx.get(
                            response.json()["result"]["sample"],
                            headers=headers,
                            timeout=timeout,
                        )
                        return Image.open(BytesIO(image.content))

                    retries += 1
                    time.sleep(1)

                return "Error: API timeout"

            if provider == "fal":
                # Sync mode means wait for image base64 string instead of CDN link
                url = response.json()["images"][0]["url"]
                if parameters.get("sync_mode", True):
                    return base64_decode_image_data_url(url)
                else:
                    image = httpx.get(url, headers=headers, timeout=timeout)
                    return Image.open(BytesIO(image.content))

            if provider == "hf":
                return Image.open(BytesIO(response.content))

            if provider == "together":
                url = response.json()["data"][0]["url"]
                image = httpx.get(url, headers=headers, timeout=timeout)
                return Image.open(BytesIO(image.content))

        else:
            return f"Error: {response.status_code} {response.text}"
    except Exception as e:
        return str(e)
