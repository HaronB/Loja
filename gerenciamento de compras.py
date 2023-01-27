# -*- coding: utf-8 -*-
"""
Created on Sun May 22 22:11:55 2022

@author: Haron
"""

import csv
import datetime

class loja:
    def __init__(self):
        self.atualizar_produtos()
        self.lista = [[],[],[]]
    
    #Atualiza os produtos na memoria
    def atualizar_produtos(self):
        with open ('Produto.csv', mode='r') as csv_file:
            dados_csv = csv.reader(csv_file, delimiter = ';')
            self.produto = [[],[],[],[],[],[],[],[]]
            for linha in dados_csv:
                for i in range(len(linha)):
                    self.produto[i].append(linha[i])
        self.log = [[],[],[],[],[],[],[],[]]
        self.estoque(0)
    
    #Remove um produto
    def remover_produto(self, produto):
        if (produto in self.produto[0]):
            x = self.produto[0].index(produto)
            for i in range(len(self.produto)):
                self.produto[i].pop(x)
            for i in range(len(self.produto[2])):
                if (i > 0):
                    self.produto[2][i] = 0;
            with open ('Produto.csv', mode='w', newline='') as csv_file:
                dados_csv = csv.writer(csv_file, delimiter = ';')
                dados_csv.writerow(["Cod_Produto", "Nome", "Quantidade","Valor_Compra","Valor_Venda","Minimo","Ideal","Maximo"])
                for linha in range(1, len(self.produto[0])):
                    dados_csv.writerow([self.produto[x][linha] for x in range(len(self.produto))])
            self.atualizar_produtos()
            print("Removido com sucesso")
        else:
            print("Nao encontrado produto com esse cod")
    
    #Adiciona um produto   
    def adiciona_produto(self, produto):
        if not(produto[0] in self.produto[0]):
            for x in range(len(self.produto[2])):
                if (x > 0):
                    self.produto[2][x] = 0;
            with open ('Produto.csv', mode='w', newline='') as csv_file:
                dados_csv = csv.writer(csv_file, delimiter = ';')
                dados_csv.writerow(["Cod_Produto", "Nome", "Quantidade","Valor_Compra","Valor_Venda","Minimo","Ideal","Maximo"])
                for linha in range(1, len(self.produto[0])):
                    dados_csv.writerow([self.produto[x][linha] for x in range(len(self.produto))])
                dados_csv.writerow(produto)
            self.atualizar_produtos()
            print("Adicionado com sucesso")
        else:
            print("ja existe produto com esse cod")
    
    #Metodo de vendas
    #0 - adiciona, 1 - modifica, 2 - lista as venda, 3 - mostra os valores, 4 - finaliza a venda
    #5 - cancela
    def vendas(self,tipo, produto = 0, quant = 0):
        #Adicionar e verifica se existe o produto
        if (tipo == 0 and produto in self.produto[0]):
            #Verifica se tem produto o suficiente no estoque
            if (quant <= int(self.produto[2][self.produto[0].index(produto)])):
                #0 cod do produto. 1 Quantidade, 2 Preço total
                self.lista[0].append(produto)
                self.lista[1].append(quant)
                self.lista[2].append(float(self.produto[4][self.produto[0].index(produto)])*quant)
            else:
                print("Estoque insuficiente")
         #Adicionar e verifica se existe o produto na lista de vendas   
        elif (tipo == 1 and produto in self.lista[0]):
            #Verifica se tem produto o suficiente no estoque
            if (quant <= int(self.produto[2][self.produto[0].index(produto)])):
                x = self.lista[0].index(produto)
                #0 cod do produto. 1 Quantidade, 2 Preço total
                self.lista[0].pop(x)
                self.lista[1].pop(x)
                self.lista[2].pop(x)
                self.lista[0].append(produto)
                self.lista[1].append(quant)
                self.lista[2].append(float(self.produto[4][self.produto[0].index(produto)])*quant)
            else:
                print("Estoque insuficiente")
        #Lista
        elif (tipo == 2):
            print("Produtos na lista de vendas: ")
            for x in range(len(self.lista[0])):
                print("Produto: {0} Quantidade: {1}".format(self.produto[1][self.produto[0].index(self.lista[0][x])], self.lista[1][x]))
        #Lista preços
        elif (tipo == 3):
            print("Produto\tQuantidade\tPreco unit\tPreco Total")
            for x in range(len(self.lista[0])):
                print("{0}\t\t\t{1}\t\t\t{2}\t\t\t{3}".format(self.produto[1][self.produto[0].index(self.lista[0][x])], self.lista[1][x], self.produto[4][self.produto[0].index(self.lista[0][x])], self.lista[2][x]))
            print("Custo total:", sum(self.lista[2]))
        #Finaliza
        elif (tipo == 4):  
            self.vendas(3)
            print("Finalizando vendas")
            for x in range(len(self.lista[0])):
                self.transacao(1, int(self.lista[0][x]), self.lista[1][x])
                self.estoque(0)
            self.lista = [[],[],[]]
            print("venda finalizada")
        #Cancela
        elif (tipo == 5):
            print("venda cancelada")
            self.lista = [[],[],[]]
        else:
            print("Escolha Invalida")
    
    #Metodo de compras
    #0 - adiciona, 1 - modifica, 2 - lista as compras, 3 - mostra os valores, 4 - finaliza a compras
    #5 - cancela    
    def compras(self, tipo, produto = "0", quant = 0):
        #Adicionar e verifica se existe o produto
        if (tipo == 0 and produto in self.produto[0]):
            #Verifica se vai passar a quantidade max do produto
            if (quant+int(self.produto[2][self.produto[0].index(produto)]) >= int(self.produto[7][self.produto[0].index(produto)])):
                print("Essa compra vai ultrapassar a quantidade maxima")
            #Verifica se vai passar a quantidade ideal do produto
            elif (quant+int(self.produto[2][self.produto[0].index(produto)]) >= int(self.produto[6][self.produto[0].index(produto)]) > int(self.produto[2][self.produto[0].index(produto)])):
                print("Essa compra vai ultrapassar a quantidade ideal")
            #0 cod do produto. 1 Quantidade, 2 Preço total
            self.lista[0].append(produto)
            self.lista[1].append(quant)
            self.lista[2].append(float(self.produto[3][self.produto[0].index(produto)])*quant)
            print("Produto adicionado a lista\n")
        #Adicionar e verifica se existe o produto na lista de compras      
        elif (tipo == 1 and produto in self.lista[0]):
            #Verifica se vai passar a quantidade max do produto
            if (quant+int(self.produto[2][self.produto[0].index(produto)]) >= int(self.produto[7][self.produto[0].index(produto)])):
                print("Essa compra vai ultrapassar a quantidade maxima")
            #Verifica se vai passar a quantidade ideal do produto
            elif (quant+int(self.produto[2][self.produto[0].index(produto)]) >= int(self.produto[6][self.produto[0].index(produto)])> int(self.produto[2][self.produto[0].index(produto)])):
                print("Essa compra vai ultrapassar a quantidade ideal")
            x = self.lista[0].index(produto)
            #0 cod do produto. 1 Quantidade, 2 Preço total
            self.lista[0].pop(x)
            self.lista[1].pop(x)
            self.lista[2].pop(x)
            self.lista[0].append(produto)
            self.lista[1].append(quant)
            self.lista[2].append(float(self.produto[3][self.produto[0].index(produto)])*quant)
            print("Produto modificado da lista\n")
        #Lista
        elif (tipo == 2):
            print("Produtos na lista de compras: ")
            for x in range(len(self.lista[0])):
                print("Produto: {0} Quantidade: {1}".format(self.produto[1][self.produto[0].index(self.lista[0][x])], self.lista[1][x]))
        #Lista preços
        elif (tipo == 3):
            print("Produto\tQuantidade\tPreco unit\tPreco Total")
            for x in range(len(self.lista[0])):
                print("{0}\t\t\t{1}\t\t\t{2}\t\t\t{3}".format(self.produto[1][self.produto[0].index(self.lista[0][x])], self.lista[1][x], self.produto[3][self.produto[0].index(self.lista[0][x])], self.lista[2][x]))
            print("Custo total:", sum(self.lista[2]))
        #Finaliza
        elif (tipo == 4):  
            self.compras(3)
            print("Finalizando compra")
            for x in range(len(self.lista[0])):
                self.transacao(0, int(self.lista[0][x]), self.lista[1][x])
                self.estoque(0)
            self.lista = [[],[],[]]
            print("Compra finalizada")
        #Cancela
        elif (tipo == 5):
            print("compra cancelada")
            self.lista = [[],[],[]]
        else:
            print("Escolha Invalida")
    
    #Metodo de estoque
    #0 - atualiza os produtos pelo log, 1 - verifica min, 2 - verifica ideal, 3 - verifica max, 4 - lista
    #5 - procura, 6 - sai
    def estoque(self, tipo, produto = ""):
        #Atualiza os produtos da memoria com o log
        if (tipo == 0):
            with open ('Log.csv', mode='r') as csv_file:
                    dados_csv = csv.reader(csv_file, delimiter = ';')
                    for linha in dados_csv:
                        if not(linha[0] in self.log[0]):
                            if (linha[3] in self.produto[0]):
                                if (linha[2] == "Compra"):
                                        self.produto[2][self.produto[0].index(linha[3])] = str(int(self.produto[2][self.produto[0].index(linha[3])]) + int(linha[5]))
                                        for i in range(len(linha)):
                                            self.log[i].append(linha[i]) 
                                elif (linha[2] == "Venda"):
                                    self.produto[2][self.produto[0].index(linha[3])] = str(int(self.produto[2][self.produto[0].index(linha[3])])- int(linha[5]))
                                    for i in range(len(linha)):
                                        self.log[i].append(linha[i])
        #verifica os produtos em falta
        elif (tipo == 1):
            pouco = [[self.produto[0][x], self.produto[1][x]] for x in range(1, len(self.produto[2])) if int(self.produto[2][x]) < int(self.produto[5][x])]
            print("Tem {0} produtos abaixo da quantidade min de produtos".format(len(pouco)))
            print(len(pouco))
            
            if (len(pouco) != 0):
                print("Produtos em falta:")
                for x in range(len(pouco)):
                    print("Cod_produto: {0}, Nome: {1}".format(pouco[x][0],pouco[x][1]))
        #Verifica quantos precisa de produto para ter o ideal
        elif (tipo == 2):
            ideal = [[self.produto[0][x],self.produto[1][x], int(self.produto[6][x]) - int(self.produto[2][x])] for x in range(1, len(self.produto[0])) if int(self.produto[2][x])< int(self.produto[6][x])]
            for x in range(len(ideal)):
                print("O produto {0} {1} precisa de {2} para ter a quantidade ideal para o estoque".format(ideal[x][0],ideal[x][1],ideal[x][2]))
        #Verifica quantos precisa de produto para ter o max
        elif (tipo == 3):
            muito = [[self.produto[0][x],self.produto[1][x], int(self.produto[7][x]) - int(self.produto[2][x])] for x in range(1, len(self.produto[0])) if int(self.produto[2][x])< int(self.produto[7][x])]
            for x in range(len(muito)):
                print("O produto {0} {1} precisa de {2} para ter a quantidade maxima para o estoque".format(muito[x][0],muito[x][1],muito[x][2]))
        #Listas todos os produtos
        elif (tipo == 4):
            for x in range(1, len(self.produto[0])):
                print("Produto {0} nome {1} tem {2} unidades, min: {3}, ideal: {4} e max: {5}".format(self.produto[0][x], self.produto[1][x], self.produto[2][x], self.produto[5][x], self.produto[6][x], self.produto[7][x]))
        #Procura um produto
        elif (tipo == 5):
            if (produto in self.produto[0]):
                x = self.produto[0].index(produto)
                print("o produto {0} {1} tem {2} unidade".format(self.produto[0][x], self.produto[1][x], self.produto[2][x]))
            else:
                print("Produto nao encontrado")
        else:
            print("Escolha Invalida")   
            
    #escreve um arquivo log.csv        
    def transacao(self, tipo, produto, quant):
        with open ('Log.csv', mode='w', newline='') as csv_file:
            dados_csv = csv.writer(csv_file, delimiter = ';')
            dados_csv.writerow(["id", "Data", "Tipo","Cod_Produto","Nome","Quantidade","Valor_unit","Valor_total"])
            conta_linha = 0
            for linha in range(len(self.log[0])):
                dados_csv.writerow([self.log[x][linha] for x in range(len(self.log))])
                conta_linha += 1
            if(tipo == 0):
                dados_csv.writerow([conta_linha, datetime.datetime.now(), "Compra", self.produto[0][produto], self.produto[1][produto], quant, self.produto[3][produto], quant*float(self.produto[3][produto])])
            elif(tipo == 1):
                dados_csv.writerow([conta_linha, datetime.datetime.now(), "Venda", self.produto[0][produto], self.produto[1][produto], quant, self.produto[4][produto], quant*float(self.produto[4][produto])])
     
        
Loja = loja()
#Menu
while True:
    escolha = int(input("\n1 - Comprar\n2 - Vender\n3 - Estoque\n4 - Adicionar produto\n5 - Remover produto\n6 - Sair\n"))
    #Menu compras
    if(escolha == 1):
        while True:
            escolha = int(input("\n1 - Adicionar\n2 - Modificar\n3 - Listar\n4 - Listar Preço\n5 - Finalizar\n6 - Cancelar\n"))
            #Adicionar
            if(escolha == 1):
                Loja.compras(0, input("Digite o Cod do produto: "), int(input("Digite a quantidade da compra: ")))
                print("")
            #Modificar
            elif(escolha == 2):
                Loja.compras(1, input("Digite o Cod do produto: "), int(input("Digite a quantidade da compra: ")))
                print("")
            #Listar
            elif(escolha == 3):
                Loja.compras(2)
                print("")
            #Listar preço
            elif(escolha == 4):
                Loja.compras(3)
                print("")
            #Finalizar
            elif(escolha == 5):
                Loja.compras(4)
                print("")
                break
            #Cancelar
            elif(escolha == 6):
                Loja.compras(5)
                print("")
                break
    #Menu vendas
    elif(escolha == 2):
        while True:
            escolha = int(input("\n1 - Adicionar\n2 - Modificar\n3 - Listar\n4 - Listar Preço\n5 - Finalizar\n6 - Cancelar\n"))
            #Adjcionar
            if(escolha == 1):
                Loja.vendas(0, input("Digite o Cod do produto: "), int(input("Digite a quantidade da venda: ")))
                print("")
            #Modificar
            elif(escolha == 2):
                Loja.vendas(1, input("Digite o Cod do produto: "), int(input("Digite a quantidade da venda: ")))
                print("")
            #Listar
            elif(escolha == 3):
                Loja.vendas(2)
                print("")
            #Listar Preço
            elif(escolha == 4):
                Loja.vendas(3)
                print("")
            #Finalizar
            elif(escolha == 5):
                Loja.vendas(4)
                print("")
                break
            #Cancelar
            elif(escolha == 6):
                Loja.vendas(5)
                print("")
                break
    #Menu estoque
    elif(escolha == 3):
        while True:
            escolha = int(input("\n1 - Verificar quantidade min\n2 - Verificar quantidade ideal\n3 - Verificar quantidade max\n4 - Listar\n5 - Procurar\n6 - Sair\n"))
            #Min
            if(escolha == 1):
                Loja.estoque(1)
                print("")
            #Ideal
            elif(escolha == 2):
                Loja.estoque(2)
                print("")
            #Mac
            elif(escolha == 3):
                Loja.estoque(3)
                print("")
            #Listar
            elif(escolha == 4):
                Loja.estoque(4)
                print("")
            #Procurar
            elif(escolha == 5):
                Loja.estoque(5, input("Digite o cod do produto: "))
                print("")
            #Sair
            elif(escolha == 6):
                break
    #Adicionar produto
    elif(escolha == 4):
        Loja.adiciona_produto([input("Cod produto: "), input("Nome: "), 0, input("Valor_compra: "), input("Valor_venda: "), input("Minimo: "), input("Ideal: "), input("Max: ")])
    #Remover produto
    elif(escolha == 5):
        Loja.remover_produto(input("Cod do produto: "))
    #Sair
    elif(escolha == 6):
        break
    #Invalido
    else:
        print("Escolha invalida")
