import customtkinter as ctk
from tkcalendar import DateEntry
import sqlite3
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from functools import partial

# ===== Banco de dados =====
conn = sqlite3.connect('financas.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    categoria TEXT NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    data TEXT NOT NULL
)
""")
conn.commit()

# ===== Funções Finanças =====
def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def atualizar_saldo():
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo='Receita'")
    receitas = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo='Despesa'")
    despesas = cursor.fetchone()[0] or 0
    saldo = receitas - despesas
    saldo_label.configure(
        text=f"💰 Saldo Atual: {formatar_valor(saldo)}",
        text_color="green" if saldo >= 0 else "red"
    )
    atualizar_grafico()

def listar_transacoes():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT id, tipo, categoria, descricao, valor, data FROM transacoes ORDER BY id DESC")
    for trans in cursor.fetchall():
        tree.insert("", "end", values=trans)

def adicionar_transacao():
    tipo = tipo_var.get()
    categoria = categoria_var.get()
    descricao = desc_entry.get()
    try:
        valor = float(valor_entry.get().replace(',', '.'))
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido!")
        return
    data = data_entry.get_date().strftime("%d/%m/%Y")
    if not descricao:
        messagebox.showerror("Erro", "Digite a descrição!")
        return
    cursor.execute("INSERT INTO transacoes (tipo, categoria, descricao, valor, data) VALUES (?, ?, ?, ?, ?)",
                   (tipo, categoria, descricao, valor, data))
    conn.commit()
    desc_entry.delete(0, ctk.END)
    valor_entry.delete(0, ctk.END)
    listar_transacoes()
    atualizar_saldo()
    messagebox.showinfo("Sucesso", f"{tipo} adicionada!")

def excluir_transacao():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Erro", "Selecione uma transação!")
        return
    tid = tree.item(selected[0])['values'][0]
    cursor.execute("DELETE FROM transacoes WHERE id=?", (tid,))
    conn.commit()
    listar_transacoes()
    atualizar_saldo()
    messagebox.showinfo("Sucesso", "Transação excluída!")

def atualizar_grafico():
    cursor.execute("SELECT categoria, SUM(valor) FROM transacoes WHERE tipo='Despesa' GROUP BY categoria")
    data = cursor.fetchall()
    categorias = [d[0] for d in data]
    valores = [d[1] for d in data]
    ax.clear()
    if valores:
        ax.pie(
            valores, 
            labels=categorias, 
            autopct="%1.1f%%", 
            startangle=90, 
            textprops={'color':'white' if ctk.get_appearance_mode()=="Dark" else 'black'}
        )
        ax.set_title("Despesas por Categoria", color='white' if ctk.get_appearance_mode()=="Dark" else 'black')
    canvas.draw()

# ===== Alternar tema =====
def alternar_tema():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("light")
        tema_btn.configure(text="🌙 Modo Escuro")
    else:
        ctk.set_appearance_mode("dark")
        tema_btn.configure(text="☀️ Modo Claro")
    atualizar_grafico()

# ===== Calculadora 2.0 =====
class Calculadora(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Display
        self.display = ctk.CTkEntry(
            self, 
            font=("Roboto", 32),
            justify="right",
            height=60,
            width=500,
            corner_radius=15
        )
        self.display.grid(row=0, column=0, columnspan=4, pady=20, sticky="nsew")

        # Layout botões
        botoes = [
            ['C', '⌫', '^', '/'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '+'],
            ['1', '2', '3', '-'],
            ['.', '0', '()', '=']
        ]

        for i, linha in enumerate(botoes):
            for j, texto in enumerate(linha):
                btn = ctk.CTkButton(
                    self, 
                    text=texto, 
                    font=("Roboto", 22, "bold"),
                    width=100, height=70,
                    corner_radius=12,
                    fg_color="#3B82F6" if texto == "=" else "#1E293B",
                    hover_color="#2563EB" if texto == "=" else "#334155",
                    text_color="white",
                    command=partial(self.interpretar, texto)
                )
                btn.grid(row=i+1, column=j, padx=5, pady=5, sticky="nsew")

        # Expandir responsivo
        for i in range(5):
            self.rowconfigure(i+1, weight=1)
        for j in range(4):
            self.columnconfigure(j, weight=1)

    def interpretar(self, valor):
        texto = self.display.get()
        if valor == "C":
            self.display.delete(0, ctk.END)
        elif valor == "⌫":
            self.display.delete(len(texto)-1, ctk.END)
        elif valor == "=":
            self.calcular()
        elif valor == "()":
            if not texto or texto[-1] in "+-/^x":
                self.display.insert(ctk.END, "(")
            else:
                self.display.insert(ctk.END, ")")
        else:
            self.display.insert(ctk.END, valor)

    def calcular(self):
        expr = self.display.get().replace("x", "*").replace("^", "**")
        try:
            self.display.delete(0, ctk.END)
            self.display.insert(0, str(eval(expr)))
        except:
            self.display.delete(0, ctk.END)
            self.display.insert(0, "Erro")

# ===== Interface Principal =====
ctk.set_appearance_mode("dark")  # começa no escuro
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
root.title("App Profissional: Finanças + Calculadora")
root.geometry("1100x650")

notebook = ctk.CTkTabview(root, width=1080)
notebook.pack(fill="both", expand=True, padx=10, pady=10)
notebook.add("Finanças")
notebook.add("Calculadora")

# === Aba Finanças ===
aba_fin = notebook.tab("Finanças")

# Frame superior
frame_top = ctk.CTkFrame(aba_fin)
frame_top.pack(fill="x", padx=20, pady=10)

saldo_label = ctk.CTkLabel(frame_top, text="💰 Saldo Atual: R$ 0,00", font=("Roboto", 28))
saldo_label.pack(side="left", padx=20)

tema_btn = ctk.CTkButton(frame_top, text="☀️ Modo Claro", command=alternar_tema)
tema_btn.pack(side="right", padx=20)

# Frame lateral inputs
frame_inputs = ctk.CTkFrame(aba_fin)
frame_inputs.pack(side="left", fill="y", padx=20, pady=10)

tipo_var = ctk.StringVar(value="Despesa")
categoria_var = ctk.StringVar(value="Alimentação")

ctk.CTkLabel(frame_inputs, text="Tipo:").pack(pady=5)
ctk.CTkOptionMenu(frame_inputs, values=["Receita","Despesa"], variable=tipo_var).pack(pady=5)

ctk.CTkLabel(frame_inputs, text="Categoria:").pack(pady=5)
ctk.CTkOptionMenu(frame_inputs, values=["Alimentação","Transporte","Saúde","Lazer","Outros"], variable=categoria_var).pack(pady=5)

ctk.CTkLabel(frame_inputs, text="Descrição:").pack(pady=5)
desc_entry = ctk.CTkEntry(frame_inputs, width=200)
desc_entry.pack(pady=5)

ctk.CTkLabel(frame_inputs, text="Valor:").pack(pady=5)
valor_entry = ctk.CTkEntry(frame_inputs, width=200)
valor_entry.pack(pady=5)

ctk.CTkLabel(frame_inputs, text="Data:").pack(pady=5)
data_entry = DateEntry(frame_inputs, date_pattern='dd/mm/yyyy')
data_entry.pack(pady=5)

ctk.CTkButton(frame_inputs, text="Adicionar", command=adicionar_transacao).pack(pady=5, fill="x")
ctk.CTkButton(frame_inputs, text="Excluir Selecionado", fg_color="red", command=excluir_transacao).pack(pady=5, fill="x")

# Frame central tabela + gráfico
frame_central = ctk.CTkFrame(aba_fin)
frame_central.pack(side="right", fill="both", expand=True, padx=20, pady=10)

# Treeview histórico
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", background="#2B2B2B", foreground="white", fieldbackground="#2B2B2B")
style.configure("Treeview.Heading", background="#1F1F1F", foreground="white")
tree = ttk.Treeview(frame_central, columns=("ID","Tipo","Categoria","Descrição","Valor","Data"), show="headings")
for col in ("ID","Tipo","Categoria","Descrição","Valor","Data"):
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill="both", expand=True, pady=10)

# Gráfico
fig, ax = plt.subplots(figsize=(4,4), facecolor="#2B2B2B")
ax.patch.set_facecolor('#2B2B2B')
canvas = FigureCanvasTkAgg(fig, master=frame_central)
canvas.get_tk_widget().pack(pady=10)

# === Aba Calculadora ===
aba_calc = notebook.tab("Calculadora")
Calculadora(aba_calc)

# Inicializa
listar_transacoes()
atualizar_saldo()

root.mainloop()
