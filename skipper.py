import cv2
import mouse
import json
from datetime import datetime
from time import sleep
from PIL import ImageGrab
from PIL import ImageOps


THRESHOLD = 0.65

def main():
    cfg = loadConfig()
    maxSpeed = cfg["maxSpeed"]
    while True:
        now = datetime.now().second
        find(cfg)
        now2 = datetime.now().second
        dif = abs(now - now2)
        if dif < maxSpeed:
            sleep(maxSpeed - dif)

def loadConfig():
    f = open("settings.json")
    config = json.load(f)
    return config

def find(config):
    img = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=False, xdisplay=None)
    modImg = ImageOps.grayscale(img)
    modImg.save("screen.png")

    img = cv2.imread('screen.png')
    template = cv2.imread('skip.png')
    temp2 = cv2.imread('skip2.png')
    h, w = template.shape[:2]

    found = None

    for size in config["sizes"]:
        width = int(img.shape[1] * size)
        height = int(img.shape[0] * size)
        dim = (width, height)
        resized = cv2.resize(img, dim)
        r = img.shape[1] / float(resized.shape[1])

        if resized.shape[0] < h or resized.shape[1] < w:
            break

        

        res = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)
        res2 = cv2.matchTemplate(resized, temp2, cv2.TM_CCOEFF_NORMED)

        _, maxVal, _, maxLoc = cv2.minMaxLoc(res)
        _, maxVal2, _, maxLoc2 = cv2.minMaxLoc(res2)

        if maxVal2 > maxVal:
            maxVal, maxLoc = maxVal2, maxLoc2

        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

    maxVal, maxLoc, r = found
    print(maxVal)
    if maxVal > THRESHOLD:            
        startX, startY = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        endX, endY = (int((maxLoc[0] + w) * r), int((maxLoc[1] + h) * r))

        if config["mouseReturn"]:
            old = mouse.get_position()
            mouse.move((startX + endX)/2, (startY+endY)/2)
            mouse.click()
            mouse.move(old[0], old[1])
        else:
            mouse.move((startX + endX)/2, (startY+endY)/2)
            mouse.click()

        cv2.rectangle(img, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.imwrite('result.png', img)

if __name__ == "__main__":
    main()