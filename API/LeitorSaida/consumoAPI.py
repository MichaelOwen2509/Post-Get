import requests





def verificar_livro(rfid_do_livro):
    # A URL onde o seu servidor Flask está rodando.
    # Altere a porta (5000) se o seu servidor estiver usando outra.
    url = 'http://192.168.80.253:5000/api/livros/consultar'

    # Os dados que vamos enviar no formato JSON
    dados_enviados = {
        "rfid": rfid_do_livro
    }

    try:
        # Fazendo a requisição POST para a API
        resposta = requests.post(url, json=dados_enviados)

        # Verifica se o código de status HTTP é 200 (OK)
        if resposta.status_code == 200:
            dados_retornados = resposta.json()
            print(f"Livro: {dados_retornados['nomeLivro']}")
            print(f"Status: {dados_retornados['mensagem']}")

        # Verifica se o código é 404 (Não encontrado)
        elif resposta.status_code == 404:
            print("Erro: Livro não cadastrado no banco de dados.")

        else:
            print(f"Erro inesperado: Status {resposta.status_code}")

    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao servidor. O Flask está rodando?")


