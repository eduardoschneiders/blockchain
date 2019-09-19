#### TODO:
* [ ] Enviar as wallets para o /internal/connect
* [ ] Wallet verificar assinatura
* [ ] Quando receber o blockchain de um minerador, verificar se as transações são validas
* [ ] Amounts não estão sincronizando entre os nodos
* [ ] Criar uma documentação de como usar o sistema
* [ ] Exportar o projeto postman

### install libs:
```
pip3 install PyCryptodome
pip3 install flask
```

### How to start application:
#### Start first server:

```
python3 ./api.py 8001
```
This means server will start at http port 8001

#### Start the other servers:

```
python3 ./api.py 8002 http://localhost:8001
```
This means server will start at http port 8002 and will connect to the server at the same machine on the port 8001

#### Criar as wallets e os novos blocos do blockchain
Importar as collections e as variaveis do postman na pasta /postman do projeto
Rodas as requests


https://medium.com/@gnsrikanth/implementing-asymmetric-encryption-to-secure-your-project-35368049cb5f
`easy_install pycrypto`
pip install PyCryptodome
pip install flask
pip install websocket-client

#Debug
import pdb;pdb.set_trace()
$ n //next line
$ ll //list context
$ c //continue

#Start first server:
$ ./api.py 8001
8001 http port

#Start next servers:
$ ./api.py 8002 http://0.0.0.0:8001
8002 http port
ws://0.0.0.0:8001 node to connect

https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
https://gist.github.com/adamar/a4c573c724f647d7fdcfce5a0f1638d9
https://websockets.readthedocs.io/en/stable/intro.html

#generate private/public key
from Crypto.PublicKey import RSA
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

#create signature
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384


digest = SHA384.new()
digest.update(b"data")

signer = pkcs1_15.new(RSA.import_key(private_key))
sig = signer.sign(digest)

#verify


#generate_key
key = RSA.importKey(private_key)
pkcs1_15.new(key).verify(digest, sig)



TODO:
- add amount to wallet(admin-promotion)
- add transactions thouth a miner


# Requests to api

## Set machine host
$ export HOST=http://localhost:5000


## Get info (Admin)
$ curl -X get $HOST/info/wallets

## Create wallet
$ curl -X POST  \
	-d "username=XPTO" \
	$HOST/wallets

## Create block
 export PRIVATE_KEY="XPTO"
 export PUBLIC_KEY="asdf"

 curl -X POST  \
	-H "Content-Type: Application/Json" \
	-d '
	 	[
	 	  {
	 	  	"private_key": "`$PRIVATE_KEY`",
	 	  	"public_key": "$PUBLIC_KEY",
	 	  	"amount": 4
	 	  }
	 	]
	' \
	$HOST/block
