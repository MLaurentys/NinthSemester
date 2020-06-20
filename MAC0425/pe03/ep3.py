"""
  AO PREENCHER ESSE CABECALHO COM O MEU NOME E O MEU NUMERO USP,
  DECLARO QUE SOU A UNICA PESSOA AUTORA E RESPONSAVEL POR ESSE PROGRAMA.
  TODAS AS PARTES ORIGINAIS DESSE EXERCICIO PROGRAMA (EP) FORAM
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUCOES
  DESSE EP E, PORTANTO, NAO CONSTITUEM ATO DE DESONESTIDADE ACADEMICA,
  FALTA DE ETICA OU PLAGIO.
  DECLARO TAMBEM QUE SOU A PESSOA RESPONSAVEL POR TODAS AS COPIAS
  DESSE PROGRAMA E QUE NAO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUICAO. ESTOU CIENTE QUE OS CASOS DE PLAGIO E
  DESONESTIDADE ACADEMICA SERAO TRATADOS SEGUNDO OS CRITERIOS
  DIVULGADOS NA PAGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NAO SERAO CORRIGIDOS E,
  AINDA ASSIM, PODERAO SER PUNIDOS POR DESONESTIDADE ACADEMICA.

  Nome : Matheus Tararam de Laurentys
  NUSP : 9793714

  Referencias: Com excecao das rotinas fornecidas no enunciado
  e em sala de aula, caso voce tenha utilizado alguma referencia,
  liste-as abaixo para que o seu programa nao seja considerado
  plagio ou irregular.

  Exemplo:
  - O algoritmo Quicksort foi baseado em:
  https://pt.wikipedia.org/wiki/Quicksort
  http://www.ime.usp.br/~pf/algoritmos/aulas/quick.html
"""

import math
import random
from collections import defaultdict
import util


# **********************************************************
# **            PART 01 Modeling BlackJack                **
# **********************************************************


class BlackjackMDP(util.MDP):
    """
    The BlackjackMDP class is a subclass of MDP that models the BlackJack game as a MDP
    """
    def __init__(self, valores_cartas, multiplicidade, limiar, custo_espiada):
        """
        valores_cartas: list of integers (face values for each card included in the deck)
        multiplicidade: single integer representing the number of cards with each face value
        limiar: maximum number of points (i.e. sum of card values in hand) before going bust
        custo_espiada: how much it costs to peek at the next card
        """
        self.valores_cartas = valores_cartas
        self.multiplicidade = multiplicidade
        self.limiar = limiar
        self.custo_espiada = custo_espiada

    def startState(self):
        """
         Return the start state.
         Each state is a tuple with 3 elements:
           -- The first element of the tuple is the sum of the cards in the player's hand.
           -- If the player's last action was to peek, the second element is the index
              (not the face value) of the next card that will be drawn; otherwise, the
              second element is None.
           -- The third element is a tuple giving counts for each of the cards remaining
              in the deck, or None if the deck is empty or the game is over (e.g. when
              the user quits or goes bust).
        """
        return (0, None, (self.multiplicidade,) * len(self.valores_cartas))

    def actions(self, state):
        """
        Return set of actions possible from |state|.
        You do not must to modify this function.
        """
        if state[2] is None:
            return ['Sair']
        if state[1] is None:
            return ['Pegar', 'Espiar', 'Sair']
        return ['Pegar', 'Sair']

    def succAndProbReward(self, state, action):
        """
        Given a |state| and |action|, return a list of (newState, prob, reward) tuples
        corresponding to the states reachable from |state| when taking |action|.
        A few reminders:
         * Indicate a terminal state (after quitting, busting, or running out of cards)
           by setting the deck to None.
         * If |state| is an end state, you should return an empty list [].
         * When the probability is 0 for a transition to a particular new state,
           don't include that state in the list returned by succAndProbReward.
        """
        # BEGIN_YOUR_CODE
        def make_draw_state(prev_state, index, espiou=False):
            sumc = sum(prev_state[2])
            new_sum = prev_state[0] + self.valores_cartas[index]
            if espiou:
                prob = 1
            else:
                prob = state[2][index]/sumc
            if new_sum > self.limiar:
                return ((new_sum, None, None), prob, 0)
            if sumc == 1:
                return ((new_sum, None, None), 1, new_sum)
            cards = list(state[2])
            cards[index] -= 1
            new_st = (new_sum, None, tuple(cards))
            return (new_st, prob, prev_state[0])

        reachable = []
        if action == 'Pegar':
            if state[1] is None:
                for i in range(len(state[2])):
                    if state[2][i]:
                        reachable.append(make_draw_state(state, i))
            else:
                reachable.append(make_draw_state(state, state[1], True))
        elif action == "Espiar":
            for i in range(len(state[2])):
                if state[2][i]:
                    new_st = (state[0], i, state[2])
                    reachable.append((new_st, state[2][i]/sum(state[2],\
                                      state[0] - self.custo_espiada)))
        elif action == 'Sair':
            reachable.append(((state[0], None, None), 1, state[0]))
        return reachable
        # END_YOUR_CODE

    def discount(self):
        """
        Return the descount  that is 1
        """
        return 1

# **********************************************************
# **                    PART 02 Value Iteration           **
# **********************************************************

class ValueIteration(util.MDPAlgorithm):
    """ Asynchronous Value iteration algorithm """
    def __init__(self):
        self.state_to_action = {}
        self.state_to_value = {}

    def solve(self, mdp, epsilon=0.001):
        """
        Solve the MDP using value iteration.  Your solve() method must set
        - self.state_to_value to the dictionary mapping states to optimal values
        - self.state_to_action to the dictionary mapping states to an optimal action
        Note: epsilon is the error tolerance: you should stop value iteration when
        all of the values change by less than epsilon.
        The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
        """
        def computeQ(mdp, st_val, state, action):
            # Return Q(state, action) based on st_val(state).
            return sum(prob * (reward + mdp.discount() * st_val[newState]) \
                        for newState, prob, reward in\
                            mdp.succAndProbReward(state, action))

        def compute_optimal_policy(mdp, st_val):
            # Return the optimal policy given the values st_val.
            st_act = {}
            for state in mdp.states:
                st_act[state] = max((computeQ(mdp, st_val, state, action), action)\
                    for action in mdp.actions(state))[1]
            return st_act

        st_val = defaultdict(float)  # state -> value of state

        # Implement the main loop of Asynchronous Value Iteration Here:
        # BEGIN_YOUR_CODE
        mdp.computeStates()
        next_val = {}; prev_val = {}
        # starting next_val: any number larger than epsilon/len(mdp.states)
        for st in mdp.states: next_val[st] = 0; prev_val[st] = -1
        while sum(next_val.values()) - sum(prev_val.values()) > epsilon:
            for st in mdp.states: prev_val[st] = next_val[st]
            for st in mdp.states:
                next_val[st] = max(mdp.actios(st),\
                    key=lambda act: computeQ(mdp, prev_val, st, act))

        # END_YOUR_CODE

        # Extract the optimal policy now
        st_act = compute_optimal_policy(mdp, st_val)
        # print("ValueIteration: %d iterations" % numIters)
        self.state_to_action = st_act
        self.state_to_value = st_val

# First MDP
MDP1 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=10, custo_espiada=1)

# Second MDP
MDP2 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=15, custo_espiada=1)

def geraMDPxereta():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action for at least 10% of the states.
    """
    # BEGIN_YOUR_CODE
    raise Exception("Not implemented yet")
    # END_YOUR_CODE


# **********************************************************
# **                    PART 03 Q-Learning                **
# **********************************************************

class QLearningAlgorithm(util.RLAlgorithm):
    """
    Performs Q-learning.  Read util.RLAlgorithm for more information.
    actions: a function that takes a state and returns a list of actions.
    discount: a number between 0 and 1, which determines the discount factor
    featureExtractor: a function that takes a state and action and returns a
    list of (feature name, feature value) pairs.
    explorationProb: the epsilon value indicating how frequently the policy
    returns a random action
    """
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def getQ(self, state, action):
        """
         Return the Q function associated with the weights and features
        """
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    def getAction(self, state):
        """
        Produce an action given a state, using the epsilon-greedy algorithm: with probability
        |explorationProb|, take a random action.
        """
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    def getStepSize(self):
        """
        Return the step size to update the weights.
        """
        return 1.0 / math.sqrt(self.numIters)

    def incorporateFeedback(self, state, action, reward, newState):
        """
         We will call this function with (s, a, r, s'), which you should use to update |weights|.
         You should update the weights using self.getStepSize(); use
         self.getQ() to compute the current estimate of the parameters.

         HINT: Remember to check if s is a terminal state and s' None.
        """
        # BEGIN_YOUR_CODE
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

def identityFeatureExtractor(state, action):
    """
    Return a single-element list containing a binary (indicator) feature
    for the existence of the (state, action) pair.  Provides no generalization.
    """
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

# Large test case
largeMDP = BlackjackMDP(valores_cartas=[1, 3, 5, 8, 10], multiplicidade=3,\
    limiar=40, custo_espiada=1)

# **********************************************************
# **        PART 03-01 Features for Q-Learning             **
# **********************************************************

def blackjackFeatureExtractor(state, action):
    """
    You should return a list of (feature key, feature value) pairs.
    (See identityFeatureExtractor() above for a simple example.)
    """
    # BEGIN_YOUR_CODE
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

# smallMDP = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2,
#                                        limiar=15, custo_espiada=1)
# preEmptyState = (11, None, (1,0))
# # Make sure the succAndProbReward function is implemented correctly.
# tests = [
#     ([((12, None, None), 1, 12)], smallMDP, preEmptyState, 'Pegar'),
#     ([((5, None, (2, 1)), 1, 0)], smallMDP, (0, 1, (2, 2)), 'Pegar')
# ]
# total_tests_global = 0
# total_tests = 0
# results = 0
# for gold, mdp, state, action in tests:
#     total_tests_global += 1
#     total_tests += 1
#     res = mdp.succAndProbReward(state, action)
#     print(gold)
#     print(res)
#     if  gold==res:
#         results += 1
# print(results)
