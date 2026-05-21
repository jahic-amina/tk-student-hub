from sqlmodel import SQLModel, Field, UniqueConstraint
from typing import Optional
from datetime import datetime, timezone
import sqlalchemy as sa

class SavedOpportunity(SQLModel, table=True):
    __tablename__ = "saved_opportunities" 
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    ad_id: int = Field(foreign_key="ads.id", index=True)
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": sa.text("CURRENT_TIMESTAMP")}
    )

    __table_args__ = (
        UniqueConstraint("user_id", "ad_id", name="unique_user_opportunity"),
        {"extend_existing": True} 
    )
class SavedOpportunityCreate(SQLModel):

    ad_id: int