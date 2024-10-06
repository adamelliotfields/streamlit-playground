import os
from datetime import datetime

import streamlit as st

from lib import Config, ServicePresets, txt2txt_generate

SERVICE_SESSION = {
    "Hugging Face": "api_key_hugging_face",
    "Perplexity": "api_key_perplexity",
}

SESSION_TOKEN = {
    "api_key_hugging_face": os.environ.get("HF_TOKEN") or None,
    "api_key_perplexity": os.environ.get("PPLX_API_KEY") or None,
}

# config
st.set_page_config(
    page_title=f"{Config.TITLE} | Text Generation",
    page_icon=Config.ICON,
    layout=Config.LAYOUT,
)

# initialize state
if "api_key_hugging_face" not in st.session_state:
    st.session_state.api_key_hugging_face = ""

if "api_key_perplexity" not in st.session_state:
    st.session_state.api_key_perplexity = ""

if "running" not in st.session_state:
    st.session_state.running = False

if "txt2txt_messages" not in st.session_state:
    st.session_state.txt2txt_messages = []

if "txt2txt_seed" not in st.session_state:
    st.session_state.txt2txt_seed = 0

# sidebar
st.logo("logo.png")
st.sidebar.header("Settings")
service = st.sidebar.selectbox(
    "Service",
    options=["Hugging Face", "Perplexity"],
    index=0,
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
    options=Config.TXT2TXT_MODELS[service],
    index=Config.TXT2TXT_DEFAULT_MODEL[service],
    disabled=st.session_state.running,
    format_func=lambda x: x.split("/")[1] if service == "Hugging Face" else x,
)
system = st.sidebar.text_area(
    "System Message",
    value=Config.TXT2TXT_DEFAULT_SYSTEM,
    disabled=st.session_state.running,
)

# build parameters from preset
parameters = {}
service_key = service.upper().replace(" ", "_")
preset = getattr(ServicePresets, service_key, {})
for param in preset["parameters"]:
    if param == "max_tokens":
        parameters[param] = st.sidebar.slider(
            "Max Tokens",
            step=512,
            value=512,
            min_value=512,
            max_value=4096,
            disabled=st.session_state.running,
            help="Maximum number of tokens to generate (default: 512)",
        )
    if param == "temperature":
        parameters[param] = st.sidebar.slider(
            "Temperature",
            step=0.1,
            value=1.0,
            min_value=0.0,
            max_value=2.0,
            disabled=st.session_state.running,
            help="Used to modulate the next token probabilities (default: 1.0)",
        )
    if param == "frequency_penalty":
        parameters[param] = st.sidebar.slider(
            "Frequency Penalty",
            step=0.1,
            value=preset["frequency_penalty"],
            min_value=preset["frequency_penalty_min"],
            max_value=preset["frequency_penalty_max"],
            disabled=st.session_state.running,
            help="Penalize new tokens based on their existing frequency in the text (default: 0.0)",
        )
    if param == "seed":
        parameters[param] = st.sidebar.number_input(
            "Seed",
            value=-1,
            min_value=-1,
            max_value=(1 << 53) - 1,
            disabled=st.session_state.running,
            help="Make a best effort to sample deterministically (default: -1)",
        )

# heading
st.html("""
    <h1>Text Generation</h1>
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

        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌", help="Delete last message") and len(st.session_state.txt2txt_messages) >= 2:
                st.session_state.txt2txt_messages.pop()
                st.session_state.txt2txt_messages.pop()
                st.rerun()
        with col2:
            if st.button("🗑️", help="Clear all messages"):
                st.session_state.txt2txt_messages = []
                st.rerun()
else:
    button_container = None

# chat input
if prompt := st.chat_input(
    "What would you like to know?",
    on_submit=lambda: setattr(st.session_state, "running", True),
):
    if "seed" in parameters and parameters["seed"] >= 0:
        st.session_state.txt2txt_seed = parameters["seed"]
    else:
        st.session_state.txt2txt_seed = int(datetime.now().timestamp() * 1e6) % (1 << 53)
        if "seed" in parameters:
            parameters["seed"] = st.session_state.txt2txt_seed

    if button_container:
        button_container.empty()

    messages = [{"role": "system", "content": system}]
    messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.txt2txt_messages])
    messages.append({"role": "user", "content": prompt})
    parameters["messages"] = messages

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        session_key = f"api_key_{service.lower().replace(' ', '_')}"
        api_key = st.session_state[session_key] or SESSION_TOKEN[session_key]
        response = txt2txt_generate(api_key, service, model, parameters)
        st.session_state.running = False

    st.session_state.txt2txt_messages.append({"role": "user", "content": prompt})
    st.session_state.txt2txt_messages.append({"role": "assistant", "content": response})
    st.rerun()
