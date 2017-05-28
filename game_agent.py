"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def Xcustom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    meLoc = game.get_player_location(game.active_player)
    oppLoc = game.get_player_location(game.get_opponent(game.active_player))
    usDist = abs(meLoc[0] - oppLoc[0]) + abs(meLoc[1] - oppLoc[1])

    meX = meLoc[0]
    meY = meLoc[1]
    bcx = game.width / 2
    bcy = game.height / 2
    
    return -abs(meX-bcx)-abs(meY-bcy) + usDist

def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    oppMoves = set(game.get_legal_moves(game.get_opponent(player)))
    myMoves = set(game.get_legal_moves(player))

    myTurn = game.active_player == player
    return len(myMoves) / (1 + len(oppMoves.intersection(myMoves)))
    #return 1.7*len(myMoves) - 1.1*len(oppMoves.intersection(myMoves)) if myTurn else -1.7*len(myMoves)+1.1*len(oppMoves.intersection(myMoves))    


def Xcustom_score_2(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    meLoc = game.get_player_location(game.active_player)
    oppLoc = game.get_player_location(game.get_opponent(game.active_player))
    usDist = abs(meLoc[0] - oppLoc[0]) + abs(meLoc[1] - oppLoc[1])

    return len(game.get_legal_moves(player))/len(game.get_blank_spaces()) + usDist

def custom_score_2(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blanks = game.get_blank_spaces()
    myMoves = set(game.get_legal_moves(player))

    outs = 0
    for blank in  blanks:
        if blank[0] <= game.width/3 or blank[0] >= 2/3*game.width:
            outs+=1
        elif blank[1] <= game.height/3 or blank[1] >= 2/3*game.height:
            outs+=1
    return -outs + len(myMoves) / len(game.get_blank_spaces())


def custom_score_3(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    totalMoves = len(game.get_blank_spaces())
    oppMoves = len(game.get_legal_moves(game.get_opponent(player)))
    myMoves = len(game.get_legal_moves(player))

    meLoc = game.get_player_location(game.active_player)
    oppLoc = game.get_player_location(game.get_opponent(game.active_player))
    usDist = abs(meLoc[0] - oppLoc[0]) + abs(meLoc[1] - oppLoc[1])

    return float(myMoves - oppMoves) / float(totalMoves)

def updateBest(candidateScore, incumbentScore, candidateMove, incumbentMove, objective):
    if objective == "max":
        if(candidateScore > incumbentScore):
            return candidateScore, candidateMove
    elif objective == "min":
        if(candidateScore < incumbentScore):
            return candidateScore, candidateMove
    return incumbentScore, incumbentMove


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):

    def get_move(self, game, time_left):
        self.time_left = time_left
        initialSet = game.get_legal_moves(game.active_player)
        if len(initialSet) == 0:
            return (-1,-1)

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = random.choice(initialSet)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        self.user = game.active_player;

        return self.findBest(game, depth, "max")

    def findBest(self, game, depth, objective):
        if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

        expanse = game.get_legal_moves(game.active_player)
        if depth == 0 or len(expanse) == 0:
            return self.score(game, self.user)

        bestMove = random.choice(expanse)
        bestScore = float("-inf") if objective == "max" else float("inf")
        for move in expanse:
            outcome = self.findBest(game.forecast_move(move), depth-1, "min" if objective == "max" else "max")
            bestScore, bestMove = updateBest(outcome, bestScore, move, bestMove, objective)

        return bestMove if depth == self.search_depth else bestScore




class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        
        initialSet = game.get_legal_moves(game.active_player)
        if len(initialSet) == 0:
            return (-1,-1)

        self.time_left = time_left
        bestMove = random.choice(initialSet)
        try:
            deepening = 0;
            while True:
                deepening += 1
                self.search_depth = deepening # need to update search-depth for depth-limited search to work

                bestMove = self.alphabeta(game, deepening)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return bestMove


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        self.user = game.active_player

        return self.findBest2(game, depth, "max", alpha, beta)


    def findBest2(self, game, depth, objective, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

        expanse = game.get_legal_moves(game.active_player)
        if depth == 0 or len(expanse) == 0:
            return self.score(game, self.user)


        bestMove = random.choice(expanse)
        bestScore = float("-inf") if objective == "max" else float("inf")
        for move in expanse:
            outcome = self.findBest2(game.forecast_move(move), depth-1, "min" if objective == "max" else "max", alpha, beta)
            if objective == "max":
                if outcome >= beta:
                    bestScore = beta
                    break
                alpha = max(outcome, alpha)
            elif objective == "min":
                if outcome <= alpha:
                    bestScore = alpha
                    break
                beta = min(outcome, beta)

            bestScore, bestMove = updateBest(outcome, bestScore, move, bestMove, objective)

        return bestMove if depth == self.search_depth else bestScore # only return a move if top-level caller
