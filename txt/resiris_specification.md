# Resiris – A nyelv felépítése

A Resiris programozási nyelv több különböző elemből épül fel. Ezek együtt határozzák meg, hogy hogyan lehet programot írni, és hogy a program mit csinál futás közben.

## 1. Forráskód

A forráskód az, amit a programozó leír.

A Resiris programok szöveges fájlokban vannak.

**Fájlkiterjesztés:** `.resy`

Például:

```
main.resy
game.resy
calculator.resy
```

A `.resy` fájl tartalmazza a Resiris programot.

## 2. Sorok

A Resiris program sorokból áll.

Például:

```resiris
v x int = 10
v y int = 20
print_cmd(x + y)
```

Itt három külön sor van.

Egy sor általában egy külön nyelvi műveletet vagy deklarációt tartalmaz.

## 3. Kommentek

A komment olyan szöveg, amit a Resiris nem hajt végre.

Kommentet a `##` jellel lehet kezdeni.

```resiris
## Ez egy komment
v x int = 10
```

A komment a programozónak szól. Például magyarázatot vagy megjegyzést lehet beleírni.

## 4. Behúzás

A Resiris a behúzást használja annak megmutatására, hogy egy sor melyik blokkhoz tartozik.

Például:

```resiris
if x == 10:
    print_cmd("x tíz")
    print_cmd("Ez is az if része")
```

A behúzott sorok az if blokkhoz tartoznak.

A Resirisben nincs szükség olyan lezárásra, mint például:

```
end
```

A blokkot a behúzás határozza meg.

## 5. Kulcsszavak

A kulcsszavak olyan különleges szavak, amelyeknek a Resirisben saját jelentésük van.

Jelenlegi Resiris kulcsszavak/nyelvi elemek például:

- `include`
- `v`
- `c`
- `fn`
- `if`
- `elif`
- `else`
- `mat`
- `return`
- `pass`
- `await`

Ezeket a Resiris saját szabályai szerint értelmezi.

## 6. Nevek

A programban sok dolognak nevet adhatunk.

Például:

```resiris
v score int = 100
```

Itt `score` a neve annak, amit létrehoztunk.

Függvénynek is lehet neve:

```resiris
fn calculate():
    pass
```

Itt `calculate` a függvény neve.

A név segítségével később hivatkozhatunk az adott dologra.

## 7. Értékek

Az érték maga az adat.

Például:

- `10` — egy egész szám érték.
- `3.14` — egy lebegőpontos érték.
- `"Hello"` — egy szöveges érték.
- `true` — egy logikai érték.

## 8. Literálok

A literál olyan érték, amit közvetlenül leírunk a programban.

Például:

```resiris
10
3.14
"Hello"
true
false
```

Ezeket a Resiris közvetlenül értékként értelmezi.

## 9. Típusok

A típus azt mondja meg, hogy milyen fajta adatot tárolunk.

A jelenlegi Resiris típusok:

- `UnknownObject`
- `int`
- `float`
- `string`
- `bool`
- `Vector2`
- `ResirisModuleObject`
- `FunctionalObject`

Például:

```resiris
v age int = 18
```

Az `age` típusa `int`. Ez azt jelenti, hogy egész számot tárol.

## 10. int

Az `int` egész szám.

Például:

```resiris
v age int = 18
v score int = 100
v number int = -5
```

Az `int` nem tartalmaz tizedes részt.

## 11. float

A `float` lebegőpontos szám.

Például:

```resiris
v pi float = 3.14
v result float = 10.5
```

A `/` osztás eredménye jelenleg float.

Például:

```resiris
v result float = 20 / 4
```

eredménye:

```
5.0
```

## 12. string

A `string` szöveget tárol.

Például:

```resiris
v name string = "Peter"
```

Szövegeket a Resirisben idézőjelek között írunk.

Stringek össze is adhatók:

```resiris
v first string = "Hello "
v second string = "World"

v result string = first + second
```

Az eredmény:

```
Hello World
```

## 13. bool

A `bool` két lehetséges értéket használ:

- `true`
- `false`

Például:

```resiris
v enabled bool = true
```

A `bool` elsősorban olyan helyzetekben használható, ahol valamire igen/nem választ akarunk adni.

## 14. UnknownObject

Az `UnknownObject` egy olyan típus, amelynek a konkrét típusa létrehozáskor még nincs meghatározva.

Például:

```resiris
v number UnknownObject
```

Az első értékadás határozza meg, hogy pontosan milyen típusú lesz.

Például:

```resiris
number = 10
```

Ezzel `int` értéket kap.

Vagy:

```resiris
number = "hello"
```

akkor `string` értéket kap.

Az első értékadás tehát fontos szerepet játszik az `UnknownObject` működésében.

## 15. Változók – v

A `v` egy varint deklaráció.

Például:

```resiris
v score int = 100
```

Ez létrehoz egy `score` nevű varintot.

A varint értéke később megváltoztatható.

```resiris
v score int = 100
score = 200
```

A `v` jelentése tehát: hozz létre egy módosítható értéket.

## 16. Konstansok – c

A `c` konstans létrehozására szolgál.

```resiris
c max_score int = 100
```

A konstans értéke később nem módosítható.

Tehát ez hibás:

```resiris
c max_score int = 100
max_score = 200
```

A konstans lényege: ezt az értéket létrehozás után nem lehet átírni.

## 17. Értékadás

Az `=` segítségével értéket adunk valaminek.

Például:

```resiris
v x int = 10
```

Itt a `10` értéket az `x` kapja.

Később:

```resiris
x = 20
```

Ekkor az `x` új értéke `20`.

## 18. Rövidített értékadás

A Resiris támogat rövidített műveleteket is.

```resiris
x += 10
x -= 10
x *= 2
x /= 2
```

Például:

```resiris
v x int = 10
x += 5
```

Az eredmény `15`.

Ezek lényegében egy érték módosítását végzik el egy művelettel együtt.

## 19. Operátorok

Az operátorok olyan jelek, amelyekkel műveleteket végzünk.

**Matematikai operátorok:**

- `+`
- `-`
- `*`
- `/`
- `%`

Például:

```resiris
10 + 5
10 - 5
10 * 5
10 / 5
10 % 5
```

## 20. Összehasonlító operátorok

Ezek két értéket hasonlítanak össze.

- `==`
- `!=`
- `>`
- `<`
- `>=`
- `<=`

Például:

```resiris
score > 50
```

vagy:

```resiris
x == 10
```

Az összehasonlítás eredménye `bool`.

## 21. Negatív és pozitív számok

A `+` és `-` önmagában is használható egy érték előtt.

Például:

```resiris
-10
+10
```

Összetett kifejezésnél is:

```resiris
-(a + b)
```

## 22. Zárójelek

A zárójelekkel meghatározhatjuk, hogy egy kifejezés melyik része legyen előbb kiszámolva.

Például:

```resiris
(a + b) * 2
```

Itt először `a + b` számolódik ki.

Ezután az eredmény megszorzódik 2-vel.

## 23. Műveleti sorrend

Ha több operátor szerepel egy kifejezésben, a Resirisnek tudnia kell, melyik műveletet kell előbb elvégezni.

Például:

```resiris
a + b * c
```

és:

```resiris
(a + b) * c
```

nem ugyanazt jelentik.

A zárójel segítségével a programozó egyértelműen megadhatja a kívánt sorrendet.

## 24. Kifejezések

A kifejezés olyan programrész, amelyből egy érték születik.

Egyszerű kifejezés:

```resiris
10
```

Változó:

```resiris
score
```

Művelet:

```resiris
score + 10
```

Összetettebb kifejezés:

```resiris
(score + 10) * 2
```

Függvényhívás is lehet kifejezés:

```resiris
calculate(10, 20)
```

## 25. Függvények – fn

A függvény egy elnevezett műveletsor.

Például:

```resiris
fn greet():
    print_cmd("Hello")
```

A `fn` jelzi, hogy egy függvényt definiálunk.

A függvényben lévő sorok csak akkor hajtódnak végre, amikor a függvényt meghívjuk.

## 26. Függvény paraméterei

A függvény paramétereket is kaphat.

```resiris
fn add(a, b):
    return a + b
```

Az `a` és `b` a paraméterek.

A függvény meghívásakor értékeket adhatunk nekik:

```resiris
add(10, 20)
```

## 27. Függvényhívás

Egy függvényt a nevével és zárójelekkel hívunk meg.

```resiris
greet()
```

Paraméterekkel:

```resiris
add(10, 20)
```

A függvényhívás lehet önálló utasítás:

```resiris
print_cmd("Hello")
```

de egy kifejezés része is lehet:

```resiris
v result int = add(10, 20)
```

## 28. return

A `return` egy függvényből való visszatérésre szolgál.

Például:

```resiris
fn add(a, b):
    return a + b
```

A `return` után a függvény eredménye visszakerül a hívóhoz.

A `return` azonnal kilép a függvényből.

Ezért:

```resiris
fn test():
    print_cmd("A")
    return
    print_cmd("B")
```

a `B` rész már nem fut le.

A `return` függvényen kívül nem használható.

## 29. Függvény visszatérési érték nélkül

Egy függvénynek nem kötelező értéket visszaadnia.

Például:

```resiris
fn hello():
    print_cmd("Hello")
```

Ez érvényes függvény.

## 30. Rekurzió

Egy függvény meghívhatja saját magát.

Például egy matematikai számításnál:

```resiris
fn factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
```

Ez rekurzív függvény.

## 31. Hatókör

A hatókör azt határozza meg, hogy egy változó vagy más név hol érhető el.

Például egy függvényen belül létrehozott varint lokális lehet:

```resiris
fn test():
    v x int = 10
```

Az `x` a függvény belső környezetéhez tartozik.

A Resiris jelenlegi prototípusában a függvényekből a globális változók olvashatók, miközben a függvényen belül létrehozott változók lokálisak.

## 32. if

Az `if` segítségével feltételt vizsgálunk.

```resiris
if score > 50:
    print_cmd("Nyertél")
```

A blokk csak akkor hajtódik végre, ha a feltétel teljesül.

A jelenlegi prototípusban az `if` feltétele bool értéket vár.

## 33. elif

Az `elif` egy újabb feltételt ad az előző `if` után.

```resiris
if score > 90:
    print_cmd("A")
elif score > 50:
    print_cmd("B")
```

Így több lehetséges esetet lehet egymás után vizsgálni.

## 34. else

Az `else` akkor használható, amikor az előző feltételek egyike sem teljesült.

```resiris
if score > 50:
    print_cmd("Nyertél")
else:
    print_cmd("Vesztettél")
```

## 35. mat

A `mat` több konkrét érték közül választ.

Például:

```resiris
mat number:
    1:
        print_cmd("Egy")
    2:
        print_cmd("Kettő")
    else:
        print_cmd("Más")
```

A `mat` egy konkrét értéket hasonlít össze a megadott esetekkel.

A case értéke konkrét megadott érték lehet, nem tetszőleges kifejezés.

Tehát például ez:

```resiris
a + 10:
```

nem érvényes case.

## 36. mat működése

Ha van megfelelő egyezés, a megfelelő ág végrehajtódik.

A Resiris jelenlegi szabálya szerint azonos case előfordulásokat a nyelv nem kezel egyszerűen úgy, hogy az elsőt választja ki: a specifikációban a duplicate case hibás állapotként szerepel.

Ha nincs egyezés és van `else`, az `else` fut le.

Ha nincs egyezés és `else` sincs, akkor semmi nem történik, és a program folytatódik.

A `mat` befejezése után a program normálisan folytatódik.

## 37. pass

A `pass` egy különleges vezérlési elem.

A Resirisben a `pass` nem állítja le a függvényt, és nem lép ki a blokkból.

A `pass` az adott sor további részét hagyja ki.

Például:

```resiris
fn test():
    print_cmd("A")
    pass print_cmd("B")
```

eredménye:

```
A
```

A függvény ezután normálisan folytatódik.

Ez fontos: **`return` ≠ `pass`**

A `return` kilép a függvényből.

A `pass` nem lép ki a függvényből.

## 38. await

Az `await` eseményre vagy valamely várakozási műveletre szolgál.

Ez a Resiris végrehajtási modelljének része.

A pontos eseménykezelési és várakozási szabályokat külön kell meghatározni azoknál a moduloknál, amelyek ezt használják.

> **CURRENT:** a kulcsszó létezik.

További részletes szemantika: jelenleg nincs teljesen véglegesítve a nyelvi specifikációban.

## 39. start()

A `start()` a program indulásához kapcsolódó speciális függvény.

```resiris
start():
    ...
```

A Resiris program futási életciklusában ez szolgál a kezdő részhez.

A pontos runtime-életciklus külön specifikációs terület.

## 40. process(delta)

A `process(delta)` ismétlődően végrehajtott programrészhez tartozó speciális elem.

```resiris
process(delta):
    ...
```

A `delta` az adott feldolgozási ciklushoz tartozó érték.

Ez különösen olyan Resiris környezetekben fontos, ahol folyamatos feldolgozás történik.

## 41. include

Az `include` más Resiris komponensek vagy modulok használatához kapcsolódik.

Például a projektben modulok használhatók vele.

> **CURRENT:** az `include` nyelvi elemként definiálva van.

Részletes végleges include-szemantika: jelenleg nincs teljesen kidolgozva.

## 42. str()

A `str()` érték szöveggé alakítására szolgál.

Például:

```resiris
str(10)
```

eredménye egy string érték.

Ez lehetővé teszi, hogy különböző típusú értékeket szövegként használjunk.

## 43. print_cmd()

A `print_cmd()` egy beépített terminál-kimeneti funkció.

Például:

```resiris
print_cmd("Hello")
```

vagy:

```resiris
v x int = 10
print_cmd(x)
```

A `print_cmd` nem kulcsszó, hanem függvény/beépített nyelvi funkció.

## 44. FunctionalObject

A `FunctionalObject` egy speciális Resiris típus.

Segítségével új hívható objektumot lehet létrehozni.

Például:

```resiris
v double FunctionalObject = FunctionalObject.new(x):
    return x * 2
```

Ezután:

```resiris
v result int = double(5)
```

A `result` értéke: `10`

A `FunctionalObject` célja tehát, hogy a programozó létrehozhasson egy saját hívható objektumot.

**Fontos:** a jelenlegi Resiris nem támogatja azt, hogy egy már meglévő `fn`-t egyszerűen értékként továbbadjunk vagy eltároljunk.

## 45. Modulok

A modulok a Resiris környezetének külön funkcióit biztosítják.

A program modulokon keresztül férhet hozzá bizonyos rendszerfunkciókhoz.

A fő Resiris modul:

```
Resiris.module
```

A modulok saját objektumokat, függvényeket és egyéb használható elemeket biztosíthatnak.

## 46. Modulobjektumok

A modulokból származó speciális objektumoknak külön típusuk lehet:

```
ResirisModuleObject
```

Ezek nem egyszerű számok vagy stringek, hanem a Resiris környezet által biztosított objektumok.

## 47. Hibák

A Resiris különböző hibákat jelezhet, ha a program nem felel meg a nyelv szabályainak.

Például:

- `UnknownVariableError`
- `TypeError`
- `ConstantAssignmentError`
- `MissingValueError`
- `SyntaxError`
- `InvalidInputError`
- `FunctionError`

## 48. UnknownVariableError

Akkor történik, ha a program egy olyan nevet próbál használni, amely nincs definiálva.

Például:

```resiris
print_cmd(abc)
```

ha az `abc` nem létezik.

## 49. TypeError

Akkor történik, amikor egy művelethez nem megfelelő típusú értéket használunk.

Például ha egy művelet olyan típust kap, amit az adott művelet nem támogat.

## 50. ConstantAssignmentError

Akkor történik, amikor egy konstans értékét megpróbáljuk megváltoztatni.

```resiris
c x int = 10
x = 20
```

## 51. MissingValueError

Olyan helyzethez kapcsolódik, amikor egy szükséges érték hiányzik.

## 52. SyntaxError

Akkor történik, amikor a program szintaxisa hibás.

Például hiányzik egy szükséges elem, vagy egy szerkezet nem felel meg a Resiris szabályainak.

## 53. InvalidInputError

Érvénytelen bemeneti adathoz kapcsolódó hiba.

## 54. FunctionError

Függvényekhez kapcsolódó hibák.

Például egy függvény nem megfelelő helyen történő használata.

A `return` például nem használható függvényen kívül.

## 55. Hibák helyének megjelölése

A Resiris hibáihoz forráskód-hely is tartozhat.

Például:

```
sor 3, oszlop 5: TypeError
```

Így a programozó tudja, hogy hol kell keresnie a problémát.

## 56. Tokenek

A tokenek a program legkisebb értelmezett részei.

Például:

```resiris
v x int = 10
```

a Resiris számára nem egyszerűen egy hosszú szöveg.

A tokenizer külön részekre bontja:

```
v
x
int
=
10
```

Ezekből később a parser felépíti a program szerkezetét.

## 57. Tokenizer

A tokenizer az első fontos feldolgozó lépés.

Feladata: a Resiris forráskódot felismerhető elemekre bontani.

Egyszerűen:

```
forráskód
   ↓
tokenizer
   ↓
tokenek
```

## 58. Parser

A parser a tokenekből megpróbálja megérteni, hogy milyen programstruktúrát írtunk.

Például:

```resiris
v x int = 10
```

nem csak tokenek halmaza lesz, hanem a parser felismeri: ez egy varint deklaráció.

## 59. AST

Az AST egy belső fa-szerű reprezentációja annak, amit a programozó leírt.

Például:

```
VariableDeclaration
├── name: x
├── type: int
└── value: 10
```

Az interpreter ezt a struktúrát tudja végrehajtani.

## 60. Interpreter

Az interpreter a Resiris program tényleges végrehajtásáért felel.

A folyamat leegyszerűsítve:

```
Resiris forráskód
       ↓
   Tokenizer
       ↓
     Parser
       ↓
      AST
       ↓
  Interpreter
       ↓
    Runtime
```

Ez azt jelenti, hogy a Resiris program először értelmezésre kerül, majd az interpreter végrehajtja.

## 61. Runtime

A runtime az a környezet, amelyben a Resiris program fut.

Itt történnek például:

- változók kezelése
- értékek kezelése
- függvényhívások
- scope kezelése
- típusellenőrzés
- hibák kezelése
- modulok használata

## 62. A Resiris nyelvi elemeinek nagy térképe

Ha az egészet egyetlen egyszerű listába akarjuk rendezni:

```
RESIRIS
│
├── Forráskód
│   ├── Sorok
│   ├── Kommentek
│   └── Behúzás
│
├── Alapelemek
│   ├── Kulcsszavak
│   ├── Nevek
│   ├── Értékek
│   ├── Literálok
│   └── Tokenek
│
├── Típusok
│   ├── UnknownObject
│   ├── int
│   ├── float
│   ├── string
│   ├── bool
│   ├── Vector2
│   ├── ResirisModuleObject
│   └── FunctionalObject
│
├── Adatok
│   ├── Varint
│   └── Konstans
│
├── Műveletek
│   ├── Operátorok
│   ├── Értékadás
│   └── Kifejezések
│
├── Függvények
│   ├── fn
│   ├── Paraméterek
│   ├── Argumentumok
│   ├── Hívás
│   └── return
│
├── Programvezérlés
│   ├── if
│   ├── elif
│   ├── else
│   ├── mat
│   ├── pass
│   └── await
│
├── Programstruktúra
│   ├── start()
│   ├── process(delta)
│   ├── include
│   └── Modulok
│
├── Beépített funkciók
│   ├── str()
│   └── print_cmd()
│
├── Speciális objektumok
│   ├── FunctionalObject
│   └── ResirisModuleObject
│
└── Hibakezelés
    ├── SyntaxError
    ├── TypeError
    ├── UnknownVariableError
    ├── ConstantAssignmentError
    ├── MissingValueError
    ├── InvalidInputError
    └── FunctionError
```