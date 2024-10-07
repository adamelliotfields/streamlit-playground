from dataclasses import dataclass
from typing import Dict, List

from .preset import preset


def txt2img_models_from_presets(presets):
    models = {}
    for p in presets:
        service = p.service
        model_id = p.model_id
        if service not in models:
            models[service] = []
        models[service].append(model_id)
    return models


@dataclass
class Txt2TxtConfig:
    default_system: str
    default_model: Dict[str, int]
    models: Dict[str, List[str]]


@dataclass
class Txt2ImgConfig:
    default_model: Dict[str, int]
    models: Dict[str, List[str]]
    hidden_parameters: List[str]
    negative_prompt: str
    default_image_size: str
    image_sizes: List[str]
    default_aspect_ratio: str
    aspect_ratios: List[str]
    timeout: int = 60


@dataclass
class Config:
    title: str
    icon: str
    layout: str
    services: Dict[str, str]
    txt2img: Txt2ImgConfig
    txt2txt: Txt2TxtConfig


# TODO: API keys should be with services (make a dataclass)
config = Config(
    title="API Inference",
    icon="⚡",
    layout="wide",
    services={
        "Black Forest Labs": "https://api.bfl.ml/v1",
        "Fal": "https://fal.run",
        "Hugging Face": "https://api-inference.huggingface.co/models",
        "Perplexity": "https://api.perplexity.ai",
        "Together": "https://api.together.xyz/v1/images/generations",
    },
    txt2img=Txt2ImgConfig(
        default_model={
            "Black Forest Labs": 2,
            "Fal": 0,
            "Hugging Face": 2,
            "Together": 0,
        },
        models=txt2img_models_from_presets(preset.txt2img.presets),
        hidden_parameters=[
            # Sent to API but not shown in generation parameters accordion
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
        negative_prompt="ugly, unattractive, disfigured, deformed, mutated, malformed, blurry, grainy, oversaturated, undersaturated, overexposed, underexposed, worst quality, low details, lowres, watermark, signature, sloppy, cluttered",
        default_image_size="square_hd",
        image_sizes=[
            "landscape_16_9",
            "landscape_4_3",
            "square_hd",
            "portrait_4_3",
            "portrait_16_9",
        ],
        default_aspect_ratio="1024x1024",  # fooocus aspect ratios
        aspect_ratios=[
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
    ),
    txt2txt=Txt2TxtConfig(
        default_system="You are a helpful assistant. Be precise and concise.",
        default_model={
            "Hugging Face": 4,
            "Perplexity": 3,
        },
        models={
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
                "llama-3.1-sonar-huge-128k-online",
            ],
        },
    ),
)
