from datetime import datetime

import streamlit as st

from lib import config, txt2txt_generate

st.set_page_config(
    page_title=f"Text Generation - {config.title}",
    layout=config.layout,
)

if "api_key_anthropic" not in st.session_state:
    st.session_state.api_key_anthropic = ""

if "api_key_hf" not in st.session_state:
    st.session_state.api_key_hf = ""

if "api_key_openai" not in st.session_state:
    st.session_state.api_key_openai = ""

if "api_key_pplx" not in st.session_state:
    st.session_state.api_key_pplx = ""

if "running" not in st.session_state:
    st.session_state.running = False

if "txt2txt_messages" not in st.session_state:
    st.session_state.txt2txt_messages = []

if "txt2txt_seed" not in st.session_state:
    st.session_state.txt2txt_seed = 0

st.logo(config.logo, size="small")
st.sidebar.header("Settings")

text_providers = {
    provider_id: provider_config
    for provider_id, provider_config in config.providers.items()
    if getattr(provider_config, "text", None)
}

provider = st.sidebar.selectbox(
    "Provider",
    options=text_providers.keys(),
    format_func=lambda x: text_providers[x].name,
    disabled=st.session_state.running,
)

# Show the API key input for the selected provider.
for provider_id, provider_preset in text_providers.items():
    if provider == provider_id:
        session_key = f"api_key_{provider}"
        api_key = provider_preset.api_key
        st.session_state[session_key] = st.sidebar.text_input(
            "API Key",
            type="password",
            value="" if api_key else st.session_state[session_key],
            disabled=bool(api_key) or st.session_state.running,
            help="Set by environment variable" if api_key else "Cleared on page refresh",
        )

provider_config = text_providers[provider]

model = st.sidebar.selectbox(
    "Model",
    options=provider_config.text.keys(),
    format_func=lambda x: provider_config.text[x].name,
    disabled=st.session_state.running,
)

model_config = provider_config.text[model]

system = st.sidebar.text_area(
    "System Message",
    value=model_config.system_prompt,
    disabled=st.session_state.running,
)

st.html("""
    <h1>Text Generation</h1>
    <p>Chat with large language models.</p>
""")

# Build parameters from preset by rendering the appropriate input widgets
parameters = {"model": model}
for param in model_config.parameters:
    if param == "max_tokens":
        parameters[param] = st.sidebar.slider(
            "Max Tokens",
            step=512,
            value=model_config.max_tokens,
            min_value=model_config.max_tokens_range[0],
            max_value=model_config.max_tokens_range[1],
            disabled=st.session_state.running,
            help="Maximum number of tokens to generate (default: 512)",
        )

    if param == "temperature":
        parameters[param] = st.sidebar.slider(
            "Temperature",
            step=0.1,
            value=model_config.temperature,
            min_value=model_config.temperature_range[0],
            max_value=model_config.temperature_range[1],
            disabled=st.session_state.running,
            help="Used to modulate the next token probabilities (default: 1.0)",
        )

    if param == "frequency_penalty":
        parameters[param] = st.sidebar.slider(
            "Frequency Penalty",
            step=0.1,
            value=model_config.frequency_penalty,
            min_value=model_config.frequency_penalty_range[0],
            max_value=model_config.frequency_penalty_range[1],
            disabled=st.session_state.running,
            help="Penalize new tokens based on their existing frequency in the text (default: 0.0)",
        )

    if param == "presence_penalty":
        parameters[param] = st.sidebar.slider(
            "Presence Penalty",
            step=0.1,
            value=model_config.presence_penalty,
            min_value=model_config.presence_penalty_range[0],
            max_value=model_config.presence_penalty_range[1],
            disabled=st.session_state.running,
            help="Penalize new tokens based on their presence in the text so far (default: 0.0)",
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

# Chat messages
for message in st.session_state.txt2txt_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Buttons for deleting last message or clearing all messages
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

# Chat input
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

    if provider == "anthropic":
        messages = []
        parameters["system"] = system
    else:
        messages = [{"role": "system", "content": system}]

    messages.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.txt2txt_messages])
    messages.append({"role": "user", "content": prompt})
    parameters["messages"] = messages

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        session_key = f"api_key_{provider}"
        api_key = st.session_state[session_key] or text_providers[provider].api_key
        response = txt2txt_generate(api_key, provider, parameters)
        st.session_state.running = False

    st.session_state.txt2txt_messages.append({"role": "user", "content": prompt})
    st.session_state.txt2txt_messages.append({"role": "assistant", "content": response})
    st.rerun()
