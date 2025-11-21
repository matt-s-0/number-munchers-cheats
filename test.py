import cv2
import numpy
import mss
from PIL import Image
import tkinter as tk
import ctypes
import keyboard
import time
import sys

global rects

rects = []

def scan_image(screenshot,template_image,threshold=0.8):

    template = cv2.imread(template_image)

    w, h = template.shape[1], template.shape[0]

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # OBSOLETE
    # screenshot_edges = cv2.Canny(screenshot_gray, 100, 400)
    # template_edges = cv2.Canny(template_gray, 10, 100)
    
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    locations = numpy.where(result >= threshold)

    #debug
    cv2.imwrite("template.png", template)
    cv2.imwrite("debug_screenshot_edges.png", screenshot_gray)
    cv2.imwrite("debug_template_edges.png", template_gray)

    # more debug
    # for pt in zip(*locations[::-1]):
    #     cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    # cv2.imshow("Matches", screenshot)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    rects = [(pt[0], pt[1], w, h) for pt in zip(*locations[::-1])]

    return rects

def sc():
    with mss.mss() as sc:
        screenshot = sc.grab(sc.monitors[1])

        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img_bgr = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)

        cv2.imwrite("screenshot.png", img_bgr)
        return img_bgr

def gui(rects):
    try:
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.overrideredirect(True)
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.wm_attributes("-transparentcolor", "white")

        canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="white", highlightthickness=0)
        canvas.pack()

        for x, y, w, h in rects:
            canvas.create_rectangle(x, y, x + w, y + h, outline="lime", width=2)

        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        styles = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, styles | 0x80000 | 0x20)
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0x00ffffff, 255, 0x2)

        # WIP
        # while True:
        #     try:
        #         if keyboard.is_pressed()

        root.after(10000, root.destroy)
        root.mainloop()

    except Exception as e:
        print("TK/CTYPES error", e)


while True:
    if keyboard.is_pressed("1"):
        print("run 1")
        sys.exit()
    elif keyboard.is_pressed("2"):
        rects = []
        print("run 2")
        rects = rects + scan_image(sc(),"targets/2.png")
        rects = rects + scan_image(sc(),"targets/4.png")
        rects = rects + scan_image(sc(),"targets/6.png")
        rects = rects + scan_image(sc(),"targets/8.png")
        rects = rects + scan_image(sc(),"targets/10.png",0.85)
        rects = rects + scan_image(sc(),"targets/12.png",0.85)
        rects = rects + scan_image(sc(),"targets/14.png",0.85)
        rects = rects + scan_image(sc(),"targets/16.png",0.85)
        rects = rects + scan_image(sc(),"targets/18.png",0.85)
        rects = rects + scan_image(sc(),"targets/20.png")
        rects = rects + scan_image(sc(),"targets/22.png",0.85)
        rects = rects + scan_image(sc(),"targets/24.png",0.85)
        print(rects)
        gui(rects)
        time.sleep(0.3)
    elif keyboard.is_pressed("3"):
        rects = []
        print("run 3")
        rects = rects + scan_image(sc(),"targets/3.png")
        rects = rects + scan_image(sc(),"targets/6.png",0.85)
        rects = rects + scan_image(sc(),"targets/9.png")
        rects = rects + scan_image(sc(),"targets/12.png",0.85)
        rects = rects + scan_image(sc(),"targets/15.png")
        rects = rects + scan_image(sc(),"targets/18.png",0.85)
        rects = rects + scan_image(sc(),"targets/21.png",0.75)
        rects = rects + scan_image(sc(),"targets/24.png",0.85)
        print(rects)
        gui(rects)
        time.sleep(0.3)
    elif keyboard.is_pressed("4"):
        rects = []
        print("run 4")
        rects = rects + scan_image(sc(),"targets/4.png")
        rects = rects + scan_image(sc(),"targets/8.png",0.85)
        rects = rects + scan_image(sc(),"targets/12.png",0.85)
        rects = rects + scan_image(sc(),"targets/16.png",0.85)
        rects = rects + scan_image(sc(),"targets/20.png")
        rects = rects + scan_image(sc(),"targets/24.png",0.85)
        print(rects)
        gui(rects)
        time.sleep(0.3)
    elif keyboard.is_pressed("5"):
        rects = []
        print("run 5")
        rects = rects + scan_image(sc(),"targets/5.png",0.85)
        rects = rects + scan_image(sc(),"targets/10.png",0.85)
        rects = rects + scan_image(sc(),"targets/15.png")
        rects = rects + scan_image(sc(),"targets/20.png")
        rects = rects + scan_image(sc(),"targets/25.png",0.85)
        print(rects)
        gui(rects)
        time.sleep(0.3)
    time.sleep(0.05)