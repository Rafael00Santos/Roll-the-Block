class Hole:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "standing"  
        self.move_count = 0  

    def right(self):
        self.move_count += 1  
        if self.state == "standing":
            self.x += 2  
            self.state = "horizontal_x"
        elif self.state == "horizontal_x":
            self.x += 1 
            self.state = "standing"
        elif self.state == "horizontal_y":
            self.x += 1  

    def left(self):
        self.move_count += 1  
        if self.state == "standing":
            self.x -= 1  
            self.state = "horizontal_x"
        elif self.state == "horizontal_x":
            self.x -= 2  
            self.state = "standing"
        elif self.state == "horizontal_y":
            self.x -= 1  

    def up(self):
        self.move_count += 1  
        if self.state == "standing":
            self.y -= 1  
            self.state = "horizontal_y"
        elif self.state == "horizontal_y":
            self.y -= 2  
            self.state = "standing"
        elif self.state == "horizontal_x":
            self.y -= 1  

    def down(self):
        self.move_count += 1  
        if self.state == "standing":
            self.y += 2  
            self.state = "horizontal_y"
        elif self.state == "horizontal_y":
            self.y += 1  
            self.state = "standing"
        elif self.state == "horizontal_x":
            self.y += 1  

class Board:
    def __init__(self, h, l):
        self.h = h
        self.l = l
        self.danger_holes = []
        self.gems = []  
        self.glass_floors = []  

    def add_danger_hole(self, hole):
        self.danger_holes.append(hole)

    def add_gem(self, gem):
        self.gems.append(gem)
        
    def add_glass_floor(self, glass_floor):
        self.glass_floors.append(glass_floor)

    def block_print(self, block):
        coordinates = []
        if block.state == 'horizontal_x':
            coordinates = [(block.x - 1, block.y), (block.x, block.y)]
            return "horizontal_x", coordinates
        elif block.state == 'horizontal_y':
            coordinates = [(block.x, block.y - 1), (block.x, block.y)]
            return "horizontal_y", coordinates
        elif block.state == 'standing':
            return "standing", [(block.x, block.y)]

    def check_win(self, block, hole): #def check_win(self, block, hole, gem_found)
        # se existir gema, ganhou se a encontrar
        # if len(self.gem)>0:  # ou seja, existe uma gema no board 
            # if block.state == "standing" and block.x == hole.x and block.y == hole.y and gem_found: # flag para ver se a gema foi encontrada (esta flag deve vir do 
            # #                     código do algoritmo: quando o x,y do bloco coincidirem 
            # #                     com o x,y da gema, gem_found=True, senão fica com o valor default de False)
            #     return True
        # else: # se não existir gema no mapa
        if block.state == "standing" and block.x == hole.x and block.y == hole.y:  # se se usar o else, meter isto tudo para a frente
            return True
        return False

    def check_danger(self, block):
        state, coordinates = self.block_print(block)
        for x, y in coordinates:
            for danger_hole in self.danger_holes:
                if x == danger_hole.x and y == danger_hole.y:
                    return True

    def is_valid_move(self, block):
        state, coordinates = self.block_print(block)
        for x, y in coordinates:
            if x < 0 or x >= self.l or y < 0 or y >= self.h:
                return False
        return True
    
    def check_special_obstacles(self, block):
        state, coordinates = self.block_print(block)
        effects = {
            'gem': False,
            'glass_break': False
        }
        
        for x, y in coordinates:
            for i, gem in enumerate(self.gems[:]):
                if x == gem.x and y == gem.y:
                    effects['gem'] = True
                    self.gems.pop(i)  
            
            if block.state == "standing":
                for i, glass in enumerate(self.glass_floors[:]):
                    if x == glass.x and y == glass.y:
                        effects['glass_break'] = True
                        
        return effects
    
    def calculate_manhattan_distance(self, block, win_hole):
        if block.state == "standing":
            return abs(block.x - win_hole.x) + abs(block.y - win_hole.y)
        else:
            return abs(block.x - win_hole.x) + abs(block.y - win_hole.y)