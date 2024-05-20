import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import threading
import importlib
import sys
import os
from pygments import lex
from pygments.lexers import PythonLexer
import logging
import pygame

class GameObject:
    def __init__(self, name, x=0, y=0, z=0):
        self.name = name
        self.transform = {"x": x, "y": y, "z": z}

    def set_position(self, x, y, z):
        self.transform["x"] = x
        self.transform["y"] = y
        self.transform["z"] = z

    def get_position(self):
        return self.transform["x"], self.transform["y"], self.transform["z"]


class GameEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Game Editor')
        self.geometry('1360x800')

        # Área de texto para edição do código do jogo com rolagem
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(side='left', expand=1, fill='both')

        self.text_editor = tk.Text(self.text_frame, wrap='none')
        self.text_editor.pack(side='left', expand=1, fill='both')

        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_editor.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text_editor['yscrollcommand'] = self.scrollbar.set

        self.setup_tags()

        self.text_editor.bind('<KeyRelease>', self.highlight_syntax)

        # Barra de menus
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Menu Arquivo
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Save', command=self.save_file)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Botões para controlar o jogo
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side='bottom', fill='x')

        self.start_button = tk.Button(self.control_frame, text='Start Game', command=self.start_game)
        self.start_button.pack(side='left', padx=10, pady=5)

        self.reload_button = tk.Button(self.control_frame, text='Reload Game Code', command=self.reload_game_code)
        self.reload_button.pack(side='left', padx=10, pady=5)

        self.quit_button = tk.Button(self.control_frame, text='Quit', command=self.quit)
        self.quit_button.pack(side='right', padx=10, pady=5)

        self.game_thread = None
        self.game_instance = None

        self.file_path = 'MyGame.py'
        self.load_file()

        # Configurar o Pygame
        self.embed_frame = tk.Frame(self, width=600, height=400)
        self.embed_frame.pack(side='right', expand=1, fill='both')

        os.environ['SDL_WINDOWID'] = str(self.embed_frame.winfo_id())
        try:
            pygame.display.init()
            self.screen = pygame.display.set_mode((600, 400))
            pygame.display.update()
        except pygame.error as e:
            messagebox.showerror("Error", f"Pygame initialization error: {e}")

        # Gerenciamento de objetos do jogo
        self.objects_frame = tk.Frame(self)
        self.objects_frame.pack(side='top', fill='both', expand=True)

        self.objects_label = tk.Label(self.objects_frame, text="Game Objects")
        self.objects_label.pack(side='top')

        self.objects_list = tk.Listbox(self.objects_frame, selectmode=tk.SINGLE)
        self.objects_list.pack(side='left', fill='both', expand=True)
        self.objects_list.bind('<<ListboxSelect>>', self.on_object_select)  # Adicionando um evento de seleção

        self.inspector_frame = tk.Frame(self.objects_frame)
        self.inspector_frame.pack(side='left', fill='both', expand=True)

        self.inspector_label = tk.Label(self.inspector_frame, text="Inspector")
        self.inspector_label.pack(side='top')

        self.properties_list = tk.Listbox(self.inspector_frame)
        self.properties_list.pack(side='top', fill='both', expand=True)

        self.add_object_button = tk.Button(self.objects_frame, text="Add Object", command=self.add_object)
        self.add_object_button.pack(side='bottom')

        # Adiciona alguns objetos de teste
        self.add_test_objects()

    def setup_tags(self):
        tamanho = 10
        # Configurar fontes
        comment_font = font.Font(family='Helvetica', size=tamanho, slant='italic', weight='bold')
        keyword_font = font.Font(family='Helvetica', size=tamanho, weight='bold', slant='italic')
        string_font = font.Font(family='Helvetica', size=tamanho, weight='bold', slant='italic')

        # Configurar tags
        self.text_editor.tag_configure('Token.Comment', foreground='grey', font=comment_font)
        self.text_editor.tag_configure('Token.Keyword', foreground='blue', font=keyword_font)
        self.text_editor.tag_configure('Token.String', foreground='green', font=string_font)
        self.text_editor.tag_configure('Token.Number', foreground='purple', font=keyword_font)
        self.text_editor.tag_configure('Token.Operator', foreground='red', font=keyword_font)
        self.text_editor.tag_configure('Token.Function', foreground='darkblue', underline=True)
        self.text_editor.tag_configure('Token.Variable', foreground='darkred', overstrike=True)
        self.text_editor.tag_configure('Token.Name', foreground='purple', font=keyword_font)
        self.text_editor.tag_configure('Token.Keyword.Namespace', foreground='red', font=keyword_font)
        self.text_editor.tag_configure('Token.Keyword.Constant', foreground='red', font=keyword_font)

    def open_file(self):
        try:
            file_path = filedialog.askopenfilename(defaultextension='.py', filetypes=[('Python Files', '*.py')])
            if file_path:
                self.file_path = file_path
                self.load_file()
        except Exception as e:
            messagebox.showerror("Error", f"Error while opening file: {e}")

    def save_file(self):
        try:
            if self.file_path:
                with open(self.file_path, 'w') as file:
                    code = self.text_editor.get('1.0', tk.END)
                    file.write(code)
        except Exception as e:
            messagebox.showerror("Error", f"Error while saving file: {e}")

    def load_file(self):
        try:
            if self.file_path:
                with open(self.file_path, 'r') as file:
                    code = file.read()
                    self.text_editor.delete('1.0', tk.END)
                    self.text_editor.insert('1.0', code)
                self.highlight_syntax()
        except Exception as e:
            messagebox.showerror("Error", f"Error while loading file: {e}")

    def start_game(self):
        try:
            if self.game_thread is None or not self.game_thread.is_alive():
                logging.info("Starting game thread")
                self.game_thread = threading.Thread(target=self.run_game)
                self.game_thread.start()
            else:
                logging.info("Game thread already running")
        except Exception as e:
            messagebox.showerror("Error", f"Error while starting the game: {e}")

    def run_game(self):
        try:
            if 'MyGame' in sys.modules:
                logging.info("Reloading MyGame module")
                importlib.reload(sys.modules['MyGame'])
            else:
                logging.info("Importing MyGame module")
                import MyGame
            logging.info("Running MyGame.main()")
            MyGame.main()
        except Exception as e:
            messagebox.showerror("Error", f"Error while running the game: {e}")

    def reload_game_code(self):
        try:
            if self.game_instance:
                self.save_file()
                importlib.reload(sys.modules['MyGame'])
                messagebox.showinfo('Info', 'Game code reloaded successfully')
        except Exception as e:
            messagebox.showerror("Error", f"Error while reloading game code: {e}")
    
    def quit(self):
        # Aqui você pode adicionar qualquer lógica personalizada que deseja executar antes de sair
        self.destroy()  # Chama o método destroy() para fechar a janela principal
        self.sys.exit()


    def highlight_syntax(self, event=None):
        try:
            code = self.text_editor.get('1.0', tk.END)
            self.text_editor.mark_set('range_start', '1.0')
            data = self.text_editor.get('1.0', 'end-1c')
            for token, content in lex(data, PythonLexer()):
                self.text_editor.mark_set('range_end', 'range_start + %dc' % len(content))
                self.text_editor.tag_add(str(token), 'range_start', 'range_end')
                self.text_editor.mark_set('range_start', 'range_end')
        except Exception as e:
            messagebox.showerror("Error", f"Error while highlighting syntax: {e}")

    def add_object(self):
        try:
            new_object_name = "NewObject"  # Nome padrão para um novo objeto
            self.objects_list.insert(tk.END, new_object_name)
        except Exception as e:
            messagebox.showerror("Error", f"Error while adding object: {e}")

    def on_object_select(self, event):
        try:
            selected_index = self.objects_list.curselection()
            if selected_index:
                index = int(selected_index[0])
                selected_object = self.objects_list.get(index)
                self.update_inspector(selected_object)
        except Exception as e:
            messagebox.showerror("Error", f"Error while selecting object: {e}")

    def update_inspector(self, object_name):
        try:
            # Limpa a lista de propriedades
            self.properties_list.delete(0, tk.END)

            # Procura pelo objeto na lista de objetos
            # Aqui você pode ter uma lista de objetos
            # Ou pode buscar em um dicionário onde a chave é o nome do objeto
            # e o valor é o objeto em si.
            # Por simplicidade, vou supor que você tenha uma lista
            # de objetos onde cada objeto é uma instância da classe GameObject.
            for obj in self.game_objects:
                if obj.name == object_name:
                    # Adiciona as propriedades do objeto à lista de propriedades
                    for prop, val in obj.transform.items():
                        self.properties_list.insert(tk.END, f"{prop}: {val}")
        except Exception as e:
            messagebox.showerror("Error", f"Error while updating inspector: {e}")

    def add_test_objects(self):
        try:
            # Cria alguns objetos de teste
            self.game_objects = [
                GameObject("Cube", x=10, y=20, z=30),
                GameObject("Sphere", x=50, y=60, z=70),
                GameObject("Player", x=100, y=110, z=120)
            ]

            # Adiciona os nomes dos objetos à lista de objetos na interface
            for obj in self.game_objects:
                self.objects_list.insert(tk.END, obj.name)
        except Exception as e:
            messagebox.showerror("Error", f"Error while adding test objects: {e}")

if __name__ == '__main__':
    editor = GameEditor()
    editor.mainloop()

