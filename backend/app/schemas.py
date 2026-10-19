from pydantic import BaseModel, Field, field_validator

class CropInputs(BaseModel):
    N: float = Field(ge=0, le=300, description="Nitrogen content (dataset units)")
    P: float = Field(ge=0, le=300, description="Phosphorus content (dataset units)")
    K: float = Field(ge=0, le=300, description="Potassium content (dataset units)")
    temperature: float = Field(ge=-10, le=60, description="Temperature in Celsius")
    humidity: float = Field(ge=0, le=100, description="Relative humidity percentage")
    ph: float = Field(ge=0, le=14, description="Soil pH")
    rainfall: float = Field(ge=0, le=5000, description="Rainfall in mm")

class KnowledgeQuestion(BaseModel):
    question: str = Field(min_length=5, max_length=1000)

class AdvisoryRequest(CropInputs):
    location: str = Field(default="Not specified", max_length=120)
