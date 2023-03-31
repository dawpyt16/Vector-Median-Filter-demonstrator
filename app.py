import tkinter as tk
from tkinter import filedialog, ttk, HORIZONTAL, LEFT, TOP
import cv2
import numpy as np
from PIL import ImageTk, Image
from imgaug import augmenters as iaa
import atexit
import os
import os.path

root = tk.Tk()
root.title('Vector Median Filter demo')
images = []
images_noise = []


def exit_handler():
    os.remove('./vmf_l.png')
    os.remove('./vmf_r.png')


def addImg():
    panel_left.pack_forget()
    panel_right.pack_forget()
    images.clear()
    images_noise.clear()
    filename = filedialog.askopenfilename(title="Select File")
    images.append(filename)
    save_left(filename)


def add_salt_and_pepper_noise():
    img = cv2.imread("vmf_l.png")
    s_val = scale_frame.get() / 10
    aug = iaa.SaltAndPepper(p=s_val)
    img_arr = aug.augment_image(img)
    cv2.imwrite("vmf_r.png", img_arr)
    images_noise.append(img_arr)
    save_right("vmf_r.png")


def add_gaussian_noise():
    img = cv2.imread("vmf_l.png")
    mean = 0
    sigma = scale_frame.get()
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
    panel_left.pack_forget()
    panel_left.photo = img_photo
    panel_left.configure(image=img_photo)
    panel_left.pack()


def save_right(filename):
    imgf = cv2.imread(filename)
    cv2.imwrite("vmf_r.png", imgf)
    img_photo = ImageTk.PhotoImage(Image.open(filename).resize((400, 400), Image.ANTIALIAS))
    panel_right.pack_forget()
    panel_right.photo = img_photo
    panel_right.configure(image=img_photo)
    panel_right.pack()


def save_image(filename, save_filename, panel):
    imgf = cv2.imread(filename)
    cv2.imwrite(save_filename, imgf)
    img_photo = ImageTk.PhotoImage(Image.open(filename).resize((400, 400), Image.ANTIALIAS))
    panel.pack_forget()
    panel.photo = img_photo
    panel.configure(image=img_photo)
    panel.pack()


def save_left2():
    save_image("vmf_r.png", "vmf_l.png", panel_left)


def save_right2():
    save_image("vmf_l.png", "vmf_r.png", panel_right)


def save_img_left():
    im = Image.open('vmf_l.png')
    file = filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=(("PNG file", "*.png"),
                                                                                  ("All Files", "*.*")))
    if file:
        abs_path = os.path.abspath(file.name)
        out = im
        out.save(abs_path)


def save_img_right():
    im = Image.open('vmf_r.png')
    file = filedialog.asksaveasfile(mode='w', defaultextension=".png", filetypes=(("PNG file", "*.png"),
                                                                                  ("All Files", "*.*")))
    if file:
        abs_path = os.path.abspath(file.name)
        out = im
        out.save(abs_path)


def toggle():
    if change_language_button.config('text')[-1] == 'PL':
        change_language_button.config(text='ENG')
        open_file_button.config(text="Wybierz Plik")
        add_salt_and_pepper_noise_button.config(text="Szum Sól i Pieprz")
        add_gaussian_noise_button.config(text="Szum Gaussowski")
        select_window_label_frame.config(text="Wybierz okno")
        save_left_image_button.config(text="Zapisz Lewy Obraz")
        save_right_image_button.config(text="Zapisz Prawy Obraz")
        title_label.config(text="Wektorowa Filtracja Medianowa - demonstrator")
    else:
        change_language_button.config(text='PL')
        open_file_button.config(text="Open File")
        add_salt_and_pepper_noise_button.config(text="Salt&Pepper Noise")
        add_gaussian_noise_button.config(text="Gaussian Noise")
        select_window_label_frame.config(text="Select Window")
        save_left_image_button.config(text="Save Left image")
        save_right_image_button.config(text="Save Rigth image")
        title_label.config(text="Vector Median Filter - demo")


main_box = tk.Frame(master=root, width=1200, height=400, bg='lightgray')
title_box = tk.Frame(master=root, width=1200, height=15, bg='lightgray')
main_frame = tk.Frame(master=main_box, width=400, height=400)
left_frame = tk.Frame(master=main_box, width=400, height=400, bg='lightgray')
right_frame = tk.Frame(master=main_box, width=400, height=400, bg='lightgray')

frame_1 = tk.Frame(master=main_frame)
frame_2 = tk.Frame(master=main_frame)
frame_3 = tk.Frame(master=main_frame)
frame_4 = tk.Frame(master=main_frame)

panel_left = tk.Label(left_frame)
panel_right = tk.Label(right_frame)

open_file_button = tk.Button(master=frame_1, text="Open File", width=12, padx=10, pady=5, fg="white", bg="#263D42",
                             command=addImg)
change_language_button = tk.Button(master=frame_1, text="PL", width=12, padx=10, pady=5, fg="white", bg="#263D42",
                                   command=toggle)
add_salt_and_pepper_noise_button = tk.Button(master=main_frame, text="Salt&Pepper", width=30, padx=10, pady=5,
                                             fg="white", bg="#263D42",
                                             command=add_salt_and_pepper_noise)
add_gaussian_noise_button = tk.Button(master=main_frame, text="Gaussian Noise", width=30, padx=10, pady=5, fg="white",
                                      bg="#263D42",
                                      command=add_gaussian_noise)

scale_frame = tk.Scale(main_frame, from_=1, to=3, orient=HORIZONTAL)

select_window_label_frame = tk.Label(frame_4, text="Select window")
select_window_label_frame.config(font=("Courier", 14))

title_label = tk.Label(title_box, text="Vector Median Filter - demo")
title_label.config(font=("Courier", 14))

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

runApp = tk.Button(master=main_frame, text="VMF", width=30, padx=10, pady=5, fg="white", bg="#263D42", command=runApp)

save_right_to_left_button = tk.Button(master=main_frame, text="<<<", width=30, padx=10, pady=5, fg="white",
                                      bg="#263D42", command=save_left2)
save_left_to_right_button = tk.Button(master=main_frame, text=">>>", width=30, padx=10, pady=5, fg="white",
                                      bg="#263D42", command=save_right2)

save_left_image_button = tk.Button(master=left_frame, text="Save Left image", width=55, padx=10, pady=5, fg="white",
                                   bg="#263D42", command=save_img_left)
save_right_image_button = tk.Button(master=right_frame, text="Save Rigth image", width=55, padx=10, pady=5, fg="white",
                                    bg="#263D42", command=save_img_right)

title_box.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
title_label.pack(fill=tk.BOTH, expand=True)
main_box.pack(fill=tk.BOTH, expand=True)

save_left_image_button.pack(side=tk.BOTTOM, fill='x')
save_right_image_button.pack(side=tk.BOTTOM, fill='x')

left_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
main_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
right_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
frame_1.pack(side=TOP)
open_file_button.pack(padx=5, pady=5, in_=frame_1, side=LEFT)
change_language_button.pack(padx=5, pady=5, in_=frame_1, side=LEFT)
add_salt_and_pepper_noise_button.pack(fill='x', padx=5, pady=5)
add_gaussian_noise_button.pack(fill='x', padx=5, pady=5)
scale_frame.pack(fill='x', padx=5, pady=5)
frame_3.pack()
frame_4.pack()
select_window_label_frame.pack()
frame_2.pack()
runApp.pack(fill='x', pady=5, padx=5)
save_right_to_left_button.pack(fill='x', padx=5)
save_left_to_right_button.pack(fill='x', padx=5, pady=(0, 5))

atexit.register(exit_handler)

root.mainloop()
