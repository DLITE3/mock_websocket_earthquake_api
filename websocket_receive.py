import asyncio
import websockets

async def receive_data():
    uri = "ws://localhost:6789"  # サーバーのアドレス
    try:
        async with websockets.connect(uri) as websocket:
            print("サーバーに接続しました。データを待機中...")
            while True:
                # サーバーからのメッセージを受信
                message = await websocket.recv()
                print("受信したデータ:", message)
    except websockets.ConnectionClosed:
        print("サーバーとの接続が切れました")

# asyncioのイベントループで非同期関数を実行
if __name__ == "__main__":
    asyncio.run(receive_data())
