import argparse
import os
import subprocess
import tempfile

PAYLOADS_DIR = "payloads"
PAYLOAD_TEMPLATES = {}

def load_payload_templates():
    if not os.path.exists(PAYLOADS_DIR):
        print(f"O diretório de payloads '{PAYLOADS_DIR}' não encontrado.")
        return {}

    payload_templates = {}
    payload_files = os.listdir(PAYLOADS_DIR)
    for file_name in payload_files:
        if file_name.endswith(".c"):
            template_name = os.path.splitext(file_name)[0]
            payload_templates[template_name] = os.path.join(PAYLOADS_DIR, file_name)
    return payload_templates

PAYLOAD_TEMPLATES = load_payload_templates()

def generate_payload(payload, output_file, **kwargs):
    template_file = PAYLOAD_TEMPLATES.get(payload)
    if not template_file:
        print(f"Arquivo de payload '{payload}' não encontrado.")
        return

    with open(template_file, "r") as file:
        payload_code = file.read()

    # Customize payload code based on additional arguments
    for key, value in kwargs.items():
        payload_code = payload_code.replace("{" + key + "}", str(value))

    with open(output_file, 'w') as f:
        f.write(payload_code)

    print(f"Payload gerado com sucesso: {output_file}")

def compile_payload(payload, output_file, mingw=False):
    compiler = "gcc"
    if mingw:
        compiler = "i686-w64-mingw32-gcc"
        lws = "-lws2_32"
    try:
     compile_command = f"{compiler} -o {output_file}-nous.exe {output_file} {lws}"
    except:
     compile_command = f"{compiler} -o {output_file}-nous.bin {output_file}"
    try:
        subprocess.run(compile_command, shell=True, check=True)
        print(f"Payload compilado com sucesso: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao compilar o payload: {e}")

def list_payloads():
    print("Payloads disponíveis:")
    for payload in PAYLOAD_TEMPLATES:
        print(f"- {payload}")

def main():
    parser = argparse.ArgumentParser(description="Payload Generator")
    parser.add_argument("-p", "--payload", help="Nome do payload", required=True)
    parser.add_argument("-o", "--output", help="Arquivo de saída", required=True)
    parser.add_argument("--host", help="Endereço do host")
    parser.add_argument("--port", type=int, help="Porta")
    parser.add_argument("--mingw", help="Compilar para Windows com Mingw", action="store_true")
    args = parser.parse_args()

    if args.payload not in PAYLOAD_TEMPLATES:
        print("Payload não reconhecido.")
        return

    generate_payload(args.payload, args.output, host=args.host, port=args.port)
    file = args.output + ".c"
    if args.mingw:
        compile_payload(args.payload, args.output, mingw=True)
    else:
        compile_payload(args.payload, args.output)

if __name__ == "__main__":
    main()
