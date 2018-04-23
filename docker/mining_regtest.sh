#!/usr/bin/bash

btc="docker exec docker_bitcoin_1 bitcoin-cli -regtest -rpcuser=test -rpcpassword=test -rpcconnect=bitcoin -rpcport=18332"
ltc="docker exec docker_litecoin_1 litecoin-cli -regtest -rpcuser=test -rpcpassword=test -rpcconnect=litecoin -rpcport=19332"
dash="docker exec docker_dash_1 dash-cli -regtest -rpcuser=test -rpcpassword=test -rpcconnect=dash -rpcport=19994"

$btc generate 5000
$ltc generate 5000
$dash generate 5000

$btc move "" admin 100
$btc move "" test1 200
$btc move "" test2 300

$ltc move "" admin 200
$ltc move "" test1 300
$ltc move "" test2 400

$dash move "" admin 300
$dash move "" test1 400
$dash move "" test2 500

