import tkinter as tk
import json
from functools import partial


def salvar_provas_em_json():
    with open('json/' +'provas.json', 'w') as arquivo:
        json.dump(provas, arquivo)

def atualizar_lista_provas():
    
    #lista_provas.clear()
    for prova in provas:
        lista_provas.update( {prova["id"]: prova["nome_prova"]} )

    salvar_provas_em_json()
    listar_items()

def listar_items():
    i = 0
    for x,y in lista_provas.items():

        lbl_id_prova = tk.Label(master=frm_provas, text=str(x) + " : ")
        lbl_nome_prova = tk.Label(master=frm_provas, text=y)

        preencher_repostas_arg = partial(onClick_preencher_respostas, x)
        preencher_gabarito_arg = partial(onClick_preencher_gabarito, x)
        apagar_prova_arg = partial(apagar_prova, x)

        #btn_editar_prova = tk.Button(frm_provas, text="Editar")
        btn_gabarito_prova = tk.Button(frm_provas, text="Gabarito", command=preencher_gabarito_arg)
        btn_respostas_prova = tk.Button(frm_provas, text="Respostas", command=preencher_repostas_arg)
        btn_apagar_prova = tk.Button(frm_provas, text="Apagar", command=apagar_prova_arg)

        lbl_id_prova.grid(row=i, column=0, pady=5, padx=5)
        lbl_nome_prova.grid(row=i, column=1, pady=5, padx=5)
        #btn_editar_prova.grid(row=i,column=2, padx=5, pady=5)
        btn_gabarito_prova.grid(row=i,column=3, padx=5, pady=5)
        btn_respostas_prova.grid(row=i,column=4, padx=5, pady=5)
        btn_apagar_prova.grid(row=i,column=5, padx=5, pady=5)

        i = i+1
        

def registrar_nova_prova():
    window_registro = tk.Toplevel(window)
    window_registro.title("Registrar Prova")

    evar = tk.StringVar()
    nvar = tk.IntVar()
    tvar = tk.StringVar()

    lbl_nome_prova = tk.Label(window_registro, text="Nome da Prova:")
    entr_nome_prova = tk.Entry(window_registro, textvariable=evar)
    lbl_n_qts_prova = tk.Label(window_registro, text="Número de Questões:")
    entr_n_qts_prova = tk.Entry(window_registro, textvariable=nvar)
    lbl_tp_qts_prova = tk.Label(window_registro, text="Tipo de Questões:")
    rd1_tp_qts_prova = tk.Radiobutton(window_registro, text="C - E", variable=tvar, value='CE')
    rd2_tp_qts_prova = tk.Radiobutton(window_registro, text="A B C D", variable=tvar, value='ABCD')
    rd3_tp_qts_prova = tk.Radiobutton(window_registro, text="A B C D E", variable=tvar, value='ABCDE')

    lbl_nome_prova.grid(row=0, column=0)
    entr_nome_prova.grid(row=0, column=1)
    lbl_n_qts_prova.grid(row=1, column=0)
    entr_n_qts_prova.grid(row=1, column=1)
    lbl_tp_qts_prova.grid(row=2, column=0)
    rd1_tp_qts_prova.grid(row=2, column=1)
    rd2_tp_qts_prova.grid(row=2, column=2)
    rd3_tp_qts_prova.grid(row=2, column=3)

    """
    global var_nome_prova
    var_nome_prova = entr_nome_prova.get()
    print("registrar prova: " + var_nome_prova)
    print("registrar prova entr: " + entr_nome_prova.get())
    """

    def salvar_prova():

        #global var_nome_prova
        #nome_prova = var_nome_prova
        nome_prova = entr_nome_prova.get()
        n_qts_prova = entr_n_qts_prova.get()
        tp_qst_prova = tvar.get()
        gabarito = nome_prova + "_gabarito.json"
        respostas = nome_prova + "_respostas.json"

        prova = {
            "id": len(provas) + 1,
            "nome_prova": nome_prova,
            "numero_questoes": n_qts_prova,
            "tipo_questoes": tp_qst_prova,
            "gabarito": gabarito,
            "respostas": respostas
        }

        provas.append(prova)
        salvar_provas_em_json()


        atualizar_lista_provas()
        """
        for p in provas:
            print(p)
        """
        window_registro.destroy()

    btn_criar_prova = tk.Button(window_registro, text="Criar Prova", command=salvar_prova)
    btn_criar_prova.grid(row=3, column=0, padx=5, pady=5)


    window_registro.wait_window()
    return(evar)

def onClick_registrar():
    registrar_nova_prova()

def onClick_preencher_respostas(id):
    preencher_repostas(id)

def onClick_preencher_gabarito(id):
    preencher_gabarito(id)

def editar_prova(id):
    
    window_editar = tk.Toplevel(window)
    window_editar.title("Editar Prova" + id)

    evar = tk.StringVar()

    lbl_nome_prova = tk.Label(window_editar, text="Nome da Prova:")
    entr_nome_prova = tk.Entry(window_editar, textvariable=evar)

    lbl_nome_prova.grid(row=0, column=0)
    entr_nome_prova.grid(row=0, column=1)

    #TODO

def apagar_prova(id):

    indice_prova = -1
    for p in provas:
        if p["id"] == id:
            indice_prova = provas.index(p)
    
    if indice_prova == -1:
        raise Exception("Problemas para localizar a folha de respostas") 

    def confirma_apagar():
        provas.pop(indice_prova)
        #lista_provas.pop(id)
        lista_provas.pop(indice_prova)
        atualizar_lista_provas()
        window_apagar.destroy()

    window_apagar = tk.Toplevel(window)
    window_apagar.title("Apagar prova")
    frm_texto = tk.Frame(window_apagar)
    frm_botoes = tk.Frame(window_apagar)

    nome_prova = provas[indice_prova]["nome_prova"]
    id_prova = provas[indice_prova]["id"]

    lbl_confirmacao = tk.Label(frm_texto, text="Tem Certeza que deseja apagar:")
    lbl_id_nome_prova = tk.Label(frm_texto, text=str(id_prova) + ": " +nome_prova)

    btn_confirma = tk.Button(frm_botoes, text="Sim", command=confirma_apagar)
    btn_cancela = tk.Button(frm_botoes, text="Cancelar", command=window_apagar.destroy)

    frm_texto.pack(padx=10, pady=10)
    frm_botoes.pack(padx=10, pady=10)

    lbl_confirmacao.pack()
    lbl_id_nome_prova.pack()

    btn_confirma.grid(row=0, column=0)
    btn_cancela.grid(row=0, column=1)



def preencher_repostas(id):

    window_respostas = tk.Toplevel()
    window_respostas.title("Folha de respostas")

    respostas_usuario = []

    window_respostas.rowconfigure(0, minsize=100, weight=1)
    window_respostas.columnconfigure(1, minsize=800, weight=1)

    indice_prova = -1
    for p in provas:
        if p["id"] == id:
            indice_prova = provas.index(p)
    
    if indice_prova == -1:
        raise Exception("Problemas para localizar a folha de respostas") 

    #n_questoes = int(provas[id-1]["numero_questoes"])
    #nome_prova = provas[id-1]["nome_prova"]
    n_questoes = int(provas[indice_prova]["numero_questoes"])
    nome_prova = provas[indice_prova]["nome_prova"]
    tipo_questoes = provas[indice_prova]["tipo_questoes"]

    frm_form = tk.Frame(window_respostas, bd=3)
    frm_ttl = tk.Frame(frm_form, bd=3)
    canvas = tk.Canvas(frm_form)
    scrl_v = tk.Scrollbar(frm_form, orient="vertical", command=canvas.yview)
    frm_qsts = tk.Frame(canvas)
    frm_corr = tk.Frame(frm_form)

    frm_form.pack(fill="both", expand=1)
    frm_ttl.pack()
    canvas.pack(side="left", fill="both", expand=1)
    frm_corr.pack()

    lbl_titulo = tk.Label(
        master=frm_ttl, 
        text="Folha de Respostas - "+nome_prova,
        )

    lbl_titulo.pack(padx=20, pady=20)



    scrl_v.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrl_v.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0,0), window=frm_qsts, anchor="nw")

    # Questões da folha de respostas:
    alternativas_respostas = {}
    try:
        with open("json/" + provas[indice_prova]["respostas"] ,"r") as arquivo:
            alternativas_respostas = json.load(arquivo)
    except FileNotFoundError:
        print("Folha de Respostas não encontrada")
    if(tipo_questoes == 'CE'):
        for i in range(n_questoes):
            lbl_questao = tk.Label(master=frm_qsts, text="Q " + str(i + 1) + ":")

            resposta_var = tk.StringVar()
            def limpa_selecao():
                resposta_var.set("")
            RC1 = tk.Radiobutton(master=frm_qsts, text="C", variable=resposta_var, value='C')
            RE1 = tk.Radiobutton(master=frm_qsts, text="E", variable=resposta_var, value='E')
            Radio_Branco = tk.Radiobutton(master=frm_qsts, text="Branco", variable=resposta_var, value='')

            indice_alt = i + 1
            alt_atual = ""
            alt_atual = alternativas_respostas.get(str(indice_alt))
            if alt_atual != "":
                resposta_var.set(alt_atual)

            lbl_questao.grid(row=i, column=0, pady=5)
            RC1.grid(row=i, column=1, pady=5)
            RE1.grid(row=i, column=2, pady=5)
            Radio_Branco.grid(row=i, column=3, pady=5)

            #lbl_correto.grid(row=i, column=3, pady=15)
            #lbl_errado.grid(row=i, column=4, pady=15)

            respostas_usuario.append(resposta_var)
            #respostas_usuario.append(resposta_var.get())
            #print(resposta_var)
    elif(tipo_questoes == 'ABCD'):
        for i in range(n_questoes):
            lbl_questao = tk.Label(master=frm_qsts, text="Q " + str(i + 1) + ":")

            resposta_var = tk.StringVar()
            RA1 = tk.Radiobutton(master=frm_qsts, text="A", variable=resposta_var, value='A')
            RB1 = tk.Radiobutton(master=frm_qsts, text="B", variable=resposta_var, value='B')
            RC1 = tk.Radiobutton(master=frm_qsts, text="C", variable=resposta_var, value='C')
            RD1 = tk.Radiobutton(master=frm_qsts, text="D", variable=resposta_var, value='D')

            indice_alt = i + 1
            alt_atual = ""
            alt_atual = alternativas_respostas.get(str(indice_alt))
            if alt_atual != "":
                resposta_var.set(alt_atual)

            lbl_questao.grid(row=i, column=0, pady=5)
            RA1.grid(row=i, column=1, pady=5)
            RB1.grid(row=i, column=2, pady=5)
            RC1.grid(row=i, column=3, pady=5)
            RD1.grid(row=i, column=4, pady=5)

            #lbl_correto.grid(row=i, column=3, pady=15)
            #lbl_errado.grid(row=i, column=4, pady=15)

            respostas_usuario.append(resposta_var)
            #respostas_usuario.append(resposta_var.get())
            #print(resposta_var)
    elif(tipo_questoes == 'ABCDE'):
        for i in range(n_questoes):
            lbl_questao = tk.Label(master=frm_qsts, text="Q " + str(i + 1) + ":")

            resposta_var = tk.StringVar()
            RA1 = tk.Radiobutton(master=frm_qsts, text="A", variable=resposta_var, value='A')
            RB1 = tk.Radiobutton(master=frm_qsts, text="B", variable=resposta_var, value='B')
            RC1 = tk.Radiobutton(master=frm_qsts, text="C", variable=resposta_var, value='C')
            RD1 = tk.Radiobutton(master=frm_qsts, text="D", variable=resposta_var, value='D')
            RE1 = tk.Radiobutton(master=frm_qsts, text="E", variable=resposta_var, value='E')

            indice_alt = i + 1
            alt_atual = ""
            alt_atual = alternativas_respostas.get(str(indice_alt))
            if alt_atual != "":
                resposta_var.set(alt_atual)

            lbl_questao.grid(row=i, column=0, pady=5)
            RA1.grid(row=i, column=1, pady=5)
            RB1.grid(row=i, column=2, pady=5)
            RC1.grid(row=i, column=3, pady=5)
            RD1.grid(row=i, column=4, pady=5)
            RE1.grid(row=i, column=5, pady=5)

            #lbl_correto.grid(row=i, column=3, pady=15)
            #lbl_errado.grid(row=i, column=4, pady=15)

            respostas_usuario.append(resposta_var)
            #respostas_usuario.append(resposta_var.get())
            #print(resposta_var)
        else:
            print("Problemas no Tipo de Questões")

    
    #print(respostas_usuario)
    
    def salvar_respostas():
        respostas = {}
        for i in range(n_questoes):
            questao = i + 1
            resposta = respostas_usuario[i].get()
            #resposta = respostas_usuario[i]
            #print("Q: ")
            #print(resposta)
            respostas[questao] = resposta
            respostas.update( {questao: resposta} )
        with open( "json/" + nome_prova + "_respostas" + '.json', 'w') as arquivo:
            json.dump(respostas, arquivo)
        
        lbl_confirmacao.config(text='Respostas salvas com sucesso"')

    def corrigir_prova():

        #Pegar respostas atuais
        salvar_respostas()
        
        alternativas_respostas = {}
        try:
            with open("json/" + provas[indice_prova]["respostas"] ,"r") as arquivo:
                alternativas_respostas = json.load(arquivo)
        except FileNotFoundError:
            print("Folha de Respostas não encontrada")

        alternativas_gabarito = {}
        try:
            with open("json/" + provas[indice_prova]["gabarito"] ,"r") as arquivo:
                alternativas_gabarito = json.load(arquivo)
        except FileNotFoundError:
            print("Gabarito não encontrado")

        n_corretas = 0
        n_erradas = 0
        n_anuladas = 0
        n_branco = 0
        for i in range(n_questoes):

            indice_correcao = i + 1
            alt_resp = alternativas_respostas.get(str(indice_correcao))
            alt_gab = alternativas_gabarito.get(str(indice_correcao))

            lbl_correto = tk.Label(frm_qsts, text="\u2705")
            lbl_errado = tk.Label(frm_qsts, text="\u274C")
            lbl_anulado = tk.Label(frm_qsts, text="\u26D4")
            lbl_branco = tk.Label(frm_qsts, text="\u25A1")

            if alt_gab != "C" and alt_gab != "E" and alt_gab != "A" and alt_gab != "B" and alt_gab != "D" and alt_gab != "X":
                print("Preencha o gabarito todo antes de corrigir a prova!")
                break
            
            if alt_resp == alt_gab :
                n_corretas += 1
                lbl_correto.grid(row=i, column=3, pady=15)
                lbl_errado.grid_forget()
                lbl_anulado.grid_forget()
                lbl_branco.grid_forget()
                #print("Q" + str(indice_correcao) + "Correto")
            elif alt_gab == "X":
                n_anuladas += 1
                lbl_anulado.grid(row=i, column=3, pady=15)
                lbl_correto.grid_forget()
                lbl_errado.grid_forget()
                lbl_branco.grid_forget()
            elif alt_resp == "":
                n_branco += 1
                lbl_branco.grid(row=i, column=3, pady=15)
                lbl_correto.grid_forget()
                lbl_anulado.grid_forget()
                lbl_errado.grid_forget()
            else:
                n_erradas += 1
                lbl_errado.grid(row=i, column=3, pady=15)
                lbl_correto.grid_forget()
                lbl_anulado.grid_forget()
                lbl_branco.grid_forget()
                #print("Q" + str(indice_correcao) + "Errado")

        lbl_confirmacao.config(text='Respostas corrigidas com sucesso"')
        lbl_resultado_certo = tk.Label(frm_corr, text= str(n_corretas) + " \u2705 repostas corretas")
        lbl_resultado_errado = tk.Label(frm_corr, text= str(n_erradas) + " \u274C repostas erradas")
        lbl_resultado_anulado = tk.Label(frm_corr, text= str(n_anuladas) + " \u26D4 questões anuladas")
        lbl_resultado_branco = tk.Label(frm_corr, text= str(n_branco) + " \u25A1 questões em branco")


        lbl_resultado_certo.pack()
        lbl_resultado_errado.pack()
        lbl_resultado_anulado.pack()
        lbl_resultado_branco.pack()


    btn_salvar = tk.Button(window_respostas, text="Salvar Respostas", command=salvar_respostas)
    btn_salvar.pack()

    btn_corrigir = tk.Button(window_respostas, text="Corrigir Prova", command=corrigir_prova)
    btn_corrigir.pack(pady=10)

    lbl_confirmacao = tk.Label(window_respostas, text="")
    lbl_confirmacao.pack()

    window_respostas.wait_window()
    #window_respostas.mainloop()

def preencher_gabarito(id):

    window_gabarito = tk.Toplevel()
    window_gabarito.title("Folha de gabarito")

    respostas_usuario = []

    window_gabarito.rowconfigure(0, minsize=100, weight=1)
    window_gabarito.columnconfigure(1, minsize=800, weight=1)

    indice_prova = -1
    for p in provas:
        if p["id"] == id:
            indice_prova = provas.index(p)
    
    if indice_prova == -1:
        raise Exception("Problemas para localizar o gabarito") 

    n_questoes = int(provas[indice_prova]["numero_questoes"])
    nome_prova = provas[indice_prova]["nome_prova"]
    #print("id: " + str(id-1) + " " + nome_prova)
    tipo_questoes = provas[indice_prova]["tipo_questoes"]

    frm_form = tk.Frame(window_gabarito, bd=3)
    frm_ttl = tk.Frame(frm_form, bd=3)
    canvas = tk.Canvas(frm_form)
    scrl_v = tk.Scrollbar(frm_form, orient="vertical", command=canvas.yview)
    frm_qsts = tk.Frame(canvas)

    frm_form.pack(fill="both", expand=1)
    frm_ttl.pack()
    canvas.pack(side="left", fill="both", expand=1)

    lbl_titulo = tk.Label(
        master=frm_ttl, 
        text="Folha de Gabarito - "+nome_prova,
        )

    lbl_titulo.pack(padx=20, pady=20)

    scrl_v.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrl_v.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0,0), window=frm_qsts, anchor="nw")

    # Questões do gabarito:
    alternativas_gabarito = {}
    try:
        with open("json/" + provas[indice_prova]["gabarito"] ,"r") as arquivo:
            alternativas_gabarito = json.load(arquivo)
    except FileNotFoundError:
        print("Gabarito não encontrado")

    if(tipo_questoes == "CE"):
        for i in range(n_questoes):
            lbl_questao = tk.Label(master=frm_qsts, text="Q " + str(i + 1) + ":")

            resposta_var = tk.StringVar()
            RC1 = tk.Radiobutton(master=frm_qsts, text="C", variable=resposta_var, value='C')
            RE1 = tk.Radiobutton(master=frm_qsts, text="E", variable=resposta_var, value='E')
            RX1 = tk.Radiobutton(master=frm_qsts, text="Anulada", variable=resposta_var, value='X')

            indice_alt = i + 1
            alt_atual = ""
            alt_atual = alternativas_gabarito.get(str(indice_alt))
            if alt_atual != "":
                resposta_var.set(alt_atual)

            lbl_questao.grid(row=i, column=0, pady=5)
            RC1.grid(row=i, column=1, pady=5)
            RE1.grid(row=i, column=2, pady=5)
            RX1.grid(row=i, column=3, pady=5)

            respostas_usuario.append(resposta_var)
            #respostas_usuario.append(resposta_var.get())
            #print(resposta_var)
    elif(tipo_questoes == "ABCD"):
        for i in range(n_questoes):
            lbl_questao = tk.Label(master=frm_qsts, text="Q " + str(i + 1) + ":")

            resposta_var = tk.StringVar()
            RA1 = tk.Radiobutton(master=frm_qsts, text="A", variable=resposta_var, value='A')
            RB1 = tk.Radiobutton(master=frm_qsts, text="B", variable=resposta_var, value='B')
            RC1 = tk.Radiobutton(master=frm_qsts, text="C", variable=resposta_var, value='C')
            RD1 = tk.Radiobutton(master=frm_qsts, text="D", variable=resposta_var, value='D')
            RX1 = tk.Radiobutton(master=frm_qsts, text="Anulada", variable=resposta_var, value='X')

            indice_alt = i + 1
            alt_atual = ""
            alt_atual = alternativas_gabarito.get(str(indice_alt))
            if alt_atual != "":
                resposta_var.set(alt_atual)

            lbl_questao.grid(row=i, column=0, pady=5)
            RA1.grid(row=i, column=1, pady=5)
            RB1.grid(row=i, column=2, pady=5)
            RC1.grid(row=i, column=3, pady=5)
            RD1.grid(row=i, column=4, pady=5)
            RX1.grid(row=i, column=5, pady=5)

            respostas_usuario.append(resposta_var)
            #respostas_usuario.append(resposta_var.get())
            #print(resposta_var)
    elif(tipo_questoes == "ABCDE"):
        for i in range(n_questoes):
            lbl_questao = tk.Label(master=frm_qsts, text="Q " + str(i + 1) + ":")

            resposta_var = tk.StringVar()
            RA1 = tk.Radiobutton(master=frm_qsts, text="A", variable=resposta_var, value='A')
            RB1 = tk.Radiobutton(master=frm_qsts, text="B", variable=resposta_var, value='B')
            RC1 = tk.Radiobutton(master=frm_qsts, text="C", variable=resposta_var, value='C')
            RD1 = tk.Radiobutton(master=frm_qsts, text="D", variable=resposta_var, value='D')
            RE1 = tk.Radiobutton(master=frm_qsts, text="E", variable=resposta_var, value='E')
            RX1 = tk.Radiobutton(master=frm_qsts, text="Anulada", variable=resposta_var, value='X')

            indice_alt = i + 1
            alt_atual = ""
            alt_atual = alternativas_gabarito.get(str(indice_alt))
            if alt_atual != "":
                resposta_var.set(alt_atual)

            lbl_questao.grid(row=i, column=0, pady=5)
            RA1.grid(row=i, column=1, pady=5)
            RB1.grid(row=i, column=2, pady=5)
            RC1.grid(row=i, column=3, pady=5)
            RD1.grid(row=i, column=4, pady=5)
            RE1.grid(row=i, column=5, pady=5)
            RX1.grid(row=i, column=6, pady=5)

            respostas_usuario.append(resposta_var)
            #respostas_usuario.append(resposta_var.get())
            #print(resposta_var)
    
    #print(respostas_usuario)
    
    def salvar_gabarito():
        respostas_gabarito = {}
        for i in range(n_questoes):
            questao = i + 1
            resposta_gabarito = respostas_usuario[i].get()
            #resposta = respostas_usuario[i]
            #print("Q: ")
            #print(resposta)
            respostas_gabarito[questao] = resposta_gabarito
            respostas_gabarito.update( {questao: resposta_gabarito} )
        with open( "json/" + nome_prova + "_gabarito" + '.json', 'w') as arquivo:
            json.dump(respostas_gabarito, arquivo)
        
        lbl_confirmacao.config(text='Gabarito salvo com sucesso')

        #window_respostas.destroy()

    btn_salvar = tk.Button(window_gabarito, text="Salvar Gabarito", command=salvar_gabarito)
    btn_salvar.pack()

    lbl_confirmacao = tk.Label(window_gabarito, text="")
    lbl_confirmacao.pack()

    window_gabarito.wait_window()

window = tk.Tk()

window.title("Programa de Gabaritos")

window.rowconfigure(0, minsize=100, weight=1)
window.columnconfigure(1, minsize=100, weight=1)

frm_provas = tk.Frame(window)
frm_provas.pack()

provas = []

var_nome_prova = ""
entr_nome_global = tk.Entry(window)

"""
lista_provas = tk.Listbox(window)
lista_provas.pack()
"""
lista_provas = {}
with open("json/" +"provas.json","r") as arquivo:
    provas = json.load(arquivo)

atualizar_lista_provas()
listar_items()

btn_nova_prova = tk.Button(window, text="Nova Prova", command=onClick_registrar, pady=10)
btn_nova_prova.pack()


window.mainloop()