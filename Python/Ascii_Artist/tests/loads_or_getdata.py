from PIL import Image
import numpy as np
import time

start = time.perf_counter()
image = Image.open("/home/windy-stairs/Resume/Python/Ascii_Artist/train.jpg")
pixels = np.asarray(image)
total = 0
for i in range(100):
    for j in range(100):
        total += 1
        print(pixels[i,j])
        # print(image.getpixel((i, j)))
        # print(pixels[i*image.width + j])
end = time.perf_counter()
print(end - start)
print(total)