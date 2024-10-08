import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ServiceConfig:
    name: str
    url: str
    api_key: Optional[str] = None


@dataclass
class Txt2TxtConfig:
    default_system: str


@dataclass
class Txt2ImgConfig:
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
    layout: str
    logo: str
    service: Dict[str, ServiceConfig]
    txt2img: Txt2ImgConfig
    txt2txt: Txt2TxtConfig


config = Config(
    title="API Inference",
    layout="wide",
    logo="logo.png",
    service={
        "bfl": ServiceConfig(
            "Black Forest Labs",
            "https://api.bfl.ml/v1",
            os.environ.get("BFL_API_KEY"),
        ),
        "fal": ServiceConfig(
            "Fal",
            "https://fal.run",
            os.environ.get("FAL_KEY"),
        ),
        "hf": ServiceConfig(
            "Hugging Face",
            "https://api-inference.huggingface.co/models",
            os.environ.get("HF_TOKEN"),
        ),
        "pplx": ServiceConfig(
            "Perplexity",
            "https://api.perplexity.ai",
            os.environ.get("PPLX_API_KEY"),
        ),
        "together": ServiceConfig(
            "Together",
            "https://api.together.xyz/v1/images/generations",
            os.environ.get("TOGETHER_API_KEY"),
        ),
    },
    txt2img=Txt2ImgConfig(
        hidden_parameters=[
            # Sent to API but not shown in generation parameters accordion
            "enable_safety_checker",
            "max_sequence_length",
            "n",
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
    ),
)
