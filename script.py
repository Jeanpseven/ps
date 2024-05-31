import subprocess
import psutil

def listar_processos():
    resultado = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
    linhas = resultado.stdout.splitlines()

    processos = []
    for linha in linhas[2:]:
        dados = linha.split()
        if len(dados) >= 4:
            tipo, endereco_local, endereco_remoto, estado = dados[0], dados[3], dados[4], dados[5]
            processos.append((tipo, endereco_local, endereco_remoto, estado))

    for i, processo in enumerate(processos, 1):
        print(f"{i}: {processo}")

    return processos

def detalhar_processo(pid):
    try:
        processo = psutil.Process(pid)
        print(f"Detalhes do processo {pid}:")
        print(f"Nome: {processo.name()}")
        print(f"Executável: {processo.exe()}")
        print(f"Argumentos: {processo.cmdline()}")
        print(f"Usuário: {processo.username()}")
        print(f"Status: {processo.status()}")
    except psutil.NoSuchProcess:
        print(f"Processo com PID {pid} não encontrado.")

def desligar_processo(pid):
    try:
        processo = psutil.Process(pid)
        processo.terminate()
        processo.wait(timeout=3)
        print(f"Processo {pid} terminado com sucesso.")
    except psutil.NoSuchProcess:
        print(f"Processo com PID {pid} não encontrado.")
    except psutil.TimeoutExpired:
        print(f"Tempo esgotado ao tentar terminar o processo {pid}.")
    except Exception as e:
        print(f"Erro ao tentar terminar o processo {pid}: {e}")

def abrir_porta(porta):
    try:
        subprocess.run(['iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', str(porta), '-j', 'ACCEPT'], check=True)
        subprocess.run(['iptables', '-A', 'INPUT', '-p', 'udp', '--dport', str(porta), '-j', 'ACCEPT'], check=True)
        print(f"Porta {porta} aberta com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao tentar abrir a porta {porta}: {e}")

if __name__ == "__main__":
    processos = listar_processos()

    while True:
        print("\nEscolha uma opção:")
        print("1: Desligar um processo")
        print("2: Detalhar um processo")
        print("3: Abrir uma porta")
        print("4: Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            pid = int(input("Digite o PID do processo a ser desligado: "))
            desligar_processo(pid)
        elif opcao == "2":
            pid = int(input("Digite o PID do processo a ser detalhado: "))
            detalhar_processo(pid)
        elif opcao == "3":
            porta = int(input("Digite a porta a ser aberta: "))
            abrir_porta(porta)
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")
