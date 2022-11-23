coord = list(range(1, 10))


def show():
    table_cross = coord.copy()
    table_digit = coord.copy()
    for i in range(len(table_cross)):
        if table_cross[i] not in ["X","O"]:
            table_cross[i] = " "
        else: table_digit[i] = " "


    for i in range(0, 9, 3):
        print("       --------------")
        print(f"{table_digit[i]} {table_digit[i + 1]} {table_digit[i + 2]} "
              f" | {table_cross[i]} | {table_cross[i + 1]} | {table_cross[i + 2]} | ")
    print("       --------------")

def ask(fig):
    while True:
        dec = input("Введите номер ячейки для хода: ")
        if not dec.isdigit():
            print("Введите цифру номера ячейки")
            continue
        if int(dec) not in range(1, 10):
            print("Число вне диапазона")
            continue
        if coord[int(dec) - 1] == "X" or coord[int(dec) - 1] == "O":
            print("Ячейка занята")
            continue
        coord[int(dec) - 1] = fig
        return


def check():
    win_cond = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (2, 4, 6), (0, 4, 8)]
    for cond in win_cond:
        symbols = []
        for c in cond:
            symbols.append(coord[c])
        if symbols == ["X", "X", "X"]:
            show()
            print("Выиграл крестик!")
            return True
        if symbols == ["O", "O", "O"]:
            show()
            print("Выиграл нолик!")
            return True
    return False

turns = [" " for i in range(9)]
for i in range(0,9,2):
    turns[i] = "X"
for i in range(1, 9, 2):
    turns[i] = "O"
for i in range(9):
    if turns[i] == "X":
        print("Ходит крестик")
    else:
        print("Ходит Нолик")
    show()
    ask(turns[i])
    if check():
        break
    if turns == 8:
        print("Ничья!")








