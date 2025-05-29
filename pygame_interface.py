import pygame
import sys
from game_logic import Hole, Block, Board

pygame.init()
pygame.mixer.init()

BASE_CELL_SIZE = 50
MARGIN = 20

try:
    background_image = pygame.image.load("Wallpaper.jpg")
    SCREEN_WIDTH, SCREEN_HEIGHT = background_image.get_size()
    if SCREEN_WIDTH > 1920 or SCREEN_HEIGHT > 1080:
        SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    print("Erro ao carregar a imagem de fundo. Usando tamanho padrão.")
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 900
    background_image = None

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Block")
clock = pygame.time.Clock()

try:
    pygame.mixer.music.load("background_music.mp3")  
    pygame.mixer.music.set_volume(0.8)  
    pygame.mixer.music.play(-1)  
except Exception as e:
    print(f"Erro ao carregar música de fundo: {e}")

COLORS = {
    'background': (20, 20, 20),
    'game_background': (150, 150, 150),
    'button': (70, 70, 90, 200),
    'button_hover': (100, 100, 120, 200),
    'text': (255, 255, 255),
    'title': (40, 112, 114),
    'path': (50, 50, 60),
    'grid': (90, 90, 100),
    'block': (48, 152, 155),
    'gem': (143, 219, 131),
    'glass': (162, 212, 237),
    'holes': {
        'win': (155, 119, 48),
        'danger': (150, 150, 150)
    }
}

title_font = pygame.font.SysFont('Dune_Rise', 70)
button_font = pygame.font.SysFont('Segoe Ui', 36)
rules_font = pygame.font.SysFont('Segoe Ui', 24)
game_font = pygame.font.SysFont('Segoe Ui', 20)
large_font = pygame.font.SysFont('Segoe Ui', 32)


class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        color = COLORS['button_hover'] if self.is_hovered else COLORS['button']
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, color, (0, 0, self.rect.width, self.rect.height), border_radius=10)
        pygame.draw.rect(s, (0, 0, 0, 50), (0, 0, self.rect.width, self.rect.height), 2, border_radius=10)
        surface.blit(s, self.rect)

        text_surf = button_font.render(self.text, True, COLORS['text'])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.action:
                self.action()
                return True
        return False


def setup_board_config(level):
    """Dynamic board sizing"""
    configs = {
        1: {'width': 7, 'height': 7, 'cell_size': BASE_CELL_SIZE},
        2: {'width': 8, 'height': 8, 'cell_size': BASE_CELL_SIZE},
        3: {'width': 10, 'height': 10, 'cell_size': BASE_CELL_SIZE - 5},
        4: {'width': 12, 'height': 12, 'cell_size': BASE_CELL_SIZE - 8},
        5: {'width': 14, 'height': 14, 'cell_size': BASE_CELL_SIZE - 10},
        6: {'width': 16, 'height': 16, 'cell_size': BASE_CELL_SIZE - 12},
        7: {'width': 16, 'height': 16, 'cell_size': BASE_CELL_SIZE - 12},
        8: {'width': 16, 'height': 16, 'cell_size': BASE_CELL_SIZE - 12},
        9: {'width': 16, 'height': 16, 'cell_size': BASE_CELL_SIZE - 12}
    }
    return configs.get(level, configs[1])


def show_rules():
    rules_active = True
    rules_text = [
        "REGRAS DO JOGO:",
        "",
        "Space Block é um jogo onde o objetivo é mover",
        "o bloco até à meta (representada pelo dourado).",
        "",
        "O bloco deve terminar na posição vertical sobre a meta.",
        "",
        "- Não deixe o bloco sair do tabuleiro",
        "- Cuidado com os buracos (cinzentos)",
        "- Cuidado com os chãos de vidro (representados a azul claro)",
        "- É necessário apanhar as gemas (verdes) para completar o nível",
        "",
        "Comandos:",
        "- W: Mover para cima",
        "- A: Mover para esquerda",
        "- S: Mover para baixo",
        "- D: Mover para direita",
        "- Q: Sair do nível",
        "",
        "O jogo conta o número de movimentos realizados!"
    ]

    back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Voltar", lambda: None)

    while rules_active:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.handle_event(event):
                rules_active = False

        back_button.check_hover(mouse_pos)

        screen.fill(COLORS['background'])

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 30, 40, 200))
        screen.blit(overlay, (0, 0))

        title_surf = title_font.render("REGRAS DO JOGO", True, COLORS['title'])
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_surf, title_rect)

        for i, line in enumerate(rules_text):
            text_surf = rules_font.render(line, True, COLORS['text'])
            screen.blit(text_surf, (SCREEN_WIDTH // 2 - 300, 150 + i * 30))

        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def run_algorithm(level_config, algorithm_name):
    if algorithm_name == "DFS":
        from dfs_solver import DFSSolver
        solver = DFSSolver(level_config)
    elif algorithm_name == "BFS":
        from bfs_solver import BFSSolver
        solver = BFSSolver(level_config)
    elif algorithm_name == "Greedy":
        from greedy_solver import GreedySolver
        solver = GreedySolver(level_config)
    elif algorithm_name == "A*":
        from a_star_solver import AStarSolver
        solver = AStarSolver(level_config)
    else:
        return

    if solver.solve() and solver.solution:
        level_num = int(level_config["name"][-1])
        board_config = setup_board_config(level_num)
        CELL_SIZE = board_config['cell_size']
        BOARD_WIDTH = board_config['width']
        BOARD_HEIGHT = board_config['height']
        MARGIN = 20

        start_pos = level_config["start_pos"]
        win_pos = level_config.get("win_pos", (BOARD_WIDTH // 2, BOARD_HEIGHT // 2))
        
        block = Block(*start_pos)
        board = Board(BOARD_HEIGHT, BOARD_WIDTH)
        win_hole = Hole(*win_pos)

        for hole in level_config["holes"]:
            board.add_danger_hole(Hole(*hole))

        # Mostra a solução passo a passo
        running = True
        move_index = 0
        total_moves = len(solver.solution['path'])
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_q:  
                        running = False
                        return
            
            if not paused and move_index < total_moves:
                move = solver.solution['path'][move_index]
                if move == "right":
                    block.right()
                elif move == "left":
                    block.left()
                elif move == "up":
                    block.up()
                elif move == "down":
                    block.down()
                
                move_index += 1
                
                pygame.time.wait(600)
            
            screen.fill(COLORS['game_background'])
            draw_game_board(board, block, win_hole, BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE, MARGIN)
            
            info_text = [
                f"Algoritmo: {algorithm_name}",
                f"Movimento {move_index}/{total_moves}",
                f"Tempo de solução: {solver.solution['time']*1000:.0f}ms",
                f"Nós explorados: {solver.solution['nodes_explored']}",
                "Espaço: Pausar/Continuar"
            ]
            segoe_font = pygame.font.SysFont("Segoe UI", 20)  

            for i, text in enumerate(info_text):
                text_surface = segoe_font.render(text, True, (0, 0, 0))
                screen.blit(text_surface, (50, 30 + i * 30))
            
            pygame.display.flip()
            clock.tick(60)
        
        if move_index >= total_moves:
            show_game_message(f"Solução completa! Movimentos: {total_moves}")
    else:
        show_game_message("O algoritmo não encontrou solução!")

def select_solver_mode(level_config):
    mode_active = True
    level_num = int(level_config["name"][-1])
    
    modes = [
        {"name": "Humano", "action": lambda: play_game(level_config)},
    ]
    
    if level_num <= 6:
        modes.extend([
            {"name": "DFS", "action": lambda: run_algorithm(level_config, "DFS")},
            {"name": "BFS", "action": lambda: run_algorithm(level_config, "BFS")},
            {"name": "Greedy", "action": lambda: run_algorithm(level_config, "Greedy")},
            {"name": "A*", "action": lambda: run_algorithm(level_config, "A*")}
        ])

    mode_buttons = []
    button_width = 200
    button_height = 50
    horizontal_spacing = 250
    vertical_spacing = 100
    start_x = SCREEN_WIDTH // 2 - (2 * horizontal_spacing + button_width) // 2
    start_y = SCREEN_HEIGHT // 2 - 50

    for i, mode in enumerate(modes):
        row = i // 3
        col = i % 3
        mode_buttons.append(Button(
            start_x + col * horizontal_spacing,
            start_y + row * vertical_spacing,
            button_width,
            button_height,
            mode["name"],
            mode["action"]
        ))

    back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Voltar", lambda: None)

    while mode_active:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in mode_buttons:
                if button.handle_event(event):
                    mode_active = False
            if back_button.handle_event(event):
                mode_active = False

        for button in mode_buttons:
            button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)

        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(COLORS['background'])

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 30, 40, 180))
        screen.blit(overlay, (0, 0))

        title_surf = title_font.render("SELECIONE O MODO", True, COLORS['title'])
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, start_y - 100))
        screen.blit(title_surf, title_rect)

        for button in mode_buttons:
            button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def level_selection():
    levels_active = True

    levels = [
        {  # Nível 1
            "name": "Nível 1",
            "start_pos": (2, 4),
            "holes": [(0, 3), (6, 2), (3, 0), (2, 6)],
            "win_pos": (3, 3)
        },
        {  # Nível 2
            "name": "Nível 2",
            "start_pos": (1, 3),
            "holes": [(0, 2), (7, 1), (2, 0), (5, 5), (6, 6), (3, 7)],
            "win_pos": (4, 4)
        },
        {  # Nível 3
            "name": "Nível 3",
            "start_pos": (3, 5),
            "holes": [(1, 1), (8, 2), (2, 8), (6, 3), (4, 7), (7, 4), (9, 0)],
            "win_pos": (7, 1)
        },
        {  # Nível 4
            "name": "Nível 4",
            "start_pos": (0, 0),
            "holes": [(2, 2), (9, 1), (4, 8), (7, 5), (10, 3), (3, 10), (6, 7), (1, 11), (8, 4), (5, 9), (11, 6),
                      (0, 6), (6, 0), (5, 2), (7, 9), (9, 7), (2, 5)],
            "win_pos": (11, 11)
        },
        {  # Nível 5
            "name": "Nível 5",
            "start_pos": (1, 1),
            "holes": [(3, 3), (10, 2), (5, 8), (7, 5), (12, 3), (3, 10), (6, 7), (1, 11), (8, 4), (5, 9), (11, 6),
                      (4, 12), (0, 7), (8, 11), (8, 12), (13, 6), (6, 13), (9, 0), (2, 9), (10, 10), (7, 2), (12, 7),
                      (3, 6), (9, 9)],
            "win_pos": (13, 12)
        },
        {  # Nível 6
            "name": "Nível 6",
            "start_pos": (0, 1),
            "holes": [
                (2, 3), (2, 7), (2, 11), (2, 15),
                (4, 1), (4, 3), (4, 5), (4, 7), (4, 9), (4, 11), (4, 13), (4, 15),
                (6, 3), (6, 7), (6, 11), (6, 15), (1, 3), (3, 2),
                (8, 0), (8, 3), (8, 6), (8, 9), (8, 12), (8, 15),
                (10, 3), (10, 7), (10, 11), (10, 15), (1, 9), (0, 11),
                (12, 4), (12, 8), (12, 12), (0, 4), (7, 10),
                (14, 3), (14, 7), (14, 11), (14, 15), (3, 10),
                (1, 5), (3, 9), (5, 13), (7, 1), (9, 10), (11, 6), (13, 2), (15, 14)
            ],
            "win_pos": (0, 14)
        },
        {  # Nível 7 (com gema)
            "name": "Nível 7",
            "start_pos": (0, 1),
            "holes": [
                (2, 3), (2, 7), (2, 11), (2, 15),
                (4, 1), (4, 3), (4, 5), (4, 7), (4, 9), (4, 11), (4, 13), (4, 15),
                (6, 3), (6, 7), (6, 11), (6, 15), (1, 3), (3, 2),
                (8, 0), (8, 3), (8, 6), (8, 9), (8, 12), (8, 15),
                (10, 3), (10, 7), (10, 11), (10, 15), (1, 9), (0, 11),
                (12, 4), (12, 8), (12, 12), (0, 4), (7, 10),
                (14, 3), (14, 7), (14, 11), (14, 15), (3, 10),
                (1, 5), (3, 9), (5, 13), (7, 1), (9, 10), (11, 6), (13, 2), (15, 14)
            ],
            "win_pos": (0, 14),
            "gems": [(8, 8)],
            "glass_floors": []
        },
        {  # Nível 8 (com chão de vidro)
            "name": "Nível 8",
            "start_pos": (0, 1),
            "holes": [
                (2, 3), (2, 7), (2, 11), (2, 15),
                (4, 1), (4, 3), (4, 5), (4, 7), (4, 9), (4, 11), (4, 13), (4, 15),
                (6, 3), (6, 7), (6, 11), (6, 15), (1, 3), (3, 2),
                (8, 0), (8, 3), (8, 6), (8, 9), (8, 12), (8, 15),
                (10, 3), (10, 7), (10, 11), (10, 15), (1, 9), (0, 11),
                (12, 4), (12, 8), (12, 12), (0, 4), (7, 10),
                (14, 3), (14, 7), (14, 11), (14, 15), (3, 10),
                (1, 5), (3, 9), (5, 13), (7, 1), (9, 10), (11, 6), (13, 2), (15, 14)
            ],
            "win_pos": (0, 14),
            "gems": [],
            "glass_floors": [(5, 5),(5,9), (10, 10),(5,15),(15,8),(11,12)]
        },
        {  # Nível 9 (com gema e chão de vidro)
            "name": "Nível 9",
            "start_pos": (0, 1),
            "holes": [
                (2, 3), (2, 7), (2, 11), (2, 15),
                (4, 1), (4, 3), (4, 5), (4, 7), (4, 9), (4, 11), (4, 13), (4, 15),
                (6, 3), (6, 7), (6, 11), (6, 15), (1, 3), (3, 2),
                (8, 0), (8, 3), (8, 6), (8, 9), (8, 12), (8, 15),
                (10, 3), (10, 7), (10, 11), (10, 15), (1, 9), (0, 11),
                (12, 4), (12, 8), (12, 12), (0, 4), (7, 10),
                (14, 3), (14, 7), (14, 11), (14, 15), (3, 10),
                (1, 5), (3, 9), (5, 13), (7, 1), (9, 10), (11, 6), (13, 2), (15, 14)
            ],
            "win_pos": (0, 14),
            "gems": [(7, 7)],
            "glass_floors": [(4, 4), (8, 8),(5,7),(5,12)]
        }
    ]
 
    level_buttons = []          # Layout para os botões de nível
    button_width = 200
    button_height = 50
    horizontal_spacing = 250
    vertical_spacing = 100
    start_x = SCREEN_WIDTH // 2 - (2 * horizontal_spacing + button_width) // 2
    start_y = SCREEN_HEIGHT // 2 - 50

    start_x = SCREEN_WIDTH // 2 - (2 * horizontal_spacing + button_width) // 2
    start_y = SCREEN_HEIGHT // 2 - 70  

    
    for i in range(len(levels)):
        row = i // 3  # Cria botões para todos os níveis (1-9)
        col = i % 3   
        
        level_buttons.append(Button(
            start_x + col * horizontal_spacing,
            start_y + row * vertical_spacing,
            button_width,
            button_height,
            levels[i]["name"],
            lambda i=i: select_solver_mode(levels[i])  # Passa a configuração do nível selecionado
        ))

    back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Voltar", lambda: None)

    while levels_active:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in level_buttons:
                if button.handle_event(event):
                    levels_active = False
            if back_button.handle_event(event):
                levels_active = False

        for button in level_buttons:
            button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)

        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(COLORS['background'])

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 30, 40, 180))
        screen.blit(overlay, (0, 0))

        title_surf = title_font.render("SELECIONE O NIVEL", True, COLORS['title'])
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, start_y - 120))  
        screen.blit(title_surf, title_rect)

        for button in level_buttons:
            button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60) 


def show_settings():
    settings_active = True
    volume = pygame.mixer.music.get_volume()

    volume_up = Button(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2, 50, 50, "+", lambda: None)
    volume_down = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 50, 50, "-", lambda: None)
    back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Voltar", lambda: None)

    while settings_active:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if volume_up.handle_event(event):
                volume = min(1.0, volume + 0.1)
                pygame.mixer.music.set_volume(volume)

            if volume_down.handle_event(event):
                volume = max(0.0, volume - 0.1)
                pygame.mixer.music.set_volume(volume)

            if back_button.handle_event(event):
                settings_active = False

        volume_up.check_hover(mouse_pos)
        volume_down.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)

        screen.fill(COLORS['background'])

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 30, 40, 200))
        screen.blit(overlay, (0, 0))

        title_surf = title_font.render("CONFIGURACOES", True, COLORS['title'])
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(title_surf, title_rect)

        volume_text = large_font.render(f"Volume: {int(volume * 100)}%", True, COLORS['text'])
        screen.blit(volume_text, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 45))

        volume_down.draw(screen)
        volume_up.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def draw_game_board(board, block, win_hole, board_width, board_height, cell_size, margin):
    game_width = board_width * cell_size + 2 * margin
    game_height = board_height * cell_size + 2 * margin + 150  # Espaço para legenda

    board_x = (SCREEN_WIDTH - game_width) // 2
    board_y = (SCREEN_HEIGHT - game_height) // 2

    game_surface = pygame.Surface((game_width, game_height))
    game_surface.fill(COLORS['holes']['danger'])

    board_rect = pygame.Rect(margin, margin, board_width * cell_size, board_height * cell_size)
    pygame.draw.rect(game_surface, COLORS['path'], board_rect)

    for y in range(board_height + 1):
        pygame.draw.line(game_surface, COLORS['grid'],
                         (margin, margin + y * cell_size),
                         (margin + board_width * cell_size, margin + y * cell_size), 2)
    for x in range(board_width + 1):
        pygame.draw.line(game_surface, COLORS['grid'],
                         (margin + x * cell_size, margin),
                         (margin + x * cell_size, margin + board_height * cell_size), 2)

    for hole in board.danger_holes:
        hole_rect = pygame.Rect(margin + hole.x * cell_size, margin + hole.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(game_surface, COLORS['holes']['danger'], hole_rect)

    for gem in board.gems:
        gem_rect = pygame.Rect(margin + gem.x * cell_size + 5, margin + gem.y * cell_size + 5, 
                              cell_size - 10, cell_size - 10)
        pygame.draw.circle(game_surface, COLORS['gem'], gem_rect.center, (cell_size - 10) // 2)
        pygame.draw.circle(game_surface, (0, 0, 0), gem_rect.center, (cell_size - 10) // 2, 1)

    for glass in board.glass_floors:
        glass_rect = pygame.Rect(margin + glass.x * cell_size + 2, margin + glass.y * cell_size + 2,
                                 cell_size - 2, cell_size - 2)
        pygame.draw.rect(game_surface, COLORS['glass'], glass_rect)
        pygame.draw.rect(game_surface, (0, 0, 0), glass_rect, 1)

    win_rect = pygame.Rect(margin + win_hole.x * cell_size + 2, margin + win_hole.y * cell_size + 2, cell_size -2, cell_size -2)
    pygame.draw.rect(game_surface, COLORS['holes']['win'], win_rect)
    pygame.draw.rect(game_surface, (0, 0, 0), win_rect, 1)

    state, coordinates = board.block_print(block)
    for (x, y) in coordinates:
        rect = pygame.Rect(margin + x * cell_size + 5, margin + y * cell_size + 5, cell_size - 10, cell_size - 10)
        pygame.draw.rect(game_surface, COLORS['block'], rect, border_radius=8)

    max_distance = board_width + board_height  
    current_distance = board.calculate_manhattan_distance(block, win_hole)
    progress = 1 - (current_distance / max_distance)  # Invertido para mostrar progresso
    
    progress_bar_height = 10
    progress_bar_y = margin + board_height * cell_size + margin + 125  
    pygame.draw.rect(game_surface, (100, 100, 100), 
                    (margin, progress_bar_y, board_width * cell_size, progress_bar_height))
    
    progress_width = int(board_width * cell_size * progress)
    pygame.draw.rect(game_surface, COLORS['holes']['win'], 
                    (margin, progress_bar_y, progress_width, progress_bar_height))
    
    distance_text = game_font.render(f"Distância: {current_distance}", True, (0, 0, 0))
    game_surface.blit(distance_text, (margin, progress_bar_y - 25))

    legend_y = board_height * cell_size + margin + 10  

    legend_lines = [
        [("Objetivo", COLORS['holes']['win']),
         ("Buracos", COLORS['holes']['danger']),
         ("Bloco", COLORS['block'])],
        [("Caminho", COLORS['path']),
         ("Gema", COLORS['gem']),
         ("Vidro", COLORS['glass'])]
    ]

    for line_num, line_items in enumerate(legend_lines):
        current_y = legend_y + (line_num * 30)  

        available_width = game_width - 2 * margin
        item_width = available_width // len(line_items)

        start_x = margin + (available_width - (len(line_items) * item_width)) // 2

        for i, (text, color) in enumerate(line_items):
            item_x = start_x + i * item_width

            pygame.draw.rect(game_surface, color, (item_x, current_y, 20, 20))
            pygame.draw.rect(game_surface, (0, 0, 0), (item_x, current_y, 20, 20), 1)

            text_surface = game_font.render(text, True, (0, 0, 0))
            game_surface.blit(text_surface, (item_x + 25, current_y))

    instructions_y = legend_y + 60  
    instructions = [
        f"WASD: Mover | Q: Sair",
        f"Movimentos: {block.move_count}"
    ]

    for i, line in enumerate(instructions):
        text_surface = game_font.render(line, True, (0, 0, 0))
        game_surface.blit(text_surface, (margin, instructions_y + i * 25))

    screen.blit(game_surface, (board_x, board_y))


def show_game_message(message):
    text = large_font.render(message, True, COLORS['text'])
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 200))
    screen.blit(s, (0, 0))

    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2500)
    return True


def play_game(level_config):
    level_num = int(level_config["name"][-1])
    board_config = setup_board_config(level_num)

    CELL_SIZE = board_config['cell_size']
    BOARD_WIDTH = board_config['width']
    BOARD_HEIGHT = board_config['height']
    MARGIN = 20

    start_pos = level_config["start_pos"]
    danger_spots = level_config["holes"]
    win_pos = level_config.get("win_pos", (BOARD_WIDTH // 2, BOARD_HEIGHT // 2))  
    gems = level_config.get("gems", [])
    glass_floors = level_config.get("glass_floors", [])

    if start_pos in danger_spots:
        print(f"Error: Start position {start_pos} overlaps with danger hole!")
        return

    block = Block(*start_pos)
    board = Board(BOARD_HEIGHT, BOARD_WIDTH)
    board.level_num = level_num  
    win_hole = Hole(*win_pos)

    for hole in danger_spots:
        board.add_danger_hole(Hole(*hole))

    for gem in gems:
        board.add_gem(Hole(*gem))
        
    for glass in glass_floors:
        board.add_glass_floor(Hole(*glass))

    running = True
    game_over = False
    gem_collected = False if gems else True  

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    block.right()
                elif event.key == pygame.K_a:
                    block.left()
                elif event.key == pygame.K_w:
                    block.up()
                elif event.key == pygame.K_s:
                    block.down()
                elif event.key == pygame.K_q:
                    running = False
                    return

                effects = board.check_special_obstacles(block)
                if effects['gem']:
                    gem_collected = True
                
                if effects['glass_break']:
                    show_game_message(f"Oops! O chão de vidro partiu! Game Over (Movimentos: {block.move_count})")
                    game_over = True
                    continue

                if not board.is_valid_move(block):
                    show_game_message(f"Fora do tabuleiro! Game Over (Movimentos: {block.move_count})")
                    game_over = True
                elif board.check_win(block, win_hole):
                    if gem_collected:  
                        show_game_message(f"Vitória! Movimentos: {block.move_count}")
                    else:
                        show_game_message(f"Falta coletar a gema! Game Over (Movimentos: {block.move_count})")
                    game_over = True
                elif board.check_danger(block):
                    show_game_message(f"Caiu no buraco! Game Over (Movimentos: {block.move_count})")
                    game_over = True

        if game_over:
            pygame.time.wait(1500)
            running = False
            return

        screen.fill(COLORS['game_background'])
        draw_game_board(board, block, win_hole, BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE, MARGIN)
        pygame.display.flip()
        clock.tick(60)


def main_menu():
    menu_active = True

    button_width = 250
    button_height = 60
    button_spacing = 30
    start_y = SCREEN_HEIGHT // 2 - 130

    play_button = Button(SCREEN_WIDTH // 2 - button_width // 2, start_y, button_width, button_height, "Jogar",
                         level_selection)
    settings_button = Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + button_height + button_spacing,
                             button_width, button_height, "Configurações", show_settings)
    rules_button = Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing),
                          button_width, button_height, "Regras", show_rules)
    quit_button = Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + 3 * (button_height + button_spacing),
                         button_width, button_height, "Sair", lambda: (pygame.quit(), sys.exit()))

    while menu_active:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if play_button.handle_event(event):
                pass
            if settings_button.handle_event(event):
                pass
            if rules_button.handle_event(event):
                pass
            if quit_button.handle_event(event):
                menu_active = False

        play_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        rules_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)

        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(COLORS['background'])

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 30, 40, 150))
        screen.blit(overlay, (0, 0))

        title_surf = title_font.render("SPACE BLOCK", True, COLORS['title'])
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, start_y - 60))
        screen.blit(title_surf, title_rect)

        play_button.draw(screen)
        settings_button.draw(screen)
        rules_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
    pygame.quit()
    sys.exit()