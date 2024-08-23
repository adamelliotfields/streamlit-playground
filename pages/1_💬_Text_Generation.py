import os
from datetime import datetime

import streamlit as st

from lib import Config, ServicePresets, txt2txt_generate

HF_TOKEN = os.environ.get("HF_TOKEN") or None
PPLX_API_KEY = os.environ.get("PPLX_API_KEY") or None


# config
st.set_page_config(
    page_title=f"{Config.TITLE} | Text Generation",
    page_icon=Config.ICON,
    layout=Config.LAYOUT,
)

# initialize state
if "api_key_huggingface" not in st.session_state:
    st.session_state.api_key_huggingface = ""

if "api_key_perplexity" not in st.session_state:
    st.session_state.api_key_perplexity = ""

if "txt2txt_messages" not in st.session_state:
    st.session_state.txt2txt_messages = []

if "txt2txt_prompt" not in st.session_state:
    st.session_state.txt2txt_prompt = ""

if "txt2txt_running" not in st.session_state:
    st.session_state.txt2txt_running = False

# sidebar
st.logo("logo.svg")
st.sidebar.header("Settings")
service = st.sidebar.selectbox(
    "Service",
    options=["Huggingface", "Perplexity"],
    index=0,
    disabled=st.session_state.txt2txt_running,
)

if service == "Huggingface" and HF_TOKEN is None:
    st.session_state.api_key_huggingface = st.sidebar.text_input(
        "API Key",
        type="password",
        help="Cleared on page refresh",
        disabled=st.session_state.txt2txt_running,
        value=st.session_state.api_key_huggingface,
    )
else:
    st.session_state.api_key_huggingface = None

if service == "Perplexity" and PPLX_API_KEY is None:
    st.session_state.api_key_perplexity = st.sidebar.text_input(
        "API Key",
        type="password",
        help="Cleared on page refresh",
        disabled=st.session_state.txt2txt_running,
        value=st.session_state.api_key_perplexity,
    )
else:
    st.session_state.api_key_perplexity = None

if service == "Huggingface" and HF_TOKEN is not None:
    st.session_state.api_key_huggingface = HF_TOKEN

if service == "Perplexity" and PPLX_API_KEY is not None:
    st.session_state.api_key_perplexity = PPLX_API_KEY

model = st.sidebar.selectbox(
    "Model",
    options=Config.TXT2TXT_MODELS[service],
    index=Config.TXT2TXT_DEFAULT_MODEL[service],
    disabled=st.session_state.txt2txt_running,
    format_func=lambda x: x.split("/")[1] if service == "Huggingface" else x,
)
system = st.sidebar.text_area(
    "System Message",
    value=Config.TXT2TXT_DEFAULT_SYSTEM,
    disabled=st.session_state.txt2txt_running,
)

# build parameters from preset
parameters = {}
preset = getattr(ServicePresets, service, {})
for param in preset["parameters"]:
    if param == "max_tokens":
        parameters[param] = st.sidebar.slider(
            "Max Tokens",
            step=128,
            value=512,
            min_value=512,
            max_value=4096,
            disabled=st.session_state.txt2txt_running,
            help="Maximum number of tokens to generate (default: 512)",
        )
    if param == "temperature":
        parameters[param] = st.sidebar.slider(
            "Temperature",
            step=0.1,
            value=1.0,
            min_value=0.0,
            max_value=2.0,
            disabled=st.session_state.txt2txt_running,
            help="Used to modulate the next token probabilities (default: 1.0)",
        )
    if param == "frequency_penalty":
        parameters[param] = st.sidebar.slider(
            "Frequency Penalty",
            step=0.1,
            value=preset["frequency_penalty"],
            min_value=preset["frequency_penalty_min"],
            max_value=preset["frequency_penalty_max"],
            disabled=st.session_state.txt2txt_running,
            help="Penalize new tokens based on their existing frequency in the text (default: 0.0)",
        )
    if param == "seed":
        parameters[param] = st.sidebar.number_input(
            "Seed",
            value=-1,
            min_value=-1,
            max_value=(1 << 53) - 1,
            disabled=st.session_state.txt2txt_running,
            help="Make a best effort to sample deterministically (default: -1)",
        )

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

    if parameters.get("seed", 0) < 0:
        parameters["seed"] = int(datetime.now().timestamp() * 1e6) % (1 << 53)

    if button_container:
        button_container.empty()

    messages = [{"role": "system", "content": system}]
    messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.txt2txt_messages])
    messages.append({"role": "user", "content": st.session_state.txt2txt_prompt})
    parameters["messages"] = messages

    with st.chat_message("user"):
        st.markdown(st.session_state.txt2txt_prompt)

    with st.chat_message("assistant"):
        api_key = getattr(st.session_state, f"api_key_{service.lower()}", None)
        response = txt2txt_generate(api_key, service, model, parameters)
        st.session_state.txt2txt_running = False

    st.session_state.txt2txt_messages.append({"role": "user", "content": st.session_state.txt2txt_prompt})
    st.session_state.txt2txt_messages.append({"role": "assistant", "content": response})
    st.session_state.txt2txt_prompt = ""
    st.rerun()
