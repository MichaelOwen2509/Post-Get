import requests
import platform
import pygame
import time  # 👉 A biblioteca foi adicionada aqui!

pygame.mixer.init()


def disparar_alarme():
    try:
        # Carrega o arquivo de som
        pygame.mixer.music.load("AlarmeDeSaida.mpeg")
        pygame.mixer.music.play()

        # Define quanto tempo o alarme vai tocar (em segundos)
        tempo_de_toque = 2.0
        time.sleep(tempo_de_toque)  # Espera esse tempo passar

        # Para a música à força depois que o tempo passou
        pygame.mixer.music.stop()

    except Exception as e:
        print("Erro ao tentar tocar o áudio:", e)

def verificar_livro(rfid_do_livro):
    url = 'http://192.168.82.73:8000/livros/consultar'
    dados_enviados = {"rfid": rfid_do_livro}

    try:
        # Fazendo a requisição POST para a API
        resposta = requests.post(url, json=dados_enviados)

        # 1. LIVRO ENCONTRADO NO BANCO (Mas precisamos ver se está alugado)
        if resposta.status_code == 200:
            dados_retornados = resposta.json()
            print(f"Livro: {dados_retornados['nomeLivro']}")
            print(f"Status: {dados_retornados['mensagem']}")

            # Se "disponivel" for True, significa que NÃO FOI ALUGADO!
            if dados_retornados.get('disponivel') == True:
                print("🚨 ALARME! TENTATIVA DE SAÍDA COM LIVRO NÃO ALUGADO!")
                disparar_alarme() # 👉 Toca o som!

        # 2. LIVRO NÃO CADASTRADO (Pode ser um livro do acervo sem registro ou etiqueta errada)
        elif resposta.status_code == 404:
            print("🚨 ALARME! ETIQUETA NÃO RECONHECIDA/NÃO CADASTRADA!")
            disparar_alarme() # 👉 Toca o som!

        else:
            print(f"Erro inesperado: Status {resposta.status_code}")

    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao servidor. O Flask está rodando?")