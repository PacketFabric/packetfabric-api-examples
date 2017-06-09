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
