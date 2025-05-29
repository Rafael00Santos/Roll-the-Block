import time
from game_logic import Hole, Block, Board
import copy

class DFSSolver:
    def __init__(self, level_config, max_depth=25):
        self.level_config = level_config
        self.max_depth = max_depth  
        self.board = None
        self.win_hole = None
        self.visited = set()
        self.solution = None
        self.execution_time = 0
        self.nodes_explored = 0
        self.found_solution = False  # Nova flag para parada antecipada

    def initialize_game(self):
        level_num = int(self.level_config["name"][-1])
        board_config = {
            1: {'width': 7, 'height': 7},
            2: {'width': 8, 'height': 8},
            3: {'width': 10, 'height': 10},
            4: {'width': 12, 'height': 12},
            5: {'width': 14, 'height': 14},
            6: {'width': 16, 'height': 16}
        }.get(level_num, {'width': 10, 'height': 10})

        self.board = Board(board_config['height'], board_config['width'])
        
        win_pos = self.level_config.get("win_pos", 
                                      (board_config['width']//2, board_config['height']//2))
        self.win_hole = Hole(*win_pos)
        
        for hole_pos in self.level_config["holes"]:
            self.board.add_danger_hole(Hole(*hole_pos))

    def get_state_key(self, block):
        _, coordinates = self.board.block_print(block)
        return (block.state, tuple(sorted(coordinates)))

    def get_possible_moves(self, block):
        moves = []
        for move_func in [Block.right, Block.left, Block.up, Block.down]:
            temp_block = copy.deepcopy(block)
            move_func(temp_block)
            
            if self.board.is_valid_move(temp_block) and not self.board.check_danger(temp_block):
                moves.append((move_func.__name__, temp_block))
        return moves

    def solve(self):
        start_time = time.time()
        self.initialize_game()
        self.visited = set()
        self.nodes_explored = 0
        self.found_solution = False  # Reset da flag
        
        start_block = Block(*self.level_config["start_pos"])
        solution_path = self.dfs(start_block, [], 0, set())
        
        self.execution_time = time.time() - start_time
        
        if solution_path:
            self.solution = {
                'path': solution_path,
                'time': self.execution_time,
                'nodes_explored': self.nodes_explored
            }
            return True
        return False

    def dfs(self, current_block, path, depth, visited):
        """Recursive DFS with early stopping"""
        if self.found_solution:  # Parada antecipada se solução já encontrada
            return None

        self.nodes_explored += 1
        
        if self.nodes_explored % 10000 == 0:
            print(f"Nós explorados: {self.nodes_explored}, Profundidade atual: {depth}")
            
        if self.board.check_win(current_block, self.win_hole):
            self.found_solution = True  # Marca que encontrou solução
            return path
        
        if depth >= self.max_depth:
            return None
        
        state_key = self.get_state_key(current_block)
        if state_key in visited:
            return None
            
        visited.add(state_key)
        
        for move_name, next_block in self.get_possible_moves(current_block):
            result = self.dfs(next_block, path + [move_name], depth + 1, visited.copy())
            if result is not None:
                return result
                
        return None

    def print_solution(self):
        if not self.solution:
            print("Nenhuma solução encontrada dentro do limite de profundidade.")
            return

        print("\n=== Solução DFS ===")
        print(f"Tempo de Execução: {self.execution_time*1000:.3f} ms")
        print(f"Movimentos necessários: {len(self.solution['path'])}")
        print(f"Nós explorados: {self.solution['nodes_explored']}")
        print("\nSequência de movimentos:")
        print(" -> ".join(self.solution['path']))


if __name__ == "__main__":
    level_config = {
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
    }

    solver = DFSSolver(level_config, max_depth=25)
    
    print("A executar DFS com limite de profundidade...")
    if solver.solve():
        solver.print_solution()
    else:
        print(f"Solução não encontrada com {solver.max_depth} movimentos.")