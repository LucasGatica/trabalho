import pygame
import sys
import os

pygame.init()

screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Jogos em Destaque")

BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
PINK = (172, 117, 186)

def load_and_resize(image_path, width, height):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (width, height))

# Carregar a imagem de fundo
background_image = load_and_resize('bg.png', screen_width, screen_height)
# Carregar a imagem do logo
logo_image = load_and_resize('logo.png', 300*0.85, 200*0.85)

game_images = [
    load_and_resize('cs.png', 260, 460),
    load_and_resize('cs.png', 260, 460),
    load_and_resize('cs.png', 260, 440),
    load_and_resize('cs.png', 260, 460),
    load_and_resize('cs.png', 260, 460)
]

games_info = [
    {
        "name": "Stardew valley",
        "categories": ["Fazenda", "Relaxante", "Casual"],
        "description": "eu amo tanto esse jogo eu amo tanto esse jogo",
        "executable_path": "C:\\Program Files (x86)\\Steam\\steamapps\\common\\BOT.vinnik Chess Early USSR Championships\\bot4_release\\Bot.vinnik Chess Early USSR Championships.exe"
    },
    {
        "name": "Stardew Valley",
        "categories": ["RPG", "Casual", "Indie"],
        "description": "Stardew Valley é um RPG de simulação onde você herda uma antiga fazenda e começa uma nova vida no campo.",
        "executable_path": ""
    },
    {
        "name": "Guilty Gear",
        "categories": ["Luta", "Arcade", "Competitivo"],
        "description": "sexo",
        "executable_path": ""
    },
    {
        "name": "F1 2024",
        "categories": ["Corrida", "Simulação", "Esportes"],
        "description": "sexo",
        "executable_path": "C:\\path\\to\\f1_2024.exe"
    }
,
    {
        "name": "F1 2024",
        "categories": ["Corrida", "Simulação", "Esportes"],
        "description": "sexo",
        "executable_path": "C:\\path\\to\\f1_2024.exe"
    }

]

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("Nenhum joystick conectado!")
    sys.exit()

def draw_interface(selected_game_index):
    screen.fill(BROWN)

    # Desenhar a imagem de fundo
    screen.blit(background_image, (0, 0))

    font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font(None, 62)

    # Calcular a posição inicial x_pos para centralizar as imagens dos jogos
    total_width = sum(image.get_width() for image in game_images) + (len(game_images) - 1) * 50
    x_pos = (screen_width - total_width) // 2

    # Calcular a posição y_pos para centralizar as imagens dos jogos verticalmente
    total_height = max(image.get_height() for image in game_images)
    y_pos_images = (screen_height - total_height) // 2

    for index, image in enumerate(game_images):
        if index == selected_game_index:
            pygame.draw.rect(screen, WHITE, (x_pos - 10, y_pos_images - 10, image.get_width() + 20, image.get_height() + 20), 3)
        screen.blit(image, (x_pos, y_pos_images))
        x_pos += image.get_width() + 50

    selected_game = games_info[selected_game_index]

    # Desenhar o nome do jogo acima das categorias
    game_name_text = title_font.render(selected_game["name"], True, WHITE)
    game_name_rect = game_name_text.get_rect(center=(screen_width // 2, y_pos_images + total_height + 50))
    screen.blit(game_name_text, game_name_rect)

    # Centralizar as categorias horizontalmente abaixo do nome do jogo
    categories_text = [font.render(category, True, WHITE) for category in selected_game["categories"]]
    total_categories_width = sum(text.get_width() for text in categories_text) + (len(categories_text) - 1) * 20
    x_pos_categories = (screen_width - total_categories_width) // 2
    y_pos_categories = game_name_rect.bottom + 20

    for text in categories_text:
        text_rect = text.get_rect()
        pygame.draw.rect(screen, PINK, (x_pos_categories - 10, y_pos_categories - 10, text_rect.width + 20, text_rect.height + 20))
        screen.blit(text, (x_pos_categories, y_pos_categories))
        x_pos_categories += text_rect.width + 40

    # Centralizar a descrição verticalmente abaixo das categorias
    description = f"Sobre: {selected_game['description']}"
    description_lines = description.split('\n')
    total_description_height = len(description_lines) * 40
    y_pos_description = y_pos_categories + 60

    for line in description_lines:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(screen_width // 2, y_pos_description))
        screen.blit(text, text_rect)
        y_pos_description += 40

    # Centralizar a imagem do logo no topo da tela
    logo_rect = logo_image.get_rect(center=(screen_width // 2, logo_image.get_height() // 1.7))
    screen.blit(logo_image, logo_rect)

    pygame.display.flip()

def handle_joystick_motion(axis_value, selected_game_index, last_move_time, current_time, threshold=0.5, delay=0.2):
    if axis_value < -threshold and current_time - last_move_time > delay:
        selected_game_index = (selected_game_index - 1) % len(game_images)
        last_move_time = current_time
    elif axis_value > threshold and current_time - last_move_time > delay:
        selected_game_index = (selected_game_index + 1) % len(game_images)
        last_move_time = current_time
    return selected_game_index, last_move_time

def execute_game(executable_path):
    if os.path.exists(executable_path):
        os.startfile(executable_path)
    else:
        print(f"Executable path not found: {executable_path}")

def main():
    selected_game_index = 1
    clock = pygame.time.Clock()
    last_move_time = 0

    while True:
        current_time = pygame.time.get_ticks() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.JOYAXISMOTION:
                axis_value = joystick.get_axis(0)
                selected_game_index, last_move_time = handle_joystick_motion(axis_value, selected_game_index, last_move_time, current_time)
            elif event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(0):
                    selected_game = games_info[selected_game_index]
                    print(f"Você escolheu abrir o jogo: {selected_game['name']}")
                    execute_game(selected_game['executable_path'])

        draw_interface(selected_game_index)
        clock.tick(60)

if __name__ == "__main__":
    main()