import os
from datetime import datetime

import streamlit as st
from openai import APIError, OpenAI

from lib import Config

# TODO: key input and store in cache_data
# api key
HF_TOKEN = os.environ.get("HF_TOKEN")


# TODO: eventually support different APIs like OpenAI and Perplexity
@st.cache_resource
def get_chat_client(api_key, model):
    client = OpenAI(
        api_key=api_key,
        base_url=f"https://api-inference.huggingface.co/models/{model}/v1",
    )
    return client


# config
st.set_page_config(
    page_title=f"{Config.TITLE} | Text Generation",
    page_icon=Config.ICON,
    layout=Config.LAYOUT,
)

# initialize state
if "txt2txt_messages" not in st.session_state:
    st.session_state.txt2txt_messages = []

if "txt2txt_prompt" not in st.session_state:
    st.session_state.txt2txt_prompt = ""

# sidebar
st.logo("logo.svg")
st.sidebar.header("Settings")
model = st.sidebar.selectbox(
    "Model",
    placeholder="Select a model",
    format_func=lambda x: x.split("/")[1],
    index=Config.TXT2TXT_DEFAULT_MODEL,
    options=Config.TXT2TXT_MODELS,
)
max_tokens = st.sidebar.slider(
    "Max Tokens",
    min_value=512,
    max_value=4096,
    value=512,
    step=128,
    help="Maximum number of tokens to generate (default: 512)",
)
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=1.0,
    step=0.1,
    help="Used to modulate the next token probabilities (default: 1.0)",
)
frequency_penalty = st.sidebar.slider(
    "Frequency Penalty",
    min_value=-2.0,
    max_value=2.0,
    value=0.0,
    step=0.1,
    help="Penalize new tokens based on their existing frequency in the text (default: 0.0)",
)
seed = st.sidebar.number_input(
    "Seed",
    min_value=-1,
    max_value=(1 << 53) - 1,
    value=-1,
    help="Make a best effort to sample deterministically (default: -1)",
)
system = st.sidebar.text_area(
    "System Message",
    value="You are a helpful assistant. Be precise and concise.",
)

# random seed
if seed < 0:
    seed = int(datetime.now().timestamp() * 1e6) % (1 << 53)

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
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.txt2txt_prompt = prompt

if st.session_state.txt2txt_prompt:
    with st.chat_message("user"):
        st.markdown(st.session_state.txt2txt_prompt)

    if button_container:
        button_container.empty()

    messages = [{"role": "system", "content": system}]
    messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.txt2txt_messages])
    messages.append({"role": "user", "content": st.session_state.txt2txt_prompt})

    with st.chat_message("assistant"):
        try:
            client = get_chat_client(HF_TOKEN, model)
            stream = client.chat.completions.create(
                frequency_penalty=frequency_penalty,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=messages,
                model=model,
                stream=True,
                seed=seed,
            )
            response = st.write_stream(stream)
        except APIError as e:
            response = e.message
        except Exception as e:
            response = str(e)

    st.session_state.txt2txt_messages.append({"role": "user", "content": st.session_state.txt2txt_prompt})
    st.session_state.txt2txt_messages.append({"role": "assistant", "content": response})
    st.session_state.txt2txt_prompt = ""
    st.rerun()
