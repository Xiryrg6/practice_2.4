import requests
import threading
from PIL import Image, ImageTk
import io
import tkinter as tk
from tkinter import ttk

url_cat = "https://api.thecatapi.com/v1/images/search"
url_dog = "https://api.thedogapi.com/v1/images/search"

def show_pet(flag):
    def task():
        global label_image
        if flag:
            response = requests.get(url_cat, timeout=5)
        else:
            response = requests.get(url_dog, timeout=5)
        if response.status_code == 200:
            if label_image:
                label_image.destroy()

            data = response.json()[0]
            image_url = data["url"]
            image_response = requests.get(image_url)
            image_bytes = image_response.content

            image_pil = Image.open(io.BytesIO(image_bytes))
            max_width, max_height = 700, 700
            image_pil.thumbnail((max_width, max_height))
            image_tk = ImageTk.PhotoImage(image_pil)

            label_image = ttk.Label(root, image=image_tk)
            label_image.image = image_tk
            label_image.pack(anchor="center", pady=15)
        else:
            print(f"Ошибка запроса: {response.status_code}")
    threading.Thread(target=task).start()


root = tk.Tk()
root.title("Рандомная кошка/собака")
root.geometry("700x700")
root.resizable(False, False)
label_image = ttk.Label(root)


frame_butt = tk.Frame(root)
frame_butt.pack(fill='x', side='bottom')

frame_butt.columnconfigure(0, weight=1)
frame_butt.columnconfigure(1, weight=0)
frame_butt.columnconfigure(2, weight=1)

ttk.Button(frame_butt, text="Показать кошку", command=lambda: show_pet(True)).grid(row=0, column=0)
ttk.Button(frame_butt, text="Выход", command=lambda: root.destroy()).grid(row=1, column=1, pady=10)
ttk.Button(frame_butt, text="Показать собаку", command=lambda: show_pet(False)).grid(row=0, column=2)

root.mainloop()