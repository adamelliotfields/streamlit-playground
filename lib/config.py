from types import SimpleNamespace

Config = SimpleNamespace(
    TITLE="API Inference",
    ICON="⚡",
    LAYOUT="wide",
    TXT2IMG_NEGATIVE_PROMPT="ugly, bad, asymmetrical, malformed, mutated, disgusting, blurry, grainy, oversaturated, undersaturated, overexposed, underexposed, worst quality, low details, lowres, watermark, signature, autograph, trademark",
    TXT2IMG_DEFAULT_MODEL=2,
    TXT2IMG_MODELS=[
        "black-forest-labs/flux.1-dev",
        "black-forest-labs/flux.1-schnell",
        "stabilityai/stable-diffusion-xl-base-1.0",
    ],
    TXT2IMG_DEFAULT_AR="1:1",
    TXT2IMG_AR={
        "9:7": (1152, 896),
        "7:4": (1344, 768),
        "1:1": (1024, 1024),
        "4:7": (768, 1344),
        "7:9": (896, 1152),
    },
    TXT2TXT_DEFAULT_MODEL=4,
    TXT2TXT_MODELS=[
        "codellama/codellama-34b-instruct-hf",
        "meta-llama/llama-2-13b-chat-hf",
        "meta-llama/meta-llama-3.1-405b-instruct-fp8",
        "mistralai/mistral-7b-instruct-v0.2",
        "nousresearch/nous-hermes-2-mixtral-8x7b-dpo",
    ],
)
