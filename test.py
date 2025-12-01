#imports
import cv2
import numpy
import mss
from PIL import Image
import tkinter as tk
import ctypes
import keyboard
import time
import sys

# the list of rectangles that are being drawn
global rects
rects = []

# the function to use the template model
def scan_image(screenshot,template_image,threshold=0.8):

    # the image that is being looked for
    template = cv2.imread(template_image)
    # defining the width and height
    w, h = template.shape[1], template.shape[0]

    # makes the template and screenshot image grayscale (faster for the template matcher)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # OBSOLETE
    # screenshot_edges = cv2.Canny(screenshot_gray, 100, 400)
    # template_edges = cv2.Canny(template_gray, 10, 100)
    
    # this is where the algorithm cv2.TM_CCOEFF_NORMED is used to make a list of detections
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    # using numpy to reduce the list down to any detections above threshold
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

    # adds locations from the locations variables into the rects list.
    rects = [(pt[0], pt[1], w, h) for pt in zip(*locations[::-1])]

    return rects

def sc():
    #mss is the library for taking a screenshot of the screen
    with mss.mss() as sc:
        screenshot = sc.grab(sc.monitors[1])

        # takes the screenshot in RGB (idk if it can do BGR, but if it could than that would be better)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        # converts from RGB to BGR (bgr is what the template matching algorithm uses)
        img_bgr = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
        # saves to screenshot.png so it can be read later
        cv2.imwrite("screenshot.png", img_bgr)
        return img_bgr

def gui(rects):
    # in a try as to not crash the program if it fails
    try:
        # defines the window parent
        root = tk.Tk()
        # makes the window appear on top of all other windows
        root.attributes("-topmost", True)
        # makes the window frameless
        root.overrideredirect(True)
        # defines the size of the window to be the size of the screen
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        # makes it transparent
        root.wm_attributes("-transparentcolor", "white")

        # creates a canvas that we can draw rectangles on
        canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="white", highlightthickness=0)
        canvas.pack()

        # draws rectangles from the rects[] list
        for x, y, w, h in rects:
            canvas.create_rectangle(x, y, x + w, y + h, outline="lime", width=2)

        # uses ctypes to get windows dlls to make the window be able to be clicked through
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        styles = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        # styles | 0x80000 | 0x20 gives transparency (click through transparency)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, styles | 0x80000 | 0x20)

        # WIP----- (trying to make tkinter window close after pressing another button 1-5)
        # while True:
        #     try:
        #         if keyboard.is_pressed()
        # WIP-----

        # after 10 seconds, it destroys itself
        root.after(10000, root.destroy)
        # makes windows not appear with "this window is not responding" windows thing
        root.mainloop()

    except Exception as e:
        print("TK/CTYPES error", e)


while True:
    # this while loop checks if keys are pressed (very WIP and glitchy)
    if keyboard.is_pressed("1"):
        # if 1 is pressed, quits program
        print("run 1")
        sys.exit()
    elif keyboard.is_pressed("2"):
        # if 2 is pressed, scan for all multipes of 2
        rects = []
        print("run 2")
        # scan_image(screenshot, target image, threshold (default 80% certainty))
        # would be much more efficient if I did screenshot = sc() and then rect = += scan_image(screenshot, targets/#.png)
        # just so then it would run a little bit faster
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
        # debounce
        time.sleep(0.3)
    elif keyboard.is_pressed("3"):
        # if 3 is pressed, scan all multiples of 3
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
        # debounce
        time.sleep(0.3)
    elif keyboard.is_pressed("4"):
        # if 4 is pressed, scan for all multiples of 4
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
        # debounce
        time.sleep(0.3)
    elif keyboard.is_pressed("5"):
        # if 5 is pressed, scan for all multiples of 5
        rects = []
        print("run 5")
        rects = rects + scan_image(sc(),"targets/5.png",0.85)
        rects = rects + scan_image(sc(),"targets/10.png",0.85)
        rects = rects + scan_image(sc(),"targets/15.png")
        rects = rects + scan_image(sc(),"targets/20.png")
        rects = rects + scan_image(sc(),"targets/25.png",0.85)
        print(rects)
        gui(rects)
        # debounce
        time.sleep(0.3)
    # prevents while loop from being rate-limited (i don't think i ran into rate limit issues but might as well fix it before it becomes a problem)
    time.sleep(0.05)
