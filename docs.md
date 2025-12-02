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