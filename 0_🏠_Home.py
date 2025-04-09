import streamlit as st

from lib import config

st.set_page_config(
    page_title=f"Home - {config.title}",
    layout=config.layout,
)

# sidebar
st.logo(config.logo, size="small")

# title
st.html("""
<div style="display: flex; align-items: center; gap: 0.75rem">
    <h1 style="padding: 0">Playground</h1>
</div>
""")

st.markdown("""## Tasks""")

st.page_link("pages/1_💬_Text_Generation.py", label="Text Generation", icon="💬")
st.page_link("pages/2_🎨_Text_to_Image.py", label="Text to Image", icon="🎨")

st.markdown("""
## Providers

- [Anthropic](https://docs.anthropic.com/en/api/getting-started)
- [Black Forest Labs](https://docs.bfl.ml)
- [fal.ai](https://fal.ai/docs)
- [Hugging Face](https://huggingface.co/docs/api-inference/index)
- [OpenAI](https://platform.openai.com/docs/api-reference/introduction)
- [Perplexity](https://docs.perplexity.ai/home)
- [together.ai](https://docs.together.ai/docs/introduction)
""")
