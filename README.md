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

## Javaslatok

## Egyéb fontos tudnivalók
