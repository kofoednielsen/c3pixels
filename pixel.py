from PIL import Image
from time import sleep
from random import shuffle
from datetime import datetime
from tqdm import tqdm
from sys import argv
import socket

img = Image.open("new.gif")
prerenders = []
SIZE = (20, 20)

frames = []

duration = img.info["duration"]

for i in tqdm(range(img.n_frames)):
    img.seek(i)
    pic = img.convert("RGB")
    frame = set()
    for x in range(pic.size[0]): for y in range(pic.size[1]): pixel = pic.getpixel((x, y))
            frame.add((x, y, pixel))
    frames.append(frame)

frames.append(frames[0])

for i in range(1, len(frames)):
    prerender = []
    prev_frame = frames[i - 1]
    frame = frames[i]
    changed_pixels = frame - prev_frame
    print(len(changed_pixels))
    for k, blab in enumerate(frame):
        # y = k // img.size[0]
        # x = k % img.size[1]
        x = blab[0]
        y = blab[1]
        pixel = blab[2]
        if pixel == (0, 255, 0):
            pixel = (0, 0, 0)
        color = bytes(pixel).hex()
        prerender.append(f"PX {x} {y} {color}")
    prerenders.append(("\n".join(prerender)).encode())


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((argv[1], 1337))
i = 0
start = datetime.now()

# clear
for x in range(pic.size[0]):
    for y in range(pic.size[1]):
        sock.send(f"PX {x} {y} 000000\n".encode())

while True:
    frame = prerenders[i]
    sock.send(frame + b"\n")
    print("send")
    after = datetime.now()
    if (after - start).microseconds / 1000 > (duration):
        i = (i + 1) % len(prerenders)
        start = datetime.now()
