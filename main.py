from game import Game
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Перенесем код по созданию графика в функцию, чтобы ее можно было вызвать из tkinter приложения
def create_plot(data, names):
    # Создаем tkinter приложение
    root = tk.Tk()
    root.title("Итоги")
    
    locs = ['penalties', 'lack_of_goods','warehouse_states']#list(data[0].keys())
    fig = Figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    #fig.subplots_adjust(top=1)
    ln = len(names)
    ll = len(locs)
    x = [i for i in range(len(data[0][locs[0]]))]
    
    for i in range(ll):
        ax = fig.add_subplot(ll, 1, i+1)
        ax.set_title(locs[i])
        for j in range(ln):
            #print(data[j][locs[i]])
            ax.plot(x, data[j][locs[i]], label=names[j])
        ax.legend()
    
    # Создаем объект FigureCanvasTkAgg с использованием созданной ранее фигуры
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    # Запускаем главный цикл tkinter приложения
    root.mainloop()


def run_games():
    # реализуем функцию запуска игры
    name = name_entry.get()
    stress_mod_for_turn = stress_mod_for_turn_entry.get()
    target_inventory = target_inventory_entry.get()
    # проверяем корректность ввода
    if name.count(';') != stress_mod_for_turn.count(';'):
        messagebox.showerror("Ошибка", "Некорректное введен стресс!")
    if name.count(';') != target_inventory.count(';'):
        messagebox.showerror("Ошибка", "Некорректное введен минимум на складе!")
    
    game = Game()
    try:
        data=game.main(name.split('; '), file_entry.get(), stress_mod_for_turn.split('; '), target_inventory.split('; '), use_stress.get(), regime_var.get(), second_entry.get(), use_draw.get(), int(window_width*1.5), int(window_height*1.5))
        #print(data)
        create_plot(data[0], data[1])
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте ввод данных!")
   
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл не найден!")
    #except:
    #    messagebox.showerror("Ошибка", "Не опознанная ошибка! Приносим извинения")
    
        



# создаем главное окно
root = tk.Tk()
root.title("Главное меню")

# получаем размер окна пользователя
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# устанавливаем размер окна главного меню
window_width = int(screen_width / 2)
window_height = int(screen_height / 2)
root.geometry(f'{window_width}x{window_height}+{int(screen_width / 4)}+{int(screen_height / 4)}')



# создаем фрейм с опциями
options_frame = tk.Frame(root)
options_frame.pack(pady=10)


start_button = tk.Button(options_frame, text="Старт игры", command=run_games)
start_button.grid(row=0, column=0, padx=10)


name_label = tk.Label(options_frame, text="Имя игрока:")
name_label.grid(row=1, column=0)
name_entry = tk.Entry(options_frame)
name_entry.insert(0, "manufacturer; distributor; wholesaler; retailer")
name_entry.grid(row=1, column=1, padx=10)



file_label = tk.Label(options_frame, text="Путь до файла со спросом пользователей:")
file_label.grid(row=2, column=0)
file_entry = tk.Entry(options_frame)
file_entry.insert(0, "demand_data.xlsx")
file_entry.grid(row=2, column=1, padx=10)


target_inventory_label = tk.Label(options_frame, text="Минимум на складе:")
target_inventory_label.grid(row=3, column=0)
target_inventory_entry = tk.Entry(options_frame)
target_inventory_entry.insert(0, "20; 20; 20; 20")
target_inventory_entry.grid(row=3, column=1, padx=10)


regime_label = tk.Label(options_frame, text="Режим дозаказа:")
regime_label.grid(row=4, column=0)
regimes = ["Продвинутая", "Наивная"]
regime_var = tk.StringVar(options_frame)
regime_var.set(regimes[0])
regime_option = tk.OptionMenu(options_frame, regime_var, *regimes)
regime_option.grid(row=4, column=1, padx=10)



stress_mod_for_turn_label = tk.Label(options_frame, text="Стресс за ход:")
stress_mod_for_turn_label.grid(row=5, column=0)
stress_mod_for_turn_entry = tk.Entry(options_frame)
stress_mod_for_turn_entry.insert(0, "0.05; 0.05; 0.05; 0.05")
stress_mod_for_turn_entry.grid(row=5, column=1, padx=10)



use_stress_label = tk.Label(options_frame, text="Использовать стресс:")
use_stress_label.grid(row=6, column=0)
use_stress = tk.BooleanVar()
use_stress.set(True)
use_stress_checkbutton = tk.Checkbutton(options_frame, variable=use_stress)
use_stress_checkbutton.grid(row=6, column=1, padx=10)


#second.get(), use_draw.get()
second_label = tk.Label(options_frame, text="Секунд на ход:")
second_label.grid(row=7, column=0)
second_entry = tk.Entry(options_frame)
second_entry.insert(0, "1")
second_entry.grid(row=7, column=1, padx=10)



use_draw_label = tk.Label(options_frame, text="Отображать игру:")
use_draw_label.grid(row=8, column=0)
use_draw = tk.BooleanVar()
use_draw.set(True)
use_draw_checkbutton = tk.Checkbutton(options_frame, variable=use_draw)
use_draw_checkbutton.grid(row=8, column=1, padx=10)


# запускаем основной цикл обработки событий
root.mainloop()
