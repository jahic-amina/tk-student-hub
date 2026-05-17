from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import sqlalchemy as sa

# 1. Definišemo Enum za tipove (isto kao i prije)
class NotificationType(str, Enum):
    NOVA_PRILIKA = "nova_prilika"
    PROMJENA_STATUSA = "promjena_statusa"
    ROK_ISTICE = "rok_istice"

# 2. Base klasa
class NotificationBase(SQLModel):
    tekst: str
    # Dodajemo sa_type=sa.Enum da baza tačno zna da je ovo ENUM kolona
    tip: NotificationType = Field(sa_type=sa.Enum(NotificationType, name="notification_type"))
    procitano: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id") # Veza sa tvojom tabelom korisnika

# 3. Model tabele u bazi podataka
class Notification(NotificationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Koristimo moderniji i sigurniji način za dobijanje trenutnog vremena u UTC-u
    kreirano: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": sa.text("CURRENT_TIMESTAMP")}
    )

# 4. Shema za kreiranje (Request)
class NotificationCreate(NotificationBase):
    pass

# 5. Shema za djelimično ažuriranje (Update)
class NotificationUpdate(SQLModel):
    tekst: Optional[str] = None
    tip: Optional[NotificationType] = None
    procitano: Optional[bool] = None
    user_id: Optional[int] = None