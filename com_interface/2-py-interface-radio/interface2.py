# Usando biblioteca Tkinter (Padrão Python para interfaces)
import tkinter as tk
from tkinter import ttk  # Widgets mais modernos

# Mapeamento de cores em PT -> EN para Tkinter
mapa_cores = {
    "Vermelho": "red",
    "Azul": "blue",
    "Amarelo": "yellow",
    "Preto": "black",
    "Branco": "white"
}

def atualizar_resultado():
    nome = caixa_texto.get()
    preferencia = var_radio.get()

    # Saudação informal
    if var_check_saudacao.get():
        saudacao = "Olá"
    else:
        saudacao = "Bem-vindo"

    # Saudação personalizada
    if var_check_personalizada.get():
        saudacao = f"{saudacao}, caro(a)"

    cor_favorita = combo_cor.get()
    cor_tk = mapa_cores.get(cor_favorita, "black")  # pega a cor em inglês ou preto padrão

    mensagem = f"{saudacao} {nome}! Você prefere {preferencia}."
    if cor_favorita:
        mensagem += f" Sua cor favorita é {cor_favorita}."

    # Atualiza o label uma única vez, sem duplicação
    label_resultado.config(text=mensagem, fg=cor_tk)

def limpar_campos():
    """Função para limpar todos os campos"""
    caixa_texto.delete(0, tk.END)
    var_radio.set("Café")
    var_check_saudacao.set(False)
    var_check_personalizada.set(False)
    combo_cor.set("")
    label_resultado.config(text="", fg="black")  # chama config apenas uma vez

# Criar a janela principal
janela = tk.Tk()
janela.title("Interface avançada")
janela.geometry("400x500")

# Caixa de entrada
label_nome = tk.Label(janela, text="Digite seu nome:")
label_nome.pack(pady=5)
caixa_texto = tk.Entry(janela, width=40)
caixa_texto.pack(pady=5)

# Botões de rádio
label_preferencia = tk.Label(janela, text="Escolha sua preferência:")
label_preferencia.pack(pady=5)

var_radio = tk.StringVar(value="Café")
tk.Radiobutton(janela, text="Café", variable=var_radio, value="Café").pack()
tk.Radiobutton(janela, text="Chá", variable=var_radio, value="Chá").pack()
tk.Radiobutton(janela, text="Suco", variable=var_radio, value="Suco").pack()
tk.Radiobutton(janela, text="Água", variable=var_radio, value="Água").pack()

# Checkboxes
var_check_saudacao = tk.BooleanVar()
tk.Checkbutton(janela, text="Usar saudação informal", variable=var_check_saudacao).pack(pady=5)

var_check_personalizada = tk.BooleanVar()
tk.Checkbutton(janela, text="Usar saudação personalizada", variable=var_check_personalizada).pack(pady=5)

# ComboBox
label_cor = tk.Label(janela, text="Escolha sua cor favorita:")
label_cor.pack(pady=5)
combo_cor = ttk.Combobox(janela, values=["Vermelho", "Azul", "Amarelo", "Preto", "Branco"])
combo_cor.pack(pady=5)

# Botões
botao_atualizar = tk.Button(janela, text="Atualizar", command=atualizar_resultado)
botao_atualizar.pack(pady=10)

botao_limpar = tk.Button(janela, text="Limpar", command=limpar_campos)
botao_limpar.pack(pady=10)

# Resultado final
label_resultado = tk.Label(janela, text="", wraplength=350, justify="center")
label_resultado.pack(pady=20)

# Loop principal
janela.mainloop()
