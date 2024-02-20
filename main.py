import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor

class Janela():
    def __init__(self, master, título, text1, text2):
        self.master = master
        master.title(título)
        master.geometry('640x640')
        self.fonte_nome = 'Arial'
        self.fonte_tamanho = 18
        fonte = (self.fonte_nome, self.fonte_tamanho, 'bold')

        padx_padrao = 15
        pady_padrao = 15

        self.frame = tk.Frame(master, padx=padx_padrao, pady=pady_padrao)
        self.frame.pack(expand=True, fill='both')

        self.label_1 = tk.Label(self.frame, text=text1, font=fonte)
        self.label_1.grid(row=0, column=0, padx=padx_padrao, pady=pady_padrao, sticky='ew')

        self.input_1 = tk.Entry(self.frame)
        self.input_1.grid(row=0, column=1, padx=padx_padrao, pady=pady_padrao, sticky='ew', ipady=self.fonte_tamanho * 0.25)

        self.label_2 = tk.Label(self.frame, text=text2, font=fonte)
        self.label_2.grid(row=1, column=0, padx=padx_padrao, pady=pady_padrao, sticky="ew")

        self.input_2 = tk.Entry(self.frame)
        self.input_2.grid(row=1, column=1, padx=padx_padrao, pady=pady_padrao, sticky='ew', ipady=self.fonte_tamanho * 0.25)

        self.choose_directory_button = tk.Button(self.frame, text="Escolher", command=self.choose_directory,
                                                 font=(self.fonte_nome, int(self.fonte_tamanho * 0.5)))
        self.choose_directory_button.grid(row=1, column=2, padx=padx_padrao, pady=pady_padrao, sticky='ew')

        self.frame.columnconfigure(1, weight=3)

        options = ['.doc', '.docx', '.xls', '.xlsx', '.xlsb', '.xml','.txt']
        options=sorted(options)
        self.listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, font=(self.fonte_nome, int(self.fonte_tamanho * 0.5)),
                                  height=len(options))
        self.listbox.grid(row=2, column=0, columnspan=3, padx=padx_padrao * 15, pady=pady_padrao, sticky='ew')
        for option in options:
            self.listbox.insert(tk.END, option)
            self.listbox.select_set(tk.END)

        self.botao = tk.Button(self.frame, text="Buscar", font=(self.fonte_nome, int(self.fonte_tamanho * 0.5)),
                               command=self.iniciarBusca)
        self.botao.grid(row=3, column=0, columnspan=3, padx=padx_padrao * 15, pady=pady_padrao, sticky='ew')

        self.frame.rowconfigure(4, weight=1) # Verificar como preencher o resto do espaço com ela

        self.input_3 = tk.Text(self.frame, wrap=tk.WORD, height=4,font=(self.fonte_nome, int(self.fonte_tamanho * 0.5)))
        self.input_3.grid(row=4, column=0, columnspan=3, padx=padx_padrao, pady=pady_padrao, sticky='nsew')
        self.input_3.tag_configure("hyperlink", foreground="blue", underline=True)
        self.input_3.tag_bind("hyperlink", "<Button-1>", self.on_hyperlink_click)

    def choose_directory(self):
        directory_path = filedialog.askdirectory()
        self.input_2.delete(0, tk.END)
        self.input_2.insert(0, directory_path)

    def iniciarBusca(self):
        # Function to be executed in parallel
        def search_files(file):
            for item in search_list:
                if item in file:
                    return item,file
                else:
                    return
        
        search_list = set(self.input_1.get().split("; "))
        directory_path = self.input_2.get()
        self.input_3.delete(1.0, tk.END)

        if not search_list or not directory_path:
            messagebox.showinfo("Erro", "Favor, inserir código(s) e caminho antes de buscar.")
            return

        with ThreadPoolExecutor() as executor:
            # Get the results using ThreadPoolExecutor.map
            search_results = executor.map(lambda f: search_files(f), [(file) for _, _, files in os.walk(directory_path) for file in files])

        print(search_results)

        if not search_results:
            self.input_3.delete(1.0, tk.END)
            self.input_3.insert(tk.END, "Nenhum arquivo encontrado para o(s) código(s) listado(s).")
        else:
            for result in search_results:
                    item_localizado, file_path = result
                    self.input_3.insert(tk.END, item_localizado + "\n")
                    self.input_3.insert(tk.END, file_path + "\n\n", "hyperlink")

        
    def get_selected_items(self):
        lista_selecionados=[]
        selected_items = self.listbox.curselection()
        for index in selected_items:
            lista_selecionados.append(self.listbox.get(index))
        return lista_selecionados

    def on_hyperlink_click(self, event):
        index = self.input_3.index(tk.CURRENT)
        file_path = self.input_3.get(index + " linestart", index + " lineend").strip()

        try:
            # Open the file explorer using the appropriate system command
            #subprocess.Popen(['start', '""', file_path], shell=True)
            os.startfile(file_path)
        except Exception as e:
            messagebox.showinfo("Erro", "Erro ao abrir o hyperlink.")

if __name__ == '__main__':
    root = tk.Tk()
    app = Janela(root, 'Localizador de Códigos', 'Código(s)', 'Pasta')
    root.mainloop()
