import tkinter as tk

def mostrar_mensagem():
    # Obter o texto da caixa de texto 
    texto = caixa_texto.get()
    # Atualizar o texto do rótulo com o texto da caixa 
    label_resultado.config(text=texto)

def limpar_campos():
    # Limpar o conteúdo da caixa de texto e do rótulo
    caixa_texto.delete(0, tk.END)
    label_resultado.config(text="")

# Criar a janela principal
janela = tk.Tk()
janela.title("Exemplo de interface")
janela.geometry("400x200")

# Mudar cor de fundo da tela
janela.config(bg="sky blue")

# Criar uma caixa de entrada (Entry)
caixa_texto = tk.Entry(janela, width=60)
caixa_texto.pack(pady=10)

# Criar botões
botao = tk.Button(janela, text="Mostrar Texto", command=mostrar_mensagem, bg="blue", fg="white")
botao.pack(pady=5)

botao_limpar = tk.Button(janela, text="Limpar", command=limpar_campos, bg="red", fg="white")
botao_limpar.pack(pady=5)

# Criar um rótulo para mostrar o resultado
label_resultado = tk.Label(janela, text="", bg="sky blue")
label_resultado.pack(pady=10)

# Executar 
janela.mainloop()
