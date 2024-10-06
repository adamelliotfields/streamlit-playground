import streamlit as st

from lib import Config

st.set_page_config(
    page_title=Config.TITLE,
    page_icon=Config.ICON,
    layout=Config.LAYOUT,
)

# sidebar
st.logo("logo.png")

# title
st.html("""
<style>
.pro-badge {
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
@media (prefers-color-scheme: dark) {
    .pro-badge {
        box-shadow: 0 0 #0000, 0 0 #0000, 0 10px 15px -3px rgb(16 185 129 / .2), 0 4px 6px -4px rgb(16 185 129 / .2);
        background-image: linear-gradient(to bottom right, #ec4899, #10b981, #f59e0b);
        border: 1px solid rgb(20 28 46 / 1);
    }
}
</style>
<div style="display: flex; align-items: center; gap: 0.75rem">
    <h1>API Inference</h1>
    <span class="pro-badge">PRO</span>
</div>
""")

st.markdown("## Tasks")
st.page_link("pages/1_💬_Text_Generation.py", label="Text Generation", icon="💬")
st.page_link("pages/2_🎨_Text_to_Image.py", label="Text to Image", icon="🎨")

st.markdown("""
## Services

- [Black Forest Labs](https://docs.bfl.ml)
- [fal.ai](https://fal.ai/docs)
- [Hugging Face](https://huggingface.co/docs/api-inference/index)
- [Perplexity](https://docs.perplexity.ai/home)
- [together.ai](https://docs.together.ai/docs/introduction)
""")

st.markdown("""
## Usage

Choose a task from the sidebar. Enter your API key for the service you want to use. Refresh your browser to remove it.

I recommend [duplicating this space](https://huggingface.co/spaces/adamelliotfields/api-inference?duplicate=true) **privately** and persisting your keys as secrets. See [`README.md`](https://huggingface.co/spaces/adamelliotfields/api-inference/blob/main/README.md).
""")
