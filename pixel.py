import socket
import threading
import random
from PIL import Image
im = Image.open(r"c3pixels/img.png")
colors = im.load()
commands = []
for x in range (0,800):
    for y in range (0,200):
        p = colors[x,y]
        if p != (255,255,255,255):
            commands.append(bytes(f'PX {x+200} {y+50} {p[0]:02x}{p[1]:02x}{p[2]:02x}\n', encoding='utf8'))
#print(commands)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("151.217.118.128", 1234))
random.shuffle(commands)
while True:
    package = b''.join(commands)
    sock.send(package)
