import time
import heapq
from game_logic import Hole, Block, Board
import copy

class AStarSolver:
    def __init__(self, level_config):
        self.level_config = level_config
        self.board = None
        self.win_hole = None
        self.visited = set()
        self.solution = None
        self.execution_time = 0
        self.nodes_explored = 0
        self.counter = 0  # Used to break ties in heap

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

    def heuristic(self, block):
        """
        Heuristic function for A* Search (same as Greedy).
        Estimates the cost to reach the goal from the given block state.
        Lower values are better.
        """
        # Manhattan distance to win hole (center of the block)
        if block.state == "standing":
            x_dist = abs(block.x - self.win_hole.x)
            y_dist = abs(block.y - self.win_hole.y)
        elif block.state == "horizontal_x":
            # For horizontal_x, the block occupies (x-1, y) and (x, y)
            x_dist = min(abs(block.x - 1 - self.win_hole.x), abs(block.x - self.win_hole.x))
            y_dist = abs(block.y - self.win_hole.y)
            if self.win_hole.y != block.y:
                y_dist += 2

        else:  # horizontal_y
            # For horizontal_y, the block occupies (x, y-1) and (x, y)
            x_dist = abs(block.x - self.win_hole.x)
            y_dist = min(abs(block.y - 1 - self.win_hole.y), abs(block.y - self.win_hole.y))
            if self.win_hole.x != block.x:
                x_dist += 2

        distance = x_dist + y_dist
        
        # Penalty for not being in standing state (needed to win)
        orientation_penalty = 0 if block.state == "standing" else 2
        
        # Additional penalty for being near danger holes
        danger_penalty = 0
        _, coordinates = self.board.block_print(block)
        for (x, y) in coordinates:
            for hole in self.board.danger_holes:
                if abs(x - hole.x) <= 1 and abs(y - hole.y) <= 1:
                    danger_penalty += 1
        
        return distance + orientation_penalty + danger_penalty

    def solve(self):
        start_time = time.time()
        self.initialize_game()
        
        start_block = Block(*self.level_config["start_pos"])
        
        # Priority queue for A* Search (using heap)
        # Each heap element is a tuple: (f_score, counter, g_score, block, path)
        # f_score = g_score + heuristic
        heap = []
        self.counter = 0
        initial_g_score = 0
        initial_f_score = initial_g_score + self.heuristic(start_block)
        heapq.heappush(heap, (initial_f_score, self.counter, initial_g_score, start_block, []))
        self.counter += 1
        self.visited.add(self.get_state_key(start_block))
        
        while heap:
            _, _, g_score, current_block, path = heapq.heappop(heap)
            self.nodes_explored += 1

            if self.nodes_explored % 10000 == 0:
                print(f"Nós explorados: {self.nodes_explored}... Caminho atual: {len(path)} movimentos")

            if self.board.check_win(current_block, self.win_hole):
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
                    # Calculate new scores
                    new_g_score = g_score + 1  # Each move has cost 1
                    new_f_score = new_g_score + self.heuristic(new_block)
                    heapq.heappush(heap, (new_f_score, self.counter, new_g_score, new_block, path + [move]))
                    self.counter += 1

        self.execution_time = time.time() - start_time
        return False

    def print_solution(self):
        if not self.solution:
            print("Não foi encontrada solução para este nível.")
            return

        print("\n=== Solução A* Search ===")
        print(f"Tempo de execução: {self.solution['time']*1000:.3f} ms")
        print(f"Número de movimentos: {self.solution['move_count']}")
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

    print("A executar A* Search...")
    solver = AStarSolver(level_config)
    
    if solver.solve():
        solver.print_solution()
    else:
        print("Não foi encontrada solução para este nível.")