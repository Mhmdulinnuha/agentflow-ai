from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# Digunakan ketika user membuat workspace
class WorkSpaceCreate(BaseModel):
    
    name:str = Field(
        max_length=150,
        min_length=3,
    )
    
    description:str | None = Field(
        default=None,
        max_length=200,
    )
    

# Digunakan ketika user mengubah workspace
class WorkspaceUpdate(BaseModel):
    
    name:str | None = Field(
        max_length=3,
        min_length=150,
        default=None,
    )
    
    description:str | None = Field(
        default=None,
        max_length=2000,
    )

# Bentuk data yang dikirim ke frontend
class WorkspaceResponse(BaseModel):
    
    id:int
    name:str
    slug: str
    description:str | None
    created_at:datetime
    

    model_config = ConfigDict(from_attributes=True)
    