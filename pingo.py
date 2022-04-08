import os
import subprocess
import time
from time import strftime
import pyautogui
import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import *

class GUI:
    def __init__(self): # METODO CONSTRUTOR DA CLASSE COM GUI
        self.ip = ''
        self.condominio = '' 
        self.ultimo_evento = ''
        self.nova_lista = []
        self.minuto_atual = ''
        self.ultimo_minuto = ''
        self.response = []
        self.hora = ''
        self.contador = 0
        self.janela = Tk()
        self.janela.title('PING')
        self.janela.geometry('600x500')
        
        self.frameIP = Frame(self.janela)
        self.frameCOND = Frame(self.janela)
        self.frameEXIB = Frame(self.janela)
        
        self.label_ip = Label(self.frameIP, text="DIGITE O HOST OU IP: ", width=20, height=2)
        self.entrar_ip = Entry(self.frameIP, width=30)
        self.label_ip.pack(side='left')
        self.entrar_ip.pack(side='left')
        self.btn1 = Button(self.frameIP, text='EXECUTAR', command=self.pegar_dados, width=20)
        self.btn1.pack(side='left')
        self.frameIP.pack()

        self.label_local = Label(self.frameCOND, text="NOME IDENTIFICADOR: ", width=20, height=2)
        self.entrar_local = Entry(self.frameCOND, width=30)
        self.label_local.pack(side='left')
        self.entrar_local.pack(side='left')
        self.btn2 = Button(self.frameCOND, text='SAIR', command=self.confirma_sair, width=20)
        self.btn2.pack(side='left')
        self.frameCOND.pack()

        self.empty_label = Text(self.frameEXIB, width=70, height=20)
        self.empty_label.pack(side='right')
        self.frameEXIB.pack()

        self.janela.mainloop()

    def pegar_dados(self): # METODO BUSCA OS DADOS DOS CAMPOS
        if self.contador == 0:
            self.imprimir_boasvindas()
            self.ip = self.entrar_ip.get()
            self.local = self.entrar_local.get()
            self.contador = 1

        if not self.ip or not self.local: # VALIDA ERRO, CASO OS CAMPOS ESTEJAM VAZIOS
            mb.showerror("ERRO!", "Os campos não podem ficar vazios!")
            self.contador = 0
        else: # PEGA OS DADOS E EXECUTA A FUNÇÃO PRINCIPAL
            self.janela.after(1000, self.pegar_dados)
            self.execucao_principal()

    def execucao_principal(self): # METODO EXECUTA O PING, GUARDA DATA E HORA ATUAL
        self.response = os.popen('ping -n 1 {}'.format(self.ip)).read()
        self.hora = strftime(' - %d %b %Y - %H:%M')
        self.minuto_atual = self.hora.split()

        if 'Esgotado' in self.response: # VERIFICA RETORNO DO PING PARA TEMPO ESGOTADO
            if self.ultimo_minuto != self.minuto_atual[-1]:
                self.ultimo_evento = 'Esgotado o tempo limite do pedido - '
                with open('RELATORIO.txt', 'a') as data: # ABRE ARQUIVO TXT PARA PERSISTENCIA DOS DADOS
                    data.write(self.ultimo_evento)
                    data.write(self.local)
                    data.write(self.hora)
                    data.write('\n')
                self.imprimir_log()
                self.ultimo_minuto = self.minuto_atual[-1]

        if 'Falha' in self.response: # VERIFICA RETORNO DO PING PARA FALHA GERAL
            if self.ultimo_minuto != self.minuto_atual[-1]:
                self.ultimo_evento = 'Falha geral - '
                with open('RELATORIO.txt', 'a') as data: # ABRE ARQUIVO TXT PARA PERSISTENCIA DOS DADOS
                    data.write(self.ultimo_evento)
                    data.write(self.local)
                    data.write(self.hora)
                    data.write('\n')
                self.imprimir_log()
                self.ultimo_minuto = self.minuto_atual[-1]
            
        if 'Host' in self.response: # VERIFICA RETORNO DO PING PARA HOST INACESSIVEL
            if self.ultimo_minuto != self.minuto_atual[-1]:
                self.ultimo_evento = 'Host Inacessivel - '
                with open('RELATORIO.txt', 'a') as data: # ABRE ARQUIVO TXT PARA PERSISTENCIA DOS DADOS
                    data.write(self.ultimo_evento)
                    data.write(self.local)
                    data.write(self.hora)
                self.imprimir_log()
                self.ultimo_minuto = self.minuto_atual[-1]
  
    def imprimir_monitoramento(self): # MOSTRA INFORMAÇÃO INICIAL DE MONITORAMENTO NA TELA
        self.empty_label.insert(END, f'Iniciando monitoramento...\n')

    def imprimir_log(self): # MOSTRA NA TELA DO USUARIO UMA MENSAGEM DE SUCESSO NA GRAVACAO DOS DADOS
        self.empty_label.insert(END, f'Log gerado com sucesso em RELATORIO.txt{self.hora}\n')
    
    def message_error(self): # MOSTRA ERRO CASO CAMPOS ESTEJAM VAZIOS
        mb.showerror("Erro", "Campo incorreto!")
    
    def confirma_sair(self): # MOSTRA JANELA DE CONFIRMAÇÃO PARA SAIR OU NÃO DO SOFTWARE
        self.sair = mb.askyesno('Confirmar saida', 'Deseja sair?')
        if self.sair: # FINALIZA O PROGRAMA
            return self.janela.destroy()

    def limpar_prompt(self): # LIMPA PROMPT DE COMANDO
        return os.system('cls')

pingo_gui = GUI() # INSTANCIA A CLASSE DO SOFTWARE
            

