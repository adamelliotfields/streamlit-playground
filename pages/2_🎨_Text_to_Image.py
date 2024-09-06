import os
from datetime import datetime

import streamlit as st

from lib import Config, ModelPresets, txt2img_generate

SERVICE_SESSION = {
    "Fal": "api_key_fal",
    "Hugging Face": "api_key_hugging_face",
}

SESSION_TOKEN = {
    "api_key_fal": os.environ.get("FAL_KEY") or None,
    "api_key_hugging_face": os.environ.get("HF_TOKEN") or None,
}

PRESET_MODEL = {
    "black-forest-labs/flux.1-dev": ModelPresets.FLUX_DEV,
    "black-forest-labs/flux.1-schnell": ModelPresets.FLUX_SCHNELL,
    "stabilityai/stable-diffusion-xl-base-1.0": ModelPresets.STABLE_DIFFUSION_XL,
    "fal-ai/aura-flow": ModelPresets.AURA_FLOW,
    "fal-ai/flux-pro": ModelPresets.FLUX_PRO,
    "fal-ai/fooocus": ModelPresets.FOOOCUS,
    "fal-ai/kolors": ModelPresets.KOLORS,
    "fal-ai/stable-diffusion-v3-medium": ModelPresets.STABLE_DIFFUSION_3,
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

if "api_key_hugging_face" not in st.session_state:
    st.session_state.api_key_hugging_face = ""

if "running" not in st.session_state:
    st.session_state.running = False

if "txt2img_messages" not in st.session_state:
    st.session_state.txt2img_messages = []

if "txt2img_seed" not in st.session_state:
    st.session_state.txt2img_seed = 0

# sidebar
st.logo("logo.svg")
st.sidebar.header("Settings")
service = st.sidebar.selectbox(
    "Service",
    options=list(SERVICE_SESSION.keys()),
    index=1,
    disabled=st.session_state.running,
)

# disable API key input and hide value if set by environment variable (handle empty string value later)
for display_name, session_key in SERVICE_SESSION.items():
    if service == display_name:
        st.session_state[session_key] = st.sidebar.text_input(
            "API Key",
            type="password",
            value="" if SESSION_TOKEN[session_key] else st.session_state[session_key],
            disabled=bool(SESSION_TOKEN[session_key]) or st.session_state.running,
            help="Set by environment variable" if SESSION_TOKEN[session_key] else "Cleared on page refresh",
        )

model = st.sidebar.selectbox(
    "Model",
    options=Config.TXT2IMG_MODELS[service],
    index=Config.TXT2IMG_DEFAULT_MODEL[service],
    disabled=st.session_state.running,
    format_func=lambda x: x.split("/")[1],
)

# heading
st.html("""
    <h1>Text to Image</h1>
    <p>Generate an image from a text prompt.</p>
""")

# build parameters from preset
parameters = {}
preset = PRESET_MODEL[model]
for param in preset["parameters"]:
    if param == "seed":
        parameters[param] = st.sidebar.number_input(
            "Seed",
            min_value=-1,
            max_value=(1 << 53) - 1,
            value=-1,
            disabled=st.session_state.running,
        )
    if param == "negative_prompt":
        parameters[param] = st.sidebar.text_area(
            "Negative Prompt",
            value=Config.TXT2IMG_NEGATIVE_PROMPT,
            disabled=st.session_state.running,
        )
    if param == "width":
        parameters[param] = st.sidebar.slider(
            "Width",
            step=64,
            value=1024,
            min_value=512,
            max_value=2048,
            disabled=st.session_state.running,
        )
    if param == "height":
        parameters[param] = st.sidebar.slider(
            "Height",
            step=64,
            value=1024,
            min_value=512,
            max_value=2048,
            disabled=st.session_state.running,
        )
    if param == "image_size":
        parameters[param] = st.sidebar.select_slider(
            "Image Size",
            options=Config.TXT2IMG_IMAGE_SIZES,
            value=Config.TXT2IMG_DEFAULT_IMAGE_SIZE,
            disabled=st.session_state.running,
        )
    if param == "aspect_ratio":
        parameters[param] = st.sidebar.select_slider(
            "Aspect Ratio",
            options=Config.TXT2IMG_ASPECT_RATIOS,
            value=Config.TXT2IMG_DEFAULT_ASPECT_RATIO,
            disabled=st.session_state.running,
        )
    if param == "guidance_scale":
        parameters[param] = st.sidebar.slider(
            "Guidance Scale",
            preset["guidance_scale_min"],
            preset["guidance_scale_max"],
            preset["guidance_scale"],
            0.1,
            disabled=st.session_state.running,
        )
    if param == "num_inference_steps":
        parameters[param] = st.sidebar.slider(
            "Inference Steps",
            preset["num_inference_steps_min"],
            preset["num_inference_steps_max"],
            preset["num_inference_steps"],
            1,
            disabled=st.session_state.running,
        )
    if param == "expand_prompt":
        parameters[param] = st.sidebar.checkbox(
            "Expand Prompt",
            value=False,
            disabled=st.session_state.running,
        )
    if param == "prompt_expansion":
        parameters[param] = st.sidebar.checkbox(
            "Prompt Expansion",
            value=False,
            disabled=st.session_state.running,
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
                    filtered_parameters = [
                        f"`{k}`: {v}"
                        for k, v in message["parameters"].items()
                        if k not in Config.TXT2IMG_HIDDEN_PARAMETERS
                    ]
                    st.markdown(f"`model`: {message['model']}\n\n" + "\n\n".join(filtered_parameters))

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

        col1, col2 = st.columns(2)
        with col1:
            if (
                st.button("❌", help="Delete last generation", disabled=st.session_state.running)
                and len(st.session_state.txt2img_messages) >= 2
            ):
                st.session_state.txt2img_messages.pop()
                st.session_state.txt2img_messages.pop()
                st.rerun()

        with col2:
            if st.button("🗑️", help="Clear all generations", disabled=st.session_state.running):
                st.session_state.txt2img_messages = []
                st.session_state.txt2img_seed = 0
                st.rerun()
else:
    button_container = None

# show the prompt and spinner while loading then update state and re-render
if prompt := st.chat_input(
    "What do you want to see?",
    on_submit=lambda: setattr(st.session_state, "running", True),
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
            session_key = f"api_key_{service.lower().replace(' ', '_')}"
            api_key = st.session_state[session_key] or SESSION_TOKEN[session_key]
            image = txt2img_generate(api_key, service, model, prompt, parameters)
        st.session_state.running = False

    model_name = PRESET_MODEL[model]["name"]
    st.session_state.txt2img_messages.append(
        {"role": "user", "content": prompt, "parameters": parameters, "model": model_name}
    )
    st.session_state.txt2img_messages.append({"role": "assistant", "content": image})
    st.rerun()
