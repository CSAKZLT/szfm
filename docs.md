# Projekt dokumentáció - szabadság nyilvántartó 

## Projekt rövid leírása:
A szabadság nyilvántartóval egyedi kulcs alapján tudjuk monitorozni a még rendelkezésre álló szabadságaink számát.

## Alapkövetelmények:
DB alapú adat tárolás.
Webes interfész.
Mobil interfész.
Dokumentáció.

## Funkciók:
Login felület, itt belépés és új felhasználó rögzítése szükséges.
Új felhasználó rögzítése a DB-be. Egy formon keresztül lehessen felvinni legalább az egyedi kulcsot és a rendelkezésre álló szabadságok számát.
Belépést követően lássa a felhasználó a rendelkezésre álló szabadságainak számát.
Legyen lehetőség szabadság kivételére, ekkor az elérhető szabadságok száma arányosan csökkenjen. Ez nem kötelező, de jó lenne egy másik táblában rögzíteni a szabadság kivétel napját.

## pontozás Pepa malac című animációs sorozat karakterei alapján
Zsoli malac (ksitesó)
Pepa malac (főhősünk)
Mama malac (Pepa fiatalabb szülője)
Papa malac (Pepa idősebb szülője)
Malac bácsi (Papa malac bátyja)
Nagymami (Fiatalabb nagyszülő)
Nagypapi (Idősebb nagyszülő)

## Trellóban követjük a taskokat, ha módosítani kell ezen a doksin, akkor nyugodtan bele lehet nyúlni a következő módokon:
Direktben GitHub-on.
Vagy Git Bash-sal. Ekkor a https://github.com/CSAKZLT/szfm.git repoban kell dolgozni.
- Aktualizáld a repot, vagy dobd el. Én eldobtam: rm -rf szfm
- Klónozd a repót: git clone https://github.com/CSAKZLT/szfm.git
- Tallózd ki az szfm mappát: cd szfm
- itt találod a docs.md-t, ezt a nano-val meg tudod nyitni: nano docs.md

Ne felejts el kommitolni!
- git add <amit módosítottál> vagy git add . (ekkor mindent hozzáad a commithoz)
- git commit
- git push 


---

# Frontend
A frontend egy egyetlen HTML oldalon valósul meg (index.html), amely kettő fő részből áll:
- Regisztrációs / Bejelentkezés űrlap
- Szabadságok kezelése blokk
A felület tiszta, egyszerű, reszponzív elrendezésű, natív HTML + CSS + vanilla JavaScript használatával.

### Felépítás
- A <body> középre igazított, világosszürke háttérrel (#f4f4f4).
- A felső részben egy két hasábos konténer található (.container), amelyben:
    - bal oldalon: Regisztráció
    - jobb oldalon: Bejelentkezés
- A felső blokk alatt egy vízszintes elválasztó, majd egy külön kártyában (.vacation-container) a Szabadságok kezelése rész.

### Regisztrációs űrlap
A form beküldésekor JavaScript submit eseménykezelő fut. A mezők értékei alapján JSON készül, amit egy POST /register kérésben megy ki a backend felé. A válasz alapján:
- siker esetén: zöld üzenet jelenik meg (Sikeres regisztráció.), az űrlap kiürül
- hiba esetén: piros hibaüzenet
Sikeres regisztráció után eltároljuk a felhasználó e-mail címét, eltároljuk a felhasználó e-mail címét, majd feloldjuk a szabadságkezelő szekciót.

### Bejelentkezés űrlap
Hasonlóan a regisztrációhoz submit eseménykezelő fut. A mezők értékei alapján JSON készül, amit egy POST /login kérésben megy ki a backend felé. A válasz alapján:
- siker esetén: zöld „Sikeres bejelentkezés.” üzenet jelenik meg, elmentjük az e-mail címet, kitöltjük a szabadság e-mail mezőt, feloldjuk a szabadságkezelő szekciót.
- hiba esetén: piros hibaüzenet (hibás belépési adatok vagy hálózati hiba).

### Szabadságok kezelése blokk
Ez a rész egy külön kártyában jelenik meg, alapértelmezetten letiltva. Sikeres regisztráció vagy bejelentkezés feloldja ezt a blokkot. A frontend egy currentUserEmail változóban tárolja a legutóbb sikeresen regisztrált/belépett felhasználó e-mail címét, így a felhasználónak nem kell újra begépelnie az e-mail címét.

A „Szabadságok lekérése” gomb (loadVacationsBtn) a loadVacations(email) függvényt hívja. A státuszdoboz zöld (.ok) vagy piros (.err) állapotban jelenik meg attól függően, hogy sikeres volt-e a lekérés.

Az „Új szabadság felvétele” blokkban a szabadság kezdődátumát és a napok számét kell megadni. A „Szabadság hozzáadása” gomb ellenőrzi, hogy van-e e-mail, dátum és  érvényes nap szám. A táblázat minden sorát lehet módosítani és törölni.

---

# Backend
A backend Flask Python keretrendszerrel valósul meg (main.py), amely REST API-t biztosít a frontendnek. Az alkalmazás PostgreSQL adatbázissal kommunikál a Neon DB szolgáltatáson keresztül.

### Technológiai stack
- **Keretrendszer**: Flask
- **ORM**: Flask-SQLAlchemy
- **Adatbázis**: PostgreSQL (Neon DB)
- **Adatformátum**: JSON

### API Endpointok

#### POST /register
**Leírás**: Új felhasználó regisztrálása.
**Kérés formátuma**:
```json
{
  "email": "user@example.com",
  "password_hash": "hashed_password",
  "full_name": "John Doe",
  "base_vacation_days": 20
}
```

#### POST /login
**Leírás**: Felhasználó bejelentkezése.
**Kérés formátuma**:
```json
{
  "email": "user@example.com",
  "password_hash": "hashed_password"
}
```

#### GET /vacations
**Leírás**: A felhasználó szabadságainak lekérése.
**Paraméterek**: `email` (query paraméter)
**Válasz formátuma**:
```json
{
  "base_vacation_days": 20,
  "used_vacation_days": 5,
  "available_vacation_days": 15,
  "vacations": [
    {
      "id": 1,
      "vacation_date": "2025-12-20",
      "days": 5
    }
  ]
}
```

#### POST /vacations
**Leírás**: Új szabadság hozzáadása a felhasználó számára.
**Kérés formátuma**:
```json
{
  "email": "user@example.com",
  "vacation_date": "2025-12-20",
  "days": 5
}
```

#### PUT /vacations/<vacation_id>
**Leírás**: Meglévő szabadság módosítása.
**Kérés formátuma**:
```json
{
  "vacation_date": "2025-12-25",
  "days": 3
}
```

#### DELETE /vacations/<vacation_id>
**Leírás**: Szabadság törlése.

### Funkciók

**Regisztráció kezelése**
Az új felhasználó regisztrálásakor az alkalmazás automatikusan egy egyedi kulcsot (UKEY-001, UKEY-002, stb.) generál, amely egyedi azonosítóként szolgál a felhasználó számára. Az e-mail cím egyedi, így egy e-mail címmel nem lehet többször regisztrálni.

**Bejelentkezés kezelése**
A bejelentkezés során az alkalmazás az e-mail és jelszó hash alapján keresi meg a felhasználót az adatbázisban. Ha találat van, a bejelentkezés sikeres.

**Szabadságnapok ellenőrzése**
A szabadság hozzáadásakor és módosításakor az alkalmazás automatikusan ellenőrzi, hogy az összes igénybevett szabadságnap nem haladja-e meg az alapadagot. A logika az összes meglévő szabadság napjait összegzi, és hozzáadja az új napokat az ellenőrzéshez. Módosításkor az éppen módosított szabadságot kihagyja az összegeléséből.

**Szabadságok nyilvántartása**
Minden szabadság bevételezésekor rögzítésre kerül a kezdő dátum és az igénybe vett napok száma. Az adatok tartósan tárolódnak az adatbázisban, így később lekérdezhetők és módosíthatók.

---

# Unittest

A Flask alapú szabadságkezelő rendszer automatizált tesztjének megvalósítása ***unittest*** segítségével. A tesztek célja az üzleti logika (regisztráció, belépés, szabadságok kezelése) ellenőrzése izolált környezetben.

## Teszt környezet

Mivel izolált környezetben dolgozunk, a teszteket nem a production adatbázison végezzük (Neon PostgreSQL), hanem egy ideiglenes memóriában futó SQLite adatbázist használunk.

### Működési elv
A rendszer a ***FLASK_ENV*** környezeti változó alapján dönti el, melyik adatbázishoz csatlakozzon.

- **Production mód**: Normál futás esetén, ha a környezeti változó nincs beállítva (vagy nem 'testing'), az alkalmazés a Neon PostgreSQL-hez csatlakozik.
- **Testing mód**: A tesztfájl (***test.py***) beállítja az ***os.envrion['FLASK_ENV'] = 'testing'*** értéket. Ezt a main érzékeli és átvált ***sqlite:///:memory:*** módba.

### Életciklus

Minden egyes teszteset (test case) teljesen tiszta lappal indul:

- **setUp (Előkészítés):** Lérehoz egy új alkalmazás-kontextust és egy üres adatbázis sémát (***db.create.all()***).
- **tearDown (Takarítás):** A teszt végén törli az adatbázis tartalmát (***db.drop.all()***) és lezárja a kapcsolatot, hogy az egyik teszt adatai ne zavarják a következőt.

## Tesztesetek leírása (Test cases)

A 'TestVacationApp' osztály az alábbi funkciókat ellenőrzi:

### Felhasználókezelés (User Management)

| Teszt Függvény | Leírás | Elvárt Eredmény |
| :--- | :--- | :--- |
| `test_register_user` | Új felhasználó regisztrációja valid adatokkal. Ellenőrzi az `UKEY` (Unique Key) automatikus generálását (pl. UKEY-001). | **201 Created**, a felhasználó bekerül az adatbázisba. |
| `test_register_duplicate_email` | Regisztrációs kísérlet olyan email címmel, ami már létezik a rendszerben. | **400 Bad Request**, hibaüzenet visszaadása. |
| `test_login_success` | Bejelentkezés helyes email és jelszó párossal. | **200 OK**, sikeres belépés üzenet. |
| `test_login_failure` | Bejelentkezés helyes email címmel, de hibás jelszóval. | **401 Unauthorized**, hibaüzenet. |

### Szabadságok Kezelése (Vacation Logic)

| Teszt Függvény | Leírás | Elvárt Eredmény |
| :--- | :--- | :--- |
| `test_add_vacation_success` | Szabadság igénylése, amennyiben a kért napok száma nem lépi túl a keretet. | **201 Created**, a szabadság rögzítésre kerül. |
| `test_add_vacation_exceeds_limit` | Olyan szabadság igénylése, amely meghaladná a felhasználó éves keretét (pl. 20 napból 21 igénylése). | **400 Bad Request**, a tranzakció elutasítva. |
| `test_get_vacations_calculation` | A szabadságok összegzésének ellenőrzése. Két külön szabadság (pl. 5 nap + 3 nap) hozzáadása után lekéri a státuszt. | **200 OK**, a válaszban: `used: 8`, `available: 12`. |
| `test_delete_vacation` | Egy meglévő szabadságigénylés törlése ID alapján. | **200 OK**, az adatbázisból eltűnik a bejegyzés. |
| `test_modify_vacation_success` | Meglévő szabadság módosítása (pl. 5 napról 10 napra növelés). | **200 OK**, a napok száma frissül, az összegzés újraszámolódik. |


## Megjegyzések

- **LegacyAPIWarning:** A futtatás előfordulhatnak **LegacyAPIWarning** figyelmeztetések. Ez azért van, mert a kód a régebbi **Model.query.get()** (pl. **Vacation.query.get()** ) szintaxist használja, míg az új SQLAlchemy 2.0 a **db.session.get()**-et preferálja. Ez **nem** hiba, a tesztek ettől függetlenül helyesen működnek.
- **Path Setup:** A 'test.py' elején található **sys.path.append** biztosítja, hogy a teszt megtalálja a **main.py**-t, még akkor is, ha a könyvtárszerkezet vagy a futtatási hely eltérő.

---