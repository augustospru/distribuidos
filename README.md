
# Trabalho de Sistemas distribuidos

## Replicação semi-ativa e NACK

## Instalação

Este trabalho foi desenvolvido usando o Python 3.11 e utilizando as bibliotecas padrões e as que estão referenciadas em requirements.txt

Para fazer a instalação delas basta:
```
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
  python ./websocket_client_controlled.py -g x -f
```
Onde -g é a flag para usar um grupo predefinido e em x se informa o id grupo fara parte o nodo. Atualmente só temos 3 grupos de ids [1,2,3]. Se a flag nao for explicitada o grupo é aleatorio.
E -f é a flag caso queiras que este nodo seja um nodo faltoso. Desde modo na hora de confirmar as mensagens recebidas e os asserts com os nodos do grupo perguntará quais mensagens "recebeste"

## Funcionamento

De inicio os nodos clientes nao estao linkados à grupos nem possuem um id vinculado ao servidor websocket. Desde modo eles iniciam a comunicação enviando um "Cx" (sendo x um numero ou omitido) pedindo para se conectar. O servidor websocket entao aloca ele ao grupo "x" (random quando omitido) pedido retornando o id da conexão e tambem o perfil que aquele nodo possui.

Em seguida os clientes podem iniciar comunicação entre eles. Para podermos visualizar a comunicação de forma lenta os clientes nao controlados ficam em loop enviando "HP" para receber mensagens. Esse loop acontece de 3 em 3 segundos.

Se o cliente for um nodo de perfil lider e receber uma mensagem de lider ele então replica essas mensagens aos outros membros do grupo.

Se a mensagem enviada for uma com cabeçalho de grupo os nodos do grupo iniciam uma comunicação para enviar mensagens de assert e NACK se houver.

Os clientes controlados podem enviar qualquer mensagem como bem entenderem. E até se forem faltosos podem mentir para enviar mensagens de NACK ao emissor original da mensagem de grupo.

## Estrutura das mensagens

Existem alguns tipos de mensagens que sao aceitas a passar pelo websocket. E todos os tipos de mensagem possuem cabeçalhos e especificidades.

| Cabeçalho   | Função       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `C` | `Conexão` | Se não conectado faz um pedido de conexão com o websocket |
| `M` | `Mensagem direta` | Envia uma mensagem direta a um nodo |
| `G` | `Mensagem em grupo (NACK)` | Envia mensagem utilizando difusão confiavel baseado em NACK |
| `L` | `Mensagem em grupo (semi-ativo)` | Envia mensagem utilizando replicação semi-ativa |
| `H` | `Receber mensagem` | Pede ao canal do websocket se possui mensagens ao nodo |
| `A` | `Assert mensagens` | Acerta mensagens recebidas com os membros do grupo |
| `N` | `NACK` | Envia mensagem de nack ao emissor original para ser reenviadas as mensagens faltantes |
| `S` | `Get servos` | websocket retorna os servos pertencentes a um grupo |

Todas as mensagens são enviadas ao websocket no formato id_cliente + cabeçalho + restante da mensagem. Sendo esse restante da mensagem especifico para cada função do cabeçalho. O id_cliente é acoplado pelo proprio cliente assim se o cliente for controlado só será necessário escrever cabeçalho + restante da mandagem.

## Mensagens com os cabeçalhos

### C

Enviado pelo proprio cliente ao se conectar nao podendo ser enviado novamente.

### M

  XMYZ[...](/?[Z[...]])

  X => id_emissor (acoplado pelo cliente)

  M => identificador da funcao

  Y => id_client que se quer enviar a(s) mensagem(ns)

  Z => id_mensagem (acoplada pelo nodo)

  [...] => corpo da mensagem

  caso queira se enviar mais de uma mensagem o separador '/?' deve ser usado entre uma mensagem e outra

    exemplo:
    caso 1 uma mensagem, nodo deve enviar M21mensagem
    Será uma mensagem de id 1 e corpo "mensagem" para o cliente de id de 2

    caso 2 multiplas mensagens, nodo deve enviar M22mensagem1/?3mensagem2/?4mensagem3
    Serao 3 mensagengs de id 2, 3 e 4 e corpos "mensagem1", "mensagem2", "mensagem3" para o cliente de id de 2

### G

  XGYZ[...](/?[Z[...]])

  X => id_emissor (acoplado pelo cliente)

  G => identificador da funcao

  Y => id_grupo que se quer enviar a(s) mensagem(ns)

  Z => id_mensagem (acoplada pelo nodo)

  [...] => corpo da mensagem

  caso queira se enviar mais de uma mensagem o separador '/?' deve ser usado entre uma mensagem e outra

    exemplo:
    caso 1 uma mensagem, nodo deve enviar G21mensagem
    Será uma mensagem de id 1 e corpo "mensagem" em grupo para o grupo 2

    caso 2 multiplas mensagens, nodo deve enviar G22mensagem1/?3mensagem2/?4mensagem3
    Serao 3 mensagengs de id 2, 3 e 4 e corpos "mensagem1", "mensagem2", "mensagem3" em grupo para o grupo 2
### L
  XLYZ[...](/?[Z[...]])

  X => id_emissor (acoplado pelo cliente)

  L => identificador da funcao

  Y => id_grupo que se quer enviar a(s) mensagem(ns)

  Z => id_mensagem (acoplada pelo nodo)

  [...] => corpo da mensagem

  caso queira se enviar mais de uma mensagem o separador '/?' deve ser usado entre uma mensagem e outra

    exemplo:
    caso 1 uma mensagem, nodo deve enviar L21mensagem
    Será uma mensagem de id 1 e corpo "mensagem" para o lider do grupo de id de 2

    caso 2 multiplas mensagens, nodo deve enviar L22mensagem1/?3mensagem2/?4mensagem3
    Serao 3 mensagengs de id 2, 3 e 4 e corpos "mensagem1", "mensagem2", "mensagem3" para o lider do grupo de id de 2
### H
  XHP

  X => id_emissor (acoplado pelo cliente)

  H => identificador da funcao

  P => quero receber minhas mensagens

    exemplo:
    caso quero receber mensagem que enviaram ao cliente, nodo deve enviar HP
### A
  XAYZB[B...]

  X => id_emissor (acoplado pelo cliente)

  A => identificador da funcao

  Y => id_grupo

  Z => id_emissor_original (acoplado pelo cliente)

  B => ids das mensagens recebidas

    exemplo:
    caso 1 quero informar ao grupo 2 que recebi as mensagens 1, 2 e 3 do emissor 4: A24123
### N
  XNYZ[Z..]

  X => id_emissor (acoplado pelo cliente)

  N => identificador da funcao

  Y => id_emissor_original da mensagem (acoplado pelo cliente)

  Z => id_mensagem perida

    exemplo:
    caso 1 duas mensagens perdidas: 3N116
    Informará ao emissor original de id 1 que as mensagens 1 e 6 nao chegaram ao cliente
### S
  XSY
  X => id_emissor (acoplado pelo cliente)
  S => identificador da funcao
  Y => id_grupo que se quer saber os servos

    exemplo:
    caso 1 um nodo queira saber os servos do grupo 2: 3S2


