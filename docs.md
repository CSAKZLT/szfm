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
