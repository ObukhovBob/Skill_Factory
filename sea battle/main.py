from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Dots:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:

    def __init__(self, bow: Dots, size: int, layout: bool):
        self.bow = bow
        self.size = size
        self.layout = layout
        self.life = size

    @property
    def dot(self):
        ship_dots = []
        for i in range(self.size):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.layout:
                cur_x += i
            elif not self.layout:
                cur_y += i
            ship_dots.append(Dots(cur_x, cur_y))
        return ship_dots


class Board:

    def __init__(self, size: int = 6, hidden: bool = False):
        self.size = size
        self.hidden = hidden
        self.board = [["×"] * size for i in range(size)]
        self.count = 0
        self.busy = []
        self.ships = []

    def __str__(self):
        board_out = ""
        upper_scale = [f"{i + 1}" for i in range(self.size)]
        board_out += "    " + "   ".join(upper_scale)
        for i, row in enumerate(self.board):
            board_out += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hidden:
            board_out = board_out.replace("◙", "×")
        return board_out

    def border_check(self, dot: Dots):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def busy_check(self, dot: Dots):
        return dot not in self.busy

    def contour(self, ship: Ship, cont=False):

        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for d in ship.dot:
            for dx, dy in near:
                cur = Dots(d.x + dx, d.y + dy)
                if not (self.border_check(cur)) and self.busy_check(cur):
                    if cont:
                        self.board[cur.x][cur.y] = "•"
                    self.busy.append(cur)

    def add_ship(self, ship: Ship):
        for dot in ship.dot:
            if self.border_check(dot) or dot in self.busy:
                raise BoardWrongShipException
        for dot in ship.dot:
            self.board[dot.x][dot.y] = "◙"
            self.busy.append(dot)
        self.ships.append(ship)
        self.contour(ship)

    def shoot(self, dot):
        if self.border_check(dot):
            raise BoardOutException
        if dot in self.busy:
            raise BoardUsedException
        self.busy.append(dot)
        for ship in self.ships:
            if dot in ship.dot:
                ship.life -= 1
                self.board[dot.x][dot.y] = "■"
                if ship.life == 0:
                    self.count += 1
                    self.contour(ship, cont=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        self.board[dot.x][dot.y] = "○"
        print("Мимо")
        return False

    def begin(self):
        self.busy = []


class Game:

    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hidden = True

        self.ai = AI(co, pl)
        self.gamer = AI(pl, co)

    def board_gen(self):
        ship_pool = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for pool in ship_pool:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dots(randint(0, self.size), randint(0, self.size)), pool, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.board_gen()
        return board

    def greet(self):
        print("─" * 20)
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("─" * 20)
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.gamer.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.ai.action()
            else:
                print("Ходит компьютер!")
                repeat = self.gamer.action()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.gamer.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

class Player:
    def __init__(self, board: Board, enemy: Board):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass

    def action(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shoot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):

    def ask(self):
        pnt = Dots(randint(0, self.board.size-1), randint(0, self.board.size-1))
        print(f"Ход компьютера: {pnt.x + 1} {pnt.y + 1}")
        return pnt


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dots(x - 1, y - 1)

g = Game()
g.start()