import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class InteractivePlot:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Plot Editor")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.point_attributes = {}  # Store attributes like color and size per point
        
        # **Default Styles**
        self.initial_line_style = "-"
        self.initial_line_color = "blue"
        self.initial_marker_size = 10

        # Set current styles
        self.line_style = self.initial_line_style
        self.line_color = self.initial_line_color
        self.marker_size = self.initial_marker_size
        
        # Grid and Legend toggles
        self.grid_toggle_var = tk.BooleanVar(value=False)
        self.legend_toggle_var = tk.BooleanVar(value=False)

         # Variable for live update toggle
        self.live_update_var = tk.BooleanVar(value=False)
        self.live_update_task_id = None  # To store the scheduled task ID for live updates

        # Mouse drag variables for smoother movement
        self.prev_mouse_x = None
        self.prev_mouse_y = None
        self.drag_threshold = 5  # Minimum movement required to update the point

         # Initialize zoom factor and pan variables
        self.zoom_factor = 1.1
        self.prev_x, self.prev_y = None, None  # For panning

        self.time_step = 0

        self.selected_point = None

        # Initial and current points
        self.initial_points = [(1, 10), (2, 20), (3, 25), (4, 30)]  # Save the original state
        self.points = self.initial_points.copy()
        
        self.create_plot_tab()

       


    def create_plot_tab(self):
        """Interactive Plot Tab with dynamic editing features."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="   Interactive Plot   ")

        # Create a matplotlib figure for interactive plotting
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Advanced Plot")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")

        # Embed the figure in the GUI
        self.canvas = FigureCanvasTkAgg(self.figure, tab)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)


        # Initialize plot points
        self.points = [(1, 10), (2, 20), (3, 25), (4, 30)]

        # Initial plot
        self.update_plot()

        # Controls Frame
        controls_frame = ttk.Frame(tab, relief=tk.RIDGE, borderwidth=2)
        controls_frame.pack(side="bottom", fill="x", pady=5)
        
        # Undo/Redo Stack
        self.history = []
        self.redo_stack = []

        # Buttons
        ttk.Button(controls_frame, text="Add Point", command=self.add_point).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Undo", command=self.undo).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Redo", command=self.redo).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Export", command=self.export_plot).pack(side="left", padx=5)

        # Store original limits for reset function
        self.original_xlim = self.ax.get_xlim()
        self.original_ylim = self.ax.get_ylim()

        # Add Zoom Buttons
        ttk.Button(controls_frame, text="Zoom In", command=lambda: self.zoom(True)).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Zoom Out", command=lambda: self.zoom(False)).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Reset Zoom", command=self.reset_zoom).pack(side="left", padx=5)

        # **New Reset Button**
        ttk.Button(controls_frame, text="Reset", command=self.reset_plot).pack(side="left", padx=5)
        
        # Line style and color options
        ttk.Label(controls_frame, text="Line Style:").pack(side="left", padx=5)
        self.line_style_combo = ttk.Combobox(controls_frame, values=["-", "--", "-.", ":"], state="readonly")
        self.line_style_combo.pack(side="left", padx=5)
        self.line_style_combo.set(self.line_style)
        self.line_style_combo.bind("<<ComboboxSelected>>", self.change_line_style)
        
        ttk.Label(controls_frame, text="Line Color:").pack(side="left", padx=5)
        self.line_color_combo = ttk.Combobox(controls_frame, values=["blue", "red", "green", "black"], state="readonly")
        self.line_color_combo.pack(side="left", padx=5)
        self.line_color_combo.set(self.line_color)
        self.line_color_combo.bind("<<ComboboxSelected>>", self.change_line_color)

        # Marker size adjustment
        ttk.Label(controls_frame, text="Marker Size:").pack(side="left", padx=5)
        self.marker_size_slider = ttk.Scale(controls_frame, from_=5, to=20, orient="horizontal", command=self.change_marker_size)
        self.marker_size_slider.set(self.marker_size)
        self.marker_size_slider.pack(side="left", padx=5)

        # Toggle gridlines and legend and add live update checkbox
        ttk.Checkbutton(controls_frame, text="Live Update", variable=self.live_update_var, command=self.toggle_live_update).pack(side="left", padx=5)
        ttk.Checkbutton(controls_frame, text="Grid", variable=self.grid_toggle_var, command=self.toggle_grid).pack(side="left", padx=5)
        ttk.Checkbutton(controls_frame, text="Legend", variable=self.legend_toggle_var, command=self.toggle_legend).pack(side="left", padx=5)

        # Connect canvas events for interactivity
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.canvas.mpl_connect("button_release_event", self.on_release)

        self.canvas.mpl_connect('scroll_event', self.on_mouse_scroll)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_drag)

        self.prev_x, self.prev_y = None, None  # For panning


    def zoom(self, zoom_in=True):
     """Zoom in or out when buttons are clicked."""
     zoom_factor = 1.2 if zoom_in else 0.8  # 1.2 for zoom in, 0.8 for zoom out

     xlim = self.ax.get_xlim()
     ylim = self.ax.get_ylim()

     x_center = (xlim[0] + xlim[1]) / 2
     y_center = (ylim[0] + ylim[1]) / 2

     new_xlim = [x_center + (x - x_center) * zoom_factor for x in xlim]
     new_ylim = [y_center + (y - y_center) * zoom_factor for y in ylim]

     self.ax.set_xlim(new_xlim)
     self.ax.set_ylim(new_ylim)
     self.canvas.draw()

    def reset_zoom(self):
     """Reset the zoom to the original scale."""
     self.ax.set_xlim(self.original_xlim)
     self.ax.set_ylim(self.original_ylim)
     self.canvas.draw()



    def reset_plot(self):
        """Reset the plot to its initial state."""
        self.points = self.initial_points.copy()

        # Reset styling attributes
        self.line_style = self.initial_line_style
        self.line_color = self.initial_line_color
        self.marker_size = self.initial_marker_size
        self.grid_toggle_var.set(False)
        self.legend_toggle_var.set(False)

        # Reset UI elements
        self.line_style_combo.set(self.initial_line_style)
        self.line_color_combo.set(self.initial_line_color)
        self.marker_size_slider.set(self.initial_marker_size)

        self.update_plot()


    def update_live_plot(self):
     """Continuously update existing points dynamically (like an animated GIF)."""
     if self.live_update_var.get():
        import math
        self.points = [(x, y + math.sin(x + self.time_step) * 0.5) for x, y in self.points]
        self.time_step += 0.1

        self.update_plot()

        # Schedule the next update
        self.live_update_task_id = self.root.after(100, self.update_live_plot)  # Faster updates (100ms)

    def toggle_live_update(self):
        """Toggle live plot updates on or off."""
        if self.live_update_var.get():
            self.update_live_plot()  # Start live updates
        else:
            if self.live_update_task_id is not None:
                self.root.after_cancel(self.live_update_task_id)  # Cancel live updates
                self.live_update_task_id = None  # Clear the task ID

    def update_plot(self):
     """Update the plot with latest data and attributes."""
     self.ax.clear()
     self.ax.set_title("Advanced Plot")
     self.ax.set_xlabel("X-axis")
     self.ax.set_ylabel("Y-axis")

     for (x, y) in self.points:
        attrs = self.point_attributes.get((x, y), {"color": "red", "size": self.marker_size})
        self.ax.scatter(x, y, color=attrs["color"], s=attrs["size"])

     x_vals, y_vals = zip(*self.points) if self.points else ([], [])
     self.ax.plot(x_vals, y_vals, linestyle=self.line_style, color=self.line_color, label="Data")

     if self.grid_toggle_var.get():
        self.ax.grid(True)
     if self.legend_toggle_var.get():
        self.ax.legend()

     self.canvas.draw()


    def add_annotation(self, x, y, text):
     """Add an annotation at the given (x, y) position."""
     self.ax.annotate(text, (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
     self.canvas.draw()

    def on_click(self, event):
     """Detects click on a point and enables dragging."""
     if event.xdata is None or event.ydata is None:
        return
     for i, (x, y) in enumerate(self.points):
        if abs(x - event.xdata) < 0.5 and abs(y - event.ydata) < 0.5:
            self.selected_point = i
            break
     else:
        # Add annotation if no point is selected
        self.add_annotation(event.xdata, event.ydata, "Annotation")

    
    def on_motion(self, event):
        """Move the selected point with the mouse."""
        if self.selected_point is not None and event.xdata and event.ydata:
            self.points[self.selected_point] = (event.xdata, event.ydata)
            self.update_plot()

    def on_release(self, event):
        """Release the dragged point."""
        self.selected_point = None

    def open_add_point_popup(self):
     """Popup window to manually enter point coordinates and attributes."""
     popup = tk.Toplevel(self.root)
     popup.title("Add Custom Point")
     popup.geometry("300x250")
     popup.resizable(0,0)

     tk.Label(popup, text="X Coordinate:").pack()
     x_entry = tk.Entry(popup)
     x_entry.pack()

     tk.Label(popup, text="Y Coordinate:").pack()
     y_entry = tk.Entry(popup)
     y_entry.pack()

     # Dropdown for color selection
     tk.Label(popup, text="Point Color:").pack()
     color_var = tk.StringVar(value="red")
     color_dropdown = ttk.Combobox(popup, textvariable=color_var, values=["red", "blue", "green", "black"])
     color_dropdown.pack()

     # Slider for marker size
     tk.Label(popup, text="Marker Size:").pack()
     marker_size_var = tk.DoubleVar(value=10)
     marker_size_slider = ttk.Scale(popup, from_=5, to=300, orient="horizontal", variable=marker_size_var)
     marker_size_slider.pack()

     def confirm_point():
        """Confirm point addition with user-defined attributes."""
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())
            color = color_var.get()
            size = marker_size_var.get()

            self.points.append((x, y))
            self.point_attributes[(x, y)] = {"color": color, "size": size}  # Store attributes
            self.update_plot()
            popup.destroy()
        except ValueError:
            tk.messagebox.showerror("Input Error", "Please enter valid numbers for X and Y.")

     ttk.Button(popup, text="Add Point", command=confirm_point).pack(pady=10)


    def add_point(self):
     """Ask user whether to add points automatically or manually."""
     response = tk.messagebox.askyesno("Add Point", "Do you want to add points automatically?\n"
                                                    "Click 'Yes' for auto, 'No' for manual selection.")
     if response:
        # Automatic mode (same as before)
        new_x = self.points[-1][0] + 1 if self.points else 1
        new_y = 10
        self.points.append((new_x, new_y))
        self.update_plot()
     else:
        # Open manual input popup
        self.open_add_point_popup()

    
    def undo(self):
        """Undo last change."""
        if self.points:
            self.redo_stack.append(self.points.pop())
            self.update_plot()
    
    def redo(self):
        """Redo last undone change."""
        if self.redo_stack:
            self.points.append(self.redo_stack.pop())
            self.update_plot()
    
    def export_plot(self):
        """Export the plot as an image."""
        self.figure.savefig("plot.png")
    
    def change_line_style(self, event):
        """Change line style dynamically."""
        self.line_style = self.line_style_combo.get()
        self.update_plot()
    
    def change_line_color(self, event):
        """Change line color dynamically."""
        self.line_color = self.line_color_combo.get()
        self.update_plot()
    
    def change_marker_size(self, value):
        """Adjust marker size dynamically."""
        self.marker_size = float(value)
        self.update_plot()
    
    def toggle_grid(self):
        """Toggle grid visibility."""
        self.update_plot()
    
    def toggle_legend(self):
        """Toggle legend visibility."""
        self.update_plot()

    def on_mouse_scroll(self, event):
     """Zoom in/out with mouse wheel."""
     xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()
     if event.button == 'up':
        self.ax.set_xlim([x * self.zoom_factor for x in xlim])
        self.ax.set_ylim([y * self.zoom_factor for y in ylim])
     elif event.button == 'down':
        self.ax.set_xlim([x / self.zoom_factor for x in xlim])
        self.ax.set_ylim([y / self.zoom_factor for y in ylim])
     self.canvas.draw()

    def on_mouse_drag(self, event):
     """Pan the plot by dragging the mouse."""
     if event.button == 1:  # left mouse button
        if self.prev_x is not None and self.prev_y is not None:
            dx = event.x - self.prev_x
            dy = event.y - self.prev_y
            
            # Apply a scaling factor to slow down the movement
            pan_scale = 0.1  # Adjust this value to make panning slower or faster
            dx *= pan_scale
            dy *= pan_scale

            # Apply a threshold to avoid small, unnecessary movement
            if abs(dx) > self.drag_threshold or abs(dy) > self.drag_threshold:
                xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()
                self.ax.set_xlim([x + dx for x in xlim])
                self.ax.set_ylim([y + dy for y in ylim])
                self.canvas.draw()
        
        # Update the previous mouse position
        self.prev_x, self.prev_y = event.x, event.y


if __name__ == "__main__":
    root = tk.Tk()
    app = InteractivePlot(root)
    root.mainloop()
