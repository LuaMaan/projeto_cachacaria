import requests
from deep_translator import GoogleTranslator


def exibir_menu():
    print("\nBem-vindo à cachaçaria do Zé!")
    print("1. Ouvir conselhos")
    print("2. Mostrar conselhos guardados")
    print("3. Traduzir conselhos")
    print("4. Relembrar dicas salvas")
    print("5. Sair")
    return input("Escolha uma opção: ")


def buscar_conselhos(quantidade):
    conselhos = []
    for _ in range(quantidade):
        response = requests.get("https://api.adviceslip.com/advice")
        if response.status_code == 200:
            dados = response.json()
            conselhos.append((dados['slip']['id'], dados['slip']['advice']))
        else:
            print("Erro ao acessar a API.")
    return conselhos


def salvar_conselhos(conselhos, arquivo="conselhos.txt"):
    with open(arquivo, "a") as file:
        for id_, texto in conselhos:
            file.write(f"{id_}: {texto}\n")
    print("Conselhos salvos com sucesso!")


def mostrar_conselhos_guardados(arquivo="conselhos.txt"):
    try:
        with open(arquivo, "r") as file:
            print("\nConselhos guardados:")
            print(file.read())
    except FileNotFoundError:
        print("Nenhum conselho guardado ainda.")


def traduzir_conselho(conselho):
    try:
        tradutor = GoogleTranslator(source="en", target="pt")
        return tradutor.translate(conselho)
    except Exception as e:
        print(f"Erro na tradução: {e}")
        return None


def main():
    while True:
        opcao = exibir_menu()
        
        if opcao == "1":
            quantidade = int(input("Quantos conselhos você deseja? "))
            conselhos = buscar_conselhos(quantidade)
            for id_, texto in conselhos:
                print(f"{id_}: {texto}")
            salvar = input("Deseja salvar esses conselhos? (s/n) ")
            if salvar.lower() == 's':
                salvar_conselhos(conselhos)

        elif opcao == "2":
            mostrar_conselhos_guardados()

        elif opcao == "3":
            conselho = input("Digite o conselho para traduzir: ")
            traducao = traduzir_conselho(conselho)
            if traducao:
                print(f"Tradução: {traducao}")

        elif opcao == "4":
            mostrar_conselhos_guardados()
            traduzir = input("Deseja traduzir os conselhos guardados? (s/n) ")
            if traduzir.lower() == 's':
                with open("conselhos.txt", "r") as file:
                    for linha in file:
                        id_, texto = linha.strip().split(": ", 1)
                        traducao = traduzir_conselho(texto)
                        print(f"{id_}: {traducao}")

        elif opcao == "5":
            print("Saindo... Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()







