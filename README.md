# Rozszerzalne środowisko do agregacji i integracji informacji o grach wideo pochodzących z różnych portali informacyjnych

## Instalacja 

W naszym projekcie używaliśmy Pythona w wersji 3.8.3. Niżej podajemy procedurę przykładowego przygotowania środowiska za pomocą narzędzia Anaconda:

 * conda create -n video_games_integration python==3.8.3
 * conda activate video_games_integration 
 * conda install jupyterlab
 * conda install pandas
 * conda install matplotlib
 * conda install scikit-learn

Po wykonaniu wymienionych komend środowisko będzie gotowe do pracy.

## Używanie modułów
Moduły systemu są w postaci plików o rozszerzeniu .py. One zawierają już gotowy kod do zbierania, integracji, analizy i wizualizacji danych. Użytkownik, chcący skorzystać z naszego systemu, może pracować na trzy sposoby:
1. Praca w trybie interaktywnym. Użytkownik uruchamia środowisko oraz interpreter Pythona w trybie interaktywnym. Dalej importuje funkcje z modułów systemu do środowiska i uruchamia je w pasującej mu kolejności.
2. Praca ze skryptami. Użytkownik pisze skrypt w Pythonie, do którego importuje funkcje z modułów oraz piszę swój kod, który z nich korzysta.
3. Praca z notebookami Jupyter. Jednym z elementów przygotowania środowiska jest instalacja narzędzia Jupyter Lab, pozwalającego pracować w notebookach Jupyter. Praca w takim trybie łączy zalety pracy interaktywnej i ze skryptami.
