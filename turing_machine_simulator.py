import sys


DicFuncao = {}
DicEstado = {}
DicChar = {}



def Leitura(nome):
# Abre Arquivo para leitura e cria uma lista de Linhas
    try:
        arquivo = open(nome, 'r')

        codigo = arquivo.readlines()

        arquivo.close()
# Trata Excecao quando o nome do arquivo e invalido
    except:
        print("Arquivo Invalido")
        exit(0)

    nomeFunc = ''


# Laço para varrer cada linha do codigo
    for linha in codigo:


        if linha.startswith('    ;') or linha.startswith(';'):
            continue


        elif linha.startswith('bloco'):
            nomeFunc = Cria_Funcoes(linha)


        elif linha.startswith('fim'):
            global DicEstado
            global DicChar
            global DicFuncao
            DicFuncao[nomeFunc][0] = DicEstado
            DicEstado = {}
            DicChar = {}



        elif linha.startswith('    '):
            Cria_Estados(linha,nomeFunc)


        elif linha.startswith('\n'):
            continue

        else:
            print('Comando'+ repr(linha) +'invalido' )
            exit(0)

# Cria Dicionario de funcoes

def Cria_Funcoes(linha):

    func = linha.split()
    lista = [DicEstado,func[2]]
    DicFuncao[func[1]] = lista
    return (func[1])


# Cria dicionario de Estados
def Cria_Estados(linha,nomeFunc):
    global DicEstado
    global DicChar
    comand = linha.split()

# testa se o estado de partida possui mais de 4 bits
    if len(comand[0]) > 4:
        print('Comando'+ repr(comand[0]) +'invalido' )
        exit(0)

# testa se o estado de partida e um inteiro
    if comand[0].isdigit() == False:
        print('Comando'+ repr(comand[0]) +'invalido' )
        exit(0)

# testa se o comando e o chamado de uma funcao
    if len(comand[1])!= 1:
        if len(comand) == 3:
            lista = [comand[2]]
            DicChar = {comand[1]:lista}
            DicEstadoA = {comand[0]: DicChar}
            if comand[0] in DicEstado:
                DicEstado[comand[0]].update(DicChar)
            else:
                DicEstado.update(DicEstadoA)

# testa se o comando e o chamado de uma funcao com ! no final
        elif len(comand) == 4:
            if comand[3] == '!':
                lista = [comand[2],comand[3]]
                DicChar = {comand[1]:lista}
                DicEstadoA = {comand[0]: DicChar}
                if comand[0] in DicEstado:
                    DicEstado[comand[0]].update(DicChar)
                else:
                    DicEstado.update(DicEstadoA)
            else:
                print('Comando'+ repr(comand[3]) +'invalido' )
                exit(0)
        elif len(comand) == 6:
            if len(comand) == 6:
                lista = [comand[3],comand[4],comand[5]]
                DicChar = {comand[1]:lista}
                DicEstadoA = {comand[0]:DicChar}
                if comand[0] in DicEstado:
                    DicEstado[comand[0]].update(DicChar)
                else:
                    DicEstado.update(DicEstadoA)

            # testa se e um comando normal com ! no final

            elif len(comand) == 7:
                if comand[6] == '!':
                    lista = [comand[3],comand[4],comand[5],comand[6]]
                    DicChar = {comand[1]:lista}
                    DicEstadoA = {comand[0]:DicChar}
                    if comand[0] in DicEstado:
                        DicEstado[comand[0]].update(DicChar)
                    else:
                        DicEstado.update(DicEstadoA)
                else:
                    print('Comando'+ repr(comand[6]) +'invalido' )
                    exit(0)


# testa se e um comando normal
    elif len(comand) == 6:
        lista = [comand[3],comand[4],comand[5]]
        DicChar = {comand[1]:lista}
        DicEstadoA = {comand[0]:DicChar}
        if comand[0] in DicEstado:
            DicEstado[comand[0]].update(DicChar)
        else:
            DicEstado.update(DicEstadoA)

# testa se e um comando normal com ! no final

    elif len(comand) == 7:
        if comand[6] == '!':
            lista = [comand[3],comand[4],comand[5],comand[6]]
            DicChar = {comand[1]:lista}
            DicEstadoA = {comand[0]:DicChar}
            if comand[0] in DicEstado:
                DicEstado[comand[0]].update(DicChar)
            else:
                DicEstado.update(DicEstadoA)
        else:
            print('Comando'+ repr(comand[6]) +'invalido' )
            exit(0)

#Testa se e qualquer outra coisa que nao pode ser aceita na MT
    else:
        print('Comando'+ repr(linha) +'invalido' )
        exit(0)

#funcao que le o arquivo
#Leitura(sys.argv[1])

def executaInstrucao(charCabecote):

    global charFita2
    global Fita
    global PosCabecote
    global EstAtual
    global FuncaoAtual
    global PilhaDeEstados
    global PilhaDeFuncoes

    instExec = DicFuncao[FuncaoAtual]
    instExec = instExec[0][EstAtual]
    if ( ( charCabecote in instExec ) or (charFita2 in instExec) ):
        #codigo de quando tem transicao
        
        #verifica se o simbolo de transicao ta na fita 1 ou na fita 2 (precedencia da fita 1)
        if ( charCabecote in instExec ) :    
            instExec = instExec[charCabecote]
        else :
            instExec = instExec[charFita2]

        #coloca novo caracter na fita caso não seja para repitilo
        if (instExec[0] != '*'):
            fita1 = Fita[0:PosCabecote]
            fita2 = Fita[PosCabecote+1:len(Fita)]
            ch = instExec[0]
            Fita = fita1 + ch + fita2

        #verifica se tem alteracao no cabecote
        if ( instExec[1] == 'e'):
            PosCabecote -= 1
        elif (instExec[1] == 'd'):
            PosCabecote += 1

        #atribui novo estados
        if ( instExec[2] == '*'):
            EstAtual = EstAtual
        elif ( instExec[2] == 'retorne'):
            EstAtual = PilhaDeEstados.pop()
            FuncaoAtual = PilhaDeFuncoes.pop()
        elif ( instExec[2] == 'pare' ):
            print('O programa finalizou corretamente!')
            exit(0)
        else:
            EstAtual = instExec[2]

        #verifica se tem breakpoint
        if ( instExec[len(instExec)-1] == '!'):
            return 1

    elif ( '*' in instExec):
        #codigo de quando pode ser qualquer char
        instExec = instExec['*']

        #coloca novo caracter na fita caso não seja *
        if (instExec[0] != '*'):
            fita1 = Fita[0:PosCabecote]
            fita2 = Fita[PosCabecote+1:len(Fita)]
            ch = instExec[0]
            Fita = fita1 + ch + fita2


        #verifica se tem alteracao no cabecote
        if ( instExec[1] == 'e'):
            PosCabecote -= 1
        elif (instExec[1] == 'd'):
            PosCabecote += 1

        #atribui novo estados
        if ( instExec[2] == '*'):
            EstAtual = EstAtual
        elif ( instExec[2] == 'retorne'):
            EstAtual = PilhaDeEstados.pop()
            FuncaoAtual = PilhaDeFuncoes.pop()
        elif ( instExec[2] == 'pare' ):
            print('ACEITA')
            print('FIM SIMULAÇÃO')
        else:
            EstAtual = instExec[2]

        #verifica se tem breakpoint
        if ( instExec[len(instExec)-1] == '!'):
            return 1

    else:
        #pega as chaves do dicionario e transforma em uma lista
        chavesDict = instExec.keys()
        listaDeFuncoes = list(chavesDict)

        if ( len(listaDeFuncoes) == 1):
            if ( listaDeFuncoes[0] in DicFuncao ):
                #codigo que chama uma funcao e guarda o valor pra onde votar

                #coloca a funcao e estado na pilha de execucao
                PilhaDeFuncoes.append(FuncaoAtual)
                PilhaDeEstados.append(instExec[listaDeFuncoes[0]][0])
                #coloca a funcao inical sendo a em execucao
                FuncaoAtual = listaDeFuncoes[0]

                #verifica se tem breakpoint
                if ( len(instExec[FuncaoAtual]) == 2):
                    return 1

                #pega o estado inical da funcao
                EstAtual = DicFuncao[listaDeFuncoes[0]][1]
                if ( len(EstAtual) == 1):
                    EstAtual = '0' + EstAtual
            elif (listaDeFuncoes[0] == 'copiar'):
                #codigo que copia o char do cabecote para a fita 2

                charFita2 = '[' + charCabecote + ']'

                #Pega o estado que vai depois que copiar
                EstAtual = instExec[listaDeFuncoes[0]][0]
                if ( len(EstAtual) == 1):
                    EstAtual = '0' + EstAtual

            elif (listaDeFuncoes[0] == 'colar'):
                #codigo que copia o char da fita 2 para o cabecote

                #Pega o estado que vai depois que copiar
                EstAtual = instExec[listaDeFuncoes[0]][0]
                if ( len(EstAtual) == 1):
                    EstAtual = '0' + EstAtual

                #copiar o char para a fita
                fita1 = Fita[0:PosCabecote]
                fita2 = Fita[PosCabecote+1:len(Fita)]
                ch = charFita2[1]
                Fita = fita1 + ch + fita2

            else:
                #codigo de quando nao ha transicao definida ERRO
                print('REJEITA')
                print('FIM SIMULAÇÃO')
                exit(0)
        else :
            #codigo de quando nao ha transicao definida ERRO
            print('REJEITA')
            print('FIM SIMULAÇÃO')
            exit(0)
    return 0

'''

Simulador de Maquina de Turing V1.0

Mateus Francisco Vieira Soares
Italo Haylander Faria Galvao


PROGRAMA PRINCIPAL
'''

print('Simulador de Maquina de Turing v1.0 ')
print('Desenvolvido como trabalho pratico para a disciplina de Teoria da Computacao.')
print('Mateus F. V. Soares, Italo H. F. Galvao, IFMG, 2019.')
print('\n')

charCab1 = '('
charCab2 = ')'


NumExec = -1

if (sys.argv[1] == "-head"):
    if (sys.argv[2] == '<>'):
        charCab1 = '<'
        charCab2 = '>'
        if (sys.argv[3] == '-s'):
            NumExec = int(sys.argv[4])
            Leitura(sys.argv[5])
        elif (sys.argv[3] == '-r'):
            NumExec = -1
            Leitura(sys.argv[4])
        elif (sys.argv[3] == '-v'):
            NumExec = 0
            Leitura(sys.argv[4])
elif (sys.argv[1] == '-s'):
    NumExec = int(sys.argv[2])
    Leitura(sys.argv[3])
elif (sys.argv[1] == '-r'):
    NumExec = -1
    Leitura(sys.argv[2])
elif (sys.argv[1] == '-v'):
    NumExec = 0
    Leitura(sys.argv[2])

#variaveis que controlam os estados, fita, funcao atual, e a posicao cabecote

#coloca a funcao inical sendo a main
FuncaoAtual = "main"

#pega o estado inical da funcao main
EstAtual = DicFuncao["main"][1]
EstAtual = str(EstAtual)
if ( len(EstAtual) == 1):
    EstAtual = '0' + EstAtual

PilhaDeEstados = []
PilhaDeFuncoes = []

#coloca a fita 2 como virgem

charFita2 = "[_]"

#recebe a palavra incial
caracterFita = '____________________'
charFun = '....................'
Fita = input('Forneca a palavra inicial: ')
Fita = caracterFita + Fita + caracterFita
PosCabecote = 20



contExec = 0


if (NumExec == -1):
    while True:
        info = charFun + FuncaoAtual+'.'+EstAtual.zfill(4)+' : '
        if (EstAtual != 'pare'): 
            executaInstrucao(Fita[PosCabecote])
        else:
            print(info[len(info)-25:len(info)] + Fita[PosCabecote-20:PosCabecote]+charCab1+Fita[PosCabecote]+charCab2+Fita[PosCabecote+1:PosCabecote+20]+' : '+charFita2[1])
            print('ACEITA')
            print('FIM SIMULAÇÃO') 
            exit(0)

elif (NumExec == 0):
    while True:
        info = charFun + FuncaoAtual+'.'+EstAtual.zfill(4)+' : '
        if ( PosCabecote < 20):

            print(info[len(info)-25:len(info)]+Fita[0:PosCabecote]+charCab1+Fita[PosCabecote]+charCab2+Fita[PosCabecote+1:40]+' : '+charFita2[1])
        else:
            print(info[len(info)-25:len(info)] + Fita[PosCabecote-20:PosCabecote]+charCab1+Fita[PosCabecote]+charCab2+Fita[PosCabecote+1:PosCabecote+20]+' : '+charFita2[1])
        if (EstAtual != 'pare'):
            executaInstrucao(Fita[PosCabecote])
        else:
            print('ACEITA')
            print('FIM SIMULAÇÃO')
            exit(0)
else:
    opcao = '-s'
    while True:

        while (contExec < NumExec):

            if ( opcao == '-s'):
                contExec += 1
            if ( opcao == '-r'):
                while True:
                    if (EstAtual != 'pare'):
                        executaInstrucao(Fita[PosCabecote])
                    else:
                        print(info[len(info)-25:len(info)] + Fita[PosCabecote-20:PosCabecote]+charCab1+Fita[PosCabecote]+charCab2+Fita[PosCabecote+1:PosCabecote+20]+' : '+charFita2[1])
                        print('ACEITA')
                        print('FIM SIMULAÇÃO')
                        exit(0)

            info = charFun + FuncaoAtual+'.'+EstAtual.zfill(4)+' : '
            if ( PosCabecote < 20):

                print(info[len(info)-25:len(info)]+Fita[0:PosCabecote]+charCab1+Fita[PosCabecote]+charCab2+Fita[PosCabecote+1:40]+' : '+charFita2[1])
            else:
                print(info[len(info)-25:len(info)] + Fita[PosCabecote-20:PosCabecote]+charCab1+Fita[PosCabecote]+charCab2+Fita[PosCabecote+1:PosCabecote+20]+' : '+charFita2[1])
            if (EstAtual != 'pare'):
                executaInstrucao(Fita[PosCabecote])
            else:
                print('ACEITA')
                print('FIM SIMULAÇÃO')
                exit(0)

        contExec = 0
        novaOpcao = input('Nova opcao de execucao: (-r/-v/-s)')
        novaOpcao = novaOpcao.split()
        opcao = novaOpcao[0]
        if ( len(novaOpcao) == 2):
            NumExec = int(novaOpcao[1])