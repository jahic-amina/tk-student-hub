from datetime import date, datetime, timedelta, timezone
from sqlmodel import SQLModel, Session, select

from app.core.security import hash_password
from app.database import create_db_and_tables, engine
from app.models.user import User, UserRole
from app.models.company import Company, CompanyStatus
from app.models.ad import Ad, AdStatus, AdType
from app.models.application import Application, ApplicationStatus
from app.models.notification import Notification, NotificationType
from app.models.ad_bookmark import AdBookmark
from app.models.forum import (
    ForumCategory,
    ForumTopic,
    ForumComment,
    ForumTag,
    ForumTopicTag,
    ForumCommentVote,
)
from app.models.forum_reputation import (
    ForumUserStats,
    ForumUserMedal,
    ForumReputationEvent
)

# ---------------------------------------------------------------------------
# Forum seed data & categories
# ---------------------------------------------------------------------------

FORUM_CATEGORIES = [
    {"name": "Opšta diskusija", "color": "#ff7a00", "description": "Opšte teme vezane za studij i studentski život."},
    {"name": "Pomoć sa predmetima", "color": "#2563eb", "description": "Pitanja, objašnjenja i pomoć oko predmeta."},
    {"name": "Studijske grupe", "color": "#16a34a", "description": "Organizacija grupa za učenje i pripremu ispita."},
    {"name": "Praksa i posao", "color": "#9333ea", "description": "Diskusije o praksama, poslovima i karijeri."},
    {"name": "Projekti", "color": "#dc2626", "description": "Ideje, pitanja i pomoć oko studentskih projekata."},
    {"name": "Off-Topic", "color": "#6b7280", "description": "Neformalne teme i razgovori van nastave."},
]

# Realistične teme po kategoriji
FORUM_TOPICS_DATA = {
    "Opšta diskusija": [
        {"title": "Kako se organiziraju studijske obveze tokom zimskog semestra?", "content": "Koja je najbolja strategija za balansiranje predmeta tokom zimskog semestra? Koji redoslijed izrade seminarskih radova preporučujete?"},
        {"title": "Najbolje aplikacije za organizaciju studija", "content": "Koje aplikacije koristite za praćenje rokova i organizaciju vremena? Treba mi nešto bolje od Excel-a za raspodjelu vremena između predmeta."},
        {"title": "Iskustva studenata sa promjenom smjera tokom studija", "content": "Razmišljam o promjeni smjera. Koji su vam bili razlozi, i kako je to uticalo na vaš plan studija?"},
        {"title": "Kako balansirati rad i studije?", "content": "Neki od nas mora da radi tijekom studija. Kako ste vi to uspjeli? Koji poslovi su fleksibilni za studente?"},
        {"title": "Fakultetske vrijednosti i akademska zajednica", "content": "Šta vam je privuklo na ovaj fakultet? Kako se osjećate kao dio akademske zajednice?"},
        {"title": "Savjeti za bolju organizaciju učenja prije ispita", "content": "Ima li nekog ko je pronašao savršen način za poslednju nedelju prije ispita? Kakav je bio vaš pristup?"},
        {"title": "Izkustva sa mentorima i asistentima", "content": "Koji su vam asistenti/mentori bili najviše korisni? Kako vam je pomogla njihova podrška?"},
        {"title": "Kako se nosite sa akademskim stresom?", "content": "Visoki zahtjevi fakulteta mogu biti teški. Kako se vi suočavate sa stresom i nervozom?"},
        {"title": "Moja prva godina - šta bi trebalo da znam?", "content": "Stupam na fakultet sljedeće godine. Koji su ključni savjeti koje ste vi željeli da znate kada ste počeli?"},
        {"title": "Alumni networking - kako se održati u kontaktu?", "content": "Kako se održava kontakt sa starijim generacijama studenata? Koja je uloga alumni zajednice?"},
        {"title": "Prednosti i nedostaci online nastave", "content": "Koje su bile vaše iskustva sa online predavanjima? Je li to bilo bolje ili gore nego fizička nastava?"},
        {"title": "Interdisciplinarni projekti i suradnja", "content": "Trebalo bi više suradnje između različitih smjerova. Kako bi to moglo biti organizirano?"},
        {"title": "Kako riješiti problem sa nejasnošću na predavanjima?", "content": "Ponekad predavanja nisu dovoljno jasna. Na koje načine se obično obraćate za pojašnjenja?"},
        {"title": "Fakultetski događaji i aktivnosti koje ste propustili", "content": "Koji su vam bili najbolji fakultetski događaji? Koje aktivnosti preporučujete novim studentima?"},
        {"title": "Kako se uklapate u studentsku zajednicu?", "content": "Bili ste introvertni ili ekstrovertni? Kako ste se povezali sa drugim studentima?"},
        {"title": "Preporuke za dobrog tutora ili dodatne instrakcije", "content": "Trebam pomoć sa nekim predmetima. Gdje ste vi pronašli kvalitetnu dodatnu nastavu?"},
        {"title": "Kako se nosite sa drugim obavezama pored fakulteta?", "content": "Koje su bili vaše hobi ili aktivnosti pored fakulteta? Kako ste ih kombinirali sa studijama?"},
        {"title": "Refleksija na sredinu semestra - kako ste do sada?", "content": "Ovdje je sredina semestra. Kako ste zadovoljni sa svojim napretkom? Šta trebate da popravite?"},
        {"title": "Zahtjevi za infrastrukturu fakulteta - šta se trebalo da popravi?", "content": "Što bi trebalo biti poboljšano na fakultetu? Infrastruktura, knjižnica, računarske učionice?"},
        {"title": "Kako izabrati izborne predmete koji će vam zaista trebati?", "content": "Koji su izborni predmeti koje preporučujete? Kako ste vi brinuli za budući karijerni put?"},
    ],
    
    "Pomoć sa predmetima": [
        {"title": "Objašnjenje Fourierove transformacije - gdje početi?", "content": "Ne razumijem Fourierovu transformaciju. Koja je intuicija iza toga? Mogu li to vidjeti grafički?", "tags": ["fourier", "matematika"]},
        {"title": "Problem sa integralima - L'Hôpitalov teorem", "content": "Kada trebam da koristim L'Hôpitalov teorem? U kojim slučajevima je sigurno ga primijeniti?", "tags": ["matematika"]},
        {"title": "Linearna algebra: razumijevanje svojstvenih vrijednosti", "content": "Šta zapravo predstavljaju svojstvene vrijednosti? Zašto su bitne u praksi?", "tags": ["matematika"]},
        {"title": "Diferencijalne jednačine - kako početi sa separacijom varijabli?", "content": "Mogu li neko da objasni logiku iza separacije varijabli u diferencijalnim jednačinama?", "tags": ["matematika"]},
        {"title": "Kompleksni brojevi - rotacije u kompleksnoj ravni", "content": "Kako kompleksni brojevi predstavljaju rotacije? Koja je veza sa trigonometrijom?", "tags": ["matematika"]},
        {"title": "Programiranje: rekurzija - kako razmišljati o njoj?", "content": "Uvijek mi je teško razmišljati rekurzivno. Kako da prepravim svoj mentalni model?", "tags": ["programiranje"]},
        {"title": "Baze podataka: normalizacija - do kojeg oblika trebam?", "content": "Trebam pojašnjenje razlike između 1NF, 2NF, 3NF. Koji je praktičan nivo?", "tags": ["programiranje"]},
        {"title": "Web razvoj: razlika između REST-a i GraphQL", "content": "Kada trebam koristiti REST a kada GraphQL? Kakve su prave razlike?", "tags": ["programiranje"]},
        {"title": "OOP koncepti: polimorfizam objašnjen jednostavno", "content": "Polimorfizam mi je uvijek bio zbunjujući. Mogu li ga vidjeti na praktičnom primjeru?", "tags": ["programiranje"]},
        {"title": "Fizika: Newtonov zakon gravitacije - derivacija", "content": "Gdje dolazi formula F=GMm/r²? Koja je teorijska osnova?", "tags": ["matematika"]},
        {"title": "Kemija: redoks reaktivnost - kako razumjeti?", "content": "Kako da razumijem kada će neka supstanca biti oksidovana ili reducirana?", "tags": ["matematika"]},
        {"title": "Energija i rad: razlika između koncepta", "content": "Šta je točno razlika između rada i energije? Kako se računaju?", "tags": ["matematika"]},
        {"title": "Algoritmi: Big O notacija - zašto je bitna?", "content": "Trebam dobro razumijevanje Big O notacije. Koja je praktična primjena?", "tags": ["programiranje"]},
        {"title": "Termodinamika: entropija - što je zaista?", "content": "Entropija mi nije jasna. Je li samo mjera haosa ili nešto više?", "tags": ["matematika"]},
        {"title": "Teorija brojeva: Euklidov algoritam - kako funkcioniše?", "content": "Kako Euklidov algoritam pronalazi NZD? Matematika iza toga?", "tags": ["matematika"]},
        {"title": "SQL JOIN naredbe - koja je razlika između tipova?", "content": "INNER, LEFT, RIGHT, FULL joins... Kada trebam šta koristiti?", "tags": ["programiranje"]},
        {"title": "Statistika: standardna devijacija - intuitivno objašnjenje", "content": "Šta mi zapravo govori standardna devijacija o podacima?", "tags": ["matematika"]},
        {"title": "Logika i dokazi: proof by contradiction - kako funkcioniše?", "content": "Kada je dobar trenutak da koristim proof by contradiction?", "tags": ["matematika"]},
        {"title": "Calculus: integral vs derivacija - što je šta?", "content": "Koliko puta da premislim - integrali su obrnuto od derivacija, ali šta to znači?", "tags": ["matematika"]},
        {"title": "Mašinsko učenje: šta je zapravo loss funkcija?", "content": "Koja je uloga loss funkcije u treniranju modela? Kako se bira?", "tags": ["programiranje"]},
    ],
    
    "Studijske grupe": [
        {"title": "Matematika - Fourierova analiza - Nedjelja 19:00 Knjižnica", "content": "Organizujem grupu za učenje Fourierove analize. Trebam 3-4 osobe koje su zainteresirane za detaljnije razumijevanje. Nasljeđivanje je ponedeljak!"},
        {"title": "Programiranje Python - osnove za početnike", "content": "Grupa za početnike u Pythonu. Počinjemo od nule. Svaku četvrtak 18:00 u učionici 204. Svi su dobrodošli!"},
        {"title": "Priprema za ispit iz Baza podataka - Septembar", "content": "Ko se sprema za resit iz Baza podataka? Trebam barem 5-6 osoba. Plan: teorija srijedom, vježbe petkom."},
        {"title": "Web razvoj - React tutorial - Tuzla", "content": "Neko da se javi ako želi da korepetira React sa mnom? Imam iskustvo i materijale. Prema dogovoru vrijeme."},
        {"title": "Studijska grupa - Linearna algebra - Intenzivna priprema", "content": "Intenzivna studijska grupa prije ispita. Trebam 4-5 osoba koje su ozbiljne. Smiješno je što je većina od nas u problemu, pa hajde zajedno!"},
        {"title": "Zajedničko učenje - Fizika za sve", "content": "Grupu pokrećem za sve koji se bore sa fizikom. Bez osude, samo učenja. Ako znate više - pomognite drugima!"},
        {"title": "Engleski jezik - razgovor i gramatika", "content": "Trebam grupu za engleski. Fokus na razgovor i pisanje. Nadam se da će se jedan od vas izjasniti kao native speaker!"},
        {"title": "Kemija - organsku kemiju trebam sažeti", "content": "Trebam pomoć sa organskom kemijom. Neko od vas je sigurno u sličnoj situaciji. Hajde zajedno da riješimo zadatke!"},
        {"title": "Diskretna matematika - kombinatorika je noćna mora", "content": "Koji je najjednostavniji način da se nauči kombinatorika? Trebam grupu koja će biti strpljiva sa mnom."},
        {"title": "Algoritmi i strukture podataka - redovna grupa", "content": "Redovna studijska grupa tokom semestra. Svaki petak poslijepodne. Radi se na zadacima iz koda."},
        {"title": "Mikroekonimija - grafikoni i funkcije", "content": "Mikro je čista matematika. Trebam grupa koja razumije grafikone. Neke od tema je zaista strašno vizuelizirati."},
        {"title": "Makroekonomija - globalni ekonomski trendovi", "content": "Interesuje nas veza između teorije i realnog svijeta. Trebam 3-4 osobe za diskusiju."},
        {"title": "Operacijska istraživanja - linearno programiranje", "content": "Trebam pomoć sa simplex metodom. Neko od vas je to već sažvatio?"},
        {"title": "Vjerojatnost i statistika - test dijeljenjem teorije", "content": "Grupa koja će razumjeti vjerojatnost kao koncept, ne samo formule. Realnost je čudna!"},
        {"title": "Teorija grafova - priprema za ispit", "content": "Teorija grafova ima puno svojstava za pamćenje. Trebam grupa koja će to racionalizirati."},
        {"title": "Analiza algoritama - Big O i kompleksnost", "content": "Trebam grupu da razumjem analizu. Čini se komplikovano, ali sigurno postoji pattern."},
        {"title": "Objektno orijentisano programiranje - dizajn paterni", "content": "Design patterns su konceptualno teški. Trebam grupa od 4-5 osoba za detaljnu diskusiju."},
        {"title": "Baze podataka - normalizacija i SQL performanse", "content": "Neko sa iskustvom u bazama? Trebam pomoć sa optimizacijom."},
        {"title": "Sigurnost informacija - kriptografija osnove", "content": "Kriptografija je fascinantna ali teška. Trebam grupa da pronađe intuiciju."},
        {"title": "Cloud computing - AWS osnovni kursevi", "content": "Trebam grupa za učenje AWS-a. Nasljeđivanje nije malo, ali zajedno je lakše!"},
    ],
    
    "Projekti": [
        {"title": "Semestralski projekt - Web aplikacija za upravljanje vremenom", "content": "Trebam 2-3 člana tima za projekt upravljanja vremenom. Frontend, Backend, Design. Ideja je solida, imamo specifikaciju.", "tags": ["programiranje"]},
        {"title": "IoT projekt - pametni dom - tražim članove", "content": "Trebam inženjere za IoT projekt pametnog doma. Imamo Arduino setove i viziju. Trebam programere za backend.", "tags": ["programiranje"]},
        {"title": "Mobilna aplikacija - fitnes tracker", "content": "Trebam Flutter ili Kotlin razvijače. Projekt je za prikupljanje podataka o fitnesu i njihovu analizu.", "tags": ["programiranje"]},
        {"title": "AI projekt - chatbot za fakultetsku podršku", "content": "Trebam data scientiste i NLP inženjere. Ideja je napraviti chatbot koji pomaže studentima sa pitanjima.", "tags": ["programiranje"]},
        {"title": "Blockchain projekt - decentralizovana platforma", "content": "Trebam Solidity i Web3 developerа. Projekt je decentralizovani market place.", "tags": ["programiranje"]},
        {"title": "Grafički projekt - 3D model fakulteta", "content": "Trebam 3D artists. Trebam da napravimo virtualni tour fakulteta u Blenderu.", "tags": ["programiranje"]},
        {"title": "Baza podataka - sistem za upravljanje bibliotekom", "content": "Trebam databaze i backend dev. Sistem za upravljanje knjižnim fondovima sa search funkcionalnostima.", "tags": ["programiranje"]},
        {"title": "Machine Learning - predviđanje rezultata studenata", "content": "Trebam data scientists. Model koji predviđa akademske performanse na osnovu raznih faktora.", "tags": ["programiranje"]},
        {"title": "Igraće razvojе - indie game sa Unity", "content": "Trebam game developers. Mali 2D puzzle game. Mamo art, trebam programere.", "tags": ["programiranje"]},
        {"title": "Sigurnost - pentesting alat", "content": "Trebam ethical hackers. Trebam build pentesting tool za edukativne svrhe.", "tags": ["programiranje"]},
        {"title": "Semantička analiza teksta - prirodni jezik", "content": "NLP projekt. Analiza sentimenta društvenih mreža u realnom vremenu.", "tags": ["programiranje"]},
        {"title": "Računarska vizija - detekcija objekata", "content": "OpenCV projekt. Trebam inženjera za detekciju objekata na video stream-u.", "tags": ["programiranje"]},
        {"title": "Autonomni vozač - simulacija", "content": "Trebam programere za simulaciju autonomnog vozanja. Imaš CARLA simulator iskustvo?", "tags": ["programiranje"]},
        {"title": "Distributed sistem - message broker", "content": "Trebam inženjera za distribuirane sisteme. Gradimo message broker kao Redis.", "tags": ["programiranje"]},
        {"title": "Performance optimization - C++ jezgro", "content": "Trebam C++ dev. Optimiziranje kritičnog dijela koda za performanse.", "tags": ["programiranje"]},
        {"title": "DevOps projekt - infrastruktura kao kod", "content": "Trebam DevOps inženjera. Terraform i Kubernetes iskustvo potrebno.", "tags": ["programiranje"]},
        {"title": "Augmented reality - mobilna AR aplikacija", "content": "Trebam AR dev. Android ili iOS sa AR kitom. Imamo koncept, trebam implementaciju.", "tags": ["programiranje"]},
        {"title": "Social media analytics - dashboard", "content": "Trebam full-stack dev. Trebam dashboard koji prati društvene mreže u realnom vremenu.", "tags": ["programiranje"]},
        {"title": "E-commerce - platforma sa naprednim filterima", "content": "Trebam full stack tima. Platform sa pretraživanjem, filterima, sigurnom platežnom integracijom.", "tags": ["programiranje"]},
        {"title": "Real-time kolaborativni editor - kao Google Docs", "content": "Trebam expertsе sa WebSockets-om. Trebam real-time editor sa kolaboracijom.", "tags": ["programiranje"]},
    ],
    
    "Off-Topic": [
        {"title": "Preporuke za kafana pored fakulteta", "content": "Gdje su dobre kafica blizu fakulteta za učenje? Trebam ambijent koji je dobar za rad."},
        {"title": "Kako ste se ponašali na prvom ispitu? Luđo ili normalno?", "content": "Meni je prvi ispit bio strašan. Kako se vi nosili sa nervozom? Neki savjet?"},
        {"title": "Najbolje kriptovalute za početnike", "content": "Neko od vas se zanimao za kripto? Kako ste počeli? Šta preporučujete?"},
        {"title": "Serije i filmovi o učenju i tehnologiji", "content": "Koje serije/filmove preporučujete? Trebam nešto inspirativno ili zabavno za opuštanje."},
        {"title": "Fitness ispred fakulteta - kako se održavate u formi?", "content": "Trebam motivaciju za vježbanje. Koja je vaša rutina?"},
        {"title": "Putovanja tijekom ljeta - gdje ste bili?", "content": "Ljeto je došlo! Gdje ste putovali ili planirate putovati? Tražim inspiraciju!"},
        {"title": "Omiljene knjige - čitanja studenata", "content": "Koje knjige vam se dogodilo da pročitate osim udžbenika? Šta preporučujete?"},
        {"title": "Muzika za učenje - što slušate dok učite?", "content": "Koja je najbolja muzika za fokus? Neko ima playlistu?"},
        {"title": "Podcast preporuke - naučne i razvijajuće", "content": "Koji podcast-i vas inspirisu? Trebam nešto za put do fakulteta."},
        {"title": "Kako se psihički opravite od lošeg testa?", "content": "Upravo sam propao test koji je bio važan. Kako se navirite?"},
        {"title": "Gaming zajednica - igrači na fakultetu", "content": "Neko od vas igra? Koji su vam omiljeni timovi za multiplayer igre?"},
        {"title": "Startapi i preduzetništvo - neko razmišlja o tome?", "content": "Trebam prijatelje koji razmišljaju o biznis ideji. Zajedničko učenje?"},
        {"title": "Reddit vs Discord - gdje je bolja zajednica?", "content": "Gdje vi provodite vrijeme online? Koja je zajednica vam bliža?"},
        {"title": "Čitanjem AI - ChatGPT vam pomaže pri učenju?", "content": "Kako ste počeli da koristite AI alate? Pomažu vam ili vas ometa?"},
        {"title": "Mentalno zdravlje studenata - trebaš neko za razgovor?", "content": "Depresija je česta među studentima. Trebam da znamo da nije samo problem mene. Podrška?"},
        {"title": "Omiljeni restoran za slavlje dobre ocjene", "content": "Gdje idete na slavlje nakon dobrog testa? Trebam ideju!"},
        {"title": "Kako izbjeći procrastination - metodologije", "content": "Uvijek puštam na zadnju noć. Kako ste vi pobjegli tom cizklusu?"},
        {"title": "Najčešće greške studenata - šta nikada ne radite?", "content": "Kako izbjeći klasične greške? Šta vam je pomoglo da budete bolji student?"},
        {"title": "Noćni sovi vs jutarnje osobe - koga ma više na fakultetu?", "content": "Ja sam noćni sova, ali raspored je za jutarnje osobe. Kako se nosite?"},
        {"title": "Motiva studenata - životni moto koji vas drži motiviranom", "content": "Koji je vaš moto da se drži motivirani tijekom semestra?"},
    ],
}

FORUM_COMMENTS_DATA = {
    "Opšta diskusija": [
        "Slažem se sa ovim, trebalo bi više fokusa na to. Nadam se da će to biti promijenjeno.",
        "Odličan savjet! Ja sam to radio i zaista je pomoglo.",
        "To je teško, ali moguće. Trebam samo malo više organizacije sa moje strane.",
        "Neko ima drugačiji pristup? Meni se čini da bi to trebalo da se radi različito.",
        "Zahvaljujem što si podijelio iskustvo. To me daje novu perspektivu.",
        "Nisam sigurna kako početi, ali ovo je dobra otačka!",
        "Update: Pokušao sam ovo i zaista je bolje! Hvala na savjetu.",
    ],
    "Pomoć sa predmetima": [
        "Odličan primjer! Sada razumijem. Zahvaljujem!",
        "🎯 OVO JE ODGOVOR KOJI SAM TREBAO! Matematika je sada jasna.",
        "Grafički prikaz je mnogo pomogao da razumijem koncept.",
        "Mogu li vidjeti još primjera? Razumijem teoriju ali praksa je drugačija.",
        "Pokušao sam sa drugim pristupom i također funkcioniše. Lepo!",
        "Bila je greška u mom razumijevanju. Hvala što si me ispravito.",
        "Trebam biti malo više strpljiv sa sobom. Hvala za objašnjenje.",
    ],
    "Studijske grupe": [
        "Volim ovu ideju! Trebam se registrovati?",
        "Koliko osoba je već zainteresirano? Trebam znati prije nego što se javljam.",
        "U kojem vremenu i mjestu točno? Dat ću ti sve detalje!",
        "Ja mogu biti tutora ako trebate help! Imam iskustva.",
        "Odličan plan! Mogu li doći samo povremeno ili trebam biti regularan?",
        "Koji je nivo? Trebam grupu za početnike ili je to advancovano?",
        "Update: Prešao sem se javio i prvi susret je bio odličan!",
    ],
    "Projekti": [
        "Ovo zvuči odličnog! Mogu li da tražim više detalja o tehnologiji?",
        "Imam relevantno iskustvo, trebam informacije o primjeni!",
        "Koliko vremena je trebalo da do razvija dosadašnji dio? Trebam procjenu.",
        "Trebam biti siguran da mogu commitment-om. Koliko sati tjedno?",
        "Odličan projekat! Trebam da budem dio team-a ako je još mjesta.",
        "Jesam li previše junior za ovaj projekat ili su svi dobrodošli?",
        "Trebam portfolio koji bi bio bolji. Ovaj projekat je idealan mogućnost!",
    ],
    "Off-Topic": [
        "😄 Potpuno se slaže sa mojim iskustvom!",
        "Ovdje se čini da nije sam - više nas je u toj situaciji.",
        "Trebam to isprobati! Zvuči kao odličan savjet.",
        "Meni je pomoglo drugačije, ali vidim gdje dolazaš.",
        "Update: Pokušao sam to i sada je mnogo bolje!",
        "Toliko je istinito! Nikad prije nisam vidio da to neko kaže.",
        "Trebam više ljudi da razgovara sa mnom o tome - hvala što si otvorio temu.",
    ],
}


def seed_forum_categories(session: Session) -> None:
    print("📂 Seeding forum kategorija...")
    for category_data in FORUM_CATEGORIES:
        existing = session.exec(
            select(ForumCategory).where(ForumCategory.name == category_data["name"])
        ).first()

        if existing:
            existing.color = category_data["color"]
            existing.description = category_data["description"]
            session.add(existing)
            continue

        category = ForumCategory(
            name=category_data["name"],
            color=category_data["color"],
            description=category_data["description"]
        )
        session.add(category)
    session.commit()


def get_or_create_test_users(session: Session) -> list[User]:
    emails = ["forum.test@student.ba", "amra.begic@student.ba", "zijad.lekic@student.ba"]
    names = ["Forum Test Student", "Amra Begić", "Zijad Lekić"]
    users = []
    for email, name in zip(emails, names):
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            user = User(
                email=email,
                full_name=name,
                password_hash=hash_password("password123"),
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        users.append(user)
    return users


def get_or_create_tags(session: Session) -> dict[str, ForumTag]:
    tag_names = ["matematika", "programiranje", "fourier", "ispit", "hardware", "kafa"]
    tags_dict = {}
    for name in tag_names:
        tag = session.exec(select(ForumTag).where(ForumTag.name == name)).first()
        if not tag:
            tag = ForumTag(name=name)
            session.add(tag)
            session.commit()
            session.refresh(tag)
        tags_dict[name] = tag
    return tags_dict


def seed_topics_and_comments(session: Session) -> None:
    users = get_or_create_test_users(session)
    
    # Dodajemo više korisnika za realističnost
    additional_emails = [
        "marko.milic@student.ba", "jovana.petrovic@student.ba", "stefan.novak@student.ba",
        "ana.jovanovic@student.ba", "nikola.filipovic@student.ba", "petra.radosavljevic@student.ba",
        "uros.marjanovic@student.ba", "milena.stefanovic@student.ba", "aleksandar.vasic@student.ba",
        "dragan.simic@student.ba"
    ]
    additional_names = [
        "Marko Milić", "Jovana Petrović", "Stefan Novak", "Ana Jovanović", "Nikola Filipović",
        "Petra Radosavljević", "Uroš Marjanović", "Milena Stefanović", "Aleksandar Vasić", "Dragan Simić"
    ]
    
    additional_users = []
    for email, name in zip(additional_emails, additional_names):
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            user = User(
                email=email,
                full_name=name,
                password_hash=hash_password("password123"),
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        additional_users.append(user)
    
    all_users = users + additional_users
    tags = get_or_create_tags(session)
    categories = session.exec(select(ForumCategory)).all()

    if not categories:
        print("Kategorije nisu pronađene. Prvo pokrenite seed_forum_categories.")
        return

    print("📚 Seeding sa kvalitetnim temama, komentarima i realističnom reputacijom...")
    
    user_stats = {}
    for user in all_users:
        user_stats[user.id] = {"topics": 0, "answers": 0, "best_answers": 0}
    
    for category in categories:
        if category.name == "Praksa i posao":
            continue
            
        category_topics = FORUM_TOPICS_DATA.get(category.name, [])
        
        for topic_idx, topic_data in enumerate(category_topics[:20]):
            title_text = topic_data["title"]
            existing_topic = session.exec(
                select(ForumTopic).where(ForumTopic.title == title_text)
            ).first()

            if existing_topic:
                continue

            # Rotacija autora između korisnika
            author_idx = (hash(title_text) % len(all_users))
            topic_author = all_users[author_idx]
            
            time_offset = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=30-topic_idx, hours=topic_idx%24)
            
            topic = ForumTopic(
                title=title_text,
                content=topic_data["content"],
                category_id=category.id,
                user_id=topic_author.id,
                views_count=(topic_idx + 1) * (15 + (hash(title_text) % 40)),
                created_at=time_offset,
                is_deleted=False,
            )
            session.add(topic)
            session.commit()
            session.refresh(topic)
            
            user_stats[topic_author.id]["topics"] += 1
            
            # Dodavanje tagova ako su specificirani
            if "tags" in topic_data:
                for tag_name in topic_data["tags"]:
                    if tag_name in tags:
                        session.add(ForumTopicTag(topic_id=topic.id, tag_id=tags[tag_name].id))
            
            # Dodavanje komentara - 3-5 komentara po temi
            num_comments = 3 + (topic_idx % 3)
            comments_data = FORUM_COMMENTS_DATA.get(category.name, ["Odličan post!", "Slažem se."])
            
            for comment_idx in range(num_comments):
                commenter_idx = (author_idx + comment_idx + 1) % len(all_users)
                commenter = all_users[commenter_idx]
                
                is_best = (comment_idx == 1 and topic_idx % 3 == 0)  # Svaka treća tema ima best answer
                
                comment = ForumComment(
                    content=comments_data[comment_idx % len(comments_data)],
                    topic_id=topic.id,
                    user_id=commenter.id,
                    is_best_answer=is_best,
                    is_deleted=False,
                    created_at=time_offset + timedelta(minutes=30 + comment_idx*45)
                )
                session.add(comment)
                session.commit()
                session.refresh(comment)
                
                user_stats[commenter.id]["answers"] += 1
                if is_best:
                    user_stats[commenter.id]["best_answers"] += 1
                
                # Dodavanje glasova na komentare
                vote_count = (comment_idx + 1) * (2 if is_best else 1)
                for voter_idx in range(vote_count):
                    voter = all_users[(commenter_idx + voter_idx + 1) % len(all_users)]
                    session.add(ForumCommentVote(comment_id=comment.id, user_id=voter.id, value=1))
            
            session.commit()

    print("🏅 Seeding sistema reputacije i medalja...")
    
    # Kreiraj statistiku za sve korisnike
    for user in all_users:
        existing_stats = session.exec(select(ForumUserStats).where(ForumUserStats.user_id == user.id)).first()
        if not existing_stats:
            stats_data = user_stats[user.id]
            reputation = (stats_data["topics"] * 10) + (stats_data["answers"] * 3) + (stats_data["best_answers"] * 25)
            
            user_stats_obj = ForumUserStats(
                user_id=user.id,
                reputation_points=reputation,
                topics_started_count=stats_data["topics"],
                answers_count=stats_data["answers"],
                best_answers_count=stats_data["best_answers"],
                night_topics_count=(user.id % 7),
            )
            session.add(user_stats_obj)
    
    session.commit()
    
    # Dodaj medalje za top korisnike
    top_answerers = sorted(all_users, key=lambda u: user_stats[u.id]["best_answers"], reverse=True)[:3]
    top_topic_starters = sorted(all_users, key=lambda u: user_stats[u.id]["topics"], reverse=True)[:3]
    
    for user in top_answerers:
        if not session.exec(select(ForumUserMedal).where(ForumUserMedal.user_id == user.id, ForumUserMedal.medal_code == "best_answers_gold")).first():
            tier = "gold" if user_stats[user.id]["best_answers"] > 3 else "silver"
            session.add(ForumUserMedal(user_id=user.id, medal_code="best_answers_gold", category="best_answers", tier=tier))
    
    for user in top_topic_starters:
        if not session.exec(select(ForumUserMedal).where(ForumUserMedal.user_id == user.id, ForumUserMedal.medal_code == "topics_starter")).first():
            session.add(ForumUserMedal(user_id=user.id, medal_code="topics_starter", category="topics_started", tier="silver"))
    
    session.commit()
    print("✅ Forum je napumpan sa kvalitetnim sadržajem!")


# ---------------------------------------------------------------------------
# Main app seed data
# ---------------------------------------------------------------------------

def _build_users() -> list[User]:
    users_data = [
        {"email": "admin@test.local", "full_name": "Admin User", "role": UserRole.admin},
        {"email": "member1@test.local", "full_name": "Member One", "role": UserRole.member},
        {"email": "member2@test.local", "full_name": "Member Two", "role": UserRole.member},
        {"email": "member3@test.local", "full_name": "Member Three", "role": UserRole.member},
        {"email": "member4@test.local", "full_name": "Member Four", "role": UserRole.member},
        {"email": "member5@test.local", "full_name": "Member Five", "role": UserRole.member},
        {"email": "member6@test.local", "full_name": "Member Six", "role": UserRole.member},
        {"email": "member7@test.local", "full_name": "Member Seven", "role": UserRole.member},
        {"email": "member8@test.local", "full_name": "Member Eight", "role": UserRole.member},
        {"email": "member9@test.local", "full_name": "Member Nine", "role": UserRole.member},
        {"email": "member10@test.local", "full_name": "Member Ten", "role": UserRole.member},
    ]
    return [
        User(
            email=d["email"],
            full_name=d["full_name"],
            password_hash=hash_password("password123"),
            role=d["role"],
        )
        for d in users_data
    ]


def _build_companies() -> list[Company]:
    companies_data = [
        {"company_name": "Tech Solutions d.o.o.", "description": "Leading IT solutions provider.", "website_url": "https://techsolutions.ba", "logo_path": "logos/tech1.png", "email": "hr@techsolutions.ba", "phone_number": "+38761111111", "tin": "1111111111111", "address": "Sarajevo, Zmaja od Bosne 1"},
        {"company_name": "Digital Innovations d.o.o.", "description": "Digital transformation experts.", "website_url": "https://digitalinnovations.ba", "logo_path": "logos/digital1.png", "email": "careers@digitalinnovations.ba", "phone_number": "+38761111112", "tin": "1111111111112", "address": "Sarajevo, Obala Kulina Bana 2"},
        {"company_name": "Cloud Systems d.o.o.", "description": "Cloud infrastructure and services.", "website_url": "https://cloudsystems.ba", "logo_path": "logos/cloud1.png", "email": "jobs@cloudsystems.ba", "phone_number": "+38761111113", "tin": "1111111111113", "address": "Zenica, Cara Dusana 3"},
        {"company_name": "Mobile First d.o.o.", "description": "Mobile app development company.", "website_url": "https://mobilefirst.ba", "logo_path": "logos/mobile1.png", "email": "recruitment@mobilefirst.ba", "phone_number": "+38761111114", "tin": "1111111111114", "address": "Tuzla, Kulina Bana 4"},
        {"company_name": "Data Analytics Pro d.o.o.", "description": "Business intelligence and analytics.", "website_url": "https://dataanalyticspro.ba", "logo_path": "logos/data1.png", "email": "hr@dataanalyticspro.ba", "phone_number": "+38761111115", "tin": "1111111111115", "address": "Mostar, Aleksa Santic 5"},
        {"company_name": "Security First d.o.o.", "description": "Cybersecurity and penetration testing.", "website_url": "https://securityfirst.ba", "logo_path": "logos/security1.png", "email": "careers@securityfirst.ba", "phone_number": "+38761111116", "tin": "1111111111116", "address": "Banja Luka, Drinska 6"},
        {"company_name": "DevOps Masters d.o.o.", "description": "Infrastructure automation and CI/CD.", "website_url": "https://devopsmasters.ba", "logo_path": "logos/devops1.png", "email": "jobs@devopsmasters.ba", "phone_number": "+38761111117", "tin": "1111111111117", "address": "Doboj, Baba Radisa 7"},
        {"company_name": "UI/UX Studio d.o.o.", "description": "User experience and interface design.", "website_url": "https://uiuxstudio.ba", "logo_path": "logos/uiux1.png", "email": "hello@uiuxstudio.ba", "phone_number": "+38761111118", "tin": "1111111111118", "address": "Bijeljina, Cara Aleksandra 8"},
        {"company_name": "Backend Specialists d.o.o.", "description": "Enterprise backend development.", "website_url": "https://backendspecialists.ba", "logo_path": "logos/backend1.png", "email": "recruitment@backendspecialists.ba", "phone_number": "+38761111119", "tin": "1111111111119", "address": "Trebinje, Nemanjina 9"},
        {"company_name": "QA Automation d.o.o.", "description": "Software testing and quality assurance.", "website_url": "https://qaautomation.ba", "logo_path": "logos/qa1.png", "email": "careers@qaautomation.ba", "phone_number": "+38761111120", "tin": "1111111111120", "address": "Bihac, Zivka Dakica 10"},
    ]
    return [
        Company(**d, hashed_password=hash_password("company123"), status=CompanyStatus.approved)
        for d in companies_data
    ]


def _build_ads(companies: list[Company], users: list[User]) -> list[Ad]:
    ad_templates = [
        {"title": "Junior Web Developer", "type": AdType.internship, "field": "Web Development", "location": "Sarajevo", "description": "Exciting opportunity to learn and grow as a web developer.", "deadline": 30, "duration_months": 3, "compensation": 300.0, "spots": 2},
        {"title": "Backend Developer Internship", "type": AdType.internship, "field": "Backend Development", "location": "Zenica", "description": "Build scalable backend systems with Python and Django.", "deadline": 35, "duration_months": 4, "compensation": 350.0, "spots": 1},
        {"title": "QA Engineer", "type": AdType.internship, "field": "Quality Assurance", "location": "Tuzla", "description": "Test and ensure software quality and reliability.", "deadline": 40, "duration_months": 3, "compensation": 280.0, "spots": 3},
        {"title": "Data Analytics Internship", "type": AdType.internship, "field": "Data Analytics", "location": "Mostar", "description": "Analyze business data and generate insights.", "deadline": 25, "duration_months": 2, "compensation": 400.0, "spots": 1},
        {"title": "Cybersecurity Specialist", "type": AdType.internship, "field": "Cybersecurity", "location": "Banja Luka", "description": "Learn cybersecurity best practices and protocols.", "deadline": 45, "duration_months": 6, "compensation": 450.0, "spots": 2},
        {"title": "DevOps Engineer Intern", "type": AdType.internship, "field": "DevOps", "location": "Doboj", "description": "Work on CI/CD pipelines and infrastructure automation.", "deadline": 32, "duration_months": 4, "compensation": 420.0, "spots": 1},
        {"title": "UI/UX Designer", "type": AdType.internship, "field": "Design", "location": "Bijeljina", "description": "Create beautiful and user-friendly interfaces.", "deadline": 28, "duration_months": 3, "compensation": 330.0, "spots": 2},
        {"title": "Mobile App Developer", "type": AdType.internship, "field": "Mobile Development", "location": "Trebinje", "description": "Develop iOS and Android applications.", "deadline": 38, "duration_months": 5, "compensation": 380.0, "spots": 1},
        {"title": "Full Stack Developer", "type": AdType.internship, "field": "Full Stack", "location": "Bihac", "description": "Work on both frontend and backend systems.", "deadline": 42, "duration_months": 4, "compensation": 370.0, "spots": 2},
        {"title": "Software Engineer Apprenticeship", "type": AdType.internship, "field": "Software Engineering", "location": "Sarajevo", "description": "Comprehensive software engineering training program.", "deadline": 50, "duration_months": 6, "compensation": 400.0, "spots": 3},
        {"title": "Python Bootcamp", "type": AdType.education, "field": "Programiranje", "location": "Sarajevo", "description": "Intenzivni kurs Python programiranja za studente.", "deadline": 30, "duration_months": 2, "compensation": None, "spots": 20},
        {"title": "Web Development Kurs", "type": AdType.education, "field": "Web Development", "location": "Tuzla", "description": "Naučite HTML, CSS i JavaScript od nule.", "deadline": 35, "duration_months": 3, "compensation": None, "spots": 15},
        {"title": "Data Science Radionica", "type": AdType.education, "field": "Data Science", "location": "Mostar", "description": "Uvod u analizu podataka i machine learning.", "deadline": 40, "duration_months": 1, "compensation": None, "spots": 10},
        {"title": "Stipendija za IT studente", "type": AdType.scholarship, "field": "Informacione tehnologije", "location": "Sarajevo", "description": "Stipendija namijenjena studentima IT fakulteta.", "deadline": 45, "duration_months": None, "compensation": 500.0, "spots": 5},
        {"title": "STEM Stipendija", "type": AdType.scholarship, "field": "STEM", "location": "Banja Luka", "description": "Stipendija za studente prirodnih i tehničkih nauka.", "deadline": 50, "duration_months": None, "compensation": 400.0, "spots": 3},
    ]
    ads = []
    for index, template in enumerate(ad_templates):
        ads.append(
            Ad(
                company_id=companies[index % len(companies)].id,
                approved_by=users[0].id,
                title=template["title"],
                type=template["type"],
                field=template["field"],
                location=template["location"],
                description=template["description"],
                deadline=date.today() + timedelta(days=template["deadline"]),
                duration_months=template["duration_months"],
                compensation=template["compensation"],
                currency="BAM",
                spots=template["spots"],
                requirements="Strong motivation and willingness to learn.",
                benefits="Mentorship, practical experience, and certificate.",
                admin_comment="Approved for posting.",
                status=AdStatus.active,
            )
        )
    return ads


_APP_STATUS_PATTERN = [
    ApplicationStatus.pending,
    ApplicationStatus.pending,
    ApplicationStatus.pending,
    ApplicationStatus.pending,
    ApplicationStatus.accepted,
    ApplicationStatus.accepted,
    ApplicationStatus.accepted,
    ApplicationStatus.rejected,
    ApplicationStatus.rejected,
    ApplicationStatus.rejected,
]

_ACCEPTED_FEEDBACK = [
    "Odlican kandidat, pokazuje veliko interesovanje i potencijal.",
    "Profil kandidata odgovara svim trazenim kriterijima.",
    "Impresivno motivacijsko pismo i relevantno iskustvo.",
]

_REJECTED_FEEDBACK = [
    "Nedovoljno iskustvo u trazenim tehnologijama.",
    "Kandidat ne ispunjava minimalne uslove za poziciju.",
    "Pozicija je popunjena prikladnijim kandidatom.",
]


def _build_applications(users: list[User], ads: list[Ad]) -> list[Application]:
    members = users[1:]
    applications = []
    global_index = 0
    for ad in ads:
        for slot in range(10):
            status = _APP_STATUS_PATTERN[slot]
            user = members[slot % len(members)]
            if status == ApplicationStatus.accepted:
                feedback = _ACCEPTED_FEEDBACK[slot % len(_ACCEPTED_FEEDBACK)]
            elif status == ApplicationStatus.rejected:
                feedback = _REJECTED_FEEDBACK[slot % len(_REJECTED_FEEDBACK)]
            else:
                feedback = None
            applications.append(
                Application(
                    user_id=user.id,
                    ad_id=ad.id,
                    cv_path=f"uploads/applications/cv_{global_index}.pdf",
                    motivational_letter_path=f"uploads/applications/letter_{global_index}.pdf",
                    linkedin_url=f"https://linkedin.com/in/user{global_index}" if global_index % 2 == 0 else None,
                    phone=f"+38761{200000 + global_index:06d}",
                    status=status,
                    admin_feedback=feedback,
                    is_archived=False,
                )
            )
            global_index += 1
    return applications


def _build_notifications(users: list[User]) -> list[Notification]:
    notification_types = [
        NotificationType.NEW_OPPORTUNITY,
        NotificationType.STATUS_CHANGE,
        NotificationType.DEADLINE_EXPIRING,
    ]
    messages = [
        "New job opportunity matching your profile!",
        "Your application status has been updated.",
        "Application deadline is expiring soon!",
        "New internship posted in your field.",
        "Your profile has been reviewed.",
        "Congratulations! You've been shortlisted.",
        "Thank you for applying.",
        "New networking event available.",
        "Your CV has been downloaded.",
        "Mentor assignment confirmation.",
    ]
    notifications = []
    for index in range(10):
        notifications.append(
            Notification(
                user_id=users[(index + 1) % len(users)].id,
                text=messages[index],
                type=notification_types[index % len(notification_types)],
                is_read=index % 2 == 0,
            )
        )
    return notifications


def _build_bookmarks(users: list[User], ads: list[Ad]) -> list[AdBookmark]:
    bookmarks = []
    for index in range(10):
        bookmarks.append(
            AdBookmark(
                user_id=users[(index + 1) % len(users)].id,
                ad_id=ads[index].id,
            )
        )
    return bookmarks


def seed_demo_data(session: Session) -> dict[str, int]:
    existing_user = session.exec(select(User).where(User.email == "admin@test.local")).first()
    if existing_user:
        return {
            "users": len(session.exec(select(User)).all()),
            "companies": len(session.exec(select(Company)).all()),
            "ads": len(session.exec(select(Ad)).all()),
            "applications": len(session.exec(select(Application)).all()),
            "notifications": len(session.exec(select(Notification)).all()),
            "bookmarks": len(session.exec(select(AdBookmark)).all()),
            "created": 0,
        }

    users = _build_users()
    session.add_all(users)
    session.commit()
    for user in users:
        session.refresh(user)

    companies = _build_companies()
    session.add_all(companies)
    session.commit()
    for company in companies:
        session.refresh(company)

    ads = _build_ads(companies, users)
    session.add_all(ads)
    session.commit()
    for ad in ads:
        session.refresh(ad)

    applications = _build_applications(users, ads)
    session.add_all(applications)
    session.commit()

    notifications = _build_notifications(users)
    session.add_all(notifications)
    session.commit()

    bookmarks = _build_bookmarks(users, ads)
    session.add_all(bookmarks)
    session.commit()

    total = len(users) + len(companies) + len(ads) + len(applications) + len(notifications) + len(bookmarks)
    return {
        "users": len(users),
        "companies": len(companies),
        "ads": len(ads),
        "applications": len(applications),
        "notifications": len(notifications),
        "bookmarks": len(bookmarks),
        "created": total,
    }


def seed_database() -> None:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        result = seed_demo_data(session)
        seed_forum_categories(session)
        seed_topics_and_comments(session)
        
    print(
        f"Glavni seed završen:\n"
        f"  - {result['users']} korisnika\n"
        f"  - {result['companies']} kompanija\n"
        f"  - {result['ads']} oglasa\n"
        f"  - {result['applications']} aplikacija\n"
        f"  - {result['notifications']} notifikacija\n"
        f"  - {result['bookmarks']} bookmarkova\n"
        f"  - ukupno {result['created']} novih redova"
    )
    print("Svi seed podaci za forum, aplikaciju i reputaciju su spremni.")


if __name__ == "__main__":
    seed_database()