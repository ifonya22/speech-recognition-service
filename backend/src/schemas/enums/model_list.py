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
            ModelList.BASE: "1 GB",
            ModelList.SMALL: "2 GB",
            ModelList.MEDIUM: "5 GB",
            ModelList.LARGE: "10 GB",
            ModelList.TURBO: "6 GB",
        }
