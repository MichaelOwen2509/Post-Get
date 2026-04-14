from smartcard.System import readers
from smartcard.util import toHexString
import consumoAPI
import time  # 👉 Importado para evitar que o loop consuma 100% do CPU

def leituraSendorRfid():
    # Obtém a lista de leitores conectados
    r = readers()
    if len(r) == 0:
        print("Nenhum leitor encontrado.")
        return

    reader = r[0]
    print(f"Aguardando cartão no leitor: {reader}")

    while True:
        try:
            # Tenta conectar ao cartão
            connection = reader.createConnection()
            connection.connect()

            # Comando APDU para obter o UID do cartão (Padrão para ACR122U)
            # CLA: FF, INS: CA, P1: 00, P2: 00, Le: 00
            GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # 👉 Agora em uma linha separada!

            data, sw1, sw2 = connection.transmit(GET_UID)

            # Verifica se a leitura foi bem sucedida (sw1: 90, sw2: 00)
            if sw1 == 0x90 and sw2 == 0x00:
                uid = toHexString(data)
                uid =  uid.replace(" ", "").upper()
                print(f"Cartão Detectado! UID: {uid}")

                consumoAPI.verificar_livro(uid)

                # Aguarda o cartão ser removido para não repetir o log infinitamente
                while True:
                    try:
                        connection.connect()
                        time.sleep(0.5)  # Aguarda meio segundo antes de testar de novo
                    except:
                        print("Cartão removido. Aguardando próximo...")
                        break

        except Exception:
            # O loop continua tentando até encontrar um cartão
            time.sleep(0.5)  # 👉 Pausa para não sobrecarregar o CPU enquanto aguarda


