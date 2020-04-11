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

def get_words(s):
    if (s == ''): return []
    return s.split(' ')

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
        ret = []
        blank = state.count(' ')
        if (l - blank < len(self.query)):
            ret += [self.query[l - blank]]
        if (state[-1] != ' '): ret += ' '
        return ret

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        return state + action

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        ret = False
        if (len(self.query) == len(state) - state.count(' ')):
            ret = True
            wds = get_words(state)
            for word in wds:
                if (self.unigramCost(word) > 13.3):
                    ret = False
                    break
        return ret

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """

        j = len(state)
        while (j > 0 and state[j-1] != ' '): j -= 1
        word = state[j:]
        if(action == ' '):
            return self.unigramCost(word)
        cost1 = self.unigramCost(word)
        if(word == ''): cost1 = 0.0
        cost = self.unigramCost(word + action) - cost1
        #print(f'state = {state}, word = {word}, action = {action}, cost = {cost}')
        return cost


def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''
    query = query.lower()
    sp = SegmentationProblem(query, unigramCost)
    ret = util.uniformCostSearch(sp)
    if(ret):
        return ret.state
    else:
        return ''

############################################################
# Part 2: Vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.Problem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills
        self.fills = []
        self.not_word = "cnbdfbzadfbzfbasfaefafgdggsdgscvdvndsa"
        self.threshold = bigramCost("the", self.not_word)
        if (len(queryWords) <= 1):
            self.fills = queryWords
        else:
            #theshhold is based on the math behind bigramCost
            # a commom word followed by a word that will never appear 
            # is the maximum possible value of a bigramCost funciton
            # !!! this checks if the first word is in the corpus !!!
            for i in range (len(queryWords)):
                possible = [word for word in possibleFills(queryWords[i]) if len(word) > 1]
                #print(possible)
                self.fills.append(possible)

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
        while (i < len(state) and state[i] != ' '): i+=1
        return state[0:j] + action[0] + state[i:len(state)]

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        wds = get_words(state)
        # checks if every word in corpus - USELESS/Possible damage
        # for i in range(len(wds)):
        #     if (self.bigramCost(wds[i], self.not_word) >= self.threshold):
        #         return False
        for i in range(len(wds)):
            if (wds[i] not in self.fills[i]):
                return False
        return True

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        wds = get_words(state)
        add = 1
        if (len(wds) == 1): return 0.0
        i = action[1]
        if (self.bigramCost(action[0], self.not_word) >= self.threshold):
            #Word is not in corpus
            add = 15
        ret = 0
        if (i == 0):
            b1 = self.bigramCost(wds[0], wds[1])
            n_b1 = self.bigramCost(action[0], wds[1])
            ret = n_b1 - b1
        elif (i == len(wds) - 1):
            b2 = self.bigramCost(wds[i-1], wds[i])
            n_b2 = self.bigramCost(wds[i-1], action[0])
            ret = n_b2 - b2
        else:
            b1 = self.bigramCost(wds[i-1], wds[i])
            b2 = self.bigramCost(wds[i], wds[i+1])
            n_b1 = self.bigramCost(wds[i-1], action[0])
            n_b2 = self.bigramCost(action[0],wds[i+1])
            ret = (n_b1+n_b1) - (b1+b2)
        return ret + add



def insertVowels(queryWords, bigramCost, possibleFills):
    for i in range (len(queryWords)):
        queryWords[i] = queryWords[i].lower()
    vp = VowelInsertionProblem(queryWords, bigramCost, possibleFills)
    ret = util.uniformCostSearch(vp)
    if(ret):
        return ret.state
    else:
        return ''

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
    
    #resulSegment = segmentWords('thisisnotmybeautifulhouse', unigramCost)
    #print(resulSegment)
    #print(f'assimpleasthat = {unigramCost("assimpleasthat")}')
    #print(f'as simple as that = {unigramCost("as")}, {unigramCost("simple")}, {unigramCost("as")}, {unigramCost("tha")}')
    

    resultInsert = insertVowels('wld lk t hv mr lttrs'.split(), bigramCost, possibleFills)
    #print(f'om pa = {bigramCost("om", "pa")}')
    #print(f'me up = {bigramCost("me", "up")}')
    print(f'a cnbdfbzadfbzfbascvdvndsa = {bigramCost("a", "cnbdfbzadfbzfbascvdvndsa")}')
    print(f'enough already = {bigramCost("enough", "already")}')
    print(f'ngh lrdy = {bigramCost("ngh", "lrdy")}')

    # print(f'would like = {bigramCost("would", "like")}')
    # print(f'like to = {bigramCost("like", "to")}')
    # print(f'to have = {bigramCost("to", "have")}')
    # print(f'have more = {bigramCost("have", "more")}')
    # print(f'more letters = {bigramCost("more", "letters")}')
    
    print(resultInsert)

if __name__ == '__main__':
    main()