# PacketFabric REST API examples #

## Sending Requests ##

### Using a Session Token & Cookie ###

```
curl -H 'Cookie: session_token=abcdef0123456789abcdef0123456789' \
  https://api.packetfabric.com/interfaces/physical
```

### API Key & Hash ###

API-key requests are made by appending `api_key` and `auth_hash` parameters to the query string.

```
http://api.packetfabric.com/interfaces/physical?api_key=1-0123456789ABCDEF&auth_hash=kr2r6W4SIlje27mk3/+v0cNyr9iVBjRGBcdmQ0+Mc3A=
```

`auth_hash` is computed by taking the HMAC of your secret key and the query string using SHA256.

#### Python ####

```
import urllib
import hashlib
import hmac
import base64

api_key = '1-0123456789ABCDEF'
api_secret_key = '0123456789ABCDEF0123456789ABCDEF'
query_string = 'api_key=' + api_key

hash = hmac.new(api_secret_key, query_string, hashlib.sha256).digest()
hash = base64.b64encode(hash)
hash = urllib.quote_plus(hash)

url = 'https://api.packetfabric.com/interfaces/physical?{}&auth_hash={}'.format(query_string, hash)

# https://api.packetfabric.com/interfaces/physical?api_key=1-0123456789ABCDEF&auth_hash=BmoewII%2FOUyIX%2BjMXhHxLAlTc6XRXLobVVJ9DWUPP3Y%3D
```

#### PHP ####

```
<?php
$api_key = '1-0123456789ABCDEF';
$api_secret_key = '0123456789ABCDEF0123456789ABCDEF';
$query_string = "api_key=$api_key";

$hash = hash_hmac('sha256', $query_string, $api_secret_key, TRUE);
$hash =  base64_encode($hash);
$hash = urlencode($hash);

$url = "https://api.packetfabric.com/interfaces/physical?$query_string&auth_hash=$hash";

// https://api.packetfabric.com/interfaces/physical?api_key=1-0123456789ABCDEF&auth_hash=BmoewII%2FOUyIX%2BjMXhHxLAlTc6XRXLobVVJ9DWUPP3Y%3D
?>
```
