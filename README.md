
# Trabalho de Sistemas distribuidos

## Replicação semi-ativa e NACK

## Instalação

Este trabalho foi desenvolvido usando o Python 3.11 e utilizando as bibliotecas padrões e as que estão referenciadas em requirements.txt

Para fazer a instalação delas basta:
```http
  pip install -r ./requirements.txt
```

## Inicialização

O sistema é composto por 3 arquivos principais: 
- websocket_server.py ->
   Responsavel por controlar o meio de comunicação websocket
- websocket_client.py ->
   Cliente autonomo que fica repetindo a mesma função pedindo por mensagens à ele
- websocket_client_controlled.py ->
   Cliente controlado que envia mensagens como bem entender do usuario

Para inicializar o sistema é necessário iniciar primeiro o websocket_server.py usando:
```http
  python ./websocket_server.py
```

Ao ser inicializado os clientes podem se conectar e começar a se comunicar. Para iniciar um cliente é usado o comando:
```http
  python ./websocket_client.py -g x
```
Onde -g é a flag para usar um grupo predefinido e em x se informa o id grupo fara parte o nodo. Atualmente só temos 3 grupos de ids [1,2,3]. Se a flag nao for explicitada o grupo é aleatorio.

Para testes conseguimos usar um cliente controlado para enviar mensagens à grupos ou nodos especificos.
Para iniciar um cliente controlado é usado o comando:
```http
  python ./websocket_client.py -g x -f
```
Onde -g é a flag para usar um grupo predefinido e em x se informa o id grupo fara parte o nodo. Atualmente só temos 3 grupos de ids [1,2,3]. Se a flag nao for explicitada o grupo é aleatorio.
E -f é a flag caso queiras que este nodo seja um nodo faltoso. Desde modo na hora de confirmar as mensagens recebidas e os asserts com os nodos do grupo perguntará quais mensagens "recebeste"
