from pydantic import BaseModel, EmailStr, Field

class LeadInput(BaseModel):
    """Defines the input data structure for a new lead."""
    Email: EmailStr
    CreditScore: int = Field(..., ge=300, le=850, description="Credit score between 300 and 850.")
    AgeGroup: str
    FamilyBackground: str
    Income: int = Field(..., ge=0, description="Income must be a non-negative number.")
    LeadSource: str
    TimeOnPage: int = Field(..., ge=0)
    PagesVisited: int = Field(..., ge=0)
    Comments: str = ""

class LeadOutput(BaseModel):
    """Defines the output data structure after scoring."""
    Email: EmailStr
    InitialScore: int = Field(..., ge=0, le=100)
    RerankedScore: int = Field(..., ge=0, le=100)
    Comments: str