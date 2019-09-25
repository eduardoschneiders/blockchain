
### install libs:
```
pip3 install PyCryptodome
pip3 install flask
python version: Python3
```
Obs.: Some times pip3 fails to install. Then its possible to use easy_install:
`easy_install pycryptodome`

### How to start application:
#### Start first server:

```
python3 ./api.py 8001
```
This means server will start at HTTP port 8001

#### Start the other servers:

```
python3 ./api.py 8002 http://localhost:8001
```
This means server will start at HTTP port 8002 and will connect to the server at the same machine on the port 8001

#### Create wallets and blockchanig blocks
Import postman collections and variables at folder `/postman` and run the requests

# Encryption example:

## Generate private/public key

```python
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()
```

## Create signature

```python
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384

digest = SHA384.new()
digest.update(b"data")

signer = pkcs1_15.new(RSA.import_key(private_key))
signature = signer.sign(digest)
```

## Verify Signature

```python
key = RSA.importKey(public_key)
pkcs1_15.new(key).verify(digest, signature)
```

# Debug
```
import pdb;pdb.set_trace()
$ n //next line
$ ll //list context
$ c //continue
```


## References

https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
https://gist.github.com/adamar/a4c573c724f647d7fdcfce5a0f1638d9
https://websockets.readthedocs.io/en/stable/intro.html
https://medium.com/@gnsrikanth/implementing-asymmetric-encryption-to-secure-your-project-35368049cb5f