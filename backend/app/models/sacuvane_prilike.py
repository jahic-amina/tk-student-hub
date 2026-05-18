from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import sqlalchemy as sa

# 1. Base klasa za validaciju podataka
class SacuvanaPrilikaBase(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    oglas_id: int = Field(foreign_key="oglasi.id")

# 2. Glavni model za tabelu u bazi (Sada će se tabela automatski zvati "sacuvana_prilika")
class SacuvanaPrilika(SacuvanaPrilikaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    datum: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": sa.text("CURRENT_TIMESTAMP")}
    )

# 3. Shema za kreiranje
class SacuvanaPrilikaCreate(SacuvanaPrilikaBase):
    pass

# 4. Shema za izmjene
class SacuvanaPrilikaUpdate(SQLModel):
    user_id: Optional[int] = None
    oglas_id: Optional[int] = None