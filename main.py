import tkinter as tk
from tkinter import ttk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.canvas_manager = CanvasManager(self.root)
        self.toolbox = Toolbox(self.root, self.canvas_manager)
        self.setup_navbar()

    def setup_navbar(self):
        navbar = tk.Menu(self.root)
        self.root.config(menu=navbar)

        file_menu = tk.Menu(navbar, tearoff=False)
        navbar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Snapshot", command=self.canvas_manager.take_snapshot)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(navbar, tearoff=False)
        navbar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.canvas_manager.undo)

class Toolbox:
    def __init__(self, root, canvas_manager):
        self.canvas_manager = canvas_manager
        self.selected_tool = "pen"
        self.selected_color = "black"
        self.selected_size = 2
        self.selected_pen_type = "line"

        self.tool_frame = ttk.LabelFrame(root, text="Tools")
        self.tool_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.Y)

        self.create_tool_widgets()

    def create_tool_widgets(self):
        pen_button = ttk.Button(self.tool_frame, text="Pen", command=self.select_pen_tool)
        pen_button.pack(side=tk.TOP, padx=5, pady=5)

        eraser_button = ttk.Button(self.tool_frame, text="Eraser", command=self.select_eraser_tool)
        eraser_button.pack(side=tk.TOP, padx=5, pady=5)

        brush_size_label = ttk.Label(self.tool_frame, text="Brush Size:")
        brush_size_label.pack(side=tk.TOP, padx=5, pady=5)

        brush_size_combobox = ttk.Combobox(self.tool_frame, values=[2, 4, 6, 8], state="readonly")
        brush_size_combobox.current(0)
        brush_size_combobox.pack(side=tk.TOP, padx=5, pady=5)
        brush_size_combobox.bind("<<ComboboxSelected>>", lambda event: self.select_size(int(brush_size_combobox.get())))

        color_label = ttk.Label(self.tool_frame, text="Color:")
        color_label.pack(side=tk.TOP, padx=5, pady=5)

        color_combobox = ttk.Combobox(self.tool_frame, values=["black", "red", "green", "blue", "yellow", "orange", "purple"], state="readonly")
        color_combobox.current(0)
        color_combobox.pack(side=tk.TOP, padx=5, pady=5)
        color_combobox.bind("<<ComboboxSelected>>", lambda event: self.select_color(color_combobox.get()))

        pen_type_label = ttk.Label(self.tool_frame, text="Pen Type:")
        pen_type_label.pack(side=tk.TOP, padx=5, pady=5)

        pen_type_combobox = ttk.Combobox(self.tool_frame, values=["line", "round", "square", "arrow", "diamond"], state="readonly")
        pen_type_combobox.current(0)
        pen_type_combobox.pack(side=tk.TOP, padx=5, pady=5)
        pen_type_combobox.bind("<<ComboboxSelected>>", lambda event: self.select_pen_type(pen_type_combobox.get()))

        clear_button = ttk.Button(self.tool_frame, text="Clear Canvas", command=self.canvas_manager.clear_canvas)
        clear_button.pack(side=tk.TOP, padx=5, pady=5)

    def select_pen_tool(self):
        self.canvas_manager.set_tool("pen")
        self.canvas_manager.restore_previous_color() 

    def select_eraser_tool(self):
        self.canvas_manager.set_tool("eraser")
        self.canvas_manager.save_current_color()
        self.canvas_manager.set_color("white")

    def select_size(self, size):
        self.canvas_manager.set_size(size)

    def select_color(self, color):
        self.canvas_manager.set_color(color)

    def select_pen_type(self, pen_type):
        self.canvas_manager.set_pen_type(pen_type)

class CanvasManager:
    def __init__(self, root):
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white", bd=3, relief=tk.SUNKEN)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.prev_x = None
        self.prev_y = None
        self.selected_tool = "pen"
        self.selected_color = "black"
        self.selected_size = 2
        self.selected_pen_type = "line"

        self.setup_events()

    def setup_events(self):
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.release)

    def set_tool(self, tool):
        self.selected_tool = tool

    def set_size(self, size):
        self.selected_size = size

    def set_color(self, color):
        self.selected_color = color

    def set_pen_type(self, pen_type):
        self.selected_pen_type = pen_type

    def save_current_color(self):
        self.previous_color = self.selected_color  # Сохраняем текущий цвет

    def restore_previous_color(self):
        self.set_color(self.previous_color)  # Восстанавливаем сохранённый цвет


    def draw(self, event):
        if self.selected_tool == "pen" or self.selected_tool == "eraser":
            if self.prev_x is not None and self.prev_y is not None:
                if self.selected_pen_type == "line":
                    self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill=self.selected_color, width=self.selected_size, smooth=True)
                elif self.selected_pen_type == "round":
                    x1, y1, x2, y2 = self.calculate_oval(event)
                    self.canvas.create_oval(x1, y1, x2, y2, fill=self.selected_color, outline=self.selected_color)
                elif self.selected_pen_type == "square":
                    x1, y1, x2, y2 = self.calculate_rectangle(event)
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.selected_color, outline=self.selected_color)
                elif self.selected_pen_type == "arrow":
                    self.draw_arrow(event)
                elif self.selected_pen_type == "diamond":
                    self.draw_diamond(event)
            self.prev_x = event.x
            self.prev_y = event.y

    def release(self, event):
        self.prev_x = None
        self.prev_y = None

    def calculate_oval(self, event):
        x1 = event.x - self.selected_size
        y1 = event.y - self.selected_size
        x2 = event.x + self.selected_size
        y2 = event.y + self.selected_size
        return x1, y1, x2, y2

    def calculate_rectangle(self, event):
        x1 = event.x - self.selected_size
        y1 = event.y - self.selected_size
        x2 = event.x + self.selected_size
        y2 = event.y + self.selected_size
        return x1, y1, x2, y2

    def draw_arrow(self, event):
        x1 = event.x - self.selected_size
        y1 = event.y - self.selected_size
        x2 = event.x + self.selected_size
        y2 = event.y + self.selected_size
        self.canvas.create_polygon(x1, y1, x1, y2, event.x, y2, fill=self.selected_color, outline=self.selected_color)

    def draw_diamond(self, event):
        x1 = event.x - self.selected_size
        y1 = event.y
        x2 = event.x
        y2 = event.y - self.selected_size
        x3 = event.x + self.selected_size
        y3 = event.y
        x4 = event.x
        y4 = event.y + self.selected_size
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill=self.selected_color, outline=self.selected_color)

    def clear_canvas(self):
        self.canvas.delete("all")

    def take_snapshot(self):
        self.canvas.postscript(file="snapshot.eps")

    def undo(self):
        items = self.canvas.find_all()
        if items:
            self.canvas.delete(items[-1])

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Paint App")
    app = PaintApp(root)
    root.mainloop()
