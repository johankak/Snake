README ke hře SNAKE

Instalace a spuštění

Instalace
1. Nainstalujte Python 3.7 nebo novější
2. Stáhněte tento repozitář
3. Nainstalujte pip install pygame


Spuštění
1. Otevřete terminál nebo příkazovou řádku
2. Přejděte na soubor main.py
3. Spusťe hru pomocí příkazu python main.py


Struktura hry
1)	Modul constants.py – konstanty a parametry pro hru
2)	Modul game_manager.py = mozek hry
Hlavní třída celé hry – prvním krokem je inicializace hry (vytvoření okna hry, základní proměnné), dále nastavení okna (např. centrování), správa skóre (ukládá se do souboru last_score.json), spravuje zobrazení úvodního menu a spouštění nové hry, konec hry, v neposlední řadě vytváří herní mechaniku – aktualizuje level a zpracovává další tah hry -> next_turn je metoda klíčová která pohybuje hadem, kontroluje kolize, generuje nové jídlo a aktualizuje data
3)	Modul snake.py
Třída Snake implementuje základní mechaniku hada ve hře – had je vykreslen pomocí čtverců na plátně – protože třída importuje plátno pro vykreslování, určuje velikost těla, souřadnice částí těla, směr pohybu. Obsahuje metody pohybu (jako je change_direction), metody pro změnu velikosti (grow/shrink), metodu pro kontrolu kolizí. 
4)	Modul food.py
Třída FoodBase je rodičovská třída pro všechny druhy jídla, která obsahuje logiku pro vytvoření jídla na náhodné pozici pomocí metody generate_coordinates,  třídy dědící od FoodBase volají konstruktor rodičovské třídy a ten nastavuje počáteční stav objektu, to pomocí metody super(). Každá třída dědí z FoodBase a má vlastní tag a barvu pro identifikaci, používají metodu remove() pro odstranění z plátna
5)	Modul main.py
Hlavní spouštěč hry, definuje funkci main() která spouští hru pomocí game.run a obsahuje podmínku která zajisté že se hra spustí pouze když je tento soubor spuštěn přímo 
6)	last_score.json
Soubor sloužící k ukládání posledního dosaženého skóre ve hře, pracují s ním dvě metody – save_score a load_score
7)	snake_image.png
Obrázek hada zobrazující se na úvodním start menu hry



Možnosti rozšíření hry

a) Hra Snake není nijak omezena časem - přidání režimu s časovým limitem na dosažení určitého skóre nebo úrovně
b) Statické či pohyblivé překážky - například kámen, kterému se had musí vyhnout
c) Doplnění zvukovými efekty - aktuálně je hra bez zvuku
d) Vylepšení uživatelského rozhraní - přidání nastavení do menu, např. pro změnu pozadí hry nebo změny klávesovcýh zkratek
e) Implementace režimu pro 2 hráče - vyvtoření 2 hadů 
