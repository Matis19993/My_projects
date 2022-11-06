          I Projekt nr 1 - przenoszenie słoika

  1. Pliki źródłowe
  
1.1 W programie służącym do przeniesienia słoika z jednego stołu na drugi znajduje się 7 plików:
- plik przenoszenie_sloika.world odpowiada za utworzenie symulowanego świata z dwoma stolikami i słoikiem,
- plik velma_system.launch odpowiada za uruchomienie systemu Velmy w poprawnej konfiguracji,
- plik init.launch odpowiada za wyczyszczenie kanałów komunikacji robota, jego inicjalizację oraz uruchomienie Rviz,
- plik gazebo.launch odpowiada za uruchomienie symulatora oraz przesłanie odpowiednich układów do robota,
- plik velma.rviz odpowiada za odpowiednią wizualizację robota,
- plik octomap.py odpowiada za utworzenie octomapy dla robota,
- plik go_for_jar.py pozwala na wykonanie zadanego ćwiczenia.

1.2 W pliku octomap.py zostały utworzone dwie funkcje.

Pierwsza, movingHead(q_dest), odpowiada za ruch głową robota oraz sprawdzenie poprawności osiągniętej pozycji. Przyjmuje wartości określające obrót głowy.

Druga, movingTorso(q_map), odpowiada za ruch torsem robota oraz sprawdzenie poprawności osiągniętej pozycji. Przyjmuje wartości określające pozycję robota.

W pliku znajduje się również położenie początkowe robota oraz położenia dla obrotu torsu w prawą i lewą stronę. Następnie inicjowany jest węzeł, robot, planer, słuchacz oktomapy i uruchamiane są silniki. Robot przechodzi w tryb jimp_imp, sprawdzana jest poprawność ustawienia i tworzona jest octomapa. Robot rozgląda się odpowiednio w lewo, w prawo, w dół i przed siebie, jak również porusza torsem w lewo i w prawo. Po utworzeniu mapy wraca do pozycji początkowej.

1.3 W pliku go_for_jar.py zostały utworzone trzy funkcje.

Pierwsza, movingJimp(q_map), odpowiada za planowany ruch w trybie jimp_imp oraz sprawdzenie poprawności osiągniętej pozycji. Przyjmuje wartości określające położenie stawów robota.

Druga, movingRightHand(q_dest), odpowiada za zamykanie i otwieranie palców. Przyjmuje wartości określające położenie palców.

Trzecia, movingCimp(T_dest), odpowiada za ruch w trybie cimp_imp. Przyjmuje punkt, w którym ma znależć się końcówka robota.

W pliku znajduje się również położenie początkowe robota oraz położenia przygotowujące do chwytu oraz odłożenia słoika. Następnie inicjowany jest węzeł, robot, planer, słuchacz oktomapy, uruchamiane są silniki i resetowana jest prawa ręka. Robot przechodzi w tryb jimp_imp, sprawdzana jest poprawność ustawienia, robot zamyka palce i zaczyna wykonywać planowany ruch w kierunku słoika. Następnie otwiera palce, przechodzi w tryb cimp_imp, zbliża się do słoika, zaciska na nim palce i unosi go nad stół. Przechodzi w tryb jimp_imp i porusza się w stronę stolika, na którym ma zostawić słoik. Znowu przechodzi w tryb cimp_imp, przesuwa rękę w miejsce docelowe, opuszcza słoik, otwiera palce i wycofuje rękę. Ostatecznie zamyka palce, przechodzi w tryb jimp_imp i wraca do pozycji startowej, co kończy zadanie.


  2. Uruchomienie programu
  
Aby uruchomić program należy:
- pobrać repozytorium i umieścić je w przestrzeni roboczej ROS w katalogu src,
- w oknie konsoli uruchomić roscore,
- w oknie nowej konsoli uruchomić velma_system.launch,
- w oknie nowej konsoli uruchomić init.launch,
- w oknie nowej konsoli uruchomić gazebo.launch,
- w oknie nowej konsoli uruchomić najpierw program octomap.py, a następnie program go_for_jar.py.


          I Projekt nr 2 - otwieranie szafki

  1. Pliki źródłowe

1.1 W programie służącym do otwierania szafki znajduje się 7 plików:
- plik otwieranie_szafki.world odpowiada za utworzenie symulowanego świata z szafką na stoliku,
- plik velma_system.launch odpowiada za uruchomienie systemu Velmy w poprawnej konfiguracji,
- plik init.launch odpowiada za wyczyszczenie kanałów komunikacji robota, jego inicjalizację oraz uruchomienie Rviz,
- plik gazebo.launch odpowiada za uruchomienie symulatora oraz przesłanie odpowiednich układów do robota,
- plik velma.rviz odpowiada za odpowiednią wizualizację robota,
- plik reset.py pozwala na naprawienie pewnego błędu nie pozwalającego uruchomić pliku go_for_door.py,
- plik go_for_door.py pozwala na wykonanie zadanego ćwiczenia.

1.2 W pliku go_for_door.py zostało utworzonych sześć funkcji.

Pierwsza, movingJimp(q_map), odpowiada za planowany ruch w trybie jimp_imp oraz sprawdzenie poprawności osiągniętej pozycji. Przyjmuje wartości określające położenie stawów robota.

Druga, movingCimpRight(T_dest), odpowiada za ruch prawej ręki w trybie cimp_imp. Przyjmuje punkt, w którym ma znaleźć się końcówka robota.

Trzecia, movingCimpRight(T_dest), odpowiada za ruch lewej ręki w trybie cimp_imp. Przyjmuje punkt, w którym ma znaleźć się końcówka robota.

Czwarta, open(T_dest), wykonuje ruch otwierania szafki na niskiej sztywności. Przyjmuje punkt docelowy, w którym ma znaleźć się końcówka robota.

Piąta, movingRightHand(q_dest), odpowiada za zamykanie i otwieranie palców. Przyjmuje wartości określające położenie palców.

Szósta, makeWrench(lx, ly, lz, rx, ry, rz) odpowiada za zmienianie sztywności manipulatora. Przyjmuje wartości sztywności.

W pliku znajduje się również położenie początkowe robota oraz położenia przygotowujące do rozpoczęcia szukania rączki od drzwiczek szafki. Inicjowany jest węzeł, robot i uruchamiane są silniki. Robot przechodzi w tryb jimp_imp, sprawdzana jest poprawność ustawienia, robot zaczyna wykonywać ruch prawą ręką w kierunku drzwiczek. Następnie ustawia palce w pozycję pozwalającą chwycić za rączkę, przechodzi w tryb cimp_imp, zbliża się do drzwiczek na bardzo niskiej sztywności sprawdzając czy zaczynają one wywierać nacisk na końcówkę taki, żeby zadane koordynaty nie pokrywały się z aktualnymi. Wtedy zaczyna wykonywać ruch wzdłuż drzwiczek aż w ten sam sposób nie zlokalizuje klamki. Następnie ruchem na niskiej, ale już trochę większej sztywności wykonuje dwa następujące po sobie ruchy otwierające drzwiczki na około 70%. Potem usuwa prawą rękę z okolic drzwiczek, i lewą ręką od środkowej części drzwiczek dopycha je na zewnątrz, kończąc tym samym operację otwierania. Lewa ręka po tym manewrze także zostaje usunięta na pozycję początkową, a robot ostatecznie przechodzi w tryb jimp_imp co kończy zadanie.


  2. Uruchomienie programu

Aby uruchomić program należy:
- pobrać repozytorium i umieścić je w przestrzeni roboczej ROS w katalogu src,
- w oknie konsoli uruchomić roscore,
- w oknie nowej konsoli uruchomić velma_system.launch,
- w oknie nowej konsoli uruchomić init.launch,
- w oknie nowej konsoli uruchomić gazebo.launch,
- w oknie nowej konsoli uruchomić program go_for_door.py.


