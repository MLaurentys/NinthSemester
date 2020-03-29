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

import util

############################################################
# Part 1: Segmentation problem under a unigram model

class SegmentationProblem(util.Problem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state):
        """ Metodo que implementa verificacao de estado """
        j = 0
        for i in range (len(state)):
            if (state[i] == self.query[j]):
                j += 1
        return j == len(state) - state.count(' ')

    def initialState(self):
        """ Metodo que implementa retorno da posicao inicial """
        return ""

    def actions(self, state):
        """ Metodo que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        l = len(state)
        if (l == 0): return [self.query[0]]
        blank = state.count(' ')
        ret = [self.query[l - blank]]
        if (state[-1] != ' '): ret += ' '
        return ret

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        return state + action

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        return len(self.query) == len(state) - state.count(' ')

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        if(action == ' '): return 0.0
        j = len(state)
        while (j > 0 and state[j-1] != ' '): j -= 1
        word = state[j:]
        cost1 = self.unigramCost(word)
        if(word == ''): cost1 = 0.0
        cost = self.unigramCost(word + action) - cost1
        #print(f'state = {state}, word = {word}, action = {action}, cost = {cost}')
        return cost


def segmentWords(query, unigramCost):

    if len(query) == 0:
        return ''
    
    sp = SegmentationProblem(query, unigramCost)

    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)
    return util.uniformCostSearch(sp).state

    # END_YOUR_CODE

############################################################
# Part 2: Vowel insertion problem under a bigram cost

def get_words(s):
    j = 0
    wds = []
    for i in range(len(s)):
        if(s[i] == ' '):
            wds.append(s[j:i])
            j = i
    return wds

class VowelInsertionProblem(util.Problem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills
        self.fills = []
        for i in range (len(queryWords)):
            self.fills.append(possibleFills(queryWords[i]))

    def isState(self, state):
        """ Metodo  que implementa verificacao de estado """
        j = 0
        wds = get_words(state)
        for i in range (len(wds)):
            if (wds[i] == self.queryWords[j]):
                j += 1
            elif (state[i] in self.fills[j]):
                j += 1
        return j == len(queryWords)


    def initialState(self):
        """ Metodo  que implementa retorno da posicao inicial """
        return " ".join(self.queryWords)

    def actions(self, state):
        """ Metodo  que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        words = get_words(state)
        derived = []
        for i in range (len(words)):
            wi = words[i]
            fills = self.possibleFills(wi)
            for f in fills:
                derived.append((f, i))
        return derived

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        j = 0
        i = 0
        while (j != action[1]):
            if(state[i] == ' '): j += 1
            i += 1
        j = i
        while (state[i] != ' '): i+=1
        return " ".join(state[0:j+1]) + action[0] + " ".join(state[i:len(state)])

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        wds = get_words(state)
        for i in range(len(wds)):
            if (wds[i] not in self.fills[i]):
                return False
        return True

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        wds = get_words(state)
        i = action[1]
        if (i == 0):
            b1 = self.bigramCost(wds[i-1], wds[i])
            n_b1 = self.bigramCost(wds[i-1], action[0])
            return n_b1 - b1
        if (i==len(wds-1)):
            b2 = self.bigramCost(wds[i], wds[i+1])
            n_b2 = self.bigramCost(action[0], wsd[i+1])
            return n_b2 - b2

        b1 = self.bigramCost(wds[i-1], wds[i])
        b2 = self.bigramCost(wds[i], wds[i+1])
        n_b1 = self.bigramCost(wds[i-1], action[0])
        n_b2 = self.bigramCost(action[0], wsd[i+1])
        return (n_b1+n_b1) - (b1+b2)



def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)
    vp = VowelInsertionProblem(queryWords, bigramCost, possibleFills)
    ret = util.uniformCostSearch(vp)
    return ret.state
    # END_YOUR_CODE

############################################################


def getRealCosts(corpus='corpus.txt'):

    """ Retorna as funcoes de custo unigrama, bigrama e possiveis fills obtidas a partir do corpus."""
    
    _realUnigramCost, _realBigramCost, _possibleFills = None, None, None
    if _realUnigramCost is None:
        print('Training language cost functions [corpus: '+ corpus+']... ')
        
        _realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
        _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')

        print('Done!')

    return _realUnigramCost, _realBigramCost, _possibleFills

def main():
    """ Voce pode/deve editar o main() para testar melhor sua implementacao.

    A titulo de exemplo, incluimos apenas algumas chamadas simples para
    lhe dar uma ideia de como instanciar e chamar suas funcoes.
    Descomente as linhas que julgar conveniente ou crie seus proprios testes.
    """
    unigramCost, bigramCost, possibleFills  =  getRealCosts()
    
    #resulSegment = segmentWords('believeinyourselfhavefaithinyourabilities', unigramCost)
    #resulSegment = segmentWords('assimpleasthat', unigramCost)
    #print(f'twowords = {unigramCost("twowords")}')
    #print(f'two words = {unigramCost("two")} + {unigramCost("words")}')
    #print(f'two wor = {unigramCost("two")} + {unigramCost("wor")}')
    #print(resulSegment)
    

    resultInsert = insertVowels('smtms ltr bcms nvr'.split(), bigramCost, possibleFills)
    print(resultInsert)

if __name__ == '__main__':
    main()
