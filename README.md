---
# https://huggingface.co/docs/hub/en/spaces-config-reference
title: API Inference
short_description: Inference on API endpoints
emoji: ⚡
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.37.1
python_version: 3.11.9
app_file: 0_🏠_Home.py
full_width: true
pinned: true
header: mini
license: apache-2.0
---
# ⚡ API Inference

## Configuration

Streamlit [configuration](https://docs.streamlit.io/develop/concepts/configuration/options) has the following priority order:
1. `streamlit run` flags (highest priority)
2. environment variables
3. local config file
4. global config file

So you can deploy the local config and override with environment variables as necessary:

```bash
STREAMLIT_LOGGER_LEVEL=error
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false
STREAMLIT_CLIENT_TOOLBAR_MODE=viewer
STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
STREAMLIT_SERVER_RUN_ON_SAVE=false
STREAMLIT_BROWSER_SERVER_ADDRESS=adamelliotfields-api-inference.hf.space
```

## Installation

```sh
# clone
git clone https://huggingface.co/spaces/adamelliotfields/api-inference.git
cd api-inference
git remote set-url origin https://adamelliotfields:$HF_TOKEN@huggingface.co/spaces/adamelliotfields/api-inference

# install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run
python app.py
```
