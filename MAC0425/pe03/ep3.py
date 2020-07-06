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

  Referencias:
  Para complementar a iteracao de valores: https://artint.info/html/
  ArtInt_227.html#:~:text=Value%20iteration%20is%20a%20method,
  uses%20an%20arbitrary%20end%20point.

  Exemplo:
  - O algoritmo Quicksort foi baseado em:
  https://pt.wikipedia.org/wiki/Quicksort
  http://www.ime.usp.br/~pf/algoritmos/aulas/quick.html

  Comentario:
  Tive um grande dificuldade em fazer bons features. No final deste ep,
  existe um teste em que consigo cera 70% de acerto em relacao a iteracao.
  No entando algumas vezes ha um erro muito grande que nao posso explicar
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
        return ['Pegar', 'Espiar', 'Sair']

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
                return ((0, None, None), prob, 0)
            if sumc == 1:
                return ((new_sum, None, None), 1, new_sum)
            cards = list(state[2])
            cards[index] -= 1
            new_st = (new_sum, None, tuple(cards))
            return (new_st, prob, 0)

        reachable = []
        if state[2] is None:
            return []
        if action == 'Pegar':
            if state[1] is None:
                for i in range(len(state[2])):
                    if state[2][i]:
                        reachable.append(make_draw_state(state, i))
            else:
                reachable.append(make_draw_state(state, state[1], True))
        elif action == 'Espiar':
            if state[1] is not None:
                return []
            for i in range(len(state[2])):
                if state[2][i]:
                    new_st = (state[0], i, state[2])
                    reachable.append((new_st, state[2][i]/sum(state[2]),\
                                      - self.custo_espiada))
        elif action == 'Sair':
            reachable.append(((state[0], None, None), 1, state[0]))
        else:
            print("BIG ERROR")
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
        self.pi = {}
        self.V = {}

    def solve(self, mdp, epsilon=0.001):
        """
        Solve the MDP using value iteration.  Your solve() method must set
        - self.state_to_value to the dictionary mapping states to optimal values
        - self.state_to_action to the dictionary mapping states to an optimal action
        Note: epsilon is the error tolerance: you should stop value iteration when
        all of the values change by less than epsilon.
        The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
        """
        def computeQ(mdp, V, state, action):
            # Return Q(state, action) based on V(state).
            return sum(prob * (reward + mdp.discount() * V[newState]) \
                    for newState, prob, reward in mdp.succAndProbReward(state, action))

        def computeOptimalPolicy(mdp, V):
            # Return the optimal policy given the values V.
            pi = {}
            for state in mdp.states:
                pi[state] = max((computeQ(mdp, V, state, action), action)\
                     for action in mdp.actions(state))[1]
            return pi

        st_val = defaultdict(float)  # state -> value of state

        # Implement the main loop of Asynchronous Value Iteration Here:
        # BEGIN_YOUR_CODE
        def finished(val1, val2, factor):
            for st in val1.keys():
                if abs(val1[st] - val2[st]) >= factor:
                    return False
            return True

        if mdp.discount() < 1:
            factor = epsilon*(1-mdp.discount())/mdp.discount()
        else: factor = epsilon

        mdp.computeStates()
        states = mdp.states
        next_val = {}
        prev_val = {}
        # starting next_val: any number larger than epsilon/len(mdp.states)
        for st_ in states:
            prev_val[st_] = -1
            next_val[st_] = 0
        while not finished(next_val, prev_val, factor):
            for st_ in states: prev_val[st_] = next_val[st_]
            for st_ in states:
                next_val[st_] = max(computeQ(mdp, next_val, st_, act)\
                            for act in mdp.actions(st_))

        # END_YOUR_CODE

        # Extract the optimal policy now
        st_act = computeOptimalPolicy(mdp, prev_val)
        # print("ValueIteration: %d iterations" % numIters)
        self.pi = st_act
        self.V = st_val

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
    # valores_cartas = [i for i in range(5, 12)]
    # valores_cartas.append(30)
    valores_cartas = [6, 22]
    multiplicidade = 10
    limiar = 20
    custo_espiada = 1
    return BlackjackMDP(valores_cartas, multiplicidade, limiar, custo_espiada)
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
         We will call this function with (s, a, r, s'), which you should
         use to update |weights|.
         You should update the weights using self.getStepSize(); use
         self.getQ() to compute the current estimate of the parameters.

         HINT: Remember to check if s is a terminal state and s' None.
        """
        # BEGIN_YOUR_CODE
        def update_terminal(reward, q_val, _):
            return self.getStepSize() * (reward - q_val)

        def update_reg(reward, q_val, newState):
            max_new_s = max([self.getQ(newState, act)\
                for act in self.actions(newState)])
            dif = reward + self.discount * max_new_s - q_val
            return self.getStepSize() * dif

        if newState is None:
            #return
            update = update_terminal
        else:
            update = update_reg
        q_val = self.getQ(state, action)
        for feat_, val_ in self.featureExtractor(state, action):
            to_update = update(reward, q_val, newState)
            if to_update != 0:
                #total = (abs(to_update) + abs(val_))
                self.weights[feat_] += to_update * val_# * (to_update/total)

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
    # feature 1
    ret = []

    # feature 1: Identity Feature
    feat_ = ('Identity Feature',state[0],action)
    value_ = 1 # any number
    ret.append((feat_, value_))

    # feature 2: remaining cards of the deck
    feat_ = 'Remaining cards'
    value_ = sum(state[2]) if state[2] is not None else 0
    if action == 'Pegar':
        value_ -= 1
    ret.append((feat_, value_))

    # feature 3: profit if leaving immediately
    feat_ = 'Immediate Profit'
    value_ = 0
    if action == 'Sair':
        value_ += state[0]
    elif action == 'Espiar':
        value_ -= 1 # any number -> weight is handling this
    ret.append((feat_, value_))

    # 1 feature per card in deck
    if state[2] is not None:
        card_deck = tuple([1 if num > 0 else 0 for num in state[2]])
        feat_ = ('Has deck', card_deck, action)
        value_ = 1 # any number
        ret.append((feat_, value_))

        for i, num in enumerate(state[2]):
            feat_ = ('Has card', i, num, action)
            value_ = 1
            ret.append((feat_, value_))
    return ret
    # END_YOUR_CODE

# ql = QLearningAlgorithm(largeMDP.actions, largeMDP.discount(), blackjackFeatureExtractor)
# util.simulate(largeMDP, ql, maxIterations=10000, numTrials=100)
# vi = ValueIteration()
# vi.solve(largeMDP)
# states = largeMDP.states
# ql_ans={}
# for st in states:
#     max_v = -float('inf')
#     max_a = ''
#     for act in largeMDP.actions(st):
#         b = ql.getQ(st, act)
#         if b == float('nan'): print("WTF")
#         if b > max_v:
#             max_v = b
#             max_a = act
#     ql_ans[st] = max_a
# vi_answ = vi.pi
# total = len(states)
# partial = 0
# for st in states:
#     if vi_answ[st] == ql_ans[st]:
#         partial += 1
# print("Total = %d Partial = %d" % (total, partial))
