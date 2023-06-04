import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import keyword
import matplotlib.pyplot as plt
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from PIL import Image, ImageTk
import time


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.textarea = tk.Text(root)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.linenumbers = tk.Text(root, width=3, padx=5, takefocus=0, border=0, background='lightgray', state=tk.DISABLED)
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
        self.textarea.bind('<Key>', self.update_linenumbers)
        self.create_menu()
        self.create_dom_frame()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar como...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Imprimir", command=self.print_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Buscar", command=self.find_text)
        edit_menu.add_command(label="Reemplazar", command=self.replace_text)
        edit_menu.add_command(label="Ir a línea", command=self.goto_line)
        menubar.add_cascade(label="Editar", menu=edit_menu)

        self.root.config(menu=menubar)

        # Highlight keywords
        self.textarea.tag_configure('keyword', foreground='blue')
        self.textarea.bind('<KeyRelease>', self.highlight_text)

    def create_dom_frame(self):
        self.frame_dom = tk.Frame(self.root)
        self.frame_dom.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def new_file(self):
        self.textarea.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.textarea.delete(1.0, tk.END)
                    self.textarea.insert(tk.END, content)
            except IOError:
                messagebox.showerror("Error", "No se pudo abrir el archivo.")

    def save_file(self):
        content = self.textarea.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(content)
            except IOError:
                messagebox.showerror("Error", "No se pudo guardar el archivo.")

    def save_file_as(self):
        content = self.textarea.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(content)
            except IOError:
                messagebox.showerror("Error", "No se pudo guardar el archivo.")

    def find_text(self):
        # Implementar función de búsqueda de texto
        pass

    def replace_text(self):
        # Implementar función de reemplazo de texto
        pass

    def goto_line(self):
        # Implementar función de ir a línea
        pass

    def update_linenumbers(self, event=None):
        lines = self.textarea.get('1.0', 'end').split('\n')
        line_numbers_text = '\n'.join(str(i) for i in range(1, len(lines) + 1))
        self.linenumbers.config(state=tk.NORMAL)
        self.linenumbers.delete('1.0', tk.END)
        self.linenumbers.insert(tk.END, line_numbers_text)
        self.linenumbers.config(state=tk.DISABLED)

    def highlight_text(self, event=None):
        content = self.textarea.get(1.0, tk.END)
        self.textarea.tag_remove('keyword', '1.0', tk.END)
        for word in keyword.kwlist:
            start_pos = '1.0'
            while True:
                start_pos = self.textarea.search(word, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                self.textarea.tag_add('keyword', start_pos, end_pos)
                start_pos = end_pos

        self.textarea.tag_config('keyword', foreground='blue')

        # Generate and visualize DOM with delay
        try:
            self.frame_dom.after(1500, self.generate_and_show_dom, content)
        except Exception as e:
            print(f'Error generando y visualizando el DOM: {e}')

    def generate_and_show_dom(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        self.show_dom_tree(soup)

    def show_dom_tree(self, soup):
        self.frame_dom.destroy()
        self.create_dom_frame()

        root_node = Node("root")
        self.build_dom_tree(root_node, soup)

        plt.close('all')
        plt.figure(figsize=(5, 5))
        plt.title("DOM Tree")
        plt.axis('off')
        plt.tight_layout()

        DotExporter(root_node, nodeattrfunc=lambda node: 'label="{}"'.format(node.name)).to_picture("dom_tree.png")
        image = Image.open("dom_tree.png")
        image = image.resize((int(image.width * 0.5), int(image.height * 0.5)))  # Reduce size by 20%
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.frame_dom, image=photo)
        label.image = photo
        label.pack()

    def build_dom_tree(self, parent_node, element):
        for child in element.children:
            if child.name:
                child_node = Node(child.name, parent=parent_node)
                self.build_dom_tree(child_node, child)
            else:
                text = child.strip()
                if text:
                    text_node = Node(text, parent=parent_node)

    def print_file(self):
        # Implementar función de impresión de archivo
        pass


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
