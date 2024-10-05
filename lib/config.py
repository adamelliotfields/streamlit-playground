from types import SimpleNamespace

Config = SimpleNamespace(
    TITLE="API Inference",
    ICON="⚡",
    LAYOUT="wide",
    SERVICES={
        "Black Forest Labs": "https://api.bfl.ml/v1",
        "Fal": "https://fal.run",
        "Hugging Face": "https://api-inference.huggingface.co/models",
        "Perplexity": "https://api.perplexity.ai",
    },
    TXT2IMG_TIMEOUT=60,
    TXT2IMG_HIDDEN_PARAMETERS=[
        # sent to API but not shown in generation parameters accordion
        "enable_safety_checker",
        "max_sequence_length",
        "num_images",
        "output_format",
        "performance",
        "safety_tolerance",
        "scheduler",
        "sharpness",
        "style",
        "styles",
        "sync_mode",
    ],
    TXT2IMG_NEGATIVE_PROMPT="ugly, unattractive, disfigured, deformed, mutated, malformed, blurry, grainy, noisy, oversaturated, undersaturated, overexposed, underexposed, worst quality, low details, lowres, watermark, signature, autograph, trademark, sloppy, cluttered",
    TXT2IMG_DEFAULT_MODEL={
        # The index of model in below lists
        "Black Forest Labs": 2,
        "Fal": 0,
        "Hugging Face": 2,
    },
    TXT2IMG_MODELS={
        # Model IDs referenced in Text_to_Image.py
        "Black Forest Labs": [
            "flux-dev",
            "flux-pro",
            "flux-pro-1.1",
        ],
        "Fal": [
            "fal-ai/aura-flow",
            "fal-ai/flux/dev",
            "fal-ai/flux/schnell",
            "fal-ai/flux-pro",
            "fal-ai/flux-pro/v1.1",
            "fal-ai/fooocus",
            "fal-ai/kolors",
            "fal-ai/stable-diffusion-v3-medium",
        ],
        "Hugging Face": [
            "black-forest-labs/flux.1-dev",
            "black-forest-labs/flux.1-schnell",
            "stabilityai/stable-diffusion-xl-base-1.0",
        ],
    },
    TXT2IMG_DEFAULT_IMAGE_SIZE="square_hd",  # fal image sizes
    TXT2IMG_IMAGE_SIZES=[
        "landscape_16_9",
        "landscape_4_3",
        "square_hd",
        "portrait_4_3",
        "portrait_16_9",
    ],
    TXT2IMG_DEFAULT_ASPECT_RATIO="1024x1024",  # fooocus aspect ratios
    TXT2IMG_ASPECT_RATIOS=[
        "704x1408",  # 1:2
        "704x1344",  # 11:21
        "768x1344",  # 4:7
        "768x1280",  # 3:5
        "832x1216",  # 13:19
        "832x1152",  # 13:18
        "896x1152",  # 7:9
        "896x1088",  # 14:17
        "960x1088",  # 15:17
        "960x1024",  # 15:16
        "1024x1024",
        "1024x960",  # 16:15
        "1088x960",  # 17:15
        "1088x896",  # 17:14
        "1152x896",  # 9:7
        "1152x832",  # 18:13
        "1216x832",  # 19:13
        "1280x768",  # 5:3
        "1344x768",  # 7:4
        "1344x704",  # 21:11
        "1408x704",  # 2:1
    ],
    TXT2TXT_DEFAULT_SYSTEM="You are a helpful assistant. Be precise and concise.",
    TXT2TXT_DEFAULT_MODEL={
        "Hugging Face": 4,
        "Perplexity": 3,
    },
    TXT2TXT_MODELS={
        "Hugging Face": [
            "codellama/codellama-34b-instruct-hf",
            "meta-llama/llama-2-13b-chat-hf",
            "meta-llama/meta-llama-3.1-405b-instruct-fp8",
            "mistralai/mistral-7b-instruct-v0.2",
            "nousresearch/nous-hermes-2-mixtral-8x7b-dpo",
        ],
        "Perplexity": [
            "llama-3.1-sonar-small-128k-chat",
            "llama-3.1-sonar-large-128k-chat",
            "llama-3.1-sonar-small-128k-online",
            "llama-3.1-sonar-large-128k-online",
        ],
    },
)
