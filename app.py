import pygame
import os
import subprocess
import time

def main():
    # Inicializa o Pygame e o joystick
    pygame.init()
    pygame.joystick.init()

    screen_width, screen_height = 1920, 1080
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Stardew Valley Interface")

    try:
        background_img = pygame.image.load("bg.png")
        stardew_img = pygame.image.load("stardew.png")
        qr_img = pygame.image.load("qr.png")
    except pygame.error as e:
        print(f"Erro ao carregar imagens: {e}")
        pygame.quit()
        exit()

    # Redimensiona a imagem do Stardew
    #stardew_img = pygame.transform.scale(stardew_img, (600, 400))
    qr_img = pygame.transform.scale(qr_img, (200, 200))


    # Define as cores
    WHITE = (255, 255, 255)
    BLACK = (255, 255, 255)
    GRAY = (100, 100, 100)
    GREEN = (172, 117, 186)


    # Define as fontes
    font_title = pygame.font.Font(None, 74)
    font_desc = pygame.font.Font(None, 36)
    font_button = pygame.font.Font(None, 50)

    # Inicializa o joystick
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    # Função para desenhar texto na tela
    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    # Função para desenhar botões com bordas arredondadas
    def draw_rounded_rect(surface, color, rect, corner_radius):
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

    # Função para executar o jogo
    def execute_game():
        game_path = "C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Stardew Valley\Stardew Valley.exe"
        subprocess.run([game_path])

    # Função para exibir QR
    def display_qr():
        screen.fill(BLACK)
        qr_x = (screen_width - qr_img.get_width()) // 2
        qr_y = (screen_height - qr_img.get_height()) // 2
        screen.blit(qr_img, (qr_x, qr_y))
        pygame.display.flip()
        qr_displayed = True
        return qr_displayed

    # Estado da navegação
    selected_button = 0
    buttons = ["Jogar", "Exibir QR"]

    last_move_time = time.time()
    qr_displayed = False

    running = True
    while running:
        if not qr_displayed:
            # Desenha o fundo
            screen.blit(background_img, (0, 0))

            # Desenha a imagem do Stardew
            stardew_x = 50
            stardew_y = 150
            screen.blit(stardew_img, (stardew_x, stardew_y))

            # Desenha os textos
            draw_text("Stardew", font_title, WHITE, screen, stardew_x, stardew_y + 420)
            draw_text("Um jogo de fazenda", font_desc, WHITE, screen, stardew_x, stardew_y + 480)

            # Desenha os botões
            button_y = 600
            button_x_start = 1200
            button_x_offset = 300
            button_width = 250
            button_height = 80
            corner_radius = 20
            for i, button in enumerate(buttons):
                color = GRAY if i == selected_button else BLACK
                button_rect = pygame.Rect(button_x_start + i * button_x_offset, button_y, button_width, button_height)
                draw_rounded_rect(screen, GREEN, button_rect, corner_radius)
                text_surface = font_button.render(button, True, color)
                text_rect = text_surface.get_rect(center=button_rect.center)
                screen.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # Assumindo que o botão 0 é o botão de "A" do joystick
                    if selected_button == 0:
                        execute_game()
                    elif selected_button == 1:
                        qr_displayed = display_qr()
                elif event.button == 1:  # Assumindo que o botão 1 é o botão de "B" do joystick
                    if qr_displayed:
                        qr_displayed = False
            elif event.type == pygame.JOYAXISMOTION:
                if time.time() - last_move_time > 0.3:  # Adiciona um intervalo de 300 ms
                    if event.axis == 0:  # Eixo horizontal
                        if event.value > 0.5:
                            selected_button = (selected_button + 1) % len(buttons)
                            last_move_time = time.time()
                        elif event.value < -0.5:
                            selected_button = (selected_button - 1) % len(buttons)
                            last_move_time = time.time()

    pygame.quit()

if __name__ == "__main__":
    main()
