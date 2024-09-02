from types import SimpleNamespace

# txt2txt services
ServicePresets = SimpleNamespace(
    HUGGING_FACE={
        # every service has model and system messages
        "frequency_penalty": 0.0,
        "frequency_penalty_min": -2.0,
        "frequency_penalty_max": 2.0,
        "parameters": ["max_tokens", "temperature", "frequency_penalty", "seed"],
    },
    PERPLEXITY={
        "frequency_penalty": 1.0,
        "frequency_penalty_min": 1.0,
        "frequency_penalty_max": 2.0,
        "parameters": ["max_tokens", "temperature", "frequency_penalty"],
    },
)

# txt2img models
ModelPresets = SimpleNamespace(
    AURA_FLOW={
        "name": "AuraFlow",
        "guidance_scale": 3.5,
        "guidance_scale_min": 1.0,
        "guidance_scale_max": 10.0,
        "num_inference_steps": 28,
        "num_inference_steps_min": 10,
        "num_inference_steps_max": 50,
        "parameters": ["seed", "num_inference_steps", "guidance_scale", "expand_prompt"],
        "kwargs": {"num_images": 1, "sync_mode": False},
    },
    FLUX_DEV={
        "name": "FLUX.1 Dev",
        "num_inference_steps": 28,
        "num_inference_steps_min": 10,
        "num_inference_steps_max": 50,
        "guidance_scale": 3.5,
        "guidance_scale_min": 1.0,
        "guidance_scale_max": 10.0,
        "parameters": ["width", "height", "guidance_scale", "num_inference_steps"],
        "kwargs": {"max_sequence_length": 512},
    },
    FLUX_PRO={
        "name": "FLUX.1 Pro",
        "num_inference_steps": 28,
        "num_inference_steps_min": 10,
        "num_inference_steps_max": 50,
        "guidance_scale": 3.5,
        "guidance_scale_min": 1.0,
        "guidance_scale_max": 10.0,
        "parameters": ["seed", "image_size", "num_inference_steps", "guidance_scale"],
        "kwargs": {"num_images": 1, "sync_mode": False, "safety_tolerance": 6},
    },
    FLUX_SCHNELL={
        "name": "FLUX.1 Schnell",
        "num_inference_steps": 4,
        "num_inference_steps_min": 1,
        "num_inference_steps_max": 8,
        "parameters": ["width", "height", "num_inference_steps"],
        "kwargs": {"guidance_scale": 0.0, "max_sequence_length": 256},
    },
    FOOOCUS={
        "name": "Fooocus",
        "guidance_scale": 4.0,
        "guidance_scale_min": 1.0,
        "guidance_scale_max": 10.0,
        "parameters": ["seed", "negative_prompt", "aspect_ratio", "guidance_scale"],
        "kwargs": {
            "num_images": 1,
            "sync_mode": True,
            "enable_safety_checker": False,
            "output_format": "png",
            "sharpness": 2,
            "styles": ["Fooocus Enhance", "Fooocus V2", "Fooocus Sharp"],
            "performance": "Quality",
        },
    },
    KOLORS={
        "name": "Kolors",
        "guidance_scale": 5.0,
        "guidance_scale_min": 1.0,
        "guidance_scale_max": 10.0,
        "num_inference_steps": 50,
        "num_inference_steps_min": 10,
        "num_inference_steps_max": 50,
        "parameters": [
            "seed",
            "negative_prompt",
            "image_size",
            "guidance_scale",
            "num_inference_steps",
        ],
        "kwargs": {
            "num_images": 1,
            "sync_mode": True,
            "enable_safety_checker": False,
            "scheduler": "EulerDiscreteScheduler",
        },
    },
    STABLE_DIFFUSION_3={
        "name": "SD3",
        "guidance_scale": 5.0,
        "guidance_scale_min": 1.0,
        "guidance_scale_max": 10.0,
        "num_inference_steps": 28,
        "num_inference_steps_min": 10,
        "num_inference_steps_max": 50,
        "parameters": [
            "seed",
            "negative_prompt",
            "image_size",
            "guidance_scale",
            "num_inference_steps",
            "prompt_expansion",
        ],
        "kwargs": {"num_images": 1, "sync_mode": True, "enable_safety_checker": False},
    },
    STABLE_DIFFUSION_XL={
        "name": "SDXL",
        "guidance_scale": 7.0,
        "guidance_scale_min": 1.0,
        "guidance_scale_max": 10.0,
        "num_inference_steps": 40,
        "num_inference_steps_min": 10,
        "num_inference_steps_max": 50,
        "parameters": ["seed", "negative_prompt", "width", "height", "guidance_scale", "num_inference_steps"],
    },
)
