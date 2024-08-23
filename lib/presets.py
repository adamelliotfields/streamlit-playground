from types import SimpleNamespace

# txt2txt services
ServicePresets = SimpleNamespace(
    Huggingface={
        # every service has model and system messages
        "frequency_penalty": 0.0,
        "frequency_penalty_min": -2.0,
        "frequency_penalty_max": 2.0,
        "parameters": ["max_tokens", "temperature", "frequency_penalty", "seed"],
    },
    Perplexity={
        "frequency_penalty": 1.0,
        "frequency_penalty_min": 1.0,
        "frequency_penalty_max": 2.0,
        "parameters": ["max_tokens", "temperature", "frequency_penalty"],
    },
)

# txt2img models
ModelPresets = SimpleNamespace(
    FLUX_1_DEV={
        "name": "FLUX.1 Dev",
        "num_inference_steps": 30,
        "num_inference_steps_min": 10,
        "num_inference_steps_max": 40,
        "guidance_scale": 3.5,
        "guidance_scale_min": 1.0,
        "guidance_scale_max": 7.0,
        "parameters": ["width", "height", "guidance_scale", "num_inference_steps"],
        "kwargs": {"max_sequence_length": 512},
    },
    FLUX_1_SCHNELL={
        "name": "FLUX.1 Schnell",
        "num_inference_steps": 4,
        "num_inference_steps_min": 1,
        "num_inference_steps_max": 8,
        "parameters": ["width", "height", "num_inference_steps"],
        "kwargs": {"guidance_scale": 0.0, "max_sequence_length": 256},
    },
    STABLE_DIFFUSION_XL={
        "name": "SDXL",
        "guidance_scale": 7.0,
        "guidance_scale_min": 1.0,
        "guidance_scale_max": 15.0,
        "num_inference_steps": 40,
        "num_inference_steps_min": 10,
        "num_inference_steps_max": 50,
        "parameters": ["width", "height", "guidance_scale", "num_inference_steps", "seed", "negative_prompt"],
    },
)
