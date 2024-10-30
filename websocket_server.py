import tkinter as tk
import asyncio
import websockets
import json
from threading import Thread

# 接続されているクライアントを管理するセット
clients = set()

# WebSocketサーバーの設定
async def websocket_handler(websocket, path):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

# サーバーから全クライアントにデータをブロードキャストする
async def broadcast_data(data):
    if clients:
        await asyncio.gather(*(client.send(data) for client in clients))

# 非同期関数をバックグラウンドで実行するためのヘルパー
def run_asyncio_task(data):
    asyncio.run(broadcast_data(data))

# 送信ボタンを押した時の処理
def on_send_button_click(entries):
    data = {
        "prefecture": entries['prefecture'].get(),
        "city": entries['city'].get(),
        "max_intensity": entries['max_intensity'].get(),
        "latitude": entries['latitude'].get(),
        "longitude": entries['longitude'].get(),
        "time": entries['time'].get()
    }
    
    json_data = json.dumps(data)
    Thread(target=run_asyncio_task, args=(json_data,)).start()
    
    for entry in entries.values():
        entry.delete(0, tk.END)

# WebSocketサーバーをバックグラウンドで開始する関数
def start_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = websockets.serve(websocket_handler, "localhost", 6789)
    loop.run_until_complete(server)
    loop.run_forever()

# GUIの設定
def main():
    Thread(target=start_server, daemon=True).start()

    root = tk.Tk()
    root.title("地震情報入力")

    entries = {}
    tk.Label(root, text="都道府県名:").grid(row=0, column=0)
    entries['prefecture'] = tk.Entry(root)
    entries['prefecture'].grid(row=0, column=1)

    tk.Label(root, text="市名:").grid(row=1, column=0)
    entries['city'] = tk.Entry(root)
    entries['city'].grid(row=1, column=1)

    tk.Label(root, text="最大震度:").grid(row=2, column=0)
    entries['max_intensity'] = tk.Entry(root)
    entries['max_intensity'].grid(row=2, column=1)

    tk.Label(root, text="緯度:").grid(row=3, column=0)
    entries['latitude'] = tk.Entry(root)
    entries['latitude'].grid(row=3, column=1)

    tk.Label(root, text="経度:").grid(row=4, column=0)
    entries['longitude'] = tk.Entry(root)
    entries['longitude'].grid(row=4, column=1)

    tk.Label(root, text="時間:").grid(row=5, column=0)
    entries['time'] = tk.Entry(root)
    entries['time'].grid(row=5, column=1)

    send_button = tk.Button(root, text="送信", command=lambda: on_send_button_click(entries))
    send_button.grid(row=6, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()
