from pydantic import BaseModel, Field


class ProcessingConfig(BaseModel):
    """
    Configuration for image preprocessing.

    Each option enables/disables a preprocessing step.
    """

    use_grayscale: bool = Field(
        default=True,
        description="Convert image to grayscale.",
    )

    use_blur: bool = Field(
        default=True,
        description="Apply Gaussian blur to remove noise.",
    )

    use_threshold: bool = Field(
        default=False,
        description="Apply adaptive thresholding.",
    )

    blur_kernel_size: int = Field(
        default=3,
        ge=1,
        description="Gaussian blur kernel size.",
    )

    adaptive_block_size: int = Field(
        default=11,
        ge=3,
        description="Adaptive threshold block size.",
    )

    adaptive_constant: int = Field(
        default=2,
        description="Adaptive threshold constant.",
    )