import tkinter as tk
from tkinter import filedialog, ttk, HORIZONTAL, LEFT, TOP


import cv2
import numpy as np
from PIL import ImageTk, Image
from imgaug import augmenters as iaa
import atexit
import os
import os.path

from skimage.util import random_noise

root = tk.Tk()
root.title('Vector Median Filter demo')
images = []
images_noise = []


def exit_handler():
    os.remove('./vmf_l.png')
    os.remove('./vmf_r.png')


def addImg():
    panel_l.pack_forget()
    panel_r.pack_forget()
    images.clear()
    images_noise.clear()
    filename = filedialog.askopenfilename(title="Select File")
    images.append(filename)
    save_left(filename)


def add_sp():
    img = cv2.imread("vmf_l.png")
    s_val = w1.get() / 10
    aug = iaa.SaltAndPepper(p=s_val)
    img_arr = aug.augment_image(img)
    cv2.imwrite("vmf_r.png", img_arr)
    images_noise.append(img_arr)
    save_right("vmf_r.png")


def add_sp2():
    img = cv2.imread("vmf_l.png", 0)
    img_arr = random_noise(img, mode='s&p', amount=0.011)
    cv2.imwrite("vmf_r.png", img_arr)
    images_noise.append(img_arr)
    save_right("vmf_r.png")


def add_g():
    img = cv2.imread("vmf_l.png")
    mean = 0
    var = 10
    sigma = w1.get()
    if sigma == 1:
        sigma = 0.5
    elif sigma == 2:
        sigma = 0.75
    elif sigma == 3:
        sigma = 1

    gaussian = np.random.normal(mean, sigma, img.shape)
    gaussian = gaussian.reshape(img.shape[0], img.shape[1], img.shape[2]).astype('uint8')
    noisy_image = cv2.add(img, gaussian)
    cv2.imwrite("vmf_r.png", noisy_image)
    images_noise.append(noisy_image)
    save_right("vmf_r.png")



def runApp():
    win_size = selected_window.get()
    img = cv2.imread("./vmf_l.png")
    median = cv2.medianBlur(img, win_size)
    cv2.imwrite("vmf_r.png", median)
    save_right("vmf_r.png")


def save_left(filename):
    imgf = cv2.imread(filename)
    cv2.imwrite("vmf_l.png", imgf)
    img_photo = ImageTk.PhotoImage(Image.open(filename).resize((400, 400), Image.ANTIALIAS))
    panel_l.pack_forget()
    panel_l.photo = img_photo
    panel_l.configure(image=img_photo)
    panel_l.pack()

def save_right(filename):
    imgf = cv2.imread(filename)
    cv2.imwrite("vmf_r.png", imgf)
    img_photo = ImageTk.PhotoImage(Image.open(filename).resize((400, 400), Image.ANTIALIAS))
    panel_r.pack_forget()
    panel_r.photo = img_photo
    panel_r.configure(image=img_photo)
    panel_r.pack()


def save_left2():
    filename = "vmf_r.png"
    imgf = cv2.imread(filename)
    cv2.imwrite("vmf_l.png", imgf)
    img_photo = ImageTk.PhotoImage(Image.open(filename).resize((400, 400), Image.ANTIALIAS))
    panel_l.pack_forget()
    panel_l.photo = img_photo
    panel_l.configure(image=img_photo)
    panel_l.pack()


def save_right2():
    filename = "vmf_l.png"
    imgf = cv2.imread(filename)
    cv2.imwrite("vmf_r.png", imgf)
    img_photo = ImageTk.PhotoImage(Image.open(filename).resize((400, 400), Image.ANTIALIAS))
    panel_r.pack_forget()
    panel_r.photo = img_photo
    panel_r.configure(image=img_photo)
    panel_r.pack()


def save_img_left():
    im = Image.open('vmf_l.png')
    file = filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=(("PNG file", "*.png"),
                                                                                      ("All Files", "*.*")))
    if file:
        abs_path = os.path.abspath(file.name)
        out = im
        out.save(abs_path)


def save_img_rigth():
    im = Image.open('vmf_r.png')
    file = filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=(("PNG file", "*.png"),
                                                                                  ("All Files", "*.*")))
    if file:
        abs_path = os.path.abspath(file.name)
        out = im
        out.save(abs_path)


def toggle():

    if change_language.config('text')[-1] == 'PL':
        change_language.config(text='ENG')
        openFile.config(text="Wybierz Plik")
        addNoise_sp.config(text="Szum Sól i Pieprz")
        addNoise_g.config(text="Szum Gaussowski")
        l.config(text="Wybierz okno")
        save_l2.config(text="Zapisz Lewy Obraz")
        save_r2.config(text="Zapisz Prawy Obraz")
        title.config(text="Wektorowa Filtracja Medianowa - demonstrator")
    else:
        change_language.config(text='PL')
        openFile.config(text="Open File")
        addNoise_sp.config(text="Salt&Pepper Noise")
        addNoise_g.config(text="Gaussian Noise")
        l.config(text="Select Window")
        save_l2.config(text="Save Left image")
        save_r2.config(text="Save Rigth image")
        title.config(text="Vector Median Filter - demo")


box = tk.Frame(master=root, width=1200, height=400, bg='lightgray')
box2 = tk.Frame(master=root, width=1200, height=15, bg='lightgray')
box3 = tk.Frame(master=root, width=1200, bg='lightgray')
frame = tk.Frame(master=box, width=400, height=400)
frame_l = tk.Frame(master=box, width=400, height=400, bg='lightgray')
frame_r = tk.Frame(master=box, width=400, height=400, bg='lightgray')

frame_1 = tk.Frame(master=frame)
frame_2 = tk.Frame(master=frame)
frame_3 = tk.Frame(master=frame)
frame_4 = tk.Frame(master=frame)

panel_l = tk.Label(frame_l)
panel_r = tk.Label(frame_r)

openFile = tk.Button(master=frame_1, text="Open File", width=12, padx=10, pady=5, fg="white", bg="#263D42",
                     command=addImg)
change_language = tk.Button(master=frame_1, text="PL", width=12, padx=10, pady=5, fg="white", bg="#263D42",
                            command=toggle)
addNoise_sp = tk.Button(master=frame, text="Salt&Pepper", width=30, padx=10, pady=5, fg="white", bg="#263D42",
                        command=add_sp)
addNoise_g = tk.Button(master=frame, text="Gaussian Noise", width=30, padx=10, pady=5, fg="white", bg="#263D42",
                       command=add_g)

w1 = tk.Scale(frame, from_=1, to=3, orient=HORIZONTAL)

l = tk.Label(frame_4, text="Select window")
l.config(font=("Courier", 14))

title = tk.Label(box2, text="Vector Median Filter - demo")
title.config(font=("Courier", 14))

selected_window = tk.IntVar()
windows = (
    ('3', 3),
    ('5', 5),
    ('7', 7)
)

for w in windows:
    r = ttk.Radiobutton(
        frame_2,
        text=w[0],
        value=w[1],
        variable=selected_window
    )
    r.pack(anchor=tk.W, padx=5, pady=5)


runApp = tk.Button(master=frame, text="VMF", width=30, padx=10, pady=5, fg="white", bg="#263D42", command=runApp)

save_l = tk.Button(master=frame, text="<<<", width=30, padx=10, pady=5, fg="white", bg="#263D42", command=save_left2)
save_r = tk.Button(master=frame, text=">>>", width=30, padx=10, pady=5, fg="white", bg="#263D42", command=save_right2)

save_l2 = tk.Button(master=frame_l, text="Save Left image", width=55, padx=10, pady=5, fg="white", bg="#263D42", command=save_img_left)
save_r2 = tk.Button(master=frame_r, text="Save Rigth image", width=55, padx=10, pady=5, fg="white", bg="#263D42", command=save_img_rigth)
#empty = tk.Label(box3, text="", width=10)
# save_imgs = tk.Button(master=frame, text="Save images", width=30, padx=10, pady=5, fg="white", bg="#263D42", command=save_img_r)

box2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
title.pack(fill=tk.BOTH, expand=True)
box.pack(fill=tk.BOTH, expand=True)
#box3.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)
save_l2.pack(side=tk.BOTTOM, fill='x')
#empty.pack(side=tk.LEFT, expand=True)
save_r2.pack(side=tk.BOTTOM, fill='x')
frame_l.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
frame_r.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
frame_1.pack(side=TOP)
openFile.pack(padx=5, pady=5, in_=frame_1, side=LEFT)
change_language.pack(padx=5, pady=5, in_=frame_1, side=LEFT)
addNoise_sp.pack(fill='x', padx=5, pady=5)
addNoise_g.pack(fill='x', padx=5, pady=5)
w1.pack(fill='x', padx=5, pady=5)
frame_3.pack()
frame_4.pack()
l.pack()
frame_2.pack()
runApp.pack(fill='x', pady=5, padx=5)
save_l.pack(fill='x', padx=5)
save_r.pack(fill='x', padx=5, pady=(0, 5))
# save_imgs.pack(fill='x', padx=5, pady=5)

atexit.register(exit_handler)

root.mainloop()
