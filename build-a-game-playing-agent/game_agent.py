"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
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
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves)


    # TODO: finish this function!
    raise NotImplementedError


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        best_move = (-1, -1)
        if len(game.get_legal_moves()) == 0:
            return best_move
        if game.move_count == 0:
            return (int(game.width/2), int(game.height/2))

        
       

        try:

            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            # if use iterative deepening, use the method specified
            if self.iterative:
                if self.method == "minimax":
                    depth = 1
                    while True:
                        best_move = self.minimax(game, depth, True)[1];
                        if best_move == (-1, -1):
                            return best_move
                        depth += 1
                if self.method == "alphabeta":
                    depth = 1
                    while True:
                        best_move = self.alphabeta(game, depth)[1]
                        if best_move == (-1, -1):
                            return best_move
                        depth += 1
                
                
            else:
                if self.method == "minimax":
                    best_move = self.minimax(game, self.search_depth, True)[1]
                if self.method == "alphabeta":
                    best_move = self.minimax(game, self.search_depth, True)[1]
                return best_move

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move

        # Return the best move from the last completed search iteration
        raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        # create a list of queues
        # get current_player's current position
        # calculate one level down according to score function
        # return the max or min
        # if depth == 0:
        #     return self.score(game, game.active_player()), game.get_player_location(game.inactive_player())
        queue = game.get_legal_moves()
        scores = []
        game_queue = []
        if len(queue) == 0:
            if maximizing_player:
                return float("-inf"), (-1, -1) 
            else:
                return float("inf"), (-1, -1)

        if depth == 1:
            for possible_move in queue:
                new_game = game.forecast_move(possible_move)
                scores.append(self.score(new_game,self))

        # make a queue to store the possible moves
        # for each move in the queue, make a deep copy of the game, then move the move,
        # then recurse and depending on whether or not maximizing_player is True
        # choose a possible move
        if depth > 1:
            for possible_move in queue:
                new_game = game.forecast_move(possible_move)
                new_score = self.minimax(new_game, int(depth) - 1, not maximizing_player)
                game_queue.append(new_score[1])
                scores.append(new_score[0])
           
        
        if maximizing_player:
            max = 0
            for i in range(len(scores)):
                if scores[i] > scores[max]:
                    max = i
            return scores[max], queue[max]
        
        else: 
            min = 0
            for i in range(len(scores)):
                if scores[i] < scores[min]:
                    min = i
            return scores[min], queue[min]

        


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()


        # get a queue of the possible moves
        queue = game.get_legal_moves()
        scores = []

        if len(queue) == 0:
            if maximizing_player:
                return float("-inf"), (-1, -1) 
            else:
                return float("inf"), (-1, -1)

        # base case: depth is 0
        if depth == 0:
            return self.score(game, self), game.get_player_location(game.inactive_player)

        # base case: if only search one layer
        else:
            # if maximizing_player is True
            if maximizing_player:
                new_beta = beta
                for possible_move in queue:
                    new_game = game.forecast_move(possible_move)
                    score = self.alphabeta(new_game, int(depth) - 1, alpha, new_beta, False)
                    if score[0] > float(alpha):
                        return score[0], possible_move
                    
                    if score[0] > new_beta:
                        new_beta = score[0]
                    
                    scores.append(score[0])
                        
                max = 0
                for i in range(len(scores)):
                    if scores[i] > scores[max]:
                        max = i
                return scores[max], queue[max]

            #if maximizing_player is False
            else:
                new_alpha = alpha
                for possible_move in queue:
                    new_game = game.forecast_move(possible_move)
                    score = self.alphabeta(new_game, depth-1, new_alpha, beta, True)
                    if score[0] < new_alpha:
                        new_alpha = score[0]
                    if score[0] < beta:
                        return score[0], possible_move
                    scores.append(score[0])

                min = 0
                for i in range(len(scores)):
                    if scores[i] < scores[min]:
                        min = i
                return scores[min], queue[min]


        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        raise NotImplementedError
