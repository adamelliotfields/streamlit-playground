# Playground

This is a chat UI I made mostly to try [Streamlit](https://streamlit.io). It supports text and image generation from many cloud inference providers.

## Installation

```sh
# install
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# run
streamlit run 0_🏠_Home.py
```

## Secrets

Each provider requires an API key.

```bash
ANTHROPIC_API_KEY=...
BFL_API_KEY=...
FAL_KEY=...
HF_TOKEN=...
OPENAI_API_KEY=...
PPLX_API_KEY=...
TOGETHER_API_KEY=...
```
