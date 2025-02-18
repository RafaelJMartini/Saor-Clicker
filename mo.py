import tkinter as tk
from PIL import Image, ImageTk
import math
from datetime import datetime

# Variável global de contagem
besos = 0.0
besos_por_segundo = 10000000000.0

#numero de construções
qtd_saor = 0

def fechar(janela):
    janela.destroy()


def persistencia():
    try:
        with open("save.txt","r",encoding="utf-8") as arquivo:
            global besos,besos_por_segundo,qtd_saor
            linhas = arquivo.readlines()
            if not linhas:
                    return
            for linha in linhas:
                besos,besos_por_segundo,qtd_saor,data = linha.strip().split(";")

            #conversões
            besos = float(besos)
            besos_por_segundo = float(besos_por_segundo)
            qtd_saor = int(qtd_saor)
            
            data = datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f")
            data_atual = datetime.now()

            data = data.timestamp()
            data_atual = data_atual.timestamp()

            data_diff = round(data_atual - data)
            besos += data_diff*besos_por_segundo
    except FileNotFoundError:
        with open("save.txt","w",encoding="utf-8") as arquivo:
            arquivo.close()
        persistencia()


def recuperar_recorde():
    try:
        global recordtxt
        recordtxt = None
        with open("record.txt", "r", encoding="utf-8") as arquivo:
            if arquivo:
                for line in arquivo:
                    recordtxt = line
                if recordtxt or recordtxt == 0:
                    recordtxt = int(recordtxt)
    except FileNotFoundError:
        return



def salvar():
    with open("save.txt","w",encoding="utf-8") as arquivo:
        arquivo.write(f"{besos};{besos_por_segundo};{qtd_saor};{datetime.now()}")

def apagar_save():
        global besos
        global besos_por_segundo
        global qtd_saor
        besos = 0.0
        besos_por_segundo = 0.0
        qtd_saor = 0
        with open("save.txt", "w", encoding="utf-8") as arquivo:
            arquivo.close()

def excluir_save():

    def sair():
        confirm.destroy()
    confirm = tk.Tk()
    confirm.geometry("400x200+800+350")
    confirm.title("Excluir save")
    texto = tk.Label(confirm,text="Tem certeza que quer excluir seu save?",font=("Arial",15))
    texto.pack(pady=10)
    btn_yes = tk.Button(confirm,text="Sim desejo acabar com meu save e com minha vida",fg="red",font=("Arial",10),command=apagar_save)
    btn_yes.pack(pady=10)
    btn_no = tk.Button(confirm,text="Não",font=("Arial",10),command=sair)
    btn_no.pack(pady=10)
    confirm.mainloop()
persistencia()
recuperar_recorde()


def iniciar_jogo():
    # Criar janela
    janela = tk.Tk()
    janela.title("Saor & Rafael")
    janela.geometry("1000x800+500+100")
    janela.configure(bg="white")

    # Ícone da janela
    icon = tk.PhotoImage(file="images\\heart.png")
    janela.iconphoto(True, icon)


    def organizar_widgets():
        botao.pack()
        texto_print.pack()
        texto_bps.pack()

        
        btn_excluir_save.pack(side="bottom")
        btn_salvar.pack(pady=10,side="bottom")
        lbl_record.pack(side="bottom")

        saor.pack(side="left",padx=5)
        saor_qtd.pack(side="left",padx=5)
        btn_explodir.pack(side="right",padx=150,ipady=15,ipadx=15)
        
        
    def atualizar_btn():
        global besos,img_saor
        global saor

        #img_saor_pb = Image.open("images/saore.png").convert("L")
        img_saor_pb = Image.open("images\\saorebw.png")
        img_saor_pb = ImageTk.PhotoImage(img_saor_pb)
        img_saor_rgb = tk.PhotoImage(file="images\\saore.png")
        # Aqui você pode alterar o valor da variável para o seu caso
        if besos >= 15:  # Quando a variável atingir o valor 10 (ou outro valor desejado)
            img_saor = img_saor_rgb
            cor_saor = "black"
        else:
            img_saor = img_saor_pb
            cor_saor = "red"

        # Atualiza a imagem do botão
        saor.config(image=img_saor,fg=cor_saor)


        if besos >= 666:
            btn_explodir["fg"] = "black"


    def aumentar_inc(num):
        global besos_por_segundo
        besos_por_segundo += num
        texto_bps['text'] = f'{round(besos_por_segundo,2)} Besos por segundo'
    # Contador de beijos
    def besar():
        global besos
        besos += 1
        texto_print['text'] = f'{round(besos)} Besos'

    def incrementar_besos():
        global besos
        besos += besos_por_segundo/100
        texto_print['text'] = f'{math.floor(besos)} Besos'

        janela.after(10, incrementar_besos)

    def timer_btn():
        atualizar_btn()
        saor_qtd['text'] = f'{qtd_saor} Saor'
        texto_bps['text'] = f'{round(besos_por_segundo,2)} Besos por segundo'
        
        janela.after(50,timer_btn)


    def comprar_saor():
        global besos
        global qtd_saor

        if besos >= 15:
            qtd_saor += 1
            saor_qtd['text'] = f'{qtd_saor} Saor'
            aumentar_inc(0.2)
            besos -= 15

    def comprar_explodir():
        def verifica_record():
            try:
                with open("record.txt", "r", encoding="utf-8") as arquivo:
                    if arquivo:
                        record = arquivo.readline()
                        if record:
                            record = int(record)  
                            if qtd_saor < record:
                                return 1
                            else:
                                return 0
                        else:
                            return 1  
                    else:
                        return 1 
            except FileNotFoundError:
                return 1
        def explodir():

            global besos
            global besos_por_segundo
            global qtd_saor
            besos = 0.0
            besos_por_segundo = 0.0
            


            ultimato = tk.Tk()
            ultimato.title(":(")
            ultimato.geometry("500x300+700+350")


            texto = tk.Label(ultimato,text=f"Você exprodiu o mundo :(\n\nE fez isso usando {qtd_saor} Saor's",font=("Arial",11))

            if verifica_record():
                with open("record.txt", "w", encoding="utf-8") as arquivo:
                    arquivo.write(f"{qtd_saor}")
                texto = tk.Label(ultimato,text=f"Você exprodiu o mundo :(\n\nE fez isso usando {qtd_saor} Saor's\nÉ o atual recorde, parabéns!",font=("Arial",11))
            else:
                texto = tk.Label(ultimato,text=f"Você exprodiu o mundo :(\n\nE fez isso usando {qtd_saor} Saor's",font=("Arial",11))
            qtd_saor = 0
            texto.pack(pady=100)
            apagar_save()
            ultimato.after(4000, lambda: (ultimato.destroy(), fechar(janela)))

        global besos

        if besos>= 666:
            besos -= 666
            explodir()





    # Criar botão dentro do canvas
    img_botao = tk.PhotoImage(file="images\\rafaer.png")
    botao = tk.Button(janela, image=img_botao, borderwidth=0, bg="white",command=besar)
    
    # Texto de contagem de beijos logo abaixo do botão
    texto_print = tk.Label(janela, text="0 Besos",font=("Arial",16), bg="white")
    



    texto_bps = tk.Label(janela, text=f"{round(besos_por_segundo,2)} Besos por segundo",font=("Arial",13), bg="white")
    


    #Saor
    global img_saor
    img_saor = Image.open("images\\saorebw.png")
    img_saor = ImageTk.PhotoImage(img_saor)
    cor_saor = "red"
    global saor
    saor = tk.Button(janela,text= '15 besos\n0.2 bps', font=("Arial",13),fg=cor_saor,image = img_saor, compound= "left",command=comprar_saor)
    
    saor_qtd = tk.Label(janela,text= f"{qtd_saor} Saor",font=("Arial",16),bg="white")
    
    global recordtxt
    if recordtxt or recordtxt == 0:
        lbl_record = tk.Label(janela,text=f"O recorde é {recordtxt} Saor's",bg="white",font=("Arial",11))
    else:
        lbl_record = tk.Label(janela,text="",bg="white",font=("Arial",11))
    btn_salvar = tk.Button(janela,text="                    Salvar                    ",font=("Arial",11),command=salvar)
    btn_excluir_save = tk.Button(janela,text="                 Apagar Save                 ",font=("Arial",11),command=excluir_save)

    btn_explodir = tk.Button(text="Explodir o mundo\nPreço:666 besos",fg="red",font=("Arial",13),command=comprar_explodir)
    organizar_widgets()



    timer_btn()
    incrementar_besos()
    janela.mainloop()





iniciar_jogo()