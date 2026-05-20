from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    ______Moguće izmjene________
    Vraća personalizovane podatke za dashboard trenutno prijavljenog korisnika.

    Dashboard uključuje:
    - osnovne informacije o korisniku,
    - sažetak aktivnosti,
    - liste aktivnosti korisnika,
    - relevantne sekcije platforme.
    """

    user_activity = {
        "materials": [],
        "opportunities": [],
        "forum": [],
    }

    return {
        "student": {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role,
            "created_at": current_user.created_at,
            "profilna_slika_url": getattr(current_user, "profilna_slika_url", None),
            "biografija": getattr(current_user, "biografija", None),
            "godina_studija": getattr(current_user, "godina_studija", None),
        },
        "summary": {
            "materials_count": len(user_activity["materials"]),
            "opportunities_count": len(user_activity["opportunities"]),
            "forum_activity_count": len(user_activity["forum"]),
        },
        "activity": user_activity,
        "relevant_content": [
            {
                "title": "Prakse i edukacije",
                "description": "Pregled dostupnih praksi, stipendija i edukativnih programa.",
                "path": "/prakse-i-edukacije",
            },
            {
                "title": "Materijali",
                "description": "Brzi pristup dostupnim materijalima za učenje.",
                "path": "/materials",
            },
            {
                "title": "Forum",
                "description": "Pregled pitanja, tema i aktivnosti na forumu.",
                "path": "/forum",
            },
        ],
    }