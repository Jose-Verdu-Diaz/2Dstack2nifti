import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

from utils import Color

def auto_contrast(img):
    clr = Color()

    print(f'{clr.GREY}Min/Max values before auto contrast: {img.min()}/{img.max()}{clr.ENDC}')
    img = img / 255
    update_contrast = lambda x, a, b: (x - a) / (b - a)
    img_cont = update_contrast(img, img.min(), img.max())
    img_cont = np.where(img_cont > 0, img_cont, 0)
    img_cont = np.where(img_cont < 1, img_cont, 1)
    img_cont = np.array(img_cont * 255, dtype=np.uint8)
    print(f'{clr.GREY}Min/Max values after auto contrast:  {img_cont.min()}/{img_cont.max()}{clr.ENDC}')

    return img_cont


def create_coronal(img, vox_mult):
    rows = []
    middle = int(img.shape[1] / 2)
    n = int(1 / vox_mult)
    for i in range(img.shape[2]):
        for j in range(n): rows.insert(0, img[middle, :, i])
    img_new = np.array(rows)
    return img_new


def display_image(img):
    root = tk.Tk()
    img = ImageTk.PhotoImage(image=Image.fromarray(img))
    tk.Label(
        root,
        image=img
    ).pack()
    root.mainloop()