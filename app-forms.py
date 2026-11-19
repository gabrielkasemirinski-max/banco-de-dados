import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


class SistemaCadastroClientes:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Clientes")
        self.root.geometry("450x260")
        self.root.resizable(False, False)

        # Inicializa o banco de dados
        self.criar_banco()

        # Configura a interface gráfica
        self.criar_interface()

    def criar_banco(self):
        """Cria o banco de dados SQLite e a tabela de clientes se não existirem."""
        conexao = sqlite3.connect("clientes.db")
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        """)
        conexao.commit()
        conexao.close()

    def criar_interface(self):
        """Cria e posiciona os elementos visuais do formulário."""
        # Título principal
        lbl_titulo = tk.Label(
            self.root,
            text="Formulário de Cadastro",
            font=("Arial", 14, "bold")
        )
        lbl_titulo.pack(pady=10)

        # Frame para organizar os campos de entrada
        frame_campos = tk.Frame(self.root)
        frame_campos.pack(pady=5, padx=20, fill="x")

        # Campo Nome
        tk.Label(frame_campos, text="Nome:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.entry_nome = tk.Entry(frame_campos, width=42, font=("Arial", 10))
        self.entry_nome.grid(row=0, column=1, pady=5, padx=5)

        # Campo E-mail
        tk.Label(frame_campos, text="E-mail:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.entry_email = tk.Entry(frame_campos, width=42, font=("Arial", 10))
        self.entry_email.grid(row=1, column=1, pady=5, padx=5)

        # Campo Telefone
        tk.Label(frame_campos, text="Telefone:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.entry_telefone = tk.Entry(frame_campos, width=42, font=("Arial", 10))
        self.entry_telefone.grid(row=2, column=1, pady=5, padx=5)

        # Frame para os botões
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=20)

        # Botão Salvar
        btn_salvar = tk.Button(
            frame_botoes,
            text="Salvar Cliente",
            width=14,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.salvar_cliente
        )
        btn_salvar.grid(row=0, column=0, padx=5)

        # Botão Limpar
        btn_limpar = tk.Button(
            frame_botoes,
            text="Limpar",
            width=12,
            bg="#f44336",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.limpar_formulario
        )
        btn_limpar.grid(row=0, column=1, padx=5)

        # Botão Visualizar Clientes (NOVO)
        btn_visualizar = tk.Button(
            frame_botoes,
            text="Visualizar Clientes",
            width=16,
            bg="#2196F3",
            fg="white",
            font=("Arial", 9, "bold"),
            command=self.visualizar_clientes
        )
        btn_visualizar.grid(row=0, column=2, padx=5)

    def salvar_cliente(self):
        """Valida os campos e insere os dados no banco de dados SQLite."""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        if not nome or not email or not telefone:
            messagebox.showwarning(
                "Campos Obrigatórios",
                "Por favor, preencha todos os campos (Nome, E-mail e Telefone)."
            )
            return

        try:
            conexao = sqlite3.connect("clientes.db")
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                (nome, email, telefone)
            )
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.limpar_formulario()

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro no Banco de Dados",
                f"Ocorreu um erro ao salvar os dados: {erro}"
            )

    def limpar_formulario(self):
        """Limpa todos os campos de texto e devolve o foco ao campo Nome."""
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_nome.focus()

    def visualizar_clientes(self):
        """Abre uma nova janela listando todos os clientes cadastrados."""
        try:
            conexao = sqlite3.connect("clientes.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes")
            registros = cursor.fetchall()
            conexao.close()

        except sqlite3.Error as erro:
            messagebox.showerror(
                "Erro no Banco de Dados",
                f"Não foi possível carregar os clientes: {erro}"
            )
            return

        # Cria a janela secundária
        janela_lista = tk.Toplevel(self.root)
        janela_lista.title("Clientes Cadastrados")
        janela_lista.geometry("600x350")
        janela_lista.grab_set()  # Mantém o foco na janela aberta

        lbl_subtitulo = tk.Label(
            janela_lista,
            text="Lista de Clientes Cadastrados",
            font=("Arial", 12, "bold")
        )
        lbl_subtitulo.pack(pady=10)

        # Frame para comportar a tabela e a barra de rolagem
        frame_tabela = tk.Frame(janela_lista)
        frame_tabela.pack(fill="both", expand=True, padx=15, pady=5)

        # Configuração da tabela (Treeview)
        colunas = ("id", "nome", "email", "telefone")
        tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        tabela.heading("id", text="ID")
        tabela.heading("nome", text="Nome")
        tabela.heading("email", text="E-mail")
        tabela.heading("telefone", text="Telefone")

        tabela.column("id", width=50, anchor="center")
        tabela.column("nome", width=180, anchor="w")
        tabela.column("email", width=200, anchor="w")
        tabela.column("telefone", width=120, anchor="center")

        # Barra de rolagem vertical
        scrollbar = ttk.Scrollbar(
            frame_tabela, orient="vertical", command=tabela.yview
        )
        tabela.configure(yscrollcommand=scrollbar.set)

        tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Insere os registros do banco na tabela
        for cliente in registros:
            tabela.insert("", tk.END, values=cliente)

        # Botão para fechar a janela
        btn_fechar = tk.Button(
            janela_lista,
            text="Fechar",
            width=15,
            command=janela_lista.destroy
        )
        btn_fechar.pack(pady=10)


if __name__ == "__main__":
    janela = tk.Tk()
    app = SistemaCadastroClientes(janela)
    janela.mainloop()
