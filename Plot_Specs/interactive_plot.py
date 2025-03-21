import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import colorchooser

class InteractivePlot:
    def __init__(self, root):

        self.root = root
        self.root.title("Interactive Plot Editor")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.point_attributes = {}  # Store attributes like color and size per point

        self.font_settings_title = {}
        self.font_settings_xlabel = {}
        self.font_settings_ylabel = {}
        
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


    def apply_legend(self):
     """Save user-defined legend labels and update plot."""
     self.legend_labels = [entry.get() for entry in self.legend_entries]
     self.legend_popup.destroy()
     self.update_plot()


    def customize_legend(self):
     """Popup window for manual legend customization."""
     self.legend_popup = tk.Toplevel(self.root)
     self.legend_popup.title("Customize Legend")
     self.legend_popup.geometry("300x200")

     ttk.Label(self.legend_popup, text="Enter legend labels:").pack(pady=10)
    
     self.legend_entries = []
     for i in range(len(self.points)):  # One entry per data series
        frame = ttk.Frame(self.legend_popup)
        frame.pack(pady=2, fill="x")

        ttk.Label(frame, text=f"Label {i+1}:").pack(side="left", padx=5)
        entry = ttk.Entry(frame)
        entry.pack(side="left", expand=True, fill="x")
        entry.insert(0, f"Data {i+1}")  # Default label
        self.legend_entries.append(entry)

     ttk.Button(self.legend_popup, text="Apply", command=self.apply_legend).pack(pady=10)


    def open_color_picker(self):
     """Open a color picker and update the line color."""
     color_code = colorchooser.askcolor(title="Choose Line Color")[1]  # Get hex code
     if color_code:  # If the user picked a color, update it
        self.line_color = color_code
        self.line_color_combo.set("Custom")  # Show "Custom" in dropdown
        self.update_plot()

    
    def open_line_style_window(self):
     """Open a pop-up window to enter a custom line style."""
     style_window = tk.Toplevel(self.root)
     style_window.title("Custom Line Style")
     style_window.geometry("250x150")

     ttk.Label(style_window, text="Enter Line Style:").pack(pady=5)
     style_entry = ttk.Entry(style_window)
     style_entry.pack(pady=5)

     def apply_style():
        """Apply the entered line style."""
        new_style = style_entry.get()
        if new_style:
            self.line_style = new_style
            self.line_style_combo.set("Custom")  # Show "Custom" in dropdown
            self.update_plot()
        style_window.destroy()

     ttk.Button(style_window, text="Apply", command=apply_style).pack(pady=10)


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

        # Store original limits for reset function
        self.original_xlim = self.ax.get_xlim()
        self.original_ylim = self.ax.get_ylim()

        # Add Zoom Buttons
        ttk.Button(controls_frame, text="Zoom In", command=lambda: self.zoom(True)).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Zoom Out", command=lambda: self.zoom(False)).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Reset Zoom", command=self.reset_zoom).pack(side="left", padx=5)

        # **New Reset Button**
        ttk.Button(controls_frame, text="Reset", command=self.reset_plot).pack(side="left", padx=5)
        
        # Line Color
        ttk.Label(controls_frame, text="Line Color:").pack(side="left", padx=5)
        self.line_color_combo = ttk.Combobox(controls_frame, values=["blue", "red", "green", "black", "Custom"], state="readonly")
        self.line_color_combo.pack(side="left", padx=5)
        self.line_color_combo.set(self.line_color)
        self.line_color_combo.bind("<<ComboboxSelected>>", self.change_line_color)

        ttk.Button(controls_frame, text="Custom Color", command=self.open_color_picker).pack(side="left", padx=5)

        # Line Style
        ttk.Label(controls_frame, text="Line Style:").pack(side="left", padx=5)
        self.line_style_combo = ttk.Combobox(controls_frame, values=["-", "--", "-.", ":", "Custom"], state="readonly")
        self.line_style_combo.pack(side="left", padx=5)
        self.line_style_combo.set(self.line_style)
        self.line_style_combo.bind("<<ComboboxSelected>>", self.change_line_style)

        ttk.Button(controls_frame, text="Custom Style", command=self.open_line_style_window).pack(side="left", padx=5)


        # Marker size adjustment
        ttk.Label(controls_frame, text="Marker Size:").pack(side="left", padx=5)
        self.marker_size_slider = ttk.Scale(controls_frame, from_=5, to=300, orient="horizontal", command=self.change_marker_size)
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
        # Connect double-click events
        self.canvas.mpl_connect("button_press_event", self.on_double_click)


        self.prev_x, self.prev_y = None, None  # For panning

    
    def on_double_click(self, event):
     """Detect double-click on title, xlabel, or ylabel to edit them."""
     if event.dblclick:  # Double-click detected
        if self.ax.title.contains(event)[0]:  
            self.edit_label("title")  # Edit title
        elif self.ax.xaxis.label.contains(event)[0]:  
            self.edit_label("xlabel")  # Edit X-axis label
        elif self.ax.yaxis.label.contains(event)[0]:  
            self.edit_label("ylabel")  # Edit Y-axis label

    
    def edit_label(self, label_type):
     """Popup window to edit title, xlabel, or ylabel with font customization."""
     self.label_popup = tk.Toplevel(self.root)
     self.label_popup.title("Edit Label")
     self.label_popup.geometry("400x300")

     ttk.Label(self.label_popup, text=f"Edit {label_type}:").pack(pady=5)
    
     self.label_entry = ttk.Entry(self.label_popup, width=30)
     self.label_entry.pack(pady=5)

     # Pre-fill with current text
     if label_type == "title":
        self.label_entry.insert(0, self.ax.get_title())
     elif label_type == "xlabel":
        self.label_entry.insert(0, self.ax.get_xlabel())
     elif label_type == "ylabel":
        self.label_entry.insert(0, self.ax.get_ylabel())

     # Font type selection
     ttk.Label(self.label_popup, text="Font:").pack(pady=5)
     self.font_var = tk.StringVar(value="Arial")
     font_options = ["Arial", "Times New Roman", "Courier New", "Verdana", "Comic Sans MS"]
     self.font_dropdown = ttk.Combobox(self.label_popup, values=font_options, textvariable=self.font_var, state="readonly")
     self.font_dropdown.pack()

     # Font size selection
     ttk.Label(self.label_popup, text="Font Size:").pack(pady=5)
     self.font_size_var = tk.IntVar(value=12)
     self.font_size_dropdown = ttk.Combobox(self.label_popup, values=[8, 10, 12, 14, 16, 18, 20, 24, 30], textvariable=self.font_size_var, state="readonly")
     self.font_size_dropdown.pack()

     # Bold & Italic checkboxes
     self.bold_var = tk.BooleanVar()
     self.italic_var = tk.BooleanVar()
     ttk.Checkbutton(self.label_popup, text="Bold", variable=self.bold_var).pack()
     ttk.Checkbutton(self.label_popup, text="Italic", variable=self.italic_var).pack()

     # Color selection button
     ttk.Button(self.label_popup, text="Change Color", command=lambda: self.pick_color(label_type)).pack(pady=5)

     # Apply button
     ttk.Button(self.label_popup, text="Apply", command=lambda: self.apply_label(label_type)).pack(pady=10)


    def pick_color(self, label_type):
     global color_code_sender  

     color_code = colorchooser.askcolor(title="Select Color")[1]  # Get HEX color
    
     if color_code:  # If user selected a color
        if label_type == "title":
            self.ax.title.set_color(color_code)
        elif label_type == "xlabel":
            self.ax.xaxis.label.set_color(color_code)
        elif label_type == "ylabel":
            self.ax.yaxis.label.set_color(color_code)

     
     color_code_sender = str(color_code)

     self.canvas.draw()  # Refresh plot

    
    def apply_label(self, label_type):
     
     """Apply new text, font, and style to title, xlabel, or ylabel."""
     new_text = self.label_entry.get()
     font_family = self.font_var.get()
     font_size = self.font_size_var.get()
     font_weight = "bold" if self.bold_var.get() else "normal"
     font_style = "italic" if self.italic_var.get() else "normal"
     

     if label_type == "title":
        self.font_settings_title = {
        "fontname": font_family,
        "fontsize": font_size,
        "fontweight": font_weight,
        "style": font_style,
        "color" : color_code_sender
        }
        self.ax.set_title(new_text, **self.font_settings_title)
     elif label_type == "xlabel":
        self.font_settings_xlabel = {
        "fontname": font_family,
        "fontsize": font_size,
        "fontweight": font_weight,
        "style": font_style,
        "color" : color_code_sender
        }
        self.ax.set_xlabel(new_text, **self.font_settings_xlabel)
     elif label_type == "ylabel":
        self.font_settings_ylabel = {
        "fontname": font_family,
        "fontsize": font_size,
        "fontweight": font_weight,
        "style": font_style,
        "color" : color_code_sender
        }
        self.ax.set_ylabel(new_text, **self.font_settings_ylabel)

     self.label_popup.destroy()  # Close popup
     self.canvas.draw()  # Refresh plot


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
     """Update the plot with latest data and attributes while preserving colors and styles."""
     # ✅ Save current title, xlabel, ylabel, and their properties
     current_title = self.ax.get_title()
     current_xlabel = self.ax.get_xlabel()
     current_ylabel = self.ax.get_ylabel()

     self.ax.cla()

     # ✅ Redraw points
     for (x, y) in self.points:
        attrs = self.point_attributes.get((x, y), {"color": "red", "size": self.marker_size})
        self.ax.scatter(x, y, color=attrs["color"], s=attrs["size"])

     x_vals, y_vals = zip(*self.points) if self.points else ([], [])
     self.ax.plot(x_vals, y_vals, linestyle=self.line_style, color=self.line_color, label="Data")

     # ✅ Restore title, xlabel, ylabel with colors and fonts
     self.ax.set_title(current_title, **self.font_settings_title)
     self.ax.set_xlabel(current_xlabel, **self.font_settings_xlabel)
     self.ax.set_ylabel(current_ylabel, **self.font_settings_ylabel)

     if self.grid_toggle_var.get():
        self.ax.grid(True)
     if self.legend_toggle_var.get():
        self.ax.legend(self.legend_labels)

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
     """Toggle legend visibility and close popup when unchecked."""
     if self.legend_toggle_var.get():
        self.customize_legend()  # Open popup for manual input
     else:
        self.legend_labels = ["Data"]  # Reset to default
        if hasattr(self, 'legend_popup') and self.legend_popup.winfo_exists():
            self.legend_popup.destroy()  # Close the popup if it's open
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