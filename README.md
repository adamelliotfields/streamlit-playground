---
# https://huggingface.co/docs/hub/en/spaces-config-reference
title: Playground
short_description: Explore popular generative AI endpoints
emoji: ⚡
colorFrom: blue
colorTo: pink
sdk: streamlit
sdk_version: 1.40.2
python_version: 3.11.9
suggested_hardware: cpu-basic
app_file: 0_🏠_Home.py
full_width: true
pinned: false
header: default
license: apache-2.0
---
# ⚡ Playground

[Streamlit](https://streamlit.io) app for running inference on generative AI endpoints.

## Secrets

Setting keys as environment variables persists them so you don't have to enter them on every page load.

```bash
ANTHROPIC_API_KEY=...
BFL_API_KEY=...
FAL_KEY=...
HF_TOKEN=...
OPENAI_API_KEY=...
PPLX_API_KEY=...
TOGETHER_API_KEY=...
```

## Installation

```sh
# clone
git clone https://huggingface.co/spaces/adamelliotfields/playground.git
cd playground

# install
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# run
python 0_🏠_Home.py
```

## Development

```sh
git remote set-url origin https://adamelliotfields:$HF_TOKEN@huggingface.co/spaces/adamelliotfields/playground
```
