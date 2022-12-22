# Assumption - domino game played by 2 players only, computer and player
import random


# generate the domino set based on the
# min and max numbers of a domino piece
def generate_domino_set(min_number, max_number):
    domino_set = []

    for x in range(min_number, max_number + 1):
        for y in range(min_number, max_number + 1):
            domino_piece_exists = False

            for domino_piece in domino_set:
                if [x, y] == domino_piece or [y, x] == domino_piece:
                    domino_piece_exists = True
                    break

            if not domino_piece_exists:
                domino_set.append([x, y])

    return domino_set


# split a domino set with the specified number of pieces per player
# returns the lists for computer, player, stock pieces
# these lists are already good for starting the game
# also return the domino snake and player that starts the game (aka status)
def split_domino_set(domino_set, pieces_per_player):
    domino_set_copy = domino_set
    computer_pieces = []
    player_pieces = []
    stock_pieces = []

    while len(domino_set_copy) > 0:
        domino_piece = random.choice(domino_set)

        if len(computer_pieces) < pieces_per_player:
            computer_pieces.append(domino_piece)
            domino_set.remove(domino_piece)
        elif len(player_pieces) < pieces_per_player:
            player_pieces.append(domino_piece)
            domino_set.remove(domino_piece)
        else:
            stock_pieces.append(domino_piece)
            domino_set.remove(domino_piece)

    try:
        domino_snake, status = has_starter_piece(computer_pieces, player_pieces)
    except TypeError:
        domino_snake, status = list(), False

    if status == "player":
        computer_pieces.remove(domino_snake[0])
        return computer_pieces, player_pieces, stock_pieces, domino_snake, status
    elif status == "computer":
        player_pieces.remove(domino_snake[0])
        return computer_pieces, player_pieces, stock_pieces, domino_snake, status
    else:
        return has_starter_piece(domino_set, pieces_per_player)


# returns False if it has NOT a starting piece
# returns the starter piece and player that starts the game
def has_starter_piece(computer_pieces, player_pieces):
    # the -1 is just because 0 is  a valid domino number
    max_double_computer = [-1, -1]
    max_double_player = [-1, -1]

    for domino_piece in computer_pieces:
        if domino_piece[0] == domino_piece[1]:
            if domino_piece[0] > max_double_computer[0]:
                max_double_computer = domino_piece

    for domino_piece in player_pieces:
        if domino_piece[0] == domino_piece[1]:
            if domino_piece[0] > max_double_player[0]:
                max_double_player = domino_piece

    if max_double_computer[0] > max_double_player[0]:
        status = "player"
        return [max_double_computer], status
    elif max_double_player[0] > max_double_computer[0]:
        status = "computer"
        return [max_double_player], status
    else:
        return False


# prints the game status that should appear every turn
def print_game_status(stock_size, computer_size, domino_snake,
                      player_size, player_pieces, status):
    print("=" * 70)
    print(f"Stock size: {stock_size}")
    print(f"Computer pieces: {computer_size}\n")

    print_domino_snake(domino_snake)

    print("Your pieces:")
    for i in range(player_size):
        print(f"{i + 1}:{player_pieces[i]}")

    print_status(status)


# aux function to print the domino snake
def print_domino_snake(domino_snake):
    snake_to_print = ""

    if len(domino_snake) < 6:
        for domino in domino_snake:
            snake_to_print += str(domino)
    else:
        snake_to_print = str(domino_snake[0]) + str(domino_snake[1]) + str(domino_snake[2]) \
                         + "..." \
                         + str(domino_snake[-3]) + str(domino_snake[-2]) + str(domino_snake[-1])

    print(snake_to_print)


# aux function to print the status
def print_status(status):
    if status == "player":
        print("Status: It's your turn to make a move. Enter your command.")
    elif status == "computer":
        print("Status: Computer is about to make a move. Press Enter to continue...")
    elif status == "win":
        print("Status: The game is over. You won!")
    elif status == "loss":
        print("Status: The game is over. The computer won!")
    elif status == "draw":
        print("Status: The game is over. It's a draw!")
    else:
        print("Status: Error, something happened!")


# validate if the game is finished
# return a new status if the game is finished
# or False otherwise
def is_game_finished(computer_size, player_size, domino_snake):
    if computer_size == 0:
        return "loss"
    elif player_size == 0:
        return "win"
    elif is_draw(domino_snake):
        return "draw"
    else:
        return False


# aux function to validate if the domino snake is in the draw condition
def is_draw(domino_snake):
    value_to_count = domino_snake[0][0]

    # beginning is the same as the end
    if value_to_count == domino_snake[-1][-1]:
        count_appearance = 0

        for domino in domino_snake:
            if value_to_count == domino[0]:
                count_appearance += 1
            if value_to_count == domino[1]:
                count_appearance += 1

        if count_appearance == 8:
            return True

    return False


# aux method to check user input
# prints an error or returns the input number and if the piece needs to be switched or not
def check_player_input(player_size, player_pieces, domino_snake):
    while True:
        try:
            decision = int(input())
            if -player_size <= decision <= player_size:
                if decision > 0:
                    if domino_snake[-1][1] == player_pieces[decision - 1][0]:
                        return decision, False
                    elif domino_snake[-1][1] == player_pieces[decision - 1][1]:
                        return decision, True
                    else:
                        print("Illegal move. Please try again.")
                elif decision < 0:
                    if domino_snake[0][0] == player_pieces[abs(decision) - 1][1]:
                        return decision, False
                    elif domino_snake[0][0] == player_pieces[abs(decision) - 1][0]:
                        return decision, True
                    else:
                        print("Illegal move. Please try again.")
                else:
                    return decision, False
            else:
                raise ValueError
        except ValueError:
            print("Invalid input. Please try again.")


# aux method to check user input
# prints an error or returns the input number and if the piece needs to be switched or not
def computer_input(computer_pieces, domino_snake):
    counter_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for domino in computer_pieces:
        for number in domino:
            counter_dict[number] += 1
    for domino in domino_snake:
        for number in domino:
            counter_dict[number] += 1

    scores_dict = dict()
    for domino in computer_pieces:
        score = counter_dict[domino[0]] + counter_dict[domino[1]]
        scores_dict[computer_pieces.index(domino)] = score

    while len(scores_dict) > 0:
        max_key = max(scores_dict, key=scores_dict.get)
        decision = max_key + 1

        # left side try
        if domino_snake[0][0] == computer_pieces[max_key][1]:
            return -decision, False
        elif domino_snake[0][0] == computer_pieces[max_key][0]:
            return -decision, True
        # right side try
        elif domino_snake[-1][1] == computer_pieces[max_key][0]:
            return decision, False
        elif domino_snake[-1][1] == computer_pieces[max_key][1]:
            return decision, True
        else:
            scores_dict.pop(max_key)

    # no options left
    decision = 0
    return decision, False


def process_input(stock_size, computer_size, player_size, domino_snake,
                  stock_pieces, computer_pieces, player_pieces, status):
    if status == "player":
        decision, needs_switch = check_player_input(player_size, player_pieces, domino_snake)

        if decision == 0:
            if stock_size > 0:
                chosen_piece = random.choice(stock_pieces)
                player_pieces.append(chosen_piece)
                stock_pieces.remove(chosen_piece)
                player_size = len(player_pieces)
                stock_size = len(stock_pieces)
        else:
            chosen_piece = player_pieces[abs(decision) - 1]
            player_pieces.remove(chosen_piece)
            player_size = len(player_pieces)

            if decision > 0 and not needs_switch:
                domino_snake.append(chosen_piece)
            elif decision > 0 and needs_switch:
                chosen_piece.reverse()
                domino_snake.append(chosen_piece)
            elif decision < 0 and not needs_switch:
                domino_snake.insert(0, chosen_piece)
            elif decision < 0 and needs_switch:
                chosen_piece.reverse()
                domino_snake.insert(0, chosen_piece)
            else:
                print("Error, something happened!")

        status = "computer"

    elif status == "computer":
        if not input():
            decision, needs_switch = computer_input(computer_pieces, domino_snake)

            if decision == 0:
                if stock_size > 0:
                    chosen_piece = random.choice(stock_pieces)
                    computer_pieces.append(chosen_piece)
                    stock_pieces.remove(chosen_piece)
                    computer_size = len(computer_pieces)
                    stock_size = len(stock_pieces)
            else:
                chosen_piece = computer_pieces[abs(decision) - 1]
                computer_pieces.remove(chosen_piece)
                computer_size = len(computer_pieces)

                if decision > 0 and not needs_switch:
                    domino_snake.append(chosen_piece)
                elif decision > 0 and needs_switch:
                    chosen_piece.reverse()
                    domino_snake.append(chosen_piece)
                elif decision < 0 and not needs_switch:
                    domino_snake.insert(0, chosen_piece)
                elif decision < 0 and needs_switch:
                    chosen_piece.reverse()
                    domino_snake.insert(0, chosen_piece)
                else:
                    print("Error, something happened!")

            status = "player"

    else:
        print("Error, something happened  to Status")

    return stock_size, computer_size, player_size, \
        domino_snake, stock_pieces, computer_pieces,\
        player_pieces, status


# the values in the functions can be saved elsewhere to ensure more abstraction
# generate new domino set
new_domino_set = generate_domino_set(0, 6)

# split the domino set to have a playable game
new_computer_pieces, new_player_pieces, new_stock_pieces, \
    new_domino_snake, new_status = split_domino_set(new_domino_set, 7)

# store number of pieces for computer, player and stock
new_computer_size, new_player_size, new_stock_size \
    = len(new_computer_pieces), len(new_player_pieces), len(new_stock_pieces)

# game start
while True:
    # validate the end of the game
    end_game_status = is_game_finished(new_computer_size, new_player_size, new_domino_snake)
    if end_game_status:
        new_status = end_game_status
        # print the last status
        print_game_status(new_stock_size, new_computer_size, new_domino_snake,
                          new_player_size, new_player_pieces, new_status)
        break

    # print the status
    print_game_status(new_stock_size, new_computer_size, new_domino_snake,
                      new_player_size, new_player_pieces, new_status)

    # process input, if the game is not finished
    new_stock_size, new_computer_size, new_player_size, \
        new_domino_snake, new_stock_pieces, \
        new_computer_pieces, new_player_pieces, \
        new_status = process_input(new_stock_size, new_computer_size, new_player_size,
                                   new_domino_snake, new_stock_pieces, new_computer_pieces,
                                   new_player_pieces, new_status)
