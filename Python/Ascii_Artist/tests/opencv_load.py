import cv2
import time

start = time.perf_counter()
image = cv2.imread("/home/windy-stairs/Resume/Python/Ascii_Artist/train.jpg", cv2.IMREAD_UNCHANGED)

total = 0
for i in range(100):
    for j in range(100):
        total += 1
        print(image[i,j])
        # print(pixels[i*image.width + j])
end = time.perf_counter()
print(end - start)
print(total)