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
