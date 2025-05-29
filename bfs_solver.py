import time
from collections import deque
from game_logic import Hole, Block, Board
import copy

class BFSSolver:
    def __init__(self, level_config):
        self.level_config = level_config
        self.board = None
        self.win_hole = None
        self.visited = set()
        self.solution = None
        self.execution_time = 0
        self.nodes_explored = 0
        #self.flag=False

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
        # Key that considers all cells occupied by the block
        _, coordinates = self.board.block_print(block)
        sorted_coords = tuple(sorted(coordinates))
        return (block.state, sorted_coords)

    def get_possible_moves(self, block):
        moves = []
        for move_func in [Block.right, Block.left, Block.up, Block.down]:
            temp_block = copy.deepcopy(block)
            move_func(temp_block)
            
            if self.board.is_valid_move(temp_block) and not self.board.check_danger(temp_block):
                moves.append((
                    move_func.__name__,
                    temp_block.x,
                    temp_block.y,
                    temp_block.state
                ))
        return moves

    def solve(self):
        start_time = time.time()
        self.initialize_game()
        
        start_block = Block(*self.level_config["start_pos"])
        queue = deque([(start_block, [])])
        self.visited.add(self.get_state_key(start_block))
        
        while queue:
            current_block, path = queue.popleft()
            self.nodes_explored += 1

            if self.nodes_explored % 10000 == 0:
                print(f"Nós explorados: {self.nodes_explored}... Caminho atual: {len(path)} movimentos")

            if self.board.check_win(current_block, self.win_hole): # passar à função a flag como argumento ex:(self.board.check_win(current_block, self.win_hole, self.flag))
                self.execution_time = time.time() - start_time
                self.solution = {
                    'path': path,
                    'move_count': len(path),
                    'time': self.execution_time,
                    'nodes_explored': self.nodes_explored
                }
                return True

            for move, x, y, state in self.get_possible_moves(current_block):
                new_block = Block(x, y)
                new_block.state = state
                new_block.move_count = current_block.move_count + 1
                
                state_key = self.get_state_key(new_block)
                if state_key not in self.visited:
                    if self.board.check_win(new_block, self.win_hole):
                        self.execution_time = time.time() - start_time
                        self.solution = {
                            'path': path + [move],
                            'move_count': len(path) + 1,
                            'time': self.execution_time,
                            'nodes_explored': self.nodes_explored
                        }
                        return True
                    
                    self.visited.add(state_key)
                    queue.append((new_block, path + [move]))

        self.execution_time = time.time() - start_time
        return False

    def print_solution(self):
        if not self.solution:
            print("Não foi encontrada solução para este nível.")
            return

        print("\n=== Solução BFS ===")
        print(f"Tempo de execução: {self.solution['time']*1000:.3f} ms")
        print(f"Número de movimentos: {self.solution['move_count']}")
        print(f"Nós explorados: {self.solution['nodes_explored']}")
        print("\nSequência de movimentos:")
        print(" -> ".join(self.solution['path']))

if __name__ == "__main__":
    level_config = {
        "name": "Nível 5",
            "start_pos": (1, 1),
            "holes": [(3, 3), (10, 2), (5, 8), (7, 5), (12, 3), (3, 10), (6, 7), (1, 11), (8, 4), (5, 9), (11, 6),
                      (4, 12), (0, 7), (8, 11), (8, 12), (13, 6), (6, 13), (9, 0), (2, 9), (10, 10), (7, 2), (12, 7),
                      (3, 6), (9, 9)],
            "win_pos": (13, 12)
    }

    print("A executar BFS...")
    solver = BFSSolver(level_config)
    
    if solver.solve():
        solver.print_solution()
    else:
        print("Não foi encontrada solução para este nível.")