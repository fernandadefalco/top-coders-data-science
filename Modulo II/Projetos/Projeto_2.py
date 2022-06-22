import json
from functools import reduce
import os.path
import sys


# ----------------- Funções para manipular o arquivo JSON -----------------
def obter_dados(nome_arquivo:str):

    try:
        with open(os.path.join(sys.path[0],nome_arquivo+'.json'), 'r', encoding='utf8') as arquivo: 
            todos_cadastros = json.loads(arquivo.read())
    except:
        raise Exception("Não é possível abrir o arquivo.")
    return todos_cadastros
    
def gravar_dados(nome_arquivo:str,lista_dicionarios:list):
    try:
        with open(os.path.join(sys.path[0],nome_arquivo+'.json'), 'w', encoding='utf8') as arquivo:
            arquivo.write(json.dumps(lista_dicionarios,ensure_ascii=False))
    except:
        print(f"Não foi possível gravar no arquivo {nome_arquivo+'.json'}.")
    print ("Arquivo salvo com sucesso.")

# ----------------- Funções para o cadastro de músicos ----------------- 
def validacaoCadastro_nome(nome:str):
    for letra in nome:
        if letra.isalpha() == False and letra != " ": raise Exception ("Nome deve conter apenas espaços e letras.")

def validacaoCadastro_email(email:str):
    for caractere in email:
        if caractere.isalnum() == False and caractere not in("_",".","@"): raise Exception ("Email inválido.")
    if email.count("@") != 1: raise Exception ("Email inválido.")

def inputcadastroMusico(todos_cadastros:list):          
            try:
                nome = input("Insira o nome do músico/da musicista: ").lower()
                validacaoCadastro_nome(nome)
            except:
                print("Nome deve conter apenas espaços e letras.")
                while True:
                    nome = input("Insira o nome do músico/da musicista novamente: ").lower()
                    try: validacaoCadastro_nome(nome)
                    except:
                        print("Nome inválido")
                        continue
                    else: break
            try:
                email = input(f"Insira o email de {nome.title()}: ").lower()
                validacaoCadastro_email(email)
            except:
                print('Email inválido, deve conter apenas letras,números,"_" ou "." e um "@".')
                while True:
                    email = input("Insira o email novamente: ").lower()
                    try: validacaoCadastro_email(email)
                    except:
                        print("Email inválido.")
                        continue
                    else: break

            email_validador = [email for dicionario in todos_cadastros if dicionario["email"]==email]
            if len(email_validador) >= 1: raise Exception("Email já cadastrado.") 

            opcoes_variaveis = ["generos","instrumentos"]
            for i in range(2):
                while True:
                    try:
                        vars()["qtde_"+opcoes_variaveis[i]] = int(input(f"Quantos {opcoes_variaveis[i]} {nome.title()} toca? "))
                        if vars()["qtde_"+opcoes_variaveis[i]] == 0:
                            print("Quantidade deve ser pelo menos 1.")
                            continue
                    except:
                        print("Quantidade inválida, deve ser número.")
                        continue
                    else: break

            generos = [input(f"Insira o {numero+1}º gênero musical: ") for numero in range(vars()["qtde_"+opcoes_variaveis[0]])]  
            generos = list(dict.fromkeys(generos))         
            instrumentos = [input(f"Insira o {numero+1}º instrumento: ") for numero in range(vars()["qtde_"+opcoes_variaveis[1]])] 
            instrumentos = list(dict.fromkeys(instrumentos)) 

            return nome, email, generos, instrumentos

def cadastrarMusico(todos_cadastros:list, nome:str, email:str, generos:list, instrumentos:list):
    todos_cadastros.append({'nome':nome,'email': email,'generos': generos,'instrumentos': instrumentos})
    print("Usuário cadastrado.")
    return todos_cadastros
    
# ----------------- Funções para buscar músicos ----------------- 
def inputbuscarMusico():
    print("*** As categorias gêneros e instrumentos só aceitam 1 entrada ***")
    chaves = list(input("Insira a(s) chave(s) de busca separadas por vírgula (nome, email, generos e/ou instrumentos): ").lower().split(','))
    opcoes_chave = ("nome","email","generos","instrumentos")
    for chave in chaves:
        if chave not in opcoes_chave:
            chaves.remove(chave)
            nova_chave = input(f"Valor {chave} inválido, digite novamente (nome, email, generos ou instrumentos): ").lower()
            while nova_chave not in opcoes_chave: nova_chave = input(f"Valor {nova_chave} inválido, digite novamente (nome, email, generos ou instrumentos): ").lower()
            if nova_chave not in chaves: chaves.append(nova_chave)
    chaves = list(dict.fromkeys(chaves)) #removendo duplicatas
    valores = [input(f"Insira o {chave}: ").lower() for chave in chaves] 
    kwargs = dict(zip(chaves,valores))

    if len(valores) == 1: flag_e_ou = "e"
    else:
        flag_e_ou = input("Deseja que a busca considere todas as chaves ou elas individualmente? Insira E ou OU: ").lower()
        while flag_e_ou not in ("e","ou"): flag_e_ou = input("Opção inválida, insira E ou OU: ").lower()

    busca_exata = input("Deseja que a busca faça uma busca exata ou busca aproximada? Insira exata ou aprox: ").lower()
    while busca_exata not in ("exata","aprox"): busca_exata = input("Opção inválida, insira exata ou aprox: ").lower()  
    
    return flag_e_ou,busca_exata,kwargs


def buscarMusico(todos_cadastros:list,flag_e_ou:str,busca_exata:str,**kwargs):
    opcoes = [item for item in kwargs] #mostra as chaves dos kwargs

    if flag_e_ou == "ou":
        lista_resultados=[]
        for dicionario in todos_cadastros:
            for item_opcoes in opcoes:
                if type(dicionario[item_opcoes]) == str:
                    if busca_exata == "aprox":
                        if kwargs[item_opcoes] in dicionario[item_opcoes] and dicionario not in lista_resultados:
                            lista_resultados.append(dicionario)
                    else:
                        if kwargs[item_opcoes] == dicionario[item_opcoes] and dicionario not in lista_resultados:
                            lista_resultados.append(dicionario)
                else:
                    for indice in range(len(dicionario[item_opcoes])):
                        if busca_exata == "aprox":
                            if kwargs[item_opcoes] in dicionario[item_opcoes][indice] and dicionario not in lista_resultados:
                                lista_resultados.append(dicionario)
                        else:
                            if kwargs[item_opcoes] == dicionario[item_opcoes][indice] not in lista_resultados:
                                lista_resultados.append(dicionario)
    else:                        
        lista_resultados = []
        for dicionario in todos_cadastros:
            contador = 0
            for item_opcoes in opcoes:
                if type(dicionario[item_opcoes]) == str:
                    if busca_exata == "aprox":
                        if kwargs[item_opcoes] in dicionario[item_opcoes]:
                            contador +=1   
                    else:
                        if kwargs[item_opcoes] == dicionario[item_opcoes]:
                            contador +=1
                else:
                    for indice in range(len(dicionario[item_opcoes])):
                        if busca_exata == "aprox":
                            if kwargs[item_opcoes] in dicionario[item_opcoes][indice]:
                                contador +=1
                        else:
                            if kwargs[item_opcoes] == dicionario[item_opcoes][indice]:
                                contador +=1
                         
            if contador == len(opcoes): lista_resultados.append(dicionario)
             
    if len(lista_resultados) == 0: return ["Não foram encontrados resultados para essa busca."]
    else: return lista_resultados

# ----------------- Funções para modificar músicos ----------------- 
def inputmodificarMusico():
    try:
        email = input("Insira o email que deve ser buscado: ").lower()
        validacaoCadastro_email(email)
        email_validador = [email for dicionario in todos_cadastros if dicionario["email"]==email]
        if len(email_validador) == 0: raise Exception("Email não encontrado.") 
    except:
        print("Email inválido.")
        while True:
            email = input("Insira o email novamente: ").lower()
            try:
                validacaoCadastro_email(email)
                email_validador = [email for dicionario in todos_cadastros if dicionario["email"]==email]
                if len(email_validador) == 0: raise Exception("Email não encontrado.") 
            except:
                print("Email inválido.")
                continue
            else:
                break

    flag_add_remove = input("Gostaria de adicionar ou remover elementos? Insira adicionar ou remover: ").lower()
    while flag_add_remove not in ("adicionar","remover"):
        flag_add_remove = input("Entrada inválida. Insira adicionar ou remover: ").lower()
    

    print(f"O(s) gênero(s) cadastrado(s) desse músico são {buscarMusico(todos_cadastros,'e','exata',email = email)[0]['generos']}")
    genero_validacao = input(f"Gostaria de {flag_add_remove} gêneros (S/N)? ").upper()
    while genero_validacao not in ("S","N"):
        genero_validacao = input("Gostaria de modificar o gênero (S/N)? ").upper()
    
    kwargs = {}
    if genero_validacao == "S":
        while True:
            try: qtde_generos = int(input("Insira a quantidade de gêneros a serem modificados: "))
            except:
                print("Quantidade inválida, deve ser número.")
                continue
            else: break

        genero = [input("Insira o gênero: ").lower() for i in range(qtde_generos)]
        kwargs["generos"] = genero

    print(f"O(s) instrumento(s) cadastrados desse músico são {buscarMusico(todos_cadastros,'e','exata',email = email)[0]['instrumentos']}")
    instrumento_validacao = input(f"Gostaria de {flag_add_remove} instrumentos (S/N)? ").upper()
    while instrumento_validacao not in ("S","N"): instrumento_validacao = input("Gostaria de modificar o instrumento (S/N)? ").upper()
    
    if instrumento_validacao == "S":
        while True:
            try: qtde_instrumentos = int(input("Insira a quantidade de instrumentos a serem modificados: "))
            except:
                print("Quantidade inválida, dever ser número.")
                continue
            else: break

        instrumento = [input("Insira o instrumento: ").lower() for i in range(qtde_instrumentos)] 
        kwargs["instrumentos"] = instrumento
    
    if genero_validacao == "N" and instrumento_validacao == "N": return ["Não há modificações a serem feitas."]
    else: return email,flag_add_remove,kwargs

def modificarMusico(todos_cadastros:list, email, flag_add_remove, **kwargs): 
    for dicionario in todos_cadastros:
            if dicionario['email'] ==  email:
                for i in range(len(kwargs)):
                    if flag_add_remove == "adicionar":
                            for item_kwargs in list(kwargs.values())[i]:
                                if item_kwargs in dicionario["generos"] or item_kwargs in dicionario["instrumentos"]:
                                    print(f"{item_kwargs} já existe, não foi possível adicionar novamente.") 
                                else:
                                    dicionario[list(kwargs.keys())[i]].append(item_kwargs)    

                    elif flag_add_remove == "remover":
                        for item_kwargs in list(kwargs.values())[i]:
                                if item_kwargs in dicionario["generos"] and len(dicionario["generos"]) == 1:
                                    print("Não é possível remover o único elemento da lista.")
                                elif  item_kwargs in dicionario["instrumentos"] and len(dicionario["instrumentos"]) == 1:
                                    print("Não é possível remover o único elemento da lista.")        
                                elif item_kwargs not in dicionario["generos"] and item_kwargs not in dicionario["instrumentos"]:
                                    print(f"{item_kwargs} não está cadastrado para esse músico, não é possível remover.") 
                                else:
                                    dicionario[list(kwargs.keys())[i]].remove(item_kwargs)

    return todos_cadastros

# ----------------- Funções para montar bandas ----------------- 
def inputmontaBandas():
    genero = input("Insira um gênero musical: ").lower()
    while True:
        try: quantidade = int(input("Digite a quantidade desejada de músicos: "))
        except:
            print("Quantidade inválida, deve ser número.")
            continue
        else: break

    if quantidade == 1:
        quantidade = int(input("Insira uma quantidade maior que 1: "))
        while quantidade <=1:
            quantidade = int(input("Insira uma quantidade maior que 1: "))
    
    args = tuple([input(f"Insira o instrumento do {i+1}º músico:") for i in range(quantidade)])

    return genero, quantidade,args

class ErroGenero(Exception):
        def __init__(self, message = 'Gênero não encontrado dentro dos cadastros.'):
            self.message = message
            super().__init__(self.message)

class ErroInstrumento(Exception):
    def __init__(self, message = 'Instrumento não cadastrado'):
        self.message = message
        super().__init__(self.message)
            
def filtrar_musicos_por_genero(todos_cadastros:list,genero):
    dicionario_musicos={}
    for dicionario in todos_cadastros:
        if genero in dicionario["generos"] :dicionario_musicos.update({dicionario["email"]:dicionario["instrumentos"]})
    if dicionario_musicos == {}: raise ErroGenero() 
    return dicionario_musicos

def gera_redutor(dicionario):
    def classificadorInstrumentos(acumulador, chave):
        for i in range(len(dicionario[chave])):
            if dicionario[chave][i] in acumulador: acumulador[dicionario[chave][i]].append(chave)
            else: acumulador[dicionario[chave][i]] = [chave]   
        return acumulador  
    return classificadorInstrumentos

def montaBandas(todos_cadastros:list,genero,quantidade,*args):
    auxiliar_classificadorInstrumentos = gera_redutor(filtrar_musicos_por_genero(todos_cadastros,genero))
    dic_clas_instrumento = reduce(auxiliar_classificadorInstrumentos,filtrar_musicos_por_genero(todos_cadastros,genero),{}) 

    for item in args:
        if item not in dic_clas_instrumento: raise ErroInstrumento()

    acumulador_comb = [[(email,args[0])] + [(email_2,args[1])] for email in dic_clas_instrumento[args[0]] for email_2 in dic_clas_instrumento[args[1]] if email != email_2]
    
    lista =[]
    if len(args) == 2: return acumulador_comb
    
    for i in range(1,len(args)-1):
        for lista_tuplas in acumulador_comb:

            for email in dic_clas_instrumento[args[i+1]]:
                val_lista = [1 if email not in tupla else 0 for tupla in lista_tuplas]
                if all(val_lista):
                    lista.append(lista_tuplas + [(email,args[i+1])])
        acumulador_comb = lista[:]

    lista_final = [item for item in acumulador_comb if len(item) == quantidade]
    return lista_final

def removerRepetidos(lista):
    valores_unicos =[]
    for combinacoes in lista: 
        if set(combinacoes) not in valores_unicos:
            valores_unicos.append(set(combinacoes))
    return valores_unicos

# ----------------- Funções para menu ----------------- 
def escolhe_opcao() -> str:
    print("\nDigite a opção desejada: \n",
        "1. Cadastrar músico\n",
        "2. Buscar músico\n",
        "3. Modificar músico\n",
        "4. Montar uma banda\n",
        "0. Sair\n")
    return input("Insira uma opção: ")
    
def menu(todos_cadastros): 
    opcoes = {
        "1": cadastrarMusico,
        "2": buscarMusico,
        "3": modificarMusico,
        "4": montaBandas
    }

    opcao = escolhe_opcao()

    while opcao != "0":
        if opcao not in opcoes and opcao != "0":
            print("Opção inválida!")
            opcao = escolhe_opcao()
            continue
    
        if opcao == "1":
            try:
                input_musico = inputcadastroMusico(todos_cadastros)
                gravar_dados(nome_arquivo,opcoes[opcao](todos_cadastros,input_musico[0],input_musico[1],input_musico[2],input_musico[3]))
            except: print("Não foi possível cadastrar, email já existe.")      
       
        elif opcao == "2":
            input_busca = inputbuscarMusico()
            for item in opcoes[opcao](todos_cadastros,input_busca[0],input_busca[1],**input_busca[2]): print(item)

        elif opcao == "3":
            input_modificar = inputmodificarMusico()
            if len(input_modificar) == 1: print(input_modificar[0])
            else: gravar_dados(nome_arquivo,opcoes[opcao](todos_cadastros,input_modificar[0],input_modificar[1],**input_modificar[2]))

        elif opcao == "4":
            input_montabandas = inputmontaBandas()
            try: 
                for item in removerRepetidos(opcoes[opcao](todos_cadastros,input_montabandas[0],input_montabandas[1],*input_montabandas[2])): print(item)
            except ErroInstrumento: print("Foi inserido um instrumento que não está cadastrado.")
            except ErroGenero: print("Gênero não encontrado dentro dos cadastros.")

        opcao = escolhe_opcao()
    else: print("**** Fim do programa ****")


# ----------------- Programa Principal ----------------- 
validacao = input("É o primeiro acesso do arquivo? (S/N) ").upper()
while validacao not in ("S","N"):
    validacao = input("Insira novamente (S/N)").upper()
if validacao == "S":
    nome_arquivo = input("Digite o nome do novo arquivo: ")
    gravar_dados(nome_arquivo,[]) #gerando um arquivo
    todos_cadastros = obter_dados(nome_arquivo)
    menu(todos_cadastros)

else:
    nome_arquivo = input("Digite o nome do arquivo a ser buscado: ")
    try:
        todos_cadastros = obter_dados(nome_arquivo)
    except: print("Não foi possível abrir o arquivo.")
    else: menu(todos_cadastros)

