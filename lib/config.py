import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

TEXT_SYSTEM_PROMPT = "You are a helpful assistant. Be precise and concise."

IMAGE_NEGATIVE_PROMPT = "ugly, unattractive, disfigured, deformed, mutated, malformed, blurry, grainy, oversaturated, undersaturated, overexposed, underexposed, worst quality, low details, lowres, watermark, signature, sloppy, cluttered"

FOOOCUS_NEGATIVE_PROMPT = "(worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art:1.4), (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2), (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, mutilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (airbrushed, cartoon, anime, semi-realistic, cgi, render, blender, digital art, manga, amateur:1.3), (3D ,3D Game, 3D Game Scene, 3D Character:1.1), (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3)"

IMAGE_SIZES = [
    "landscape_16_9",
    "landscape_4_3",
    "square_hd",
    "portrait_4_3",
    "portrait_16_9",
]

IMAGE_ASPECT_RATIOS = [
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
]

IMAGE_RANGE = (256, 1408)

STRENGTH_RANGE = (0.0, 1.0)


@dataclass
class ModelConfig:
    name: str
    parameters: List[str]
    kwargs: Optional[Dict[str, Union[str, int, float, bool]]] = field(default_factory=dict)


@dataclass
class TextModelConfig(ModelConfig):
    system_prompt: Optional[str] = None
    frequency_penalty: Optional[float] = None
    frequency_penalty_range: Optional[tuple[float, float]] = None
    presence_penalty: Optional[float] = None
    presence_penalty_range: Optional[tuple[float, float]] = None
    max_tokens: Optional[int] = None
    max_tokens_range: Optional[tuple[int, int]] = None
    temperature: Optional[float] = None
    temperature_range: Optional[tuple[float, float]] = None


@dataclass
class ImageModelConfig(ModelConfig):
    negative_prompt: Optional[str] = None
    width: Optional[int] = None
    width_range: Optional[tuple[int, int]] = None
    height: Optional[int] = None
    height_range: Optional[tuple[int, int]] = None
    strength: Optional[float] = None
    strength_range: Optional[tuple[float, float]] = None
    image_size: Optional[str] = None
    image_sizes: Optional[List[str]] = field(default_factory=list)
    aspect_ratio: Optional[str] = None
    aspect_ratios: Optional[List[str]] = field(default_factory=list)
    guidance_scale: Optional[float] = None
    guidance_scale_range: Optional[tuple[float, float]] = None
    num_inference_steps: Optional[int] = None
    num_inference_steps_range: Optional[tuple[int, int]] = None


@dataclass
class ServiceConfig:
    name: str
    url: str
    api_key: Optional[str]
    text: Optional[Dict[str, TextModelConfig]] = field(default_factory=dict)
    image: Optional[Dict[str, ImageModelConfig]] = field(default_factory=dict)


@dataclass
class AppConfig:
    title: str
    layout: str
    logo: str
    icon: str
    timeout: int
    hidden_parameters: List[str]
    services: Dict[str, ServiceConfig]


_anthropic_text_kwargs = {
    "system_prompt": TEXT_SYSTEM_PROMPT,
    "max_tokens": 512,
    "max_tokens_range": (512, 4096),
    "temperature": 0.5,
    "temperature_range": (0.0, 1.0),
    "parameters": ["max_tokens", "temperature"],
}

_hf_text_kwargs = {
    "system_prompt": TEXT_SYSTEM_PROMPT,
    "frequency_penalty": 0.0,
    "frequency_penalty_range": (-2.0, 2.0),
    "max_tokens": 512,
    "max_tokens_range": (512, 4096),
    "temperature": 1.0,
    "temperature_range": (0.0, 2.0),
    "parameters": ["max_tokens", "temperature", "frequency_penalty", "seed"],
}

_openai_text_kwargs = {
    "system_prompt": TEXT_SYSTEM_PROMPT,
    "frequency_penalty": 0.0,
    "frequency_penalty_range": (-2.0, 2.0),
    "presence_penalty": 0.0,
    "presence_penalty_range": (-2.0, 2.0),
    "max_tokens": 512,
    "max_tokens_range": (512, 4096),
    "temperature": 1.0,
    "temperature_range": (0.0, 2.0),
    "parameters": ["max_tokens", "temperature", "frequency_penalty", "presence_penalty", "seed"],
}

_pplx_text_kwargs = {
    "system_prompt": TEXT_SYSTEM_PROMPT,
    "frequency_penalty": 1.0,
    "frequency_penalty_range": (1.0, 2.0),
    "max_tokens": 512,
    "max_tokens_range": (512, 4096),
    "temperature": 1.0,
    "temperature_range": (0.0, 2.0),
    "parameters": ["max_tokens", "temperature", "frequency_penalty"],
}

config = AppConfig(
    title="Playground",
    layout="wide",
    logo="logo.svg",
    icon="⚡",
    timeout=60,
    hidden_parameters=[
        # Sent to API but not shown in generation parameters accordion
        "enable_safety_checker",
        "image_url",
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
    services={
        "anthropic": ServiceConfig(
            name="Anthropic",
            url="https://api.anthropic.com/v1",
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            text={
                "claude-3-haiku-20240307": TextModelConfig("Claude 3 Haiku", **_anthropic_text_kwargs),
                "claude-3-opus-20240229": TextModelConfig("Claude 3 Opus", **_anthropic_text_kwargs),
                "claude-3-sonnet-20240229": TextModelConfig("Claude 3 Sonnet", **_anthropic_text_kwargs),
                "claude-3-5-sonnet-20240620": TextModelConfig("Claude 3.5 Sonnet", **_anthropic_text_kwargs),
            },
        ),
        "bfl": ServiceConfig(
            name="Black Forest Labs",
            url="https://api.bfl.ml/v1",
            api_key=os.environ.get("BFL_API_KEY"),
            image={
                "flux-pro-1.1": ImageModelConfig(
                    "FLUX1.1 Pro",
                    width=1024,
                    width_range=IMAGE_RANGE,
                    height=1024,
                    height_range=IMAGE_RANGE,
                    parameters=["seed", "width", "height", "prompt_upsampling"],
                    kwargs={"safety_tolerance": 6},
                ),
                "flux-pro": ImageModelConfig(
                    "FLUX.1 Pro",
                    width=1024,
                    width_range=IMAGE_RANGE,
                    height=1024,
                    height_range=IMAGE_RANGE,
                    guidance_scale=2.5,
                    guidance_scale_range=(1.5, 5.0),
                    num_inference_steps=50,
                    num_inference_steps_range=(10, 50),
                    parameters=["seed", "width", "height", "steps", "guidance", "prompt_upsampling"],
                    kwargs={"safety_tolerance": 6, "interval": 1},
                ),
                "flux-dev": ImageModelConfig(
                    "FLUX.1 Dev",
                    width=1024,
                    width_range=IMAGE_RANGE,
                    height=1024,
                    height_range=IMAGE_RANGE,
                    num_inference_steps=28,
                    num_inference_steps_range=(10, 50),
                    guidance_scale=3.0,
                    guidance_scale_range=(1.5, 5.0),
                    parameters=["seed", "width", "height", "steps", "guidance", "prompt_upsampling"],
                    kwargs={"safety_tolerance": 6},
                ),
            },
        ),
        "fal": ServiceConfig(
            name="Fal",
            url="https://fal.run",
            api_key=os.environ.get("FAL_KEY"),
            image={
                "fal-ai/aura-flow": ImageModelConfig(
                    "AuraFlow",
                    guidance_scale=3.5,
                    guidance_scale_range=(0.0, 20.0),
                    num_inference_steps=50,
                    num_inference_steps_range=(20, 50),
                    parameters=["seed", "num_inference_steps", "guidance_scale", "expand_prompt"],
                    kwargs={"num_images": 1, "sync_mode": False},
                ),
                "fal-ai/fast-sdxl": ImageModelConfig(
                    "Fast SDXL",
                    negative_prompt=IMAGE_NEGATIVE_PROMPT,
                    image_size="square_hd",
                    image_sizes=IMAGE_SIZES,
                    guidance_scale=7.5,
                    guidance_scale_range=(0.0, 20.0),
                    num_inference_steps=25,
                    num_inference_steps_range=(1, 50),
                    parameters=[
                        "seed",
                        "negative_prompt",
                        "image_size",
                        "num_inference_steps",
                        "guidance_scale",
                        "expand_prompt",
                    ],
                    kwargs={
                        "num_images": 1,
                        "sync_mode": False,
                        "enable_safety_checker": False,
                        "output_format": "png",
                    },
                ),
                "fal-ai/fast-sdxl/image-to-image": ImageModelConfig(
                    "Fast SDXL (Image)",
                    negative_prompt=IMAGE_NEGATIVE_PROMPT,
                    image_size="square_hd",
                    image_sizes=IMAGE_SIZES,
                    strength=0.95,
                    strength_range=STRENGTH_RANGE,
                    guidance_scale=7.5,
                    guidance_scale_range=(0.0, 20.0),
                    num_inference_steps=25,
                    num_inference_steps_range=(1, 50),
                    parameters=[
                        "seed",
                        "negative_prompt",
                        "image_size",
                        "num_inference_steps",
                        "guidance_scale",
                        "strength",
                        "expand_prompt",
                        "image_url",
                    ],
                    kwargs={
                        "num_images": 1,
                        "sync_mode": False,
                        "enable_safety_checker": False,
                        "output_format": "png",
                    },
                ),
                "fal-ai/flux-pro/v1.1": ImageModelConfig(
                    "FLUX1.1 Pro",
                    parameters=["seed", "image_size"],
                    image_size="square_hd",
                    image_sizes=IMAGE_SIZES,
                    kwargs={
                        "num_images": 1,
                        "sync_mode": False,
                        "safety_tolerance": 6,
                        "enable_safety_checker": False,
                    },
                ),
                "fal-ai/flux-pro": ImageModelConfig(
                    "FLUX.1 Pro",
                    image_size="square_hd",
                    image_sizes=IMAGE_SIZES,
                    guidance_scale=2.5,
                    guidance_scale_range=(1.5, 5.0),
                    num_inference_steps=40,
                    num_inference_steps_range=(10, 50),
                    parameters=["seed", "image_size", "num_inference_steps", "guidance_scale"],
                    kwargs={"num_images": 1, "sync_mode": False, "safety_tolerance": 6},
                ),
                "fal-ai/flux/dev": ImageModelConfig(
                    "FLUX.1 Dev",
                    image_size="square_hd",
                    image_sizes=IMAGE_SIZES,
                    num_inference_steps=28,
                    num_inference_steps_range=(10, 50),
                    guidance_scale=3.0,
                    guidance_scale_range=(1.5, 5.0),
                    parameters=["seed", "image_size", "num_inference_steps", "guidance_scale"],
                    kwargs={"num_images": 1, "sync_mode": False, "enable_safety_checker": False},
                ),
                "fal-ai/flux/dev/image-to-image": ImageModelConfig(
                    "FLUX.1 Dev (Image)",
                    image_size="square_hd",
                    image_sizes=IMAGE_SIZES,
                    strength=0.95,
                    strength_range=STRENGTH_RANGE,
                    num_inference_steps=28,
                    num_inference_steps_range=(10, 50),
                    guidance_scale=3.0,
                    guidance_scale_range=(1.5, 5.0),
                    parameters=[
                        "seed",
                        "image_size",
                        "num_inference_steps",
                        "guidance_scale",
                        "strength",
                        "image_url",
                    ],
                    kwargs={"num_images": 1, "sync_mode": False, "enable_safety_checker": False},
                ),
                "fal-ai/flux/schnell": ImageModelConfig(
                    "FLUX.1 Schnell",
                    image_size="square_hd",
                    image_sizes=IMAGE_SIZES,
                    num_inference_steps=4,
                    num_inference_steps_range=(1, 12),
                    parameters=["seed", "image_size", "num_inference_steps"],
                    kwargs={"num_images": 1, "sync_mode": False, "enable_safety_checker": False},
                ),
                "fal-ai/fooocus": ImageModelConfig(
                    "Fooocus",
                    negative_prompt=FOOOCUS_NEGATIVE_PROMPT,
                    aspect_ratio="1024x1024",
                    aspect_ratios=IMAGE_ASPECT_RATIOS,
                    guidance_scale=4.0,
                    guidance_scale_range=(1.0, 15.0),
                    parameters=["seed", "negative_prompt", "aspect_ratio", "guidance_scale"],
                    # TODO: more of these can be params
                    kwargs={
                        "num_images": 1,
                        "sync_mode": True,
                        "enable_safety_checker": False,
                        "output_format": "png",
                        "sharpness": 2,
                        "styles": ["Fooocus Enhance", "Fooocus V2", "Fooocus Sharp"],
                        "performance": "Quality",
                    },
                ),
                "fal-ai/kolors": ImageModelConfig(
                    "Kolors",
                    negative_prompt=IMAGE_NEGATIVE_PROMPT,
                    image_size="square_hd",
                    image_sizes=IMAGE_SIZES,
                    guidance_scale=5.0,
                    guidance_scale_range=(1.0, 10.0),
                    num_inference_steps=50,
                    num_inference_steps_range=(10, 50),
                    parameters=[
                        "seed",
                        "negative_prompt",
                        "image_size",
                        "guidance_scale",
                        "num_inference_steps",
                    ],
                    kwargs={
                        "num_images": 1,
                        "sync_mode": True,
                        "enable_safety_checker": False,
                        "scheduler": "EulerDiscreteScheduler",
                    },
                ),
                "fal-ai/stable-diffusion-v3-medium": ImageModelConfig(
                    "SD3 Medium",
                    image_size="square_hd",
                    image_sizes=IMAGE_SIZES,
                    guidance_scale=5.0,
                    guidance_scale_range=(1.0, 10.0),
                    num_inference_steps=28,
                    num_inference_steps_range=(10, 50),
                    parameters=[
                        "seed",
                        "negative_prompt",
                        "image_size",
                        "guidance_scale",
                        "num_inference_steps",
                        "prompt_expansion",
                    ],
                    kwargs={"num_images": 1, "sync_mode": True, "enable_safety_checker": False},
                ),
            },
        ),
        "hf": ServiceConfig(
            name="Hugging Face",
            url="https://api-inference.huggingface.co/models",
            api_key=os.environ.get("HF_TOKEN"),
            text={
                "codellama/codellama-34b-instruct-hf": TextModelConfig("Code Llama 34B", **_hf_text_kwargs),
                "meta-llama/llama-2-13b-chat-hf": TextModelConfig("Meta Llama 2 13B", **_hf_text_kwargs),
                "mistralai/mistral-7b-instruct-v0.2": TextModelConfig("Mistral 0.2 7B", **_hf_text_kwargs),
                "nousresearch/nous-hermes-2-mixtral-8x7b-dpo": TextModelConfig(
                    "Nous Hermes 2 Mixtral 8x7B",
                    **_hf_text_kwargs,
                ),
            },
            image={
                "black-forest-labs/flux.1-dev": ImageModelConfig(
                    "FLUX.1 Dev",
                    width=1024,
                    width_range=IMAGE_RANGE,
                    height=1024,
                    height_range=IMAGE_RANGE,
                    guidance_scale=3.0,
                    guidance_scale_range=(1.5, 5.0),
                    num_inference_steps=28,
                    num_inference_steps_range=(10, 50),
                    parameters=["width", "height", "guidance_scale", "num_inference_steps"],
                ),
                "black-forest-labs/flux.1-schnell": ImageModelConfig(
                    "FLUX.1 Schnell",
                    width=1024,
                    width_range=IMAGE_RANGE,
                    height=1024,
                    height_range=IMAGE_RANGE,
                    num_inference_steps=4,
                    num_inference_steps_range=(1, 12),
                    parameters=["width", "height", "num_inference_steps"],
                    kwargs={"guidance_scale": 0.0, "max_sequence_length": 256},
                ),
                "stabilityai/stable-diffusion-xl-base-1.0": ImageModelConfig(
                    "Stable Diffusion XL 1.0",
                    negative_prompt=IMAGE_NEGATIVE_PROMPT,
                    width=1024,
                    width_range=IMAGE_RANGE,
                    height=1024,
                    height_range=IMAGE_RANGE,
                    guidance_scale=7.0,
                    guidance_scale_range=(1.0, 15.0),
                    num_inference_steps=40,
                    num_inference_steps_range=(10, 50),
                    parameters=[
                        "seed",
                        "negative_prompt",
                        "width",
                        "height",
                        "guidance_scale",
                        "num_inference_steps",
                    ],
                ),
            },
        ),
        "openai": ServiceConfig(
            name="OpenAI",
            url="https://api.openai.com/v1",
            api_key=os.environ.get("OPENAI_API_KEY"),
            text={
                "chatgpt-4o-latest": TextModelConfig("ChatGPT-4o", **_openai_text_kwargs),
                "gpt-3.5-turbo": TextModelConfig("GPT-3.5 Turbo", **_openai_text_kwargs),
                "gpt-4-turbo": TextModelConfig("GPT-4 Turbo", **_openai_text_kwargs),
                "gpt-4o": TextModelConfig("GPT-4o", **_openai_text_kwargs),
                "gpt-4o-mini": TextModelConfig("GPT-4o mini", **_openai_text_kwargs),
                "o1-preview": TextModelConfig("o1-preview", **_openai_text_kwargs),
                "o1-mini": TextModelConfig("o1-mini", **_openai_text_kwargs),
            },
        ),
        "pplx": ServiceConfig(
            name="Perplexity",
            url="https://api.perplexity.ai",
            api_key=os.environ.get("PPLX_API_KEY"),
            text={
                "llama-3.1-sonar-small-128k-chat": TextModelConfig(
                    "Sonar Small (Offline)",
                    **_pplx_text_kwargs,
                ),
                "llama-3.1-sonar-large-128k-chat": TextModelConfig(
                    "Sonar Large (Offline)",
                    **_pplx_text_kwargs,
                ),
                "llama-3.1-sonar-small-128k-online": TextModelConfig(
                    "Sonar Small (Online)",
                    **_pplx_text_kwargs,
                ),
                "llama-3.1-sonar-large-128k-online": TextModelConfig(
                    "Sonar Large (Online)",
                    **_pplx_text_kwargs,
                ),
                "llama-3.1-sonar-huge-128k-online": TextModelConfig(
                    "Sonar Huge (Online)",
                    **_pplx_text_kwargs,
                ),
            },
        ),
        # TODO: text models, more image models
        "together": ServiceConfig(
            name="Together",
            url="https://api.together.xyz/v1/images/generations",
            api_key=os.environ.get("TOGETHER_API_KEY"),
            image={
                "black-forest-labs/FLUX.1-schnell-Free": ImageModelConfig(
                    "FLUX.1 Schnell Free",
                    width=1024,
                    width_range=IMAGE_RANGE,
                    height=1024,
                    height_range=IMAGE_RANGE,
                    num_inference_steps=4,
                    num_inference_steps_range=(1, 12),
                    parameters=["model", "seed", "width", "height", "steps"],
                    kwargs={"n": 1},
                ),
            },
        ),
    },
)
