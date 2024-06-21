id_lider = "2"
id_clients = "1234"

mensage_final = [id_client if not id_client == id_lider else None for id_client in id_clients]
mensage_final.remove(None)

print(mensage_final)