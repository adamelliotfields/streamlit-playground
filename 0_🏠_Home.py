import streamlit as st

from lib import config

st.set_page_config(
    page_title=f"Home - {config.title}",
    page_icon=config.icon,
    layout=config.layout,
)

# sidebar
st.logo(config.logo, size="small")

# title
st.html("""
<style>
.pro-badge {
    /* https://huggingface.co/subscribe/pro */
    display: inline-block;
    transform: skew(-12deg);
    font-size: 0.875rem;
    line-height: 1.25rem;
    font-weight: 700;
    padding: 0.125rem 0.625rem;
    border-radius: 0.5rem;
    color: rgb(0 0 0 / 1);
    box-shadow: 0 0 #0000, 0 0 #0000, 0 10px 15px -3px rgb(16 185 129 / .1), 0 4px 6px -4px rgb(16 185 129 / .1);
    background-image: linear-gradient(to bottom right, #f9a8d4, #a7f3d0, #fde68a);
    border: 1px solid rgb(229 231 235 / 1);
}
</style>
<div style="display: flex; align-items: center; gap: 0.75rem">
    <h1 style="padding: 0">Playground</h1>
    <span class="pro-badge">API</span>
</div>
""")

st.markdown("""## Tasks""")

st.page_link("pages/1_💬_Text_Generation.py", label="Text Generation", icon="💬")
st.page_link("pages/2_🎨_Text_to_Image.py", label="Text to Image", icon="🎨")

st.markdown("""
## Services

- [Anthropic](https://docs.anthropic.com/en/api/getting-started)
- [Black Forest Labs](https://docs.bfl.ml)
- [fal.ai](https://fal.ai/docs)
- [Hugging Face](https://huggingface.co/docs/api-inference/index)
- [OpenAI](https://platform.openai.com/docs/api-reference/introduction)
- [Perplexity](https://docs.perplexity.ai/home)
- [together.ai](https://docs.together.ai/docs/introduction)
""")
