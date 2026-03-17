import threading
import base64
from tkinter import PhotoImage
import tkinter as tk
from tkinter import ttk
import requests

api_key = "31577016568e44634c0baa939dcdeaad"
icon_image_ref = None


def show_weather():
    def task():
        global icon_image_ref
        update_ui(frame_output)
        city_name = entry.get()
        geo = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
        response = requests.get(geo, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data == []:
                ttk.Label(frame_output, text=f"Ничего не найдено").pack(pady=10)
                show_butt.config(state=["enabled"])
                return
            data = data[0]
            try:
                name = data["local_names"]["ru"]
            except:
                name = data["name"]
            lat = data["lat"]
            lon = data["lon"]
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}&lang=ru"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                weather = data["weather"][0]
                response = requests.get(f"https://rodrigokamada.github.io/openweathermap/images/{weather["icon"]}_t@2x.png")

                if response.status_code == 200:
                    image_bytes = response.content
                    b64_data = base64.b64encode(image_bytes).decode('ascii')
                    icon_image_ref = PhotoImage(data=b64_data)

                    tk.Label(frame_output, text=name, font=("", 14)).pack(pady=10)
                    tk.Label(frame_output, image=icon_image_ref, text=weather["description"], compound="top", bg="light gray").pack()
                    tk.Label(frame_output, text=f"{int(data['main']['temp'])} °C", font=("", 15)).pack(pady=10)
                else:
                    ttk.Label(frame_output, text=f"Ошибка запроса №3: {response.status_code}").pack(pady=10)
            else:
                ttk.Label(frame_output, text=f"Ошибка запроса №2: {response.status_code}").pack(pady=10)
        else:
            ttk.Label(frame_output, text=f"Ошибка запроса №1: {response.status_code}").pack(pady=10)
        show_butt.config(state=["enabled"])
    threading.Thread(target=task).start()
    


def update_ui(frame):
    for widget in frame.winfo_children():
        widget.destroy()


root = tk.Tk()
root.title("Погода")
root.geometry("400x250")
root.resizable(False, False)


frame_input = tk.Label(root)
frame_input.place(x=100, y=125, anchor="center")
ttk.Label(frame_input, text="Введите город", font=("", 14)).pack(pady=10)
entry = ttk.Entry(frame_input)
entry.pack(pady=10)
show_butt = ttk.Button(frame_input, text="Показать", command=lambda: [show_weather(), show_butt.config(state=["disabled"])])
show_butt.pack(pady=10)
ttk.Button(frame_input, text="Выход", command=lambda: root.destroy()).pack(pady=10)


frame_output = tk.Label(root)
frame_output.place(x=300, y=125, anchor="center")


root.mainloop()