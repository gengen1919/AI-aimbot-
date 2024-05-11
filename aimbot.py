import cv2
import numpy as np
import win32api
from ultralytics import YOLO
from PIL import Image
from mss import mss
from colorama import Fore
from pyautogui import size
import torch
from termcolor import colored
import sys
import time

class Aimbot:
    Aimbot_status = colored("ENABLED","green")
    def __init__(self,time_delay=0.5,mouse_value=0,toggle_value=0,) -> None:
        global model
        model = YOLO("apex.pt")

        if torch.cuda.is_available:
            print("CUDA:"+Fore.GREEN+"[ENABLED]")
        else:
            print("CUDA:"+Fore.RED+"[DISABLE]")
       
        self.model_conf = 6.0
        self.delay = time_delay
        self.mouse_value = mouse_value
        self.toggle = toggle_value

    def status_aimbot(self):
        if Aimbot.Aimbot_status == colored("ENABLED","green"):
            Aimbot.Aimbot_status = colored("DISABLED","red")
            self.toggle = 0
        else:
            Aimbot.Aimbot_status = colored("ENABLED","green")
            self.toggle = 1
        sys.stdout.write("\033[K")
        print(f"[!] AIMBOT IS [{Aimbot.Aimbot_status}]", end="\r")
        time.sleep(self.delay)

    def target_lock(self,target_X,target_Y):
            win32api.mouse_event(0x01,int(target_X),int(target_Y))
            time.sleep(float(0.01))
            
    def main(self):
        global model
        screen_width,screen_height  = size()
        region_top = (screen_height - 200) // 2
        region_left = (screen_width - 200) // 2
        mon = {'top': region_top, 'left': region_left, 'width': 200, 'height': 200}
        sct = mss()

        while True:
            if win32api.GetAsyncKeyState(0x70) != 0:
                self.status_aimbot()  # トグルの状態を更新
            if win32api.GetAsyncKeyState(0x02) != self.mouse_value:
                if self.toggle > 0:  # トグルが有効な場合のみ実行
                    sct_img = sct.grab(mon)
                    img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
                    img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                    results = model(img_bgr, verbose=False)
                    conf = results[0].boxes.conf.cpu().numpy()
                    boxes = results[0].boxes.xyxy.cpu().numpy()[:, :4]

                    if boxes is not None and len(boxes) > 0:
                        for box, conf_box in zip(boxes, conf):
                            if conf_box > 0.65:
                                x1, y1, x2, y2 = box.astype(int)
                                object_center_x = int((x1 + x2) / 2) + region_left
                                object_center_y = int((y1 + y2) / 2) + region_top
                                dx = object_center_x - screen_width // 2
                                dy = object_center_y - screen_height // 2 
                                self.target_lock(dx, dy)
                else:
                    pass

#if __name__ =="__main__":
    #a = Aimbot()
    #a.main()
