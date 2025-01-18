from enum import Enum


class ModelList(Enum):
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    TURBO = "turbo"

    def get_models_required_vram():
        return {
            ModelList.TINY: "1 GB",
            "base": "1 GB",
            "small": "2 GB",
            "medium": "5 GB",
            "large": "10 GB",
            "turbo": "6 GB",
        }
