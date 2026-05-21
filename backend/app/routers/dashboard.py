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
    student_name = getattr(current_user, "full_name", None) or current_user.email

    profile_completion_items = [
        {
            "label": "Ime i prezime",
            "completed": bool(getattr(current_user, "full_name", None)),
        },
        {
            "label": "Biografija",
            "completed": bool(getattr(current_user, "biografija", None)),
        },
        {
            "label": "Profilna slika",
            "completed": bool(getattr(current_user, "profilna_slika_url", None)),
        },
    ]

    completed_profile_items = sum(
        1 for item in profile_completion_items if item["completed"]
    )

    profile_completion_percent = int(
        (completed_profile_items / len(profile_completion_items)) * 100
    )

    return {
        "student": {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": student_name,
            "role": current_user.role,
            "created_at": current_user.created_at,
            "profilna_slika_url": getattr(current_user, "profilna_slika_url", None),
            "biografija": getattr(current_user, "biografija", None),
            "godina_studija": getattr(current_user, "godina_studija", None),
        },
        "profile_status": {
            "completion_percent": profile_completion_percent,
            "items": profile_completion_items,
        },
        "student_overview": {
            "title": "Pregled za danas",
            "message": "Dobrodošao/la nazad. Ovdje možeš brzo vidjeti stanje profila i nastaviti sa najvažnijim studentskim aktivnostima.",
            "items": [
                {
                    "title": "Profil",
                    "value": f"{profile_completion_percent}%",
                    "description": "popunjenost profila",
                },
                {
                    "title": "Status naloga",
                    "value": "Aktivan",
                    "description": "nalog je spreman za korištenje",
                },
                {
                    "title": "Uloga",
                    "value": current_user.role,
                    "description": "trenutna korisnička uloga",
                },
            ],
        },
        "next_steps": [
            {
                "title": "Dopuni profil",
                "description": "Dodaj biografiju, godinu studija i profilnu sliku kako bi tvoj nalog bio potpuniji.",
                "path": "/profile",
                "priority": "visok",
            },
            {
                "title": "Provjeri studentske prilike",
                "description": "Pogledaj prakse, edukacije ili stipendije koje bi mogle biti korisne za tvoj razvoj.",
                "path": "/prakse-i-edukacije",
                "priority": "srednji",
            },
            {
                "title": "Nastavi učenje",
                "description": "Ako tražiš materijale, koristi sekciju materijala iz glavne navigacije.",
                "path": "/materials",
                "priority": "srednji",
            },
        ],
        "reminders": [
            "Ažuriraj profil ako su tvoji podaci promijenjeni.",
            "Provjeri da li ima novih studentskih prilika.",
            "Prati forum za pitanja kolega i korisne odgovore.",
        ],
        "activity": {
            "title": "Moja aktivnost",
            "empty_message": "Još nema evidentiranih aktivnosti. Kada budeš koristio/la materijale, forum ili prakse, ovdje će se prikazati kratki pregled.",
            "items": [],
        },
    }