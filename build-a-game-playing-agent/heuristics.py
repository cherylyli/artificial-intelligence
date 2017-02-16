import math

def custom_score_1(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    
    Evaluation
    ----------
    If there is overlap between the player's and the opponents possible opp_moves
    assign a greater value to the move
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    own_moves_value = len(player_moves)
    opp_moves_value = len(opponent_moves)

    for move in player_moves:
        if move in opponent_moves:
            own_moves_value -= 0.5

    
    return float(own_moves_value - opp_moves_value)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    
    Evaluation
    ----------
    If there is overlap between the player's and the opponents possible opp_moves
    assign a lesser value to the move
    If the player and opponent is far-ish away, give a increase to the move
    """
    # if the player wins or loses, return negative or positive infinity
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # get the player's moves and opponent's moves
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    move_value = float(len(player_moves) - len(opponent_moves))

    # check for overlap between the players' possible moves
    for move in player_moves:
        if move in opponent_moves:
            move_value -= 1.5

    # check if players are close together.
    # Penalize if players are close but game board is less filled
    # Award if players are far but game board is more filled
    player_pos = game.get_player_location(player)
    opponent_pos = game.get_player_location(game.get_opponent(player))

    num_blank = len(game.get_blank_spaces())
    total_spaces = game.width * game.height

    player_distance = math.sqrt((player_pos[0] - opponent_pos[0])**2 + \
        (player_pos[1] - opponent_pos[1])**2)
    if player_distance < game.width / 3 and (num_blank > total_spaces / 3):
        move_value -= 0.8

    elif player_distance > game.width / 3 and (num_blank < total_spaces / 3):
        move_value += 0.8

    return move_value



def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    
    Evaluation
    ----------
    If there is overlap between the player's and the opponents possible opp_moves
    assign a much lesser value.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    own_moves_value = len(player_moves)
    opp_moves_value = len(opponent_moves)
    move_value = float(own_moves_value - opp_moves_value)

    total_spaces = game.width * game.height
    num_blank = total_spaces - game.move_count

    num_repeats = 0

    for move in player_moves:
        if move in opponent_moves:
            num_repeats += 1

    if opp_moves_value == num_repeats and own_moves_value == num_repeats:
        if num_repeats == 1:
            move_value -= 5
        else:
            move_value -= 0.4
    
    return move_value