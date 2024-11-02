import time
import re
import pyautogui
import pyperclip
import random
from datetime import datetime
import pygetwindow as gw

# Ścieżka do pliku logów Minecrafta
log_file_path = r"C:\Users\rafal\AppData\Roaming\Crystal-Launcher\instances\Vanilla_1.20.1\.minecraft\logs\latest.log"

# Wzorzec do wyszukania kodu nagrody
reward_pattern = r"\[(\d{2}:\d{2}:\d{2})\] \[Render thread/INFO\]: \[System\] \[CHAT\] Przepisz kod (\w+) aby otrzymać nagrodę!"

# Zmienna śledząca pozycję w pliku
last_position = 0

# Zmienna do przechowywania ostatnio znalezionego kodu
last_code = ""

# Lista losowych zdań do wysyłania po wpisaniu kodu
random_messages = [
    "I co, może ktoś powie, że mam haxy, tak?",
    "Dzięki za kod, już wygrywam!",
    "A jednak da się!",
    "Niezły trick, co?",
    "To było łatwe!",
    "Kto by pomyślał!"
]

def activate_minecraft_window():
    """Aktywuje okno Minecrafta i przełącza na pełny ekran (F11)."""
    try:
        # Próba uzyskania okna Minecrafta z odpowiednim tytułem
        mc_window = gw.getWindowsWithTitle('Minecraft 1.20.1 - Multiplayer (3rd-party Server)')[0]
        if mc_window.isMinimized:
            mc_window.restore()  # Przywraca, jeśli zminimalizowane
        mc_window.activate()  # Przenosi na pierwszy plan
        time.sleep(1)  # Zapewnia czas na aktywację
        pyautogui.press('f11')  # Przełącza na pełny ekran
        return True
    except IndexError:
        print("Okno Minecrafta nie zostało znalezione.")
        return False

def click_back_to_game_using_coordinates(x, y):
    """Kliknięcie w przycisk 'Back to Game' za pomocą koordynatów."""
    print(f"Przesuwam do współrzędnych: {x}, {y}")
    pyautogui.moveTo(x, y, duration=0.5)  # Dodanie czasu trwania dla płynniejszego ruchu
    time.sleep(0.5)  # Czekamy chwilę przed kliknięciem
    print("Klikam...")
    pyautogui.click()
    print("Kliknięcie zakończone.")

# Ustal współrzędne przycisku "Back to Game"
x_coord = 949  # Przykładowa współrzędna X
y_coord = 330  # Przykładowa współrzędna Y

while True:
    try:
        with open(log_file_path, "r", encoding="windows-1250") as log_file:
            log_file.seek(last_position)
            new_lines = log_file.readlines()
            last_position = log_file.tell()

            # Pobieranie aktualnego czasu w formacie HH:MM
            current_time = datetime.now().strftime("%H:%M")
            print(f"Current time: {current_time}")  # Debug: wyświetlanie aktualnego czasu

            for line in new_lines:
                print(f"Processing line: {line.strip()}")  # Debug: wyświetlanie przetwarzanej linii
                # Sprawdzenie, czy linia zawiera kod nagrody
                reward_match = re.search(reward_pattern, line)
                if reward_match:
                    log_time, code = reward_match.groups()  # Wyciągamy czas i kod
                    print(f"Found code: {code} at time: {log_time}")  # Debug: wyświetlanie znalezionego kodu

                    # Sprawdzenie, czy czas w logach jest zgodny z aktualnym czasem
                    if log_time[:5] == current_time:  # Porównujemy HH:MM
                        # Sprawdź, czy kod jest nowy
                        if code != last_code:  # Wysyłaj tylko, jeśli kod jest nowy
                            last_code = code  # Aktualizujemy ostatni kod

                            # Sprawdzenie, czy okno Minecrafta jest już otwarte i aktywne
                            if not activate_minecraft_window():
                                # Kliknięcie przycisku "Back to Game" za pomocą koordynatów
                                time.sleep(2)  # Czekamy, aby mieć pewność, że okno zostało przywrócone
                                click_back_to_game_using_coordinates(x_coord, y_coord)

                            # 4-sekundowe opóźnienie przed wysłaniem kodu
                            time.sleep(1)

                            # Skopiowanie kodu do schowka
                            pyperclip.copy(code)

                            # Automatyczne wprowadzanie kodu do czatu Minecrafta
                            pyautogui.click()  # Kliknięcie, aby upewnić się, że Minecraft jest aktywnym oknem
                            time.sleep(1)  # Krótkie opóźnienie
                            pyautogui.press('t')  # Otwiera czat

                            time.sleep(1)  # Czas na otwarcie czatu
                            pyautogui.hotkey('ctrl', 'v')  # Wkleja kod z schowka
                            pyautogui.press('enter')  # Wysyła kod na czacie

                            # 4-sekundowe opóźnienie przed wysłaniem dodatkowej wiadomości
                            time.sleep(6)
                            random_message = random.choice(random_messages)  # Wybiera losowe zdanie
                            pyperclip.copy(random_message)  # Kopiuje zdanie do schowka
                            pyautogui.press('t')  # Otwiera czat
                            time.sleep(1)  # Krótkie opóźnienie
                            pyautogui.hotkey('ctrl', 'v')  # Wkleja wiadomość z schowka
                            pyautogui.press('enter')  # Wysyła wiadomość

    except Exception as e:
        print(f"Error reading log file: {e}")

    # Częstsze sprawdzanie pliku logów
    time.sleep(1)
