import tkinter as tk
from tkinter import messagebox
import requests
import json
# Путь к файлу с избранными пользователями
FAVORITES_FILE = "favorites.json"
def load_favorites():
    try:
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=2)
def search_user():
    username = entry_search.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
        return
    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        response.raise_for_status()
        user_data = response.json()
        display_user(user_data)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Пользователь не найден или ошибка сети: {e}")
def display_user(user_data):
    # Очищаем список результатов
    listbox_results.delete(0, tk.END)
    # Вставляем найденного пользователя
    listbox_results.insert(tk.END, f"{user_data['login']} ({user_data['name']})")
    # Сохраняем данные пользователя для добавления в избранное
    global current_user_data
    current_user_data = user_data
def add_to_favorites():
    if not current_user_data:
        messagebox.showwarning("Ошибка", "Сначала найдите пользователя!")
        return
    favorites = load_favorites()
    # Проверяем, нет ли уже такого пользователя в избранном
    if any(u['login'] == current_user_data['login'] for u in favorites):
        messagebox.showinfo("Информация", "Пользователь уже в избранном!")
        return

    favorites.append(current_user_data)
    save_favorites(favorites)
    messagebox.showinfo("Успех", "Пользователь добавлен в избранное!")

# --- GUI ---
root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("500x400")

# Поле поиска
entry_search = tk.Entry(root, width=40)
entry_search.pack(pady=10)

# Кнопка поиска
btn_search = tk.Button(root, text="Поиск", command=search_user)
btn_search.pack(pady=5)

# Список результатов
listbox_results = tk.Listbox(root, width=60, height=10)
listbox_results.pack(pady=10)

# Кнопка добавления в избранное
btn_fav = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
btn_fav.pack(pady=5)

# Переменная для хранения данных текущего пользователя
current_user_data = None

root.mainloop()
