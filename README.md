# websocket通信の地震APIを模倣したmock API

## 使い方
まずはapiを起動する
## 使い方
まずはapiを起動する
```sh
# Windowsなら
$ python websocket_server.py
# Linuxなら
$ python3 websocket_server.py
```
次に、受信側を起動する。<br>
※ これはデモ用のコードのため、実際には自分たちが開発している環境に移植する。
```sh
# Windowsなら
$ python websocket_receive.py
# Linuxなら
$ python3 websocket_receive.py
```