class MikModule:
    description = "Um módulo de teste"
    options = {
        "lhost": "Endereço do host",
        "lport": "Porta"
    }

    def __init__(self, options):
        self.lhost = options.get("lhost", "127.0.0.1")
        self.lport = options.get("lport", 8080)

    def run(self):
        print(f"[*] Executando TestModule com lhost={self.lhost}, lport={self.lport}")

if __name__ == "__main__":
    options = {
        "lhost": input("Informe o endereço do host: "),
        "lport": input("Informe a porta: ")
    }
    test_module = MikModule(options)
    test_module.run()
