"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import miniMax

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game_agent = game_agent.MinimaxPlayer()
        self.game = isolation.Board(self.player1, self.player2)

    def test_didSetup(self):
    	self.assertTrue(self.player1 == self.game.active_player)

    def test_didMakeMinimaxAgent(self):
    	self.assertTrue(isinstance(self.game_agent, game_agent.MinimaxPlayer))

    def test_MinimaxAgentCanGetMove(self):
    	bestMove = self.game_agent.get_move(self.game, lambda x=1: x*10000)
    	self.assertTrue(bestMove == (3,0))

# class MiniMaxTest(unittest.TestCase):

# 	def setUp(self):
# 		reload(miniMax)
# 		reload(game_agent)
# 		self.player1 = "Player1"
#         self.player2 = "Player2"
#         self.game = isolation.Board(self.player1, self.player2)

#  	def test_canGetMove(self):
#  		miniMax.findBest(self.game, 2, )


if __name__ == '__main__':
    unittest.main()
