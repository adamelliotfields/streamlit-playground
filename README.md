---
# https://huggingface.co/docs/hub/en/spaces-config-reference
title: API Inference
short_description: Inference on many API endpoints
emoji: ⚡
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.37.1
python_version: 3.11.9
suggested_hardware: cpu-basic
app_file: 0_🏠_Home.py
full_width: true
pinned: true
header: default
license: apache-2.0
models:
  - black-forest-labs/FLUX.1-schnell
  - black-forest-labs/FLUX.1-dev
---
# ⚡ API Inference

[Streamlit](https://streamlit.io) app for running inference on generative AI endpoints.

## Secrets

Setting keys as environment variables persists them so you don't have to enter them on every page load.

```bash
BFL_API_KEY=...
FAL_KEY=...
HF_TOKEN=...
PPLX_API_KEY=...
TOGETHER_API_KEY=...
```

## Installation

Recommend [uv](https://github.com/astral-sh/uv).

```sh
# clone
git clone https://huggingface.co/spaces/adamelliotfields/api-inference.git
cd api-inference

# install
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# run
python app.py
```

## Development

```sh
git remote set-url origin https://adamelliotfields:$HF_TOKEN@huggingface.co/spaces/adamelliotfields/api-inference
```
