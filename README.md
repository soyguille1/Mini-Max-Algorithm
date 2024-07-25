# Algoritmo-minimax
Game tree generation. All nodes will be generated until a terminal state is reached.
Calculation of the utility function values for each terminal node.
Calculate the value of the top nodes from the value of the bottom nodes. Depending on the level, whether it is MAX or MIN, the minimum and maximum values will be chosen, representing the movements of the player and the opponent, hence the name minimax.
Choose the move by assessing the values that have reached the higher level.
The algorithm will explore the nodes of the tree by assigning them a numerical value using an evaluation function, starting with the terminal nodes and working their way up to the root. The utility function will define how good the position is for a player when he reaches it. In the case of chess, the possible values are (+1,0,-1) which correspond to winning, drawing and losing respectively. In the case of backgammon, the possible values will have a range of [+192,-192], corresponding to the value of the cards. For each game they may be different.
If minimax is faced with the prisoner's dilemma, it will always choose the option with which it maximizes its result, assuming that the opponent tries to minimize it and make us lose.
