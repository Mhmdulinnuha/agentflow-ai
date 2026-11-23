from datetime import datetime 
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

# Digunakan ketika menambahkan anggota workspace
class WorkspaceMemberCreate(BaseModel):
    user_id: int= Field(
        gt=0,
    )
    
    role:Literal["owner", "admin", "member"] = "member"
    
# Bentuk data anggota yang dikirim ke frontend
class WorkspaceMemberResponse(BaseModel):
    id: int
    workspace_id:int
    user_id:int
    role:Literal["owner", "admin", "member"]
    joined_at:datetime
    
    model_config = ConfigDict(from_attributes=True)