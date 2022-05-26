import json
import os.path
import sys

def obter_dados():
    '''
    Essa função carrega os dados dos produtos e retorna uma lista de dicionários, onde cada dicionário representa um produto.
    NÃO MODIFIQUE essa função.
    '''
    with open(os.path.join(sys.path[0], 'dados.json'), 'r') as arq:
        dados = json.loads(arq.read())
    return dados

def lista_categorias(dados: list) -> list:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá retornar uma lista contendo todas as categorias dos diferentes produtos.
    Cuidado para não retornar categorias repetidas.    
    '''
    lista_sem_repeticao = []
    lista_categoria = []
    for i in range(0,len(dados)):
        lista_categoria.append(dados[i]['categoria'])
        if dados[i]['categoria'] not in lista_sem_repeticao:
            lista_sem_repeticao.append(dados[i]['categoria'])
    
    return sorted(lista_sem_repeticao)
    

def listar_por_categoria(dados: list, categoria: str) -> list:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "categoria" é uma string contendo o nome de uma categoria.
    Essa função deverá retornar uma lista contendo todos os produtos pertencentes à categoria dada.
    '''
    lista_produtos_categoria = []
    for i in range(0,len(dados)):
        if dados[i]['categoria'] == categoria:
            lista_produtos_categoria.append(dados[i])

    return lista_produtos_categoria

def produto_mais_caro(dados: list, categoria: str) -> dict:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "categoria" é uma string contendo o nome de uma categoria.
    Essa função deverá retornar um dicionário representando o produto mais caro da categoria dada.
    
    * Suposição - se tiver mais de um produto com o mesmo preço (mais caro), retorna apenas o primeiro (classificado em ordem alfabética)
    '''

    categ = listar_por_categoria(dados, categoria)
    maximo = sorted(categ, key = lambda x: [-float(x["preco"]), x["id"].lower()])
    
    return maximo[0]

def produto_mais_barato(dados: list, categoria: str) -> dict:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    O parâmetro "categoria" é uma string contendo o nome de uma categoria.
    Essa função deverá retornar um dicionário representando o produto mais barato da categoria dada.
    
    * Suposição - se tiver mais de um produto com o mesmo preço (mais barato), retorna apenas o primeiro (classificado em ordem alfabética)
    '''
    
    categ = listar_por_categoria(dados, categoria)  
    minimo = sorted(categ, key = lambda x: [float(x["preco"]), x["id"].lower()])
    
    return minimo[0] 

def top_10_caros(dados: list) -> list:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá retornar uma lista de dicionários representando os 10 produtos mais caros.
    
    * Suposição - se tiver mais de um produto com o mesmo preço, retorna as ocorrências classificadas em ordem alfabética, limitando aos 10 produtos
    '''
    top_caros = sorted(dados, key = lambda x: [-float(x["preco"]), x["id"].lower()])[:10]
    
    return top_caros

def top_10_baratos(dados: list) -> list:
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá retornar uma lista de dicionários representando os 10 produtos mais caros.
    
    * Suposição - se tiver mais de um produto com o mesmo preço, retorna as ocorrências classificadas em ordem alfabética, ,limitando aos 10 produtos
    '''
    top_baratos = sorted(dados, key = lambda x: [float(x["preco"]), x["id"].lower()])[:10]

    return top_baratos

def menu(dados: list):
    '''
    O parâmetro "dados" deve ser uma lista de dicionários representando os produtos.
    Essa função deverá, em loop, realizar as seguintes ações:
    - Exibir as seguintes opções:
        1. Listar categorias
        2. Listar produtos de uma categoria
        3. Produto mais caro por categoria
        4. Produto mais barato por categoria
        5. Top 10 produtos mais caros
        6. Top 10 produtos mais baratos
        0. Sair
    - Ler a opção do usuário.
    - No caso de opção inválida, imprima uma mensagem de erro.
    - No caso das opções 2, 3 ou 4, pedir para o usuário digitar a categoria desejada.
    - Chamar a função adequada para tratar o pedido do usuário e salvar seu retorno.
    - Imprimir o retorno salvo. 
    O loop encerra quando a opção do usuário for 0.
    '''
    opcao = int(input("Selecione a opção desejada: "))
    
    while opcao not in range(0,7):
        opcao = int(input("Opção inválida, selecione uma das opções da lista: \n"))

    while opcao != 0:   
        if opcao == 1:
            resposta = lista_categorias(dados)
        elif opcao in (2,3,4):
            categoria = (input("Insira a categoria desejada: \n"))
            while categoria not in lista_categorias(dados):
                categoria = (input("Categoria inválida, insira novamente: \n"))
            if opcao == 2:
                resposta = listar_por_categoria(dados, categoria)
            if opcao == 3:
                resposta = produto_mais_caro(dados, categoria)
            if opcao == 4:
                resposta = produto_mais_barato(dados, categoria)
        elif opcao == 5:
            resposta = top_10_caros(dados)
        else:
            resposta = top_10_baratos(dados)
        
        if opcao in (3,4):    
            print(resposta)
        else:
            print(*resposta, sep = "\n")
            
        validacao = input("Gostaria de escolher novamente? (S/N) ").upper()
        while validacao not in ("S","N"):
            validacao = input("Opção inválida, gostaria de escolher novamente? (S/N) ").upper()          

        if validacao == "S":
            opcao = int(input("Selecione a opção desejada: "))
        else:
            opcao = 0
    
    
# Programa Principal - não modificar!
d = obter_dados()

print('''------------------MENU------------------
            Escolha uma opção:
            1. Listar categorias
            2. Listar produtos de uma categoria
            3. Produto mais caro por categoria
            4. Produto mais barato por categoria
            5. Top 10 produtos mais caros
            6. Top 10 produtos mais baratos
            0. Sair''')
menu(d)

print("********** Fim do programa **********")


