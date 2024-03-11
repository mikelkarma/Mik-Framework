import importlib.util
import os
import readline
import threading
import socket
import subprocess

# Cores para os indicadores
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"

class ModulesManager:
    def __init__(self):
        self.modules = {}
        self.selected_module = None
        self.module_options = {}
        self.background_modules = {}
        
    def load_modules(self):
        # Carrega os módulos disponíveis
        module_files = [f[:-3] for f in os.listdir("modules") if f.endswith(".py") and f != "__init__.py"]
        for module_name in module_files:
            module_path = f"modules.{module_name}"
            try:
                with open(os.path.join("modules", f"{module_name}.py"), "r") as module_file:
                    module_code = compile(module_file.read(), module_name, 'exec')
                    module_globals = {}
                    exec(module_code, module_globals)
                    if 'MikModule' in module_globals:
                        self.modules[module_name] = module_globals['MikModule']
                    else:
                        print(f"{COLOR_RED}[!]{COLOR_RESET} Módulo '{module_name}' não possui a classe 'MikModule'.{COLOR_RESET}")
            except Exception as e:
                print(f"{COLOR_RED}[!]{COLOR_RESET} Falha ao carregar o módulo '{module_name}': {e}{COLOR_RESET}")

    def list_modules(self):
        print(f"{COLOR_GREEN}\n [*] {COLOR_RESET}Modules:{COLOR_RESET}")
        for module_name, module in self.modules.items():
            if hasattr(module, "description"):  # Verifica se o módulo tem um atributo de descrição
                print(f"    {module_name}: {module.description}")
            else:
                print(f"{COLOR_RED}[!]{COLOR_RESET}Módulo '{module_name}' não possui um atributo de descrição.{COLOR_RESET}")

    def select_module(self, module_name):
        if module_name in self.modules:
            self.selected_module = module_name
            self.module_options = {}
            print(f"{COLOR_GREEN}[*]{COLOR_RESET} Módulo '{module_name}' selecionado.{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}[!]{COLOR_RESET} Módulo não encontrado.{COLOR_RESET}")

    def get_module_options(self):
        if self.selected_module:
            module = self.modules[self.selected_module]
            if hasattr(module, "options"):
                return module.options
        return None

    def show_options(self):
        if self.selected_module:
            module_options = self.get_module_options()
            if module_options:
                print(f"{COLOR_GREEN}[*]{COLOR_RESET} Options:{COLOR_RESET}")
                for option, description in module_options.items():
                    value = self.module_options.get(option)
                    if value:
                        print(f"{option} ({value}): {description}")
                    else:
                        print(f"{option}: {description}")
            else:
                print(f"{COLOR_GREEN}[!]{COLOR_RESET} Nenhuma opção definida para este módulo.{COLOR_RESET}")
        else:
            print(f"{COLOR_GREEN}[!]{COLOR_RESET} Nenhum módulo selecionado.{COLOR_RESET}")
            
    def commands(self):
            print("\nComandos disponíveis:")
            print("show modules - Mostra os módulos disponíveis")
            print("use <module_name> - Seleciona um módulo para uso")
            print("show options - Mostra as opções do módulo selecionado")
            print("set <option> <value> - Define uma opção para o módulo selecionado")
            print("run - Executa o módulo selecionado")
            print("back - Retorna ao módulo anterior (se houver)")
            print("background - Coloca o módulo em segundo plano")
            print("jobs - Lista os módulos em segundo plano")
            print("session <module_name> - Entra na sessão do módulo em segundo plano")
            print("help - Exibe essa mensagem de ajuda\n")
 
    def help(self):
        if self.selected_module:
            module = self.modules[self.selected_module]
            if hasattr(module, "description"):
                print(f"{module.description}\n")
            if hasattr(module, "options"):
                print("Opções:")
                for option, description in module.options.items():
                    print(f"  {option}: {description}")
                print()
                self.commands()
            if hasattr(module, "commands"):
                print("Comandos:")
                for command, description in module.commands.items():
                    print(f"  {command}: {description}")
            else:
                print(f"{COLOR_GREEN}[!]{COLOR_RESET} Nenhum comando definido para este módulo.{COLOR_RESET}")
        else:
            self.commands()
    def set_module_option(self, option, value):
        if self.selected_module:
            module = self.modules[self.selected_module]
            if hasattr(module, "options"):
                if option in module.options:
                    self.module_options[option] = value
                else:
                    print(f"{COLOR_RED}[!]{COLOR_RESET} Opção '{option}' inválida para o módulo '{self.selected_module}'.{COLOR_RESET}")
            else:
                print(f"{COLOR_RED}[!]{COLOR_RESET} Módulo '{self.selected_module}' não tem opções definidas.{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}[!]{COLOR_RESET} Nenhum módulo selecionado.{COLOR_RESET}")

    def run_module(self):
     if self.selected_module:
        module = self.modules[self.selected_module]
        if hasattr(module, "run"):
            module_instance = module(self.module_options)
            module_instance.run()
        else:
            print(f"{COLOR_RED}[!]{COLOR_RESET} Módulo '{self.selected_module}' não tem o método 'run' implementado.{COLOR_RESET}")
     else:
        print(f"{COLOR_RED}[!]{COLOR_RESET} Nenhum módulo selecionado.{COLOR_RESET}")

    def background_module(self):
        if self.selected_module:
            module = self.modules.get(self.selected_module)
            if module:
                self.background_modules[self.selected_module] = module
                print(f"{COLOR_GREEN}[+] Módulo '{self.selected_module}' em segundo plano.{COLOR_RESET}")
            else:
                print(f"{COLOR_RED}[!]{COLOR_RESET} Módulo não encontrado.{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}[!]{COLOR_RESET} Nenhum módulo selecionado.{COLOR_RESET}")

    def list_background_modules(self):
        print(f"{COLOR_CYAN}[*] Background modules:{COLOR_RESET}")
        for module_name in self.background_modules:
            print(module_name)

    def enter_session(self, module_name):
        if module_name in self.background_modules:
            self.selected_module = module_name
            print(f"{COLOR_GREEN}[*] Entrando na sessão do módulo '{module_name}'.{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}[!]{COLOR_RESET} Módulo em segundo plano não encontrado.{COLOR_RESET}")

# Inicializa o gerenciador de módulos
modules_manager = ModulesManager()
history = []  # Variável de histórico para armazenar o último módulo selecionado

# Função para salvar o histórico de comandos
def save_command_history(command):
    histfile = os.path.join(os.path.expanduser("~"), ".mik_history")
    readline.write_history_file(histfile)

# Carrega os módulos disponíveis
modules_manager.load_modules()

def run_module_and_listen():
    while True:
        if modules_manager.selected_module:
            module = modules_manager.modules.get(modules_manager.selected_module)
            if module:
                module.listen()  # Função que escuta a interação do módulo
            else:
                print(f"{COLOR_RED}[!]{COLOR_RESET} Módulo não encontrado.{COLOR_RESET}")
                break
        else:
            print(f"{COLOR_RED}[!]{COLOR_RESET} Nenhum módulo selecionado.{COLOR_RESET}")
            break
            

# Thread para executar o módulo e ouvir sua interação
module_thread = threading.Thread(target=run_module_and_listen)
module_thread.daemon = True
module_thread.start()

# Função para listar os jobs em segundo plano
def list_background_jobs():
    modules_manager.list_background_modules()

while True:
    prompt = f"mik{COLOR_RESET}"
    if modules_manager.selected_module:
        prompt += f"-{modules_manager.selected_module}> "
    else:
        prompt += "> "

    try:
        command = input(prompt)
        save_command_history(command)  # Salva o comando no histórico
    except KeyboardInterrupt:
        continue  # Ignora interrupções de teclado (Ctrl+C)
    except EOFError:
        break  # Sai do loop se o usuário pressionar Ctrl+D (EOF)

    if command.strip() == "exit":
        break  # Sai do loop se o usuário digitar "exit"
    elif not command.strip():
        continue  # Continua o loop se o usuário não digitar nada
    try:
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "show" and args and args[0] == "modules":
            modules_manager.list_modules()
            print("")
        elif cmd == "use" and args:
            module_name = args[0]
            history.append(modules_manager.selected_module)
            modules_manager.select_module(module_name)
        elif cmd == "back":
            if history:
                previous_module = history.pop()
                modules_manager.select_module(previous_module)
            else:
                print(f"{COLOR_RED}[!]{COLOR_RESET} Não há módulos anteriores no histórico.{COLOR_RESET}")
        elif cmd == "show" and args and args[0] == "options":
            modules_manager.show_options()
        elif cmd.startswith("set") and len(args) > 1:
            option = args[0]
            value = args[1]
            modules_manager.set_module_option(option, value)
            if modules_manager.selected_module:
                if option in modules_manager.module_options:
                    print(f"{COLOR_GREEN}[*] Opção '{option}' definida como '{value}'.{COLOR_RESET}")
                else:
                    print(f"{COLOR_RED}[!]{COLOR_RESET} Opção '{option}' inválida para o módulo '{modules_manager.selected_module}'.{COLOR_RESET}")
            else:
                print(f"{COLOR_RED}[!]{COLOR_RESET} Nenhum módulo selecionado.{COLOR_RESET}")
        elif cmd == "run":
            if modules_manager.selected_module:
                modules_manager.run_module()
                continue
            else:
                print(f"{COLOR_RED}[!]{COLOR_RESET} Nenhum módulo selecionado.{COLOR_RESET}")
        elif cmd == "background":
            modules_manager.background_module()
        elif cmd == "jobs":
            list_background_jobs()
        elif cmd == "session" and args:
            session_id = args[0]
            modules_manager.enter_session(session_id)
        elif cmd == "help":
            modules_manager.help()
                    
        else:
            print(f"{COLOR_RED}[!]{COLOR_RESET} Comando inválido. Digite 'help' para obter ajuda.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_RED}[!]{COLOR_RESET} Ocorreu um erro durante a execução do comando: {e}{COLOR_RESET}")

# Aguarda a finalização do módulo antes de encerrar
module_thread.join()
print(f"{COLOR_GREEN}[*] Módulo encerrado.{COLOR_RESET}")
