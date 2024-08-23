import os
from datetime import datetime

import streamlit as st

from lib import Config, ModelPresets, txt2img_generate

HF_TOKEN = None
FAL_KEY = None
# HF_TOKEN = os.environ.get("HF_TOKEN") or None
# FAL_KEY = os.environ.get("FAL_KEY") or None
API_URL = "https://api-inference.huggingface.co/models"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "X-Wait-For-Model": "true", "X-Use-Cache": "false"}
PRESET_MODEL = {
    "black-forest-labs/flux.1-dev": ModelPresets.FLUX_1_DEV,
    "black-forest-labs/flux.1-schnell": ModelPresets.FLUX_1_SCHNELL,
    "stabilityai/stable-diffusion-xl-base-1.0": ModelPresets.STABLE_DIFFUSION_XL,
}

# config
st.set_page_config(
    page_title=f"{Config.TITLE} | Text to Image",
    page_icon=Config.ICON,
    layout=Config.LAYOUT,
)

# initialize state
if "api_key_fal" not in st.session_state:
    st.session_state.api_key_fal = ""

if "api_key_huggingface" not in st.session_state:
    st.session_state.api_key_huggingface = ""

if "txt2img_messages" not in st.session_state:
    st.session_state.txt2img_messages = []

if "txt2img_running" not in st.session_state:
    st.session_state.txt2img_running = False

if "txt2img_seed" not in st.session_state:
    st.session_state.txt2img_seed = 0

# sidebar
st.logo("logo.svg")
st.sidebar.header("Settings")
service = st.sidebar.selectbox(
    "Service",
    options=["Huggingface"],
    index=0,
    disabled=st.session_state.txt2img_running,
)

if service == "Huggingface" and HF_TOKEN is None:
    st.session_state.api_key_huggingface = st.sidebar.text_input(
        "API Key",
        type="password",
        help="Cleared on page refresh",
        value=st.session_state.api_key_huggingface,
        disabled=st.session_state.txt2img_running,
    )
else:
    st.session_state.api_key_huggingface = st.session_state.api_key_huggingface

if service == "Fal" and FAL_KEY is None:
    st.session_state.api_key_fal = st.sidebar.text_input(
        "API Key",
        type="password",
        help="Cleared on page refresh",
        value=st.session_state.api_key_fal,
        disabled=st.session_state.txt2img_running,
    )
else:
    st.session_state.api_key_fal = st.session_state.api_key_fal

if service == "Huggingface" and HF_TOKEN is not None:
    st.session_state.api_key_huggingface = HF_TOKEN

if service == "Fal" and FAL_KEY is not None:
    st.session_state.api_key_fal = FAL_KEY

model = st.sidebar.selectbox(
    "Model",
    options=Config.TXT2IMG_MODELS,
    index=Config.TXT2IMG_DEFAULT_MODEL,
    disabled=st.session_state.txt2img_running,
    format_func=lambda x: x.split("/")[1],
)
aspect_ratio = st.sidebar.select_slider(
    "Aspect Ratio",
    options=list(Config.TXT2IMG_AR.keys()),
    value=Config.TXT2IMG_DEFAULT_AR,
    disabled=st.session_state.txt2img_running,
)

# heading
st.html("""
    <h1 style="padding: 0; margin-bottom: 0.5rem">Text to Image</h1>
    <p>Generate an image from a text prompt.</p>
""")

# build parameters from preset
parameters = {}
preset = PRESET_MODEL[model]
for param in preset["parameters"]:
    if param == "width":
        parameters[param] = Config.TXT2IMG_AR[aspect_ratio][0]
    if param == "height":
        parameters[param] = Config.TXT2IMG_AR[aspect_ratio][1]
    if param == "guidance_scale":
        parameters[param] = st.sidebar.slider(
            "Guidance Scale",
            preset["guidance_scale_min"],
            preset["guidance_scale_max"],
            preset["guidance_scale"],
            0.1,
            disabled=st.session_state.txt2img_running,
        )
    if param == "num_inference_steps":
        parameters[param] = st.sidebar.slider(
            "Inference Steps",
            preset["num_inference_steps_min"],
            preset["num_inference_steps_max"],
            preset["num_inference_steps"],
            1,
            disabled=st.session_state.txt2img_running,
        )
    if param == "seed":
        parameters[param] = st.sidebar.number_input(
            "Seed",
            min_value=-1,
            max_value=(1 << 53) - 1,
            value=-1,
            disabled=st.session_state.txt2img_running,
        )
    if param == "negative_prompt":
        parameters[param] = st.sidebar.text_area(
            label="Negative Prompt",
            value=Config.TXT2IMG_NEGATIVE_PROMPT,
            disabled=st.session_state.txt2img_running,
        )

# wrap the prompt in an expander to display additional parameters
for message in st.session_state.txt2img_messages:
    role = message["role"]
    with st.chat_message(role):
        image_container = st.empty()

        with image_container.container():
            if role == "user":
                with st.expander(message["content"]):
                    # build a markdown string for additional parameters
                    st.html("""
                    <style>
                        div[data-testid="stMarkdownContainer"] p:not(:last-of-type) { margin-bottom: 0 }
                    </style>
                    """)
                    md = f"`model`: {message['model']}\n\n"
                    md += "\n\n".join([f"`{k}`: {v}" for k, v in message["parameters"].items()])
                    st.markdown(md)

            if role == "assistant":
                # image is full width when _not_ in full-screen mode
                st.html("""
                <style>
                    div[data-testid="stImage"]:has(img[style*="max-width: 100%"]) {
                        height: auto;
                        max-width: 512px;
                    }
                    div[data-testid="stImage"] img[style*="max-width: 100%"] {
                        border-radius: 8px;
                    }
                </style>
                """)
                st.write(message["content"])  # success will be image, error will be text

# button row
if st.session_state.txt2img_messages:
    button_container = st.empty()
    with button_container.container():
        # https://discuss.streamlit.io/t/st-button-in-one-line/25966/6
        st.html("""
        <style>
            div[data-testid="column"] {
                width: fit-content;
                min-width: 0;
                flex: none;
            }
        </style>
        """)

        # retry
        col1, col2 = st.columns(2)
        with col1:
            if (
                st.button("❌", help="Delete last generation", disabled=st.session_state.txt2img_running)
                and len(st.session_state.txt2img_messages) >= 2
            ):
                st.session_state.txt2img_messages.pop()
                st.session_state.txt2img_messages.pop()
                st.rerun()

        with col2:
            if st.button("🗑️", help="Clear all generations", disabled=st.session_state.txt2img_running):
                st.session_state.txt2img_messages = []
                st.session_state.txt2img_seed = 0
                st.rerun()
else:
    button_container = None

# show the prompt and spinner while loading then update state and re-render
if prompt := st.chat_input(
    "What do you want to see?",
    on_submit=lambda: setattr(st.session_state, "txt2img_running", True),
):
    if "seed" in parameters and parameters["seed"] >= 0:
        st.session_state.txt2img_seed = parameters["seed"]
    else:
        st.session_state.txt2img_seed = int(datetime.now().timestamp() * 1e6) % (1 << 53)
        if "seed" in parameters:
            parameters["seed"] = st.session_state.txt2img_seed

    if button_container:
        button_container.empty()

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Running..."):
            if preset.get("kwargs") is not None:
                parameters.update(preset["kwargs"])
            api_key = getattr(st.session_state, f"api_key_{service.lower()}", None)
            image = txt2img_generate(api_key, service, model, prompt, parameters)
        st.session_state.txt2img_running = False

    model_name = PRESET_MODEL[model]["name"]
    st.session_state.txt2img_messages.append(
        {"role": "user", "content": prompt, "parameters": parameters, "model": model_name}
    )
    st.session_state.txt2img_messages.append({"role": "assistant", "content": image})
    st.rerun()
