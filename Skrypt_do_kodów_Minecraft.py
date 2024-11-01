import time
import re
import pyautogui
import pyperclip  # Użyj biblioteki pyperclip do pracy ze schowkiem
from datetime import datetime  # Importujemy datetime do pracy z czasem

# Ścieżka do pliku logów Minecrafta
log_file_path = r"C:\Users\rafal\AppData\Roaming\Crystal-Launcher\instances\Vanilla_1.20.1\.minecraft\logs\latest.log"

# Wzorzec do wyszukania kodu nagrody
reward_pattern = r"\[(\d{2}:\d{2}:\d{2})\] \[Render thread/INFO\]: \[System\] \[CHAT\] Przepisz kod (\w+) aby otrzymać nagrodę!"


# Zmienna śledząca pozycję w pliku
last_position = 0

# Zmienna do przechowywania ostatnio znalezionego kodu
last_code = ""

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

                            # 4-sekundowe opóźnienie przed wysłaniem kodu
                            time.sleep(2)

                            # Skopiowanie kodu do schowka
                            pyperclip.copy(code)

                            # Automatyczne wprowadzanie kodu do czatu Minecrafta
                            pyautogui.click()  # Kliknięcie, aby upewnić się, że Minecraft jest aktywnym oknem
                            time.sleep(1)  # Krótkie opóźnienie
                            pyautogui.press('t')  # Otwiera czat
                            time.sleep(1)  # Czas na otwarcie czatu
                            pyautogui.hotkey('ctrl', 'v')  # Wkleja kod z schowka
                            pyautogui.press('enter')  # Wysyła kod na czacie

    except Exception as e:
        print(f"Error reading log file: {e}")

    # Częstsze sprawdzanie pliku logów
    time.sleep(1)
