from random import random
from time import sleep

MP = list(range(32))

#coversor binário para decimal
def conv(v):
    j = len(v) - 1
    x = 0
    for i in v:
        i = int(i)
        i = i*2**j
        j -=1
        x += i
    return x
        
    

#criação de uma lista aleatoria
for i in range(32):
    celula = ''
    for j in range(8):
        x = random()
        if x<.5: celula+='0'
        else: celula+='1'
    MP[i] = celula

#exibição da lista aleatória
for i in MP:
    print('-',i,'-')




class MapeamentoDireto:
    def __init__(self):

        #criação da nossa cache vazia
        self.linhas = list(range(4))
        for i in range(4):
            byte0 = '00000000'
            byte1 = '00000000'

            bloco = [byte0,byte1]
            tag = ''
            
            self.linhas[i] = [tag,bloco]
            #Cada cache é um conjunto de linhas.
            #Cada linha contém dois ítens: a tag, e o bloco
            #Cada bloco possui duas células

    #Pegar algo que pode ou não estar na cache    
    def pega(self, end):

        #a tag está contida nos dois primeiros bits
        self.tag = end[0:2]

        #o número da linha está nos dois penultimos bits
        self.numl = conv(end[2:4])

        #vcs tão ligado
        self.byte = int(end[4])

        #pega a linha onde poderia estar contido nossos dados
        self.l = self.linhas[self.numl]



        #verifica se o nosso bloco realmente está nessa linha, através da tag
        if self.l[0] == self.tag:
            bloco = self.l[1]
            x = bloco[self.byte]
            print('\n[---------hit----------]')
            print('\n- ',x,' -')

        #se não estiver, vamos ter que ir buscar lá na meória principal
        else:
            print('\n[---------miss---------]')
            print('\nProcurando na memória principal', end='')
            for i in range(10):
                sleep(.5)
                print('.', end='')
            print('\n')

            #lá vamos nós
            self.busca(end)

            #repetimos o processo para enfim retornarmos o dado
            self.pega(end)

    def busca(self, end):
        #convertendo o endereço para decimal, já que nós vamos jogar esse endereço direto na lista MP
        e = conv(end)

        #trazendo o bloco
        if end[-1] == '0':
            byte0 = MP[e]
            byte1 = MP[e+1]
        else:
            byte1 = MP[e]
            byte0 = MP[e-1]

        #inserindo na cache
        self.linhas[self.numl][0] = self.tag
        self.linhas[self.numl][1] = [byte0, byte1]


class MapeamentoAssociativo:

    
    def __init__(batata):
        #já que nesse mapeamento os blocos podem ir para qualquer linha, precisamos de um parâmetro para substituição
        #nosso parâmetro será por idade, ou seja, o mais velho sai
        #todos os acessados vão para a lista acessados, logo, o mais velho vai ser o primeiro da lista
        batata.acessados = []
        
        batata.linhas = list(range(4))
        for i in range(4):
            byte0 = '00000000'
            byte1 = '00000000'

            bloco = [byte0,byte1]
            tag = ''
            
            batata.linhas[i] = [tag,bloco]

    def pega(batata, end):    
        batata.tag = end[:4]
        batata.byte = int(end[4])

        #adiciona a tag desse bloco aos acessados, isto é, se esta já não estiver lá
        if batata.tag not in batata.acessados:
            batata.acessados += [batata.tag]

        #procura pelo bloco na cache, se sim, retorna ele
        for i in range(4):
            tag = batata.linhas[i][0]
            if tag == batata.tag:
                print('\n[-----------hit---------]')
                #a nossa linha vai ser a linha onde as tags são iguais
                linha = batata.linhas[i]
                
                #o bloco é o item 1 da lista linhas
                bloco = linha[1]

                #a célula solicitada depende do último bit do endereço
                x = bloco[batata.byte]
                print('\n- ',x,' -')
                return x

        #caso as tags não batam
        print('\n[------------miss-----------]')
        print('\nProcurando na memória principal', end='')
        for i in range(10):
            sleep(.5)
            print('.', end='')
        print('\n')
        
        batata.busca(end)
        batata.pega(end)

    def busca(batata,end):
        e = conv(end)
        
        if end[-1] == '0':
            byte0 = MP[e]
            byte1 = MP[e+1]
        else:
            byte1 = MP[e]
            byte0 = MP[e-1]

        #agora, vamos ver se tem alguma linha em branco na cache
        branco = False
        for i in range(4):
            x = batata.linhas[i][0]
            if x=='': branco=True

        #se sim, nosso dado vai logo pra primeira que aparecer
        if branco:
            for i in range(4):
                if batata.linhas[i][0] == '':
                    batata.linhas[i][0] = batata.tag
                    batata.linhas[i][1] = [byte0,byte1]
                    return

        #se não, nosso dado vai tomar o lugar do mais velho
        else:
            velho = batata.acessados[0]
            batata.acessados = batata.acessados[1:]

            tag = velho
            for i in range(4):
                if batata.linhas[i][0] == tag:
                    print('Removendo bloco ', tag)
                    batata.linhas[i][0] = batata.tag
                    batata.linhas[i][1] = [byte0,byte1]
                    break

class MapAssocConj:

    def __init__(self):
        #Mesmo esquema de acessados da classe anterior, só que agora vai precisar
        #de um para cada conjunto.
        self.acessConj0 = []
        self.acessConj1 = []
        self.acessados = [self.acessConj0, self.acessConj1]

        self.conj0 = []
        self.conj1 = []

        self.conjuntos = [self.conj0,self.conj1]

        for i in range(2):
            self.conjuntos[i] = list(range(2))
            for j in range(2):
                byte0 = '00000000'
                byte1 = '00000000'

                bloco = [byte0,byte1]
                tag = ''
                
                self.conjuntos[i][j] = [tag,bloco]

    def pega(self, end):
        self.tag = end[:3]
        self.conj = int(end[3])
        self.byte = int(end[4])

        if self.tag not in self.acessados[self.conj]:
            self.acessados[self.conj] += [self.tag]

        for i in range(2):
            tag = self.conjuntos[self.conj][i][0]
            if tag == self.tag:
                print('\n[---------hit---------]')
                linha = self.conjuntos[self.conj][i]

                bloco = linha[1]

                x = bloco[self.byte]
                print('\n-',x,'-' )
                return x

        print('\n[------------miss---------]')
        print('\nProcurando na memória principal', end='')
        for i in range(10):
            sleep(.5)
            print('.', end='')
        print('\n')
        
        self.busca(end)
        self.pega(end)

    def busca(self, end):
        e = conv(end)

        if end[-1] == '0':
            byte0 = MP[e]
            byte1 = MP[e+1]
        else:
            byte1 = MP[e]
            byte0 = MP[e-1]
            
        branco = False
        for i in range(2):
            x = self.conjuntos[self.conj][i][0]
            if x=='': branco=True

        if branco:
            for i in range(2):
                if self.conjuntos[self.conj][i][0] == '':
                    self.conjuntos[self.conj][i][0] = self.tag
                    self.conjuntos[self.conj][i][1] = [byte0,byte1]
                    return
        else:
            velho = self.acessados[self.conj][0]
            self.acessados[self.conj] = self.acessados[self.conj][1:]

            for i in range(2):
                if self.conjuntos[self.conj][i][0] == velho:
                    print('Removendo bloco', velho, ' do conjunto ', self.conj)
                    self.conjuntos[self.conj][i][0] = self.tag
                    self.conjuntos[self.conj][i][1] = [byte0,byte1]
                    break
            
    
op=''
while op == '':
    op = input('\nDigite a opção desejada\n1 - Mapeamento Direto\n2 - Mapeamento associativo\n3 - Mapeamento Associativo de Conjuntos\n')
    if op == '1':
         cache = MapeamentoDireto()

    elif op == '2':
         cache = MapeamentoAssociativo()

    elif op == '3':
         cache = MapAssocConj()

    else:
         op = ''
         print('Valor inválido')
         

while True:
    a = ''
    while a == '':
        a = input('\nQue célula seu coração deseja? ')
        try:
            p = int(a)
            if len(a) != 5 or any((i != '0' and i != '1')for i in a):
                a = ''
                print('Valor Inválido')
                
                           
        except:
            print('Valor invalido (Apenas valores inteiros)')
            a = ''        

    cache.pega(a)
        

        

        
        

        
