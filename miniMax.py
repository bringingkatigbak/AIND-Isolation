def findBest(game, depth, objective, agent, xtime):
	if agent.time_left() < agent.TIMER_THRESHOLD:
            raise xtime()

	if(depth == 0):
		return agent.score(game, "Player1")

	expanse = game.get_legal_moves(game.active_player)

	bestMove = (-2,-2)
	bestScore = float("-inf") if objective == "max" else float("inf")
	for move in expanse:
		outcome = findBest(game.forecast_move(move), depth-1, "min" if objective == "max" else "max", agent, xtime)
		bestScore, bestMove = updateBest(outcome, bestScore, move, bestMove, objective)

	return bestMove if depth == agent.search_depth else bestScore

def updateBest(candidateScore, incumbentScore, candidateMove, incumbentMove, objective):
	if objective == "max":
		if(candidateScore > incumbentScore):
			return candidateScore, candidateMove
	elif objective == "min":
		if(candidateScore < incumbentScore):
			return candidateScore, candidateMove
	return incumbentScore, incumbentMove