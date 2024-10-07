from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class Txt2TxtPreset:
    frequency_penalty: float
    frequency_penalty_min: float
    frequency_penalty_max: float
    parameters: Optional[List[str]] = field(default_factory=list)


@dataclass
class Txt2ImgPreset:
    # FLUX1.1 has no scale or steps
    name: str
    service: str
    model_id: str
    guidance_scale: Optional[float] = None
    guidance_scale_min: Optional[float] = None
    guidance_scale_max: Optional[float] = None
    num_inference_steps: Optional[int] = None
    num_inference_steps_min: Optional[int] = None
    num_inference_steps_max: Optional[int] = None
    parameters: Optional[List[str]] = field(default_factory=list)
    kwargs: Optional[Dict[str, Union[str, int, float, bool]]] = field(default_factory=dict)


@dataclass
class Txt2TxtPresets:
    hugging_face: Txt2TxtPreset
    perplexity: Txt2TxtPreset


@dataclass
class Txt2ImgPresets:
    presets: List[Txt2ImgPreset] = field(default_factory=list)

    def __iter__(self):
        return iter(self.presets)


@dataclass
class Preset:
    txt2txt: Txt2TxtPresets
    txt2img: Txt2ImgPresets


preset = Preset(
    txt2txt=Txt2TxtPresets(
        hugging_face=Txt2TxtPreset(
            frequency_penalty=0.0,
            frequency_penalty_min=-2.0,
            frequency_penalty_max=2.0,
            parameters=["max_tokens", "temperature", "frequency_penalty", "seed"],
        ),
        perplexity=Txt2TxtPreset(
            frequency_penalty=1.0,
            frequency_penalty_min=1.0,
            frequency_penalty_max=2.0,
            parameters=["max_tokens", "temperature", "frequency_penalty"],
        ),
    ),
    txt2img=Txt2ImgPresets(
        presets=[
            Txt2ImgPreset(
                "AuraFlow",
                "Fal",
                "fal-ai/aura-flow",
                guidance_scale=3.5,
                guidance_scale_min=1.0,
                guidance_scale_max=10.0,
                num_inference_steps=28,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                parameters=["seed", "num_inference_steps", "guidance_scale", "expand_prompt"],
                kwargs={"num_images": 1, "sync_mode": False},
            ),
            Txt2ImgPreset(
                "FLUX1.1 Pro",
                "Black Forest Labs",
                "flux-pro-1.1",
                parameters=["seed", "width", "height", "prompt_upsampling"],
                kwargs={"safety_tolerance": 6},
            ),
            Txt2ImgPreset(
                "FLUX.1 Pro",
                "Black Forest Labs",
                "flux-pro",
                guidance_scale=2.5,
                guidance_scale_min=1.5,
                guidance_scale_max=5.0,
                num_inference_steps=40,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                parameters=["seed", "width", "height", "steps", "guidance", "prompt_upsampling"],
                kwargs={"safety_tolerance": 6, "interval": 1},
            ),
            Txt2ImgPreset(
                "FLUX.1 Dev",
                "Black Forest Labs",
                "flux-dev",
                num_inference_steps=28,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                guidance_scale=3.0,
                guidance_scale_min=1.5,
                guidance_scale_max=5.0,
                parameters=["seed", "width", "height", "steps", "guidance", "prompt_upsampling"],
                kwargs={"safety_tolerance": 6},
            ),
            Txt2ImgPreset(
                "FLUX1.1 Pro",
                "Fal",
                "fal-ai/flux-pro/v1.1",
                parameters=["seed", "image_size"],
                kwargs={
                    "num_images": 1,
                    "sync_mode": False,
                    "safety_tolerance": 6,
                    "enable_safety_checker": False,
                },
            ),
            Txt2ImgPreset(
                "FLUX.1 Pro",
                "Fal",
                "fal-ai/flux-pro",
                guidance_scale=2.5,
                guidance_scale_min=1.5,
                guidance_scale_max=5.0,
                num_inference_steps=40,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                parameters=["seed", "image_size", "num_inference_steps", "guidance_scale"],
                kwargs={"num_images": 1, "sync_mode": False, "safety_tolerance": 6},
            ),
            Txt2ImgPreset(
                "FLUX.1 Dev",
                "Fal",
                "fal-ai/flux/dev",
                num_inference_steps=28,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                guidance_scale=3.0,
                guidance_scale_min=1.5,
                guidance_scale_max=5.0,
                parameters=["seed", "image_size", "num_inference_steps", "guidance_scale"],
                kwargs={"num_images": 1, "sync_mode": False, "safety_tolerance": 6},
            ),
            Txt2ImgPreset(
                "FLUX.1 Schnell",
                "Fal",
                "fal-ai/flux/schnell",
                num_inference_steps=4,
                num_inference_steps_min=1,
                num_inference_steps_max=12,
                parameters=["seed", "image_size", "num_inference_steps"],
                kwargs={"num_images": 1, "sync_mode": False, "enable_safety_checker": False},
            ),
            Txt2ImgPreset(
                "FLUX.1 Dev",
                "Hugging Face",
                "black-forest-labs/flux.1-dev",
                num_inference_steps=28,
                num_inference_steps_min=10,
                num_inference_steps_max=50,
                guidance_scale=3.0,
                guidance_scale_min=1.5,
                guidance_scale_max=5.0,
                parameters=["width", "height", "guidance_scale", "num_inference_steps"],
                kwargs={"max_sequence_length": 512},
            ),
            Txt2ImgPreset(
                "FLUX.1 Schnell",
                "Hugging Face",
                "black-forest-labs/flux.1-schnell",
                num_inference_steps=4,
                num_inference_steps_min=1,
                num_inference_steps_max=12,
                parameters=["width", "height", "num_inference_steps"],
                kwargs={"guidance_scale": 0.0, "max_sequence_length": 256},
            ),
            Txt2ImgPreset(
                "FLUX.1 Schnell Free",
                "Together",
                "black-forest-labs/FLUX.1-schnell-Free",
                num_inference_steps=4,
                num_inference_steps_min=1,
                num_inference_steps_max=12,
                parameters=["model", "seed", "width", "height", "steps"],
                kwargs={"n": 1},
            ),
            Txt2ImgPreset(
                "Fooocus",
                "Fal",
                "fal-ai/fooocus",
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
            Txt2ImgPreset(
                "Kolors",
                "Fal",
                "fal-ai/kolors",
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
            Txt2ImgPreset(
                "SD3",
                "Fal",
                "fal-ai/stable-diffusion-v3-medium",
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
            Txt2ImgPreset(
                "SDXL",
                "Hugging Face",
                "stabilityai/stable-diffusion-xl-base-1.0",
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
        ]
    ),
)
