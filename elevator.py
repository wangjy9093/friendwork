import tkinter as tk
from tkinter import messagebox

class Passenger:
    def __init__(self, name, weight, destination_floor):
        self.name = name
        self.weight = weight
        self.destination_floor = destination_floor

class Elevator:
    def __init__(self, number, floors_served, max_passengers, max_weight):
        self.number = number
        self.floors_served = floors_served
        self.max_passengers = max_passengers
        self.max_weight = max_weight
        self.current_floor = 0
        self.previous_floor = 0
        self.passengers = []
        self.weight = 0
        self.destination_floors = []
        self.direction = 1

    def load_passenger(self, passenger):
        if passenger.destination_floor != self.current_floor:
            if passenger.destination_floor not in self.destination_floors:
                if len(self.passengers) < self.max_passengers and self.weight + passenger.weight <= self.max_weight:
                    self.passengers.append(passenger)
                    self.weight += passenger.weight
                    self.destination_floors.append(passenger.destination_floor)
                    messagebox.showinfo("乘客加载", f"乘客 {passenger.name} 已加载到电梯 {self.number}")
                else:
                    messagebox.showerror("错误", f"电梯 {self.number} 已满，无法加载乘客 {passenger.name}")
            else:
                if len(self.passengers) < self.max_passengers and self.weight + passenger.weight <= self.max_weight:
                    self.passengers.append(passenger)
                    self.weight += passenger.weight
                messagebox.showinfo("乘客加载", f"乘客 {passenger.name} 已加载到电梯 {self.number}")
        else:
            messagebox.showinfo("提示", f"乘客 {passenger.name} 的目标楼层和当前楼层相同")

    def move_to_floor(self, floor):
        if floor in self.floors_served:
            self.previous_floor = self.current_floor
            self.current_floor = floor-1

            # 添加安全检查以避免移除不存在的目标楼层
            if floor in self.destination_floors:
                self.destination_floors.remove(floor)
                self.passengers = [passenger for passenger in self.passengers if passenger.destination_floor != floor]
                self.weight = sum(passenger.weight for passenger in self.passengers)
                messagebox.showinfo("电梯移动", f"电梯 {self.number} 已移动到 {floor} 楼")

                # 更新电梯运行方向
                next_floor = self.get_next_floor()
                if next_floor >= self.current_floor:
                    self.direction = 1
                else:
                    self.direction = -1
            else:
                messagebox.showerror("错误", f"电梯 {self.number} 的目标楼层列表中没有楼层 {floor}")

            # 调用更新目标楼层的函数，实现目标楼层的实时更新
            update_destinations(self.number, self.destination_floors)
        else:
            messagebox.showerror("错误", f"电梯 {self.number} 不服务楼层 {floor}")

        # 在这里添加检查当前楼层为1时的标志位更新逻辑
        if self.current_floor == 1 and self.direction == -1:
            self.direction = 1  # 如果当前楼层为1且方向为向下，则改为向上

    def get_next_floor(self):
        if self.destination_floors:
            if self.direction == 1:
                next_floors = [f for f in self.destination_floors if f > self.current_floor]
                next_floor = min(next_floors) if next_floors else max(self.destination_floors)
            elif self.direction == -1:
                next_floors = [f for f in self.destination_floors if f < self.current_floor]
                next_floor = max(next_floors) if next_floors else min(self.destination_floors)
            else:
                next_floor = self.current_floor
            return next_floor
        else:
            return self.current_floor


elevator1 = Elevator(1, list(range(1, 21)), 10, 800)
elevator2 = Elevator(2, list(range(1, 21, 2)), 10, 800)
elevator3 = Elevator(3, list(range(2, 21, 2)), 10, 800)
elevator4 = Elevator(4, list(range(1, 21)), 20, 2000)


def load_passenger():
    name = name_entry.get()
    weight = int(weight_entry.get())
    destination_floor = int(floor_entry.get())

    # 检查乘客姓名是否重复
    if any(passenger.name == name for passenger in elevator1.passengers +
                                                   elevator2.passengers +
                                                   elevator3.passengers +
                                                   elevator4.passengers):
        messagebox.showerror("错误", f"姓名为 {name} 的乘客已存在，请输入其他姓名")
        return

    passenger = Passenger(name, weight, destination_floor)
    elevator_number = elevator_var.get()
    if elevator_number == 1:
        if passenger.destination_floor in elevator1.floors_served:
            elevator1.load_passenger(passenger)
            update_destinations(elevator1.number, elevator1.destination_floors)
        else:
            messagebox.showerror("错误", f"电梯1不服务楼层 {passenger.destination_floor}")
    elif elevator_number == 2:
        if passenger.destination_floor in elevator2.floors_served:
            elevator2.load_passenger(passenger)
            update_destinations(elevator2.number, elevator2.destination_floors)
        else:
            messagebox.showerror("错误", f"电梯2不服务楼层 {passenger.destination_floor}")
    elif elevator_number == 3:
        if passenger.destination_floor in elevator3.floors_served:
            elevator3.load_passenger(passenger)
            update_destinations(elevator3.number, elevator3.destination_floors)
        else:
            messagebox.showerror("错误", f"电梯3不服务楼层 {passenger.destination_floor}")
    elif elevator_number == 4:
        if passenger.destination_floor in elevator4.floors_served:
            elevator4.load_passenger(passenger)
            update_destinations(elevator4.number, elevator4.destination_floors)
        else:
            messagebox.showerror("错误", f"电梯4不服务楼层 {passenger.destination_floor}")



def update_destinations(elevator_number, destination_floors):
    for elevator, labels in zip([elevator1, elevator2, elevator3, elevator4], elevator_labels):
        if elevator.number == elevator_number:
            labels[2].config(text=f"目标楼层: {destination_floors}")
            break

def move_elevator():
    elevator_number = elevator_var.get()
    if elevator_number == 1:
        elevator1.move_to_floor(elevator1.get_next_floor())
        update_display()
    elif elevator_number == 2:
        elevator2.move_to_floor(elevator2.get_next_floor())
        update_display()
    elif elevator_number == 3:
        elevator3.move_to_floor(elevator3.get_next_floor())
        update_display()
    elif elevator_number == 4:
        elevator4.move_to_floor(elevator4.get_next_floor())
        update_display()

def update_display():
    canvas.delete("all")
    for elevator, labels in zip([elevator1, elevator2, elevator3, elevator4], elevator_labels):
        labels[0].config(text=f"载客人数: {len(elevator.passengers)}")
        labels[1].config(text=f"载重量: {elevator.weight} kg")

    for col, text in enumerate(["楼层", "电梯1", "电梯2", "电梯3", "电梯4"]):
        if col == 0:
            canvas.create_rectangle(50 + col * 150, 10, 200 + col * 150, 30, fill="lightgreen")
        else:
            canvas.create_rectangle(50 + col * 150, 10, 200 + col * 150, 30, fill="lightblue")
        canvas.create_text(125 + col * 150, 20, text=text)

    for row in range(1, 21):
        canvas.create_rectangle(50, 10 + row * 20, 200, 30 + row * 20, fill="lightgreen")
        canvas.create_text(125, 20 + row * 20, text=f"{21 - row}")
        for col in range(1, 5):
            x1, y1, x2, y2 = 200 + (col - 1) * 150, 10 + row * 20, 350 + (col - 1) * 150, 30 + row * 20
            canvas.create_rectangle(x1, y1, x2, y2, fill="white")
            if col == 1 and elevator1.current_floor == 20 - row:
                canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
                if elevator1.previous_floor <= elevator1.current_floor:
                    canvas.create_text(275, 20 + row * 20, text=f"上")
                elif elevator1.previous_floor > elevator1.current_floor:
                    canvas.create_text(275, 20 + row * 20, text=f"下")
            elif col == 2 and elevator2.current_floor == 20 - row:
                canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
                if elevator2.previous_floor <= elevator2.current_floor:
                    canvas.create_text(425, 20 + row * 20, text=f"上")
                elif elevator2.previous_floor > elevator2.current_floor:
                    canvas.create_text(425, 20 + row * 20, text=f"下")
            elif col == 3 and elevator3.current_floor == 20 - row:
                canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
                if elevator3.previous_floor <= elevator3.current_floor:
                    canvas.create_text(575, 20 + row * 20, text=f"上")
                elif elevator3.previous_floor > elevator3.current_floor:
                    canvas.create_text(575, 20 + row * 20, text=f"下")
            elif col == 4 and elevator4.current_floor == 20 - row:
                canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
                if elevator4.previous_floor <= elevator4.current_floor:
                    canvas.create_text(725, 20 + row * 20, text=f"上")
                elif elevator4.previous_floor > elevator4.current_floor:
                    canvas.create_text(725, 20 + row * 20, text=f"下")

    window.after(1000, update_display)

window = tk.Tk()
window.title("电梯控制系统")

main_frame = tk.Frame(window)
main_frame.pack(side=tk.TOP)

canvas = tk.Canvas(main_frame, width=800, height=430)
canvas.pack(side=tk.LEFT, padx=10, pady=10)

sub_frame = tk.Frame(window)
sub_frame.pack(side=tk.LEFT)

elevator_labels = []

for i in range(4):
    elevator_frame = tk.Frame(sub_frame)
    elevator_frame.pack(side=tk.LEFT, padx=20)
    if i == 0 or i == 3:
        elevator_label = tk.Label(elevator_frame, text=f"电梯{i+1} （1-20）")
        elevator_label.pack()
    elif i == 1:
        elevator_label = tk.Label(elevator_frame, text=f"电梯{i + 1} （单数楼层）")
        elevator_label.pack()
    elif i == 2:
        elevator_label = tk.Label(elevator_frame, text=f"电梯{i + 1} （双数楼层）")
        elevator_label.pack()

    info_label1 = tk.Label(elevator_frame, text="载客人数: 0")
    info_label1.pack()

    info_label2 = tk.Label(elevator_frame, text="载重量: 0 kg")
    info_label2.pack()

    dest_label = tk.Label(elevator_frame, text="目标楼层:")
    dest_label.pack()

    elevator_labels.append((info_label1, info_label2, dest_label))

input_frame = tk.Frame(main_frame)
input_frame.pack(side=tk.RIGHT, padx=10)

name_label = tk.Label(input_frame, text="姓名:")
name_label.pack(side=tk.TOP)

name_entry = tk.Entry(input_frame)
name_entry.pack(side=tk.TOP, padx=5)

weight_label = tk.Label(input_frame, text="体重:")
weight_label.pack(side=tk.TOP)

weight_entry = tk.Entry(input_frame)
weight_entry.pack(side=tk.TOP, padx=5)

floor_label = tk.Label(input_frame, text="目标楼层:")
floor_label.pack(side=tk.TOP)

floor_entry = tk.Entry(input_frame)
floor_entry.pack(side=tk.TOP, padx=5)

blank_label = tk.Label(input_frame, text="")
blank_label.pack(side=tk.TOP)

elevator_frame = tk.Frame(input_frame)
elevator_frame.pack(side=tk.TOP)

elevator_var = tk.IntVar()
elevator_var.set(1)
elevator_radio1 = tk.Radiobutton(elevator_frame, text="电梯1", variable=elevator_var, value=1)
elevator_radio1.pack(side=tk.LEFT)

elevator_radio2 = tk.Radiobutton(elevator_frame, text="电梯2", variable=elevator_var, value=2)
elevator_radio2.pack(side=tk.LEFT)

elevator_radio3 = tk.Radiobutton(elevator_frame, text="电梯3", variable=elevator_var, value=3)
elevator_radio3.pack(side=tk.LEFT)

elevator_radio4 = tk.Radiobutton(elevator_frame, text="电梯4", variable=elevator_var, value=4)
elevator_radio4.pack(side=tk.LEFT)

load_button = tk.Button(input_frame, text="加载乘客", command=load_passenger)
load_button.pack(side=tk.TOP)

move_button = tk.Button(input_frame, text="移动电梯", command=move_elevator)
move_button.pack(side=tk.TOP)

update_display()
window.mainloop()
