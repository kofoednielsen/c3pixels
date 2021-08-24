import socket
from time import sleep

text = "pyjam.as"
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from tqdm import tqdm

myfont = ImageFont.truetype("ubuntu.ttf", 16)
size = myfont.getsize(text)


SIZE = (20, 20)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("100.68.0.2", 1337))
i = 0
print(size)
frames = []

for offset in tqdm(list(reversed(list(range(-size[0], SIZE[0]))))):
    prerender = b""
    img = Image.new("RGB", SIZE, "#000005")
    draw = ImageDraw.Draw(img)
    draw.text((offset, -4), text, "yellow", font=myfont)
    frame = set()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = img.getpixel((x, y))
            frame.add((x, y, pixel))
    frames.append(frame)
frames.append(frames[0])

prerenders = []
for i in range(1, len(frames)):
    prerender = []
    prev_frame = frames[i - 1]
    frame = frames[i]
    changed_pixels = frame - prev_frame
    for k, c in enumerate(frame):
        # y = k // img.size[0]
        # x = k % img.size[1]
        x = c[0]
        y = c[1]
        pixel = c[2]
        color = bytes(pixel).hex().upper()
        prerender.append(f"PX {x} {y} {color}")

    prerenders.append(("\n".join(prerender) + '\n').encode())

while True:
    for prerender in prerenders:
        sleep(0.06)
        sock.send(prerender)
        # open("frames", "ab").write(prerender)
