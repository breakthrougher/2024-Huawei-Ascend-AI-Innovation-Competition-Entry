import asyncio
import websockets
import base64
import cv2
import numpy as np

# 打开摄像头
capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
if not capture.isOpened():
    print("Cannot open camera")
    quit()

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]

async def video_stream(websocket, path):
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        
        # 将图像编码为JPEG并转换为base64
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(imgencode)
        img = base64.b64encode(data).decode('utf-8')

        # 发送base64编码的图像
        await websocket.send("data:image/jpeg;base64," + img)
        await asyncio.sleep(0.1)  # 控制帧率

# 启动WebSocket服务器
start_server = websockets.serve(video_stream, "0.0.0.0", 8168)

# 运行服务器
asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server is running on ws://0.0.0.0:8168")
asyncio.get_event_loop().run_forever()

# 释放摄像头资源
capture.release()
