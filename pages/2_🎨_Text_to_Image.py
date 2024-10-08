from datetime import datetime
from typing import Dict

import streamlit as st

from lib import Txt2ImgPreset, config, preset, txt2img_generate

st.set_page_config(
    page_title=f"{config.title} | Text to Image",
    page_icon=config.logo,
    layout=config.layout,
)

# Initialize Streamlit session state
if "api_key_bfl" not in st.session_state:
    st.session_state.api_key_bfl = ""

if "api_key_fal" not in st.session_state:
    st.session_state.api_key_fal = ""

if "api_key_hf" not in st.session_state:
    st.session_state.api_key_hf = ""

if "api_key_together" not in st.session_state:
    st.session_state.api_key_together = ""

if "running" not in st.session_state:
    st.session_state.running = False

if "txt2img_messages" not in st.session_state:
    st.session_state.txt2img_messages = []

if "txt2img_seed" not in st.session_state:
    st.session_state.txt2img_seed = 0

st.logo(config.logo)
st.sidebar.header("Settings")

service = st.sidebar.selectbox(
    "Service",
    options=preset.txt2img.keys(),
    format_func=lambda x: config.service[x].name,
    disabled=st.session_state.running,
)

# Show the API key input for the selected service.
# Disable and hide value if set by environment variable; handle empty string value later.
# for display_name, session_key in SERVICE_SESSION.items():
for service_id in config.service.keys():
    if service == service_id:
        session_key = f"api_key_{service}"
        api_key = config.service[service].api_key
        st.session_state[session_key] = st.sidebar.text_input(
            "API Key",
            type="password",
            value="" if api_key else st.session_state[session_key],
            disabled=bool(api_key) or st.session_state.running,
            help="Set by environment variable" if api_key else "Cleared on page refresh",
        )

service_preset: Dict[str, Txt2ImgPreset] = preset.txt2img[service]

model = st.sidebar.selectbox(
    "Model",
    options=service_preset.keys(),
    format_func=lambda x: service_preset[x].name,
    disabled=st.session_state.running,
)

model_preset = service_preset[model]

# heading
st.html("""
    <h1>Text to Image</h1>
    <p>Generate an image from a text prompt.</p>
""")

# Build parameters from preset by rendering the appropriate input widgets
parameters = {}
for param in model_preset.parameters:
    if param == "model":
        parameters[param] = model
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
            value=config.txt2img.negative_prompt,
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
            options=config.txt2img.image_sizes,
            value=config.txt2img.default_image_size,
            disabled=st.session_state.running,
        )
    if param == "aspect_ratio":
        parameters[param] = st.sidebar.select_slider(
            "Aspect Ratio",
            options=config.txt2img.aspect_ratios,
            value=config.txt2img.default_aspect_ratio,
            disabled=st.session_state.running,
        )
    if param in ["guidance_scale", "guidance"]:
        parameters[param] = st.sidebar.slider(
            "Guidance Scale",
            model_preset.guidance_scale_min,
            model_preset.guidance_scale_max,
            model_preset.guidance_scale,
            0.1,
            disabled=st.session_state.running,
        )
    if param in ["num_inference_steps", "steps"]:
        parameters[param] = st.sidebar.slider(
            "Inference Steps",
            model_preset.num_inference_steps_min,
            model_preset.num_inference_steps_max,
            model_preset.num_inference_steps,
            1,
            disabled=st.session_state.running,
        )
    if param in ["expand_prompt", "prompt_expansion"]:
        parameters[param] = st.sidebar.checkbox(
            "Prompt Expansion",
            value=False,
            disabled=st.session_state.running,
        )
    if param == "prompt_upsampling":
        parameters[param] = st.sidebar.checkbox(
            "Prompt Upsampling",
            value=False,
            disabled=st.session_state.running,
        )

# Wrap the prompt in an accordion to display additional parameters
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
                        if k not in config.txt2img.hidden_parameters
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

# Buttons for deleting last generation or clearing all generations
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

# Set running state to True and show spinner while loading.
# Update state and refresh on response; errors will be displayed as chat messages.
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
            if model_preset.kwargs:
                parameters.update(model_preset.kwargs)
            session_key = f"api_key_{service}"
            api_key = st.session_state[session_key] or config.service[service].api_key
            image = txt2img_generate(api_key, service, model, prompt, parameters)
        st.session_state.running = False

    st.session_state.txt2img_messages.append(
        {"role": "user", "content": prompt, "parameters": parameters, "model": model_preset.name}
    )
    st.session_state.txt2img_messages.append({"role": "assistant", "content": image})
    st.rerun()
