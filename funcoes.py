import csv

def registro():
    while True:
        try:
            nome = input("Digite seu nome: ")
            email = input("Digite seu email: ")
            senha = input("Digite sua senha: ")

            with open('users.csv', 'a', newline='') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow([nome, email, senha])

            print("Registro realizado com sucesso!")
            break
        except ValueError:
            pass

def login():
    while True:
        try:
            email = input("Digite seu email: ")
            senha = input("Digite sua senha: ")

            with open('users.csv', 'r') as arquivo:
                reader = csv.reader(arquivo)
                for linha in reader:
                    if linha[1] == email and linha[2] == senha:
                        print("Login realizado com sucesso!")
                        return
                    else:
                        raise ValueError
        except ValueError:
            print("Email ou senha incorretos.")
