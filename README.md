## VIMIAC10 Mesterséges intelligencia tárgy - 2022/23. I. félév - 2. házi feladat

# Lunar Lander

## Környezet

## Feladat

## A szimuláció folyamata és a jutalomrendszer

## Beadandó

## A futtatókörnyezet beállítása

A feladatot **java** és **python** nyelven egyaránt meg lehet oldani, viszont a kiértékelőt python nyelven implementáltuk,
így saját számítógépen való teszteléshez szükséges egy Python környezet telepítése.
A telepítéshez elsőként telepítsük a python környezetet, amennyiben az nincs eleve telepítve. 
Ezt megtehetjük a hivatalos [Python telepítő](https://www.python.org/downloads/) vagy a - valamelyest könnyebben kezelhető -
[Anaconda keretrendszer](https://www.anaconda.com/products/distribution) segítségével. 
Mindkét opció egyformán elérhető Windows, Linux és Mac OS operációs rendszerekre.
Ezt követően telepítsük a futtatáshoz szükséges python könyvtárakat, amelyek listáját a [requirements.txt](requirements.txt) fájlban adtuk meg. 
A telepítés legegyszerűbben a `pip` parancs segítségével eszközölhető, az alábbi módon: ```pip install -r requirements.txt```
### Java-specifikus beállítások
Amennyiben a megoldásunkat java nyelven szeretnénk elkészíteni, meg kell adnunk a keretrendszer számára a java 
futtatókörnyezet helyét. Ezt a [lunar_lander_java_agent.py](lunar_lander_java_agent.py) fájlon belül a `java_path` 
változó beállításával tehetjük meg. Például, hogyha a java executable a `/usr/lib/jvm/java-11-openjdk-amd64/bin/` mappában található, 
akkor ezt az alábbi módon állíthatjuk be a [lunar_lander_java_agent.py](lunar_lander_java_agent.py) fájlban:
```
java_path = '/usr/lib/jvm/java-11-openjdk-amd64/bin/'
```
Ezt követően implementáljuk a megoldásunkat a [LunarLanderAgentBase.java](LunarLanderAgentBase.java) fájl módosításával, a lentebb
részletezett interfész-specifikáció alapján. Az implementált megoldást ki lehet próbálni egy GUI-val rendelkező megjelenítő 
([lunar_lander_gui.py](lunar_lander_gui.py)) vagy a Moodle által is használt kiértékelő 
([lunar_lander_evaluator.py](lunar_lander_evaluator.py)) futtatásával.
### Python-specifikus beállítások
Hogyha a megoldást python nyelven szeretnénk elkészíteni, győződjünk meg róla, hogy a [lunar_lander_gui.py](lunar_lander_gui.py) és a
[lunar_lander_evaluator.py](lunar_lander_evaluator.py) fájlokban a `LunarLanderAgent` osztály egy példányát adjuk meg az `agent` változó 
értékeként, és **NEM** a `LunarLanderJavaAgent` osztály példányát. Ennek hatására a keretrendszer a 
[lunar_lander_agent_base.py](lunar_lander_agent_base.py) fájlban található implementációt fogja alapul venni a futása során.

Ezt követően implementáljuk a megoldást a [lunar_lander_agent_base.py](lunar_lander_agent_base.py) fájl módosításával, a lentebb 
részletezett interfész-specifikáció alapján. Az implementált megoldást ki lehet próbálni egy GUI-val rendelkező megjelenítő 
([lunar_lander_gui.py](lunar_lander_gui.py)) vagy a Moodle által is használt kiértékelő 
([lunar_lander_evaluator.py](lunar_lander_evaluator.py)) futtatásával.


## Az interfészről

A feladat megoldása során csak a [LunarLanderAgentBase.java](LunarLanderAgentBase.java) vagy [lunar_lander_agent_base.py](lunar_lander_agent_base.py) 
fájlt szabad módosítani, illetve ez az egyetlen fájl, amelyet a Moodle rendszerbe be is kell adni. Az ezen fájlban található `LunarLanderAgentBase` osztályt 
implementálja majd a `LunarLanderAgent` osztály, amely kiegészíti azt egy `step()` függvénnyel. A `LunarLanderAgentBase` osztály konstruktorában alapból 
definiálásra kerül egy Q táblát leíró változó (`qTable` vagy `q_table`), és egy `epsilon` paraméter. Ezek létezése a `step()` függvény futása miatt fontos, 
**enélkül az nem fog működni**.

Emellett a `LunarLanderAgentBase` osztályt definiáló fájl tartalmaz egy `OBSERVATION_SPACE_RESOLUTION` nevű statikus változót, amelyben meg kell adnunk, 
hogy az állapottér 4 értékét egyenként hány szintre fogjuk kvantálni. Ez azért fontos, mert **ez határozza meg a Q tábla méretét**. Emiatt az állapot 
kvantálásáért felelős függvény (`quantizeState()` vagy `quantize_state()`) mindig egy olyan integer listát/tömböt kell visszaadjon, amellyel a 
Q tábla indexelhető. Például, hogyha a kvantálási szinteket az alábbi módon választom meg: `[15, 10, 15, 8]` akkor a kvantáló függvény 
visszatérési értékének értékkészlete, inkluzív módon az alábbinak kell lennie: `[0-14, 0-9, 0-14, 0-7]` (tehát pl. az első érték legalább 0-s és 
legfeljebb 14-es **integer** értéket kell, hogy felvegyen).

**Mielőtt belekezdenénk az implementációba, javasolt tanulmányozni a `LunarLanderAgent` osztályban definiált `step()` függvény működését!**

A megvalósítandó függvények szignatúráinak leírása az alábbi:

**konstruktor** `LunarLanderAgentBase()`, `LunarLanderAgentBase()`
  * `observation space`: minimum-maximum párok listája/tömbje, amelyek az állapotteret leíró változók által fölvett legkisebb és legnagyobb értéket (float) tartalmazzák: `[platformra mutató vektor X komponense, platformra mutató vektor Y komponense, sebességvektor X komponense, sebességvektor Y komponense]`
  * `action space`: integer lista/tömb, a lehetséges cselekvésekkel (`[0, 1, 2, 3]`, ahol a 0 a "ne csinálj semmit", 1 a "fő hajtómű", 2 a "hajtómű jobbra" és 3 a "hajtómű balra")
  * `number of iterations`: tanulási iterációk száma

**állapot kvantálás** `quantizeState()`, `quantize_state()` - Visszaadja a kapott folytonos állapothoz tartozó kvantált értéket.
  * `observation space`: a konstruktor által is megkapott minimum-maximum párok listája/tömbje, az állapottér változóihoz
  * `state`: a kvantálandó állapot

**epoch vége** `epochEnd()`, `epoch_end()` - Minden epoch végén meghívódik.
  * `epoch reward sum`: az epochban szerzett reward-ok összege

**tanulás** `learn()` - Minden iterációban meghívódik a tanulás során, ez alapján lehet tanítani az ágenst.
  * `old state`: előző állapot
  * `action`: az előző állapotban végrehajtott cselekvés
  * `new state`: a cselekvés eredményeképp létrejött állapot
  * `reward`: az új állapotba lépéssel együtt kapott jutalom

**tanítás vége** `trainEnd()`, `train_end()` - Jelzi a tanítás végét, ez után kezdődik a kiértékelés.

## Javaslatok

* A feladat megoldható maximális pontszámmal Q táblázatos módszerrel.
* A Q tábla méretének (tehát az állapottér változóira alkalmazott kvantálási szintek számának) megfelelő meghatározása kulcsfontosságú. Túlzottan nagy felbontású kvantálás mellett az ágens nem fogja kellő alapossággal fölfedezni az állapotteret, és a számításigény és a memóriaigény is jelentősen megnövekszik. Túlságosan durva (alacsony felbontású) kvantálás mellett pedig előfordulhat, hogy az ágens nem jut kellő mennyiségű információhoz, és így nem tud majd megfelelően dönteni.
* **Az állapotteret nem csak lineárisan lehet kvantálni.** Az állapottér kevésbé fontos részeit (tehát azokat a részeket, ahol feltételezzük, hogy mindenképp csak egyféle helyes döntés létezik, például a sebességvektor szélsőértékeinek közelében, ahol biztosan lassítani kell) kvantálhatjuk alacsonyabb felbontással is, mint a többi részt. Ezáltal a futásidő javul, és a tanulás során az ágens jobban fel tudja fedezni az állapotteret.
* Erősen ajánlott tanulás közben bizonyos időközönként módosítani az `epsilon` ("explore/exploit") paramétert (epsilon-decay), valamint a Q-tanulás frissítési szabályainak paramétereit. Emellett akár a reward-okat is át lehet skálázni az ágens működésén belül.
* A `trainEnd()`/`train_end()` függvények is hint-ek (tehát iránymutatásként vannak jelen).
* Bármilyen felmerülő kérdés esetén a Mesterséges Intelligencia Teams-csoport "Házi Feladat" vagy "Kérdések és Válaszok" csatornájába érdemes írni. Itt egyrészről hamarabb érkezik majd válasz a föltett kérdésekre, illetve a válaszokból így mások is okulhatnak.
* Érdemes a beadási határidő előtt legalább néhány nappal elkezdeni a házi feladat megoldását, mert a határidő közeledtével a rendszer terhelése és az oktatók válaszideje is jelentősen megnőhet.

## Egyéb fontos tudnivalók

* A megoldás forráskódja nem tartalmazhat ékezetes vagy nem ASCII[0:127] karaktert.
* A megoldásnak nem kell, hogy kimenete legyen, ezért ne legyen bennefelejtett debug print, mert errort jelezhet a kiértékelő.
* A feltöltött megoldás megengedett futásideje CPU-időben 40 másodperc. Időtúllépés esetén a rendszer automatikusan leállítja a kód futását.
* A feltöltött megoldás összesen legfeljebb 1000 MB memóriát allokálhat. Ezen érték túllépése esetén a rendszer automatikusan leállítja a kód futását.
* A 2. beadástól kezdve 10 percenként lehet újra próbálkozni.
* Az újonnan beadott megoldás eredménye felülírja az előzőt.
* Minden bugreportot/javaslatot szívesen fogadunk, igyekszünk javítani.
