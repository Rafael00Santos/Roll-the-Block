from game_logic import Hole, Block, Board

def print_board(board, block, hole):
    print("\n" + "="*47)
    print(f"Posição: ({block.x},{block.y}) | Estado: {block.state} | Movimentos: {block.move_count}")
    print("Controlos: W (↑), S (↓), A (←), D (→), Q (sair)")
    print("="*47 + "\n")
    
    for y in range(board.h):
        for x in range(board.l):
            state, coords = board.block_print(block)
            if (x, y) in coords:
                print("B", end=" ")
            elif x == hole.x and y == hole.y:
                print("X", end=" ")
            elif any(h.x == x and h.y == y for h in board.danger_holes):
                print("1", end=" ")  
            elif any(g.x == x and g.y == y for g in board.gems):
                print("4", end=" ") 
            elif any(gl.x == x and gl.y == y for gl in board.glass_floors):
                print("2", end=" ")  
            else:
                print("0", end=" ")  
        print()  

def setup_level(level):
    """Configura o nível do jogo conforme a seleção"""
    levels = {
        1: {
            "name": "Nível 1",
            "start_pos": (2, 4),
            "holes": [(0, 3), (6, 2), (3, 0), (2, 6)],
            "size": (7, 7)
        },
        2: {
            "name": "Nível 2",
            "start_pos": (1, 3),
            "holes": [(0, 2), (7, 1), (2, 0), (5, 5), (6, 6), (3, 7)],
            "size": (8, 8)
        },
        3: {
            "name": "Nível 3",
            "start_pos": (3, 5),
            "holes": [(1, 1), (8, 2), (2, 8), (6, 3), (4, 7), (7, 4), (9, 0)],
            "size": (10, 10)
        },
        4: {
            "name": "Nível 4",
            "start_pos": (0, 0),
            "holes": [(2, 2), (9, 1), (4, 8), (7, 5), (10, 3), (3, 10),
                     (6, 7), (1, 11), (8, 4), (5, 9), (11, 6), (0, 6),
                     (6, 0), (11, 11), (5, 2), (7, 9), (9, 7), (2, 5)],
            "size": (12, 12)
        },
        5: {
            "name": "Nível 5",
            "start_pos": (1, 1),
            "holes": [(3, 3), (10, 2), (5, 8), (7, 5), (12, 3), (3, 10),
                     (6, 7), (1, 11), (8, 4), (5, 9), (11, 6), (4, 12),
                     (0, 7), (13, 6), (6, 13), (9, 0), (2, 9), (10, 10),
                     (7, 2), (12, 7), (3, 6), (9, 9)],
            "size": (14, 14)
        },
        6: {
            "name": "Nível 6",
            "start_pos": (0, 8),
            "holes": [(x, y) for x in range(16) for y in [3, 7, 11, 15] 
                     if not (x == 0 and y == 7) and not (x == 15 and y == 11)] +
                     [(4, y) for y in range(16) if y not in [2, 6, 10, 14]] +
                     [(8, y) for y in range(16) if y % 3 == 0] +
                     [(12, y) for y in range(16) if y > 0 and y % 4 == 0],
            "size": (16, 16)
        },
        7: {  # Nível 7 (com gema)
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
            "size": (16, 16),
            "gems": [(8, 8)],
            "glass_floors": []
        },
        8: {  # Nível 8 (com chão de vidro)
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
            "size": (16, 16),
            "gems": [],
            "glass_floors": [(5, 5), (10, 10)]
        },
        9: {  # Nível 9 (com gema e chão de vidro)
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
            "size": (16, 16),
            "gems": [(7, 7)],
            "glass_floors": [(4, 4), (8, 8)]
        }
    }
    
    level_data = levels.get(level, levels[1])
    width, height = level_data["size"]
    
    block = Block(*level_data["start_pos"])
    board = Board(height, width)
    hole = Hole(width//2, height//2)
    
    for hole_pos in level_data["holes"]:
        board.add_danger_hole(Hole(*hole_pos))
    
    if "gems" in level_data:
        for gem_pos in level_data["gems"]:
            board.add_gem(Hole(*gem_pos))
    
    if "glass_floors" in level_data:
        for glass_pos in level_data["glass_floors"]:
            board.add_glass_floor(Hole(*glass_pos))
    
    return board, block, hole, level_data["name"]

def level_selection():
    """Menu de seleção de nível"""
    print("\n" + "="*47)
    print("SELECIONE O NÍVEL")
    print("="*47)
    print("1. Nível 1 (7x7)")
    print("2. Nível 2 (8x8)")
    print("3. Nível 3 (10x10)")
    print("4. Nível 4 (12x12)")
    print("5. Nível 5 (14x14)")
    print("6. Nível 6 (16x16)")
    print("7. Nível 7 (16x16) - Com Gema")
    print("8. Nível 8 (16x16) - Com Vidro")
    print("9. Nível 9 (16x16) - Com Gema e Vidro")
    print("Q. Voltar/Sair")
    
    while True:
        choice = input("Escolha o nível (1-9) ou Q para sair: ").strip().lower()
        
        if choice == 'q':
            return None
        elif choice.isdigit() and 1 <= int(choice) <= 9:
            return int(choice)
        else:
            print("Opção inválida! Escolha de 1 a 9 ou Q para sair.")

def play_game(board, block, hole, level_name):
    """Loop principal do jogo"""
    gem_collected = not bool(board.gems)  # True se não houver gemas para coletar
    
    while True:
        print_board(board, block, hole)
        
        move = input("Movimento (W/A/S/D/Q): ").strip().lower()
        
        if move == 'd':
            block.right()
        elif move == 'a':
            block.left()
        elif move == 'w':
            block.up()
        elif move == 's':
            block.down()
        elif move == 'q':
            print("Jogo terminado!")
            return False
        else:
            print("Movimento inválido! Use W/A/S/D ou Q para sair.")
            continue

        effects = board.check_special_obstacles(block)
        if effects['gem']:
            gem_collected = True
            print("\nGema coletada!")
        
        if effects['glass_break']:
            print("\n=== GAME OVER ===")
            print("O chão de vidro (2) quebrou!")
            return False

        if not board.is_valid_move(block):
            print("\n=== GAME OVER ===")
            print("O bloco saiu do tabuleiro!")
            return False
            
        if board.check_danger(block):
            print("\n=== GAME OVER ===")
            print("O bloco caiu num buraco (1)!")
            return False
            
        if board.check_win(block, hole):
            if gem_collected:
                print("\n=== VITÓRIA ===")
                print(f"Concluiu {level_name} em {block.move_count} movimentos!")
                return True
            else:
                print("\n=== GAME OVER ===")
                print("Você precisa coletar a gema (4) primeiro!")
                return False

def main():
    """Função principal"""
    print("=== SPACE BLOCK - Versão Console ===")
    
    while True:
        print("\nMENU PRINCIPAL")
        print("1. Jogar")
        print("2. Regras")
        print("3. Sair")
        
        choice = input("Escolha uma opção: ").strip()
        
        if choice == '1':
            level = level_selection()
            if level is not None:
                board, block, hole, level_name = setup_level(level)
                play_game(board, block, hole, level_name)
        elif choice == '2':
            print("\n" + "="*47)
            print("REGRAS DO JOGO")
            print("="*47)
            print("Objetivo: Leve o bloco (B) até ao objetivo (X)")
            print("Cuidado com os buracos (1) e com as bordas do tabuleiro!")
            print("O bloco deve estar na posição vertical para vencer.")
            print("\nNovos elementos:")
            print("4 - Gema (deve ser coletada para vencer em alguns níveis)")
            print("2 - Chão de vidro (quebra quando o bloco está em pé)")
            print("\nControles:")
            print("W - Mover para cima")
            print("A - Mover para esquerda")
            print("S - Mover para baixo")
            print("D - Mover para direita")
            print("Q - Sair do nível")
            print("\nLegenda:")
            print("B - Bloco")
            print("X - Objetivo")
            print("1 - Buraco perigoso")
            print("2 - Chão de vidro")
            print("4 - Gema")
            print("0 - Caminho seguro")
            input("\nPressione Enter para continuar...")
        elif choice == '3':
            print("Obrigado por jogar!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()