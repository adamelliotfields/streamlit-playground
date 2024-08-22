import os
from datetime import datetime

import streamlit as st

from lib import Config, HuggingFaceTxt2TxtAPI, PerplexityTxt2TxtAPI, ServicePresets

HF_TOKEN = os.environ.get("HF_TOKEN") or None
PPLX_API_KEY = os.environ.get("PPLX_API_KEY") or None


@st.cache_resource
def get_txt2txt_api(service="Huggingface", api_key=None):
    if service == "Huggingface":
        return HuggingFaceTxt2TxtAPI(api_key)
    if service == "Perplexity":
        return PerplexityTxt2TxtAPI(api_key)
    return None


# config
st.set_page_config(
    page_title=f"{Config.TITLE} | Text Generation",
    page_icon=Config.ICON,
    layout=Config.LAYOUT,
)

# initialize state
if "txt2txt_running" not in st.session_state:
    st.session_state.txt2txt_running = False

if "txt2txt_messages" not in st.session_state:
    st.session_state.txt2txt_messages = []

if "txt2txt_prompt" not in st.session_state:
    st.session_state.txt2txt_prompt = ""

# sidebar
st.logo("logo.svg")
st.sidebar.header("Settings")
service = st.sidebar.selectbox(
    "Service",
    options=["Huggingface", "Perplexity"],
    index=0,
    disabled=st.session_state.txt2txt_running,
)

# hide key input if environment variables are set
if (service == "Huggingface" and HF_TOKEN is None) or (service == "Perplexity" and PPLX_API_KEY is None):
    api_key = st.sidebar.text_input(
        "API Key",
        value="",
        type="password",
        help="Cleared on page refresh",
        disabled=st.session_state.txt2txt_running,
    )

model = st.sidebar.selectbox(
    "Model",
    format_func=lambda x: x.split("/")[1] if service == "Huggingface" else x,
    index=Config.TXT2TXT_DEFAULT_MODEL[service],
    options=Config.TXT2TXT_MODELS[service],
    disabled=st.session_state.txt2txt_running,
)
system = st.sidebar.text_area(
    "System Message",
    value=Config.TXT2TXT_DEFAULT_SYSTEM,
    disabled=st.session_state.txt2txt_running,
)

# build parameters from preset
parameters = {}
preset = getattr(ServicePresets, service)
for param in preset["parameters"]:
    if param == "max_tokens":
        parameters[param] = st.sidebar.slider(
            "Max Tokens",
            min_value=512,
            max_value=4096,
            value=512,
            step=128,
            help="Maximum number of tokens to generate (default: 512)",
            disabled=st.session_state.txt2txt_running,
        )
    if param == "temperature":
        parameters[param] = st.sidebar.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Used to modulate the next token probabilities (default: 1.0)",
            disabled=st.session_state.txt2txt_running,
        )
    if param == "frequency_penalty":
        parameters[param] = st.sidebar.slider(
            "Frequency Penalty",
            min_value=preset["frequency_penalty_min"],
            max_value=preset["frequency_penalty_max"],
            value=preset["frequency_penalty"],
            step=0.1,
            help="Penalize new tokens based on their existing frequency in the text (default: 0.0)",
            disabled=st.session_state.txt2txt_running,
        )
    if param == "seed":
        parameters[param] = st.sidebar.number_input(
            "Seed",
            min_value=-1,
            max_value=(1 << 53) - 1,
            value=-1,
            help="Make a best effort to sample deterministically (default: -1)",
            disabled=st.session_state.txt2txt_running,
        )

# random seed
if parameters.get("seed", 0) < 0:
    parameters["seed"] = int(datetime.now().timestamp() * 1e6) % (1 << 53)

# heading
st.html("""
    <h1 style="padding: 0; margin-bottom: 0.5rem">Text Generation</h1>
    <p>Chat with large language models.</p>
""")

# chat messages
for message in st.session_state.txt2txt_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# button row
if st.session_state.txt2txt_messages:
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

        # remove last assistant message and resend prompt
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄️", help="Retry last message") and len(st.session_state.txt2txt_messages) >= 2:
                st.session_state.txt2txt_messages.pop()
                st.session_state.txt2txt_prompt = st.session_state.txt2txt_messages.pop()["content"]
                st.rerun()

        # delete last message pair
        with col2:
            if st.button("❌", help="Delete last message") and len(st.session_state.txt2txt_messages) >= 2:
                st.session_state.txt2txt_messages.pop()
                st.session_state.txt2txt_messages.pop()
                st.rerun()

        # reset app state
        with col3:
            if st.button("🗑️", help="Clear all messages"):
                st.session_state.txt2txt_messages = []
                st.session_state.txt2txt_prompt = ""
                st.rerun()
else:
    button_container = None

# chat input
if prompt := st.chat_input(
    "What would you like to know?",
    on_submit=lambda: setattr(st.session_state, "txt2txt_running", True),
):
    st.session_state.txt2txt_prompt = prompt

if st.session_state.txt2txt_prompt:
    with st.chat_message("user"):
        st.markdown(st.session_state.txt2txt_prompt)

    if button_container:
        button_container.empty()

    messages = [{"role": "system", "content": system}]
    messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.txt2txt_messages])
    messages.append({"role": "user", "content": st.session_state.txt2txt_prompt})
    parameters["messages"] = messages

    with st.chat_message("assistant"):
        # allow environment variables in development for convenience
        if service == "Huggingface" and HF_TOKEN is not None:
            key = HF_TOKEN
        elif service == "Perplexity" and PPLX_API_KEY is not None:
            key = PPLX_API_KEY
        else:
            key = api_key
        api = get_txt2txt_api(service, key)
        response = api.generate_text(model, parameters)
        st.session_state.txt2txt_running = False

    st.session_state.txt2txt_messages.append({"role": "user", "content": st.session_state.txt2txt_prompt})
    st.session_state.txt2txt_messages.append({"role": "assistant", "content": response})
    st.session_state.txt2txt_prompt = ""
    st.rerun()
