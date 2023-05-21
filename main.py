from HKA_angle import get_HKA_angle
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from PIL import Image, ImageTk
from utils import image_resize
import threading
import cv2
import os

file_name = None
pred_image = None

def save_handler():
    global file_name
    # Allow user to select a directory and store it in global var
    # called folder_path
    filename = asksaveasfilename(initialfile = file_name, defaultextension=".jpg",filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    cv2.imwrite(filename, pred_image)

def HKA_thread():
    x = threading.Thread(target=upload_image)
    x.start()

def upload_image():
    global file_name, pred_image
    file_path = filedialog.askopenfilename(filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")))
    if file_path:
        save_button["state"] = "disabled"
        print("Image selected:", file_path)
        file_name = os.path.basename(file_path)
        # Read the image using OpenCV

        original_image = cv2.imread(file_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        original_image = image_resize(original_image, height=550)
        original_image_pil = Image.fromarray(original_image)
        original_photo = ImageTk.PhotoImage(original_image_pil)
        original_image_label.configure(image=original_photo)
        original_image_label.image = original_photo

        # Calculate HKA
        try:
            image = get_HKA_angle(file_path)
            pred_image = image.copy()
            image_resized = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_resized = image_resize(image_resized, height=550)

            # Convert the image to PIL format
            image_pil = Image.fromarray(image_resized)

            # Create a Tkinter-compatible photo image
            photo = ImageTk.PhotoImage(image_pil)

            # Create a label to display the image
            prediction_image_label.configure(image=photo)
            prediction_image_label.image = photo
            save_button["state"] = "active"
        except Exception as error:
            messagebox.showerror("Something went wrong", str(error))

root = tk.Tk()
root.geometry("1000x600")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
# root.attributes('-fullscreen', True)

root.title("Image Upload Example")

upload_button = tk.Button(root, text="Upload Image", command=HKA_thread, pady=2)
upload_button.grid(row=0, column=0)

save_button = tk.Button(root, text="Save Image", command=save_handler,pady=2)
save_button.grid(row=0, column=1)
save_button["state"] = "disabled"

original_image_label = tk.Label(root)
original_image_label.grid(row=1, column=0,pady=2)

prediction_image_label = tk.Label(root)
prediction_image_label.grid(row=1, column=1,pady=2)



root.mainloop()