import pygame  # Importuje moduł Pygame, który jest biblioteką służącą do tworzenia gier.
import time  # Importuje moduł time, używany do operacji związanych z czasem, ale w tym kodzie jest nieużywany.
import random  # Importuje moduł random, który pozwala na generowanie losowych liczb.

pygame.init()  # Inicjalizuje wszystkie moduły Pygame, co jest wymagane do ich prawidłowego funkcjonowania.

# Definiuje kolory, które będą używane w grze. Kolory są określone jako krotki wartości RGB.
white = (255, 255, 255)  # Biały kolor, maksymalne wartości RGB.
yellow = (255, 255, 102)  # Żółty kolor.
black = (0, 0, 0)  # Czarny kolor, brak koloru w systemie RGB.
red = (213, 50, 80)  # Czerwony kolor.
green = (0, 255, 0)  # Zielony kolor, maksymalna wartość dla zielonego w RGB.
blue = (50, 153, 213)  # Niebieski kolor.
gray = (169, 169, 169)  # Szary kolor.

# Słownik definiujący różne poziomy trudności gry, każdy poziom określa prędkość węża i rozmiar okna gry.
difficulty_settings = {
    'easy': {'speed': 15, 'width': 800, 'height': 600},  # Łatwy poziom z większym oknem i wolniejszym wężem.
    'medium': {'speed': 20, 'width': 600, 'height': 400},  # Średni poziom z mniejszym oknem i szybszym wężem.
    'hard': {'speed': 25, 'width': 400, 'height': 300}  # Trudny poziom z najmniejszym oknem i najszybszym wężem.
}

# Definicja podstawowych zmiennych gry.
snake_block = 10  # Rozmiar jednego bloku węża w pikselach.
dis_width = 800  # Szerokość okna gry w pikselach.
dis_height = 600  # Wysokość okna gry w pikselach.
top_bar_height = 40  # Wysokość górnego paska w pikselach, używanego na wyniki.
total_height = dis_height + top_bar_height  # Całkowita wysokość okna gry z paskiem wyników.
dis = pygame.display.set_mode((dis_width, total_height))  # Ustawienie trybu wyświetlania dla okna gry.
pygame.display.set_caption('Snaky Game')  # Ustawienie tytułu okna gry.

# Inicjalizacja czcionek używanych do wyświetlania tekstu w grze.
font_style = pygame.font.SysFont("comicsans", 25)  # Czcionka dla ogólnego tekstu.
score_font = pygame.font.SysFont("cooper black", 30)  # Czcionka dla wyniku.

clock = pygame.time.Clock()  # Utworzenie zegara do kontrolowania szybkości aktualizacji gry.

highest_score = 0  # Zmienna do przechowywania najwyższego wyniku uzyskanego w trakcie gry.

# Funkcje gry
def our_snake(snake_block, snake_list):
    """Rysuje węża składającego się z bloków."""
    for x in snake_list:  # Iteruje przez listę segmentów węża.
        pygame.draw.rect(dis, green, [x[0], x[1] + top_bar_height, snake_block, snake_block])  # Rysuje zielony kwadrat dla każdego segmentu.

def message(msg, color, x, y):
    """Wyświetla komunikat w określonym miejscu ekranu."""
    mesg = font_style.render(msg, True, color)  # Renderuje wiadomość z tekstem, antyaliasingiem i kolorem.
    dis.blit(mesg, [x, y])  # Umieszcza wiadomość na ekranie w określonym miejscu.

def draw_score(score):
    """Wyświetla aktualny wynik w górnej części ekranu."""
    value = score_font.render("Twój wynik: " + str(score), True, white)  # Renderuje wynik jako tekst.
    dis.blit(value, [20, 0])  # Umieszcza wynik na ekranie blisko górnego lewego rogu.

def draw_highest_score(highest_score):
    """Wyświetla najwyższy wynik na ekranie."""
    value = score_font.render("Najwyższy wynik: " + str(highest_score), True, white)  # Renderuje najwyższy wynik jako tekst.
    dis.blit(value, [dis_width - 200, -5])  # Umieszcza wynik po prawej stronie górnego paska.

def update_highest_score(score):
    """Aktualizuje najwyższy wynik, jeżeli obecny wynik jest wyższy."""
    global highest_score
    if score > highest_score:
        highest_score = score

# Zdefiniowanie stałych wymiarów przy skończeniu gry
""" Stałe wymiary okna po przegranej"""
endgame_width = 800
endgame_height = 600

# Pętla gry
def game_loop():
    """Pętla główna gry, zarządzająca logiką i mechanikami gry."""
    global snake_speed, dis_width, dis_height, dis, highest_score
    game_close = False  # Flag, że gra nie jest zamknięta.
    game_over = False  # Flag, że gra nie jest zakończona.

    x1 = dis_width / 2  # Początkowa pozycja węża w poziomie.
    y1 = dis_height / 2  # Początkowa pozycja węża w pionie.

    x1_change = 0  # Początkowa zmiana pozycji węża w poziomie.
    y1_change = 0  # Początkowa zmiana pozycji węża w pionie.

    snake_List = []  # Lista przechowująca segmenty węża.
    Length_of_snake = 1  # Początkowa długość węża.

    # Losowanie pozycji jedzenia na ekranie.
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_close:  # Kontynuuj grę, dopóki gra nie jest zamknięta.

        for event in pygame.event.get():  # Przechwytuje zdarzenia.
            if event.type == pygame.QUIT:  # Jeśli użytkownik zdecyduje się zamknąć okno.
                game_close = True
            if event.type == pygame.KEYDOWN:  # Jeśli użytkownik naciśnie klawisz.
                # Sprawdzanie kierunku ruchu i zapobieganie ruchowi w przeciwnym kierunku.
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block  # Ruch w lewo.
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block  # Ruch w prawo.
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block  # Ruch w górę.
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block  # Ruch w dół.
                    x1_change = 0

        x1 += x1_change  # Aktualizacja położenia węża w poziomie.
        y1 += y1_change  # Aktualizacja położenia węża w pionie.

        # Sprawdza, czy wąż uderzył w krawędzie ekranu.
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over = True  # Zakończenie gry, gdy wąż uderzy w krawędź.

        # Aktualizacja listy segmentów węża.
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Sprawdza, czy wąż zderzył się z samym sobą.
        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_over = True

        # Rysowanie elementów gry na ekranie.
        dis.fill(black)  # Czyszczenie ekranu.
        pygame.draw.rect(dis, red, [foodx, foody + top_bar_height, snake_block, snake_block])  # Rysowanie jedzenia.
        our_snake(snake_block, snake_List)  # Rysowanie węża.
        pygame.draw.rect(dis, gray, [0, 0, dis_width, top_bar_height])  # Rysowanie paska wyników.
        draw_score(Length_of_snake - 1)  # Wyświetlanie bieżącego wyniku.

        pygame.display.update()  # Aktualizacja pełnego ekranu.

        # Obsługa zjadania jedzenia przez węża.
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0  # Nowa pozycja jedzenia w poziomie.
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0  # Nowa pozycja jedzenia w pionie.
            Length_of_snake += 1  # Zwiększenie długości węża.

        # Obsługa zakończenia gry.
        if game_over:
            update_highest_score(Length_of_snake - 1)  # Aktualizacja najwyższego wyniku.
            # Ustawienie okna końcowego gry.
            dis = pygame.display.set_mode((endgame_width, endgame_height + top_bar_height))
            pygame.display.set_caption('Game Over')
            dis.fill(black)
            pygame.draw.rect(dis, gray, [0, 0, endgame_width, top_bar_height])  # Rysowanie paska wyników w ekranie końcowym.
            message("Przegrana! Naciśnij Q-Wyjście lub C-Graj jeszcze raz", white, endgame_width / 6, endgame_height / 3)
            message(f"Zdobyto {Length_of_snake - 1} pkt!", white, endgame_width / 6, endgame_height / 2)
            message(f"Najwyższy wynik: {highest_score}", white, endgame_width / 6, endgame_height / 1.75)
            pygame.display.update()
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_close = True
                            game_over = False
                        elif event.key == pygame.K_c:
                            game_intro()

        clock.tick(snake_speed)  # Kontroluje szybkość gry, zależną od poziomu trudności.

    pygame.quit()  # Zamyka moduły Pygame.
    quit()  # Zamyka program.

def game_intro():
    """Menu główne gry, pozwala użytkownikowi wybrać poziom trudności."""
    intro = True  # Flaga, że menu jest aktywne.
    intro_width = 800  # Szerokość ekranu startowego.
    intro_height = 600  # Wysokość ekranu startowego.
    intro_dis = pygame.display.set_mode((intro_width, intro_height + top_bar_height))  # Ustawia rozmiar okna startowego.
    pygame.display.set_caption('Snaky')  # Ustawia tytuł ekranu startowego.

    while intro:
        intro_dis.fill(black)  # Czyści ekran na czarno.
        pygame.draw.rect(intro_dis, gray, [0, 0, intro_width, top_bar_height])  # Rysuje górny pasek dla wyników.
        message("Witaj w Snaky!", white, intro_width / 10, intro_height / 3)  # Wyświetla powitanie.
        message("Aby wybrać poziom, naciśnij E-Easy, M-Medium, H-Hard", white, intro_width / 10, intro_height / 2.5)  # Instrukcje wyboru poziomu.
        message("Używaj strzałek, aby poruszać wężem", white, intro_width / 10, intro_height / 2.1)  # Instrukcje sterowania.
        pygame.display.update()  # Aktualizuje ekran.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Zamyka Pygame.
                quit()  # Zamyka program.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    set_difficulty('easy')  # Ustawia poziom łatwy.
                    intro = False  # Wyłącza menu.
                    game_loop()  # Rozpoczyna główną pętlę gry.
                elif event.key == pygame.K_m:
                    set_difficulty('medium')  # Ustawia poziom średni.
                    intro = False  # Wyłącza menu.
                    game_loop()  # Rozpoczyna główną pętlę gry.
                elif event.key == pygame.K_h:
                    set_difficulty('hard')  # Ustawia poziom trudny.
                    intro = False  # Wyłącza menu.
                    game_loop()  # Rozpoczyna główną pętlę gry.

def set_difficulty(level):
    """Ustawia poziom trudności gry na podstawie wyboru użytkownika."""
    global snake_speed, dis_width, dis_height, dis  # Zmienne globalne potrzebne do ustawienia gry.
    settings = difficulty_settings[level]  # Pobiera ustawienia dla wybranego poziomu.
    snake_speed = settings['speed']  # Ustawia prędkość węża.
    dis_width = settings['width']  # Ustawia szerokość okna gry.
    dis_height = settings['height']  # Ustawia wysokość okna gry.
    dis = pygame.display.set_mode((dis_width, dis_height + top_bar_height))  # Ustawia rozmiar okna gry.
    pygame.display.set_caption(f'Snaky poziom - {level.capitalize()}')  # Ustawia tytuł okna z nazwą poziomu.

game_intro()  # Wywołuje funkcję, która rozpoczyna grę, wyświetlając menu główne.
