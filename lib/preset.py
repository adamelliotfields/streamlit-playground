from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class Txt2TxtPreset:
    name: str
    frequency_penalty: float
    frequency_penalty_min: float
    frequency_penalty_max: float
    parameters: Optional[List[str]] = field(default_factory=list)


@dataclass
class Txt2ImgPreset:
    name: str
    guidance_scale: Optional[float] = None
    guidance_scale_min: Optional[float] = None
    guidance_scale_max: Optional[float] = None
    num_inference_steps: Optional[int] = None
    num_inference_steps_min: Optional[int] = None
    num_inference_steps_max: Optional[int] = None
    parameters: Optional[List[str]] = field(default_factory=list)
    kwargs: Optional[Dict[str, Union[str, int, float, bool]]] = field(default_factory=dict)


@dataclass
class Preset:
    txt2txt: Dict[str, Txt2TxtPreset]
    txt2img: Dict[str, Txt2ImgPreset]


hf_txt2txt_kwargs = {
    "frequency_penalty": 0.0,
    "frequency_penalty_min": -2.0,
    "frequency_penalty_max": 2.0,
    "parameters": ["max_tokens", "temperature", "frequency_penalty", "seed"],
}

pplx_txt2txt_kwargs = {
    "frequency_penalty": 1.0,
    "frequency_penalty_min": 1.0,
    "frequency_penalty_max": 2.0,
    "parameters": ["max_tokens", "temperature", "frequency_penalty"],
}


preset = Preset(
    txt2txt={
        "hf": {
            # TODO: update models
            "codellama/codellama-34b-instruct-hf": Txt2TxtPreset("Code Llama 34B", **hf_txt2txt_kwargs),
            "meta-llama/llama-2-13b-chat-hf": Txt2TxtPreset("Llama 2 13B", **hf_txt2txt_kwargs),
            "mistralai/mistral-7b-instruct-v0.2": Txt2TxtPreset("Mistral v0.2 7B", **hf_txt2txt_kwargs),
            "nousresearch/nous-hermes-2-mixtral-8x7b-dpo": Txt2TxtPreset(
                "Nous Hermes 2 Mixtral 8x7B",
                **hf_txt2txt_kwargs,
            ),
        },
        "pplx": {
            "llama-3.1-sonar-small-128k-chat": Txt2TxtPreset("Sonar Small (Offline)", **pplx_txt2txt_kwargs),
            "llama-3.1-sonar-large-128k-chat": Txt2TxtPreset("Sonar Large (Offline)", **pplx_txt2txt_kwargs),
            "llama-3.1-sonar-small-128k-online": Txt2TxtPreset("Sonar Small (Online)", **pplx_txt2txt_kwargs),
            "llama-3.1-sonar-large-128k-online": Txt2TxtPreset("Sonar Large (Online)", **pplx_txt2txt_kwargs),
            "llama-3.1-sonar-huge-128k-online": Txt2TxtPreset("Sonar Huge (Online)", **pplx_txt2txt_kwargs),
        },
    },
    txt2img={
        "bfl": {
            "flux-pro-1.1": Txt2ImgPreset(
                "FLUX1.1 Pro",
                parameters=["seed", "width", "height", "prompt_upsampling"],
                kwargs={"safety_tolerance": 6},
            ),
            "flux-pro": Txt2ImgPreset(
                "FLUX.1 Pro",
                guidance_scale=2.5,
                guidance_scale_min=1.5,
                guidance_scale_max=5.0,
                num_inference_steps=40,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                parameters=["seed", "width", "height", "steps", "guidance", "prompt_upsampling"],
                kwargs={"safety_tolerance": 6, "interval": 1},
            ),
            "flux-dev": Txt2ImgPreset(
                "FLUX.1 Dev",
                num_inference_steps=28,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                guidance_scale=3.0,
                guidance_scale_min=1.5,
                guidance_scale_max=5.0,
                parameters=["seed", "width", "height", "steps", "guidance", "prompt_upsampling"],
                kwargs={"safety_tolerance": 6},
            ),
        },
        "fal": {
            "fal-ai/aura-flow": Txt2ImgPreset(
                "AuraFlow",
                guidance_scale=3.5,
                guidance_scale_min=1.0,
                guidance_scale_max=10.0,
                num_inference_steps=28,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                parameters=["seed", "num_inference_steps", "guidance_scale", "expand_prompt"],
                kwargs={"num_images": 1, "sync_mode": False},
            ),
            "fal-ai/flux-pro/v1.1": Txt2ImgPreset(
                "FLUX1.1 Pro",
                parameters=["seed", "image_size"],
                kwargs={
                    "num_images": 1,
                    "sync_mode": False,
                    "safety_tolerance": 6,
                    "enable_safety_checker": False,
                },
            ),
            "fal-ai/flux-pro": Txt2ImgPreset(
                "FLUX.1 Pro",
                guidance_scale=2.5,
                guidance_scale_min=1.5,
                guidance_scale_max=5.0,
                num_inference_steps=40,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                parameters=["seed", "image_size", "num_inference_steps", "guidance_scale"],
                kwargs={"num_images": 1, "sync_mode": False, "safety_tolerance": 6},
            ),
            "fal-ai/flux/dev": Txt2ImgPreset(
                "FLUX.1 Dev",
                num_inference_steps=28,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                guidance_scale=3.0,
                guidance_scale_min=1.5,
                guidance_scale_max=5.0,
                parameters=["seed", "image_size", "num_inference_steps", "guidance_scale"],
                kwargs={"num_images": 1, "sync_mode": False, "safety_tolerance": 6},
            ),
            "fal-ai/flux/schnell": Txt2ImgPreset(
                "FLUX.1 Schnell",
                num_inference_steps=4,
                num_inference_steps_min=1,
                num_inference_steps_max=12,
                parameters=["seed", "image_size", "num_inference_steps"],
                kwargs={"num_images": 1, "sync_mode": False, "enable_safety_checker": False},
            ),
            "fal-ai/fooocus": Txt2ImgPreset(
                "Fooocus",
                guidance_scale=4.0,
                guidance_scale_min=1.0,
                guidance_scale_max=10.0,
                parameters=["seed", "negative_prompt", "aspect_ratio", "guidance_scale"],
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
            "fal-ai/kolors": Txt2ImgPreset(
                "Kolors",
                guidance_scale=5.0,
                guidance_scale_min=1.0,
                guidance_scale_max=10.0,
                num_inference_steps=50,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                parameters=["seed", "negative_prompt", "image_size", "guidance_scale", "num_inference_steps"],
                kwargs={
                    "num_images": 1,
                    "sync_mode": True,
                    "enable_safety_checker": False,
                    "scheduler": "EulerDiscreteScheduler",
                },
            ),
            "fal-ai/stable-diffusion-v3-medium": Txt2ImgPreset(
                "SD3",
                guidance_scale=5.0,
                guidance_scale_min=1.0,
                guidance_scale_max=10.0,
                num_inference_steps=28,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
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
        "hf": {
            "black-forest-labs/flux.1-dev": Txt2ImgPreset(
                "FLUX.1 Dev",
                num_inference_steps=28,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                guidance_scale=3.0,
                guidance_scale_min=1.5,
                guidance_scale_max=5.0,
                parameters=["width", "height", "guidance_scale", "num_inference_steps"],
                kwargs={"max_sequence_length": 512},
            ),
            "black-forest-labs/flux.1-schnell": Txt2ImgPreset(
                "FLUX.1 Schnell",
                num_inference_steps=4,
                num_inference_steps_min=1,
                num_inference_steps_max=12,
                parameters=["width", "height", "num_inference_steps"],
                kwargs={"guidance_scale": 0.0, "max_sequence_length": 256},
            ),
            "stabilityai/stable-diffusion-xl-base-1.0": Txt2ImgPreset(
                "SDXL",
                guidance_scale=7.0,
                guidance_scale_min=1.0,
                guidance_scale_max=10.0,
                num_inference_steps=40,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
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
        "together": {
            "black-forest-labs/FLUX.1-schnell-Free": Txt2ImgPreset(
                "FLUX.1 Schnell Free",
                num_inference_steps=4,
                num_inference_steps_min=1,
                num_inference_steps_max=12,
                parameters=["model", "seed", "width", "height", "steps"],
                kwargs={"n": 1},
            ),
        },
    },
)
