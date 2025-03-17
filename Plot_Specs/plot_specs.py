import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backend_bases import MouseEvent
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import os

class ComplexPlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Data Plot GUI")
        self.root.geometry("1400x900")

        self.current_line_style = "-"  # Default line style
        self.current_line_color = "blue"  # Default line color
        self.current_marker_style = "o"  # Default marker style
        self.current_x_axis_label = "X-axis"
        self.current_y_axis_label = "Y-axis"
        self.current_chart_title = "Advanced Plot"
        self.current_show_gridlines = False
        self.current_legend_position = 1

        # Data Placeholder
        self.data = pd.DataFrame({'X': [1, 2, 3, 4], 'Y': [10, 20, 25, 30], 'Category': ['A', 'B', 'A', 'B']})
        self.filtered_data = self.data.copy()

        # Undo/Redo Stack
        self.history = []
        self.redo_stack = []

        # Persistent Annotations
        self.annotations = []

        # Main Notebook for Tabbed Navigation
        self.notebook = ttk.Notebook(root , padding=[20,10])
        self.notebook.pack(fill="both", expand=True)


        # Tabs
        self.create_plot_tab()
        self.create_axis_range_tab()
        self.create_chart_properties_tab()
        self.create_subplot_properties_tab()
        self.create_data_management_tab()
        self.create_transformation_tab()
        self.create_export_tab()
        self.create_database_tab()
        self.create_theme_tab()
        
          # Add this here


    def apply_global_background(self):
      """Apply a global background color to all subplots."""
      # Get the selected color from the dropdown
      selected_color = self.bg_color_combo.get()

      # Apply the background color to all subplots
      for ax in self.figure.axes:
        ax.set_facecolor(selected_color)

      # Apply the background color to the entire figure (background behind all subplots)
      self.figure.patch.set_facecolor(selected_color)

      # Redraw the canvas to reflect the background changes
      self.canvas.draw()


    def apply_subplot_properties(self):
      """Apply properties to the selected subplot."""
      if not self.subplot_selector.get():
        messagebox.showerror("Error", "No subplot selected to apply changes.")
        return

      selected_index = int(self.subplot_selector.get().split()[-1]) - 1
      if selected_index >= len(self.figure.axes) or selected_index < 0:
        messagebox.showerror("Error", "Invalid subplot selected.")
        return

      # Get the selected subplot
      ax = self.figure.axes[selected_index]

      # Set title and labels for the subplot
      ax.set_title(self.subplot_title_entry.get())
      ax.set_xlabel(self.x_axis_entry.get())
      ax.set_ylabel(self.y_axis_entry.get())

      # Redraw the canvas to reflect changes
      self.canvas.draw()

    
    def apply_global_subplot_properties(self):
      """Apply properties to all subplots."""
      # Loop through all subplots in the figure
      for ax in self.figure.axes:
        # Set title and labels for each subplot
        ax.set_title(self.subplot_title_entry.get())
        ax.set_xlabel(self.x_axis_entry.get())
        ax.set_ylabel(self.y_axis_entry.get())

      # Redraw the canvas to reflect changes
      self.canvas.draw()



    def load_subplot_settings(self, event=None):
      """Load settings for the selected subplot."""
      if not self.subplot_selector.get():
        return

      # Get the selected subplot index
      selected_index = int(self.subplot_selector.get().split()[-1]) - 1
      if selected_index < 0 or selected_index >= len(self.figure.axes):
        messagebox.showerror("Error", "Invalid subplot selected.")
        return

      # Load subplot properties
      ax = self.figure.axes[selected_index]
      self.subplot_title_entry.delete(0, tk.END)
      self.subplot_title_entry.insert(0, ax.get_title())
      self.x_axis_entry.delete(0, tk.END)
      self.x_axis_entry.insert(0, ax.get_xlabel())
      self.y_axis_entry.delete(0, tk.END)
      self.y_axis_entry.insert(0, ax.get_ylabel())


    def add_subplot(self):
      """Add a new subplot dynamically."""
      # Determine the new subplot index
      new_subplot_index = len(self.figure.axes) + 1
      ax = self.figure.add_subplot(1, new_subplot_index, new_subplot_index)
      ax.set_title(f"Subplot {new_subplot_index}")
    
      # Update the subplot selector dropdown with new subplot options
      self.subplot_selector['values'] = [f"Subplot {i+1}" for i in range(len(self.figure.axes))]
      self.subplot_selector.set(f"Subplot {new_subplot_index}")  # Set the newly added subplot as selected
    
      # Redraw the plot
      self.canvas.draw()

    def remove_subplot(self):
      """Remove the selected subplot."""
      if not self.subplot_selector.get():
        messagebox.showerror("Error", "No subplot selected to remove.")
        return

      selected_index = int(self.subplot_selector.get().split()[-1]) - 1
    
      if selected_index >= len(self.figure.axes) or selected_index < 0:
        messagebox.showerror("Error", "Invalid subplot selected.")
        return

      # Remove the selected subplot
      self.figure.delaxes(self.figure.axes[selected_index])
    
      # Update the subplot selector dropdown
      self.subplot_selector['values'] = [f"Subplot {i+1}" for i in range(len(self.figure.axes))]
      if self.figure.axes:
        self.subplot_selector.set(self.subplot_selector['values'][-1])  # Set the last subplot as selected
      else:
        self.subplot_selector.set("")  # No subplots left, clear selection
    
      # Redraw the plot
      self.canvas.draw()


    def create_subplot_properties_tab(self):
       """Dynamic Subplot Management and Properties Tab."""
       tab = ttk.Frame(self.notebook)
       self.notebook.add(tab, text="   Subplot Properties   ")

       frame = ttk.Frame(tab)
       frame.place(relx = 0.3 , rely = 0.1)

       # Subplot Selector
       ttk.Label(frame, text="Select Subplot:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
       self.subplot_selector = ttk.Combobox(frame, values=[], state="readonly")
       self.subplot_selector.grid(row=0, column=1, padx=10, pady=20)
       self.subplot_selector.bind("<<ComboboxSelected>>", self.load_subplot_settings)

       # Add and Remove Subplot Buttons
       ttk.Button(frame, text="Add Subplot", command=self.add_subplot).grid(row=0, column=2, padx=10, pady=30)
       ttk.Button(frame, text="Remove Subplot", command=self.remove_subplot).grid(row=0, column=3, padx=10, pady=30)

       # Subplot Title
       ttk.Label(frame, text="Subplot Title:").grid(row=1, column=0, padx=10, pady=30, sticky="w")
       self.subplot_title_entry = ttk.Entry(frame)
       self.subplot_title_entry.grid(row=1, column=1, padx=10, pady=30)

       # X-axis Label
       ttk.Label(frame, text="X-axis Label:").grid(row=2, column=0, padx=10, pady=30, sticky="w")
       self.x_axis_entry = ttk.Entry(frame)
       self.x_axis_entry.grid(row=2, column=1, padx=10, pady=30)

       # Y-axis Label
       ttk.Label(frame, text="Y-axis Label:").grid(row=3, column=0, padx=10, pady=30, sticky="w")
       self.y_axis_entry = ttk.Entry(frame)
       self.y_axis_entry.grid(row=3, column=1, padx=10, pady=30)

       # Apply Changes to Subplot
       ttk.Button(frame, text="Apply to Subplot", command=self.apply_subplot_properties).grid(row=4, column=0, columnspan=2, pady=30)

       # Apply Changes to All Subplots
       ttk.Button(frame, text="Apply to All Subplots", command=self.apply_global_subplot_properties).grid(row=5, column=0, columnspan=2, pady=30)

       # Background Color for All Subplots
       ttk.Label(frame, text="Plot Background Color (Global):").grid(row=6, column=0, padx=10, pady=30, sticky="w")
       self.bg_color_combo = ttk.Combobox(frame, values=["white", "black", "lightgrey", "skyblue", "pink"])
       self.bg_color_combo.set("white")
       self.bg_color_combo.grid(row=6, column=1, padx=10, pady=10)

       # Apply Global Background Color
       ttk.Button(frame, text="Apply Global Background", command=self.apply_global_background).grid(row=6, column=2, padx=10, pady=30) 
       # Subplot Add/Remove Buttons
       ttk.Button(frame, text="Add Subplot", command=self.add_subplot).grid(row=0, column=2, padx=10, pady=30)
       ttk.Button(frame, text="Remove Subplot", command=self.remove_subplot).grid(row=0, column=3, padx=10, pady=30)
       # Apply Changes to All Subplots
       # Apply Global Background Color
       ttk.Button(frame, text="Apply Global Background", command=self.apply_global_background).grid(row=6, column=2, padx=10, pady=30)



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

     # Embed the figure in the GUI (Initialize canvas before update_plot)
     self.canvas = FigureCanvasTkAgg(self.figure, tab)
     self.canvas_widget = self.canvas.get_tk_widget()
     self.canvas_widget.pack(fill="both", expand=True)

     # Initialize tooltips and right-click menu
     self.enable_tooltip_deletion()

     # Initial Plot
     self.points = [(1, 10), (2, 20), (3, 25), (4, 30)] # Initialize with some points
     self.update_plot()

     # Controls Frame for buttons
     controls_frame = ttk.Frame(tab)
     controls_frame.pack(side="bottom", fill="x", pady=5)

     # Add buttons for interactivity
     ttk.Button(controls_frame, text="Zoom In", command=self.zoom_in).pack(side="left", padx=5)
     ttk.Button(controls_frame, text="Zoom Out", command=self.zoom_out).pack(side="left", padx=5)
     ttk.Button(controls_frame, text="Reset View", command=self.reset_view).pack(side="left", padx=5)
     ttk.Button(controls_frame, text="Add Point", command=self.add_point).pack(side="left", padx=5)
     ttk.Button(controls_frame, text="Remove Last Point", command=self.remove_point).pack(side="left", padx=5)
     ttk.Button(controls_frame, text="Edit Point", command=self.edit_point).pack(side="left", padx=5)

     # Connect canvas events for interactive editing
     self.canvas.mpl_connect("button_press_event", self.on_click)
     self.canvas.mpl_connect("motion_notify_event", self.on_hover)
     self.canvas.mpl_connect("button_release_event", self.on_release)

     self.selected_point = None  # For dragging points

     self.tooltip = None
     self.canvas.mpl_connect("motion_notify_event", self.show_tooltip)
     self.canvas.mpl_connect("button_press_event", self.on_double_click)
     self.canvas.mpl_connect("button_press_event", self.handle_mouse_events)



    def apply_chart_properties(self):
     """Apply Chart Property Changes."""
     self.update_plot()

     # Update Title
     self.ax.set_title(self.title_entry.get())

     # Update Axis Labels
     self.ax.set_xlabel(self.x_axis_entry.get())
     self.ax.set_ylabel(self.y_axis_entry.get())

     # Update Line Style, Color, and Marker
     self.current_line_style = self.line_style_combo.get()
     self.current_line_color = self.line_color_combo.get()
     self.current_marker_style = self.marker_style_combo.get()

     for line in self.ax.lines:
        line.set_linestyle(self.current_line_style)
        line.set_color(self.current_line_color)
        line.set_marker(self.current_marker_style)

     # Toggle Gridlines
     self.ax.grid(self.grid_toggle_var.get())

     # Update Legend Position
     self.ax.legend(loc=self.legend_position_combo.get())

     # Redraw the canvas
     self.canvas.draw()


    def create_axis_range_tab(self):
     """Add axis range controls to the Interactive Plot tab."""
     tab = self.notebook.nametowidget(self.notebook.tabs()[0])  # Get the Interactive Plot tab

     range_frame = ttk.Frame(tab)
     range_frame.pack(fill="x", pady=10)

     # X-Axis Range Controls
     ttk.Label(range_frame, text="X-Axis Min:").grid(row=0, column=0, padx=5, pady=5)
     self.x_min_entry = ttk.Entry(range_frame, width=10)
     self.x_min_entry.grid(row=0, column=1, padx=5, pady=5)

     ttk.Label(range_frame, text="X-Axis Max:").grid(row=0, column=2, padx=5, pady=5)
     self.x_max_entry = ttk.Entry(range_frame, width=10)
     self.x_max_entry.grid(row=0, column=3, padx=5, pady=5)

     # Y-Axis Range Controls
     ttk.Label(range_frame, text="Y-Axis Min:").grid(row=1, column=0, padx=5, pady=5)
     self.y_min_entry = ttk.Entry(range_frame, width=10)
     self.y_min_entry.grid(row=1, column=1, padx=5, pady=5)

     ttk.Label(range_frame, text="Y-Axis Max:").grid(row=1, column=2, padx=5, pady=5)
     self.y_max_entry = ttk.Entry(range_frame, width=10)
     self.y_max_entry.grid(row=1, column=3, padx=5, pady=5)

     # Apply Button
     ttk.Button(range_frame, text="Apply", command=self.apply_axis_ranges).grid(row=2, column=0, columnspan=4, pady=10)

    def apply_axis_ranges(self):
     """Apply the custom axis ranges based on user input."""
     try:
        x_min = float(self.x_min_entry.get()) if self.x_min_entry.get() else None
        x_max = float(self.x_max_entry.get()) if self.x_max_entry.get() else None
        y_min = float(self.y_min_entry.get()) if self.y_min_entry.get() else None
        y_max = float(self.y_max_entry.get()) if self.y_max_entry.get() else None

        self.ax.set_xlim(left=x_min, right=x_max)
        self.ax.set_ylim(bottom=y_min, top=y_max)
        self.canvas.draw()
     except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for axis ranges.")




    def create_data_management_tab(self):
        """Data Management Tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="   Data Management   ")

        # Filtering Section
        ttk.Label(tab, text="Filter Data By:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.filter_type = ttk.Combobox(tab, values=["Numeric Ranges", "Outlier Detection", "Specific Values", "Boolean Filtering"])
        self.filter_type.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(tab, text="Apply Filter", command=self.apply_filter).grid(row=0, column=2, padx=10, pady=10)

        # Multi-category Selection
        ttk.Label(tab, text="Select Categories:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.category_selection = tk.Listbox(tab, selectmode="multiple", height=5, exportselection=False)
        self.category_selection.grid(row=1, column=1, padx=10, pady=10)
        # Populate with Categories from Data
        for category in self.data['Category'].unique():
            self.category_selection.insert(tk.END, category)


    def create_chart_properties_tab(self):
        """Dynamic Chart Editing and Properties Tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="   Chart Properties   ")

        frame = ttk.Frame(tab)
        frame.place(relx=0.35, rely=0.1)

        # Chart Title
        ttk.Label(frame, text="Chart Title:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.title_entry = ttk.Entry(frame)
        self.title_entry.insert(0, "Advanced Plot")
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        # X-axis Label
        ttk.Label(frame, text="X-axis Label:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.x_axis_entry = ttk.Entry(frame)
        self.x_axis_entry.insert(0, "X-axis")
        self.x_axis_entry.grid(row=1, column=1, padx=10, pady=10)

        # Y-axis Label
        ttk.Label(frame, text="Y-axis Label:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.y_axis_entry = ttk.Entry(frame)
        self.y_axis_entry.insert(0, "Y-axis")
        self.y_axis_entry.grid(row=2, column=1, padx=10, pady=10)

        # Line Style
        ttk.Label(frame, text="Line Style:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.line_style_combo = ttk.Combobox(frame, values=["-", "--", "-.", ":", "None"])
        self.line_style_combo.set("-")
        self.line_style_combo.grid(row=3, column=1, padx=10, pady=10)

        # Line Color
        ttk.Label(frame, text="Line Color:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.line_color_combo = ttk.Combobox(frame, values=["blue", "red", "green", "black", "cyan"])
        self.line_color_combo.set("blue")
        self.line_color_combo.grid(row=4, column=1, padx=10, pady=10)

        # Marker Style
        ttk.Label(frame, text="Marker Style:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.marker_style_combo = ttk.Combobox(frame, values=["o", "s", "^", "D", "*", "+", "None"])
        self.marker_style_combo.set("o")
        self.marker_style_combo.grid(row=5, column=1, padx=10, pady=10)

        # Grid Toggle
        self.grid_toggle_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Show Gridlines", variable=self.grid_toggle_var).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Legend Position
        ttk.Label(frame, text="Legend Position:").grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.legend_position_combo = ttk.Combobox(frame, values=["upper right", "upper left", "lower right", "lower left", "center"])
        self.legend_position_combo.set("upper right")
        self.legend_position_combo.grid(row=7, column=1, padx=10, pady=10)

        # Apply Changes Button
        ttk.Button(frame, text="Apply Changes", command=self.apply_chart_properties).grid(row=8, column=0, columnspan=2, pady=20)


    def on_click(self, event):
     """Handle single left-click to select points (but NOT create tooltips)."""
     if event.inaxes != self.ax:
        return  # Ignore clicks outside the plot

     self.last_click_coords = (event.xdata, event.ydata)  # Track last click

     # Ensure this function does NOT create tooltips
     self.selected_annotation = None
     if self.annotations:
        for annotation in self.annotations:
            x, y = annotation.xy
            if abs(event.xdata - x) < 0.2 and abs(event.ydata - y) < 0.2:
                self.selected_annotation = annotation
                break

     self.canvas.draw_idle()




    
    def handle_mouse_events(self, event):
     """Ensure tooltips are created ONLY on double-clicks."""
     print(f"handle_mouse_events triggered: event.button = {event.button}, event.dblclick = {event.dblclick}")

     if event.dblclick:  # This ensures ONLY double-click creates tooltips
        print("Double-click detected, calling on_double_click()")
        self.on_double_click(event)
     elif event.button == 1:  # Left-click should NOT create tooltips
        print("Single left-click detected, calling on_click()")
        self.on_click(event)
     elif event.button == 3:  # Right-click for tooltip deletion
        print("Right-click detected, calling enable_tooltip_deletion()")
        self.enable_tooltip_deletion()




    def on_release(self, event):
     """Handle mouse button release to stop dragging."""
     if self.selected_point is not None:
        # Finalize the position of the dragged point
        new_x, new_y = self.points[self.selected_point]

        # Update the annotation for the selected point
        annotation = self.annotations[self.selected_point]
        annotation.xy = (new_x, new_y)
        annotation.set_position((new_x + 10, new_y + 10))  # Offset for better visibility

        # Clear the selected point
        self.selected_point = None

     self.apply_chart_properties()
     self.update_plot()


    def on_double_click(self, event):
     """Handle double-click events to persist a label above or below a point."""
     if event.inaxes != self.ax:
        return

     # Check if an annotation already exists at this location
     for annotation in self.annotations:
        x, y = annotation.xy
        if abs(event.xdata - x) < 0.2 and abs(event.ydata - y) < 0.2:
            print("Annotation already exists at this point.")
            return  # Don't add duplicate annotations

     # Default behavior if no existing annotation is found
     x_new, y_new = event.xdata, event.ydata  # Use event values directly
     offset = 15 if y_new < self.ax.get_ylim()[1] / 2 else -15  # Adjust placement

     annotation = self.ax.annotate(
        f"({x_new:.2f}, {y_new:.2f})",
        xy=(x_new, y_new),
        xytext=(0, offset),
        textcoords="offset points",
        ha='center',
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"),
        fontsize=9
     )
    
     self.annotations.append(annotation)
     self.canvas.draw_idle()





    def on_hover(self, event):
     """Handle mouse hover events for dragging points."""
     if event.inaxes != self.ax or self.selected_point is None:
        return

     # Update the position of the selected point
     new_x, new_y = event.xdata, event.ydata
     self.points[self.selected_point] = (new_x, new_y)

     # Ensure annotation moves with the point
     for annotation in self.annotations:
        x, y = annotation.xy
        if abs(x - new_x) < 0.2 and abs(y - new_y) < 0.2:
            annotation.xy = (new_x, new_y)
            annotation.set_position((new_x + 10, new_y + 10))  # Offset for better visibility
            break

     self.apply_chart_properties()
     self.update_plot()





    def add_point(self):
     """Add a new point at a default location."""
     if self.points:
        new_x = self.points[-1][0] + 1  # Increment X value by 1
     else:
        new_x = 1  # Default starting X value
     new_y = 0  # Default Y value
     self.points.append((new_x, new_y))

     self.apply_chart_properties()
     self.update_plot()


    def remove_point(self):
     """Remove the last added point."""
     if self.points:
        self.points.pop()
        self.apply_chart_properties()
        self.update_plot()
     else:
        messagebox.showinfo("Info", "No points to remove!")

    
    def edit_point(self):
     """Edit the selected point via dialog."""
     if self.selected_point is None:
        messagebox.showinfo("Info", "No point selected for editing!")
        return

     # Create a dialog to edit the point
     def save_edit():
        try:
            new_x = float(x_entry.get())
            new_y = float(y_entry.get())
            self.points[self.selected_point] = (new_x, new_y)
            self.update_plot()
            edit_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter numeric values.")

     edit_window = tk.Toplevel(self.root)
     edit_window.title("Edit Point")

     ttk.Label(edit_window, text="X:").grid(row=0, column=0, padx=5, pady=5)
     x_entry = ttk.Entry(edit_window)
     x_entry.insert(0, str(self.points[self.selected_point][0]))
     x_entry.grid(row=0, column=1, padx=5, pady=5)

     ttk.Label(edit_window, text="Y:").grid(row=1, column=0, padx=5, pady=5)
     y_entry = ttk.Entry(edit_window)
     y_entry.insert(0, str(self.points[self.selected_point][1]))
     y_entry.grid(row=1, column=1, padx=5, pady=5)

     ttk.Button(edit_window, text="Save", command=save_edit).grid(row=2, column=0, columnspan=2, pady=10)




    def create_transformation_tab(self):
        """Data Transformation Tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="   Data Transformation   ")

        # Transformation Options
        ttk.Label(tab, text="Apply Transformation:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.transformation_type = ttk.Combobox(tab, values=["Normalization", "Aggregation (Sum)", "Custom Expression"])
        self.transformation_type.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(tab, text="Apply", command=self.apply_transformation).grid(row=0, column=2, padx=10, pady=10)

        # Custom Expression Entry
        ttk.Label(tab, text="Custom Expression:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.custom_expression_entry = ttk.Entry(tab)
        self.custom_expression_entry.grid(row=1, column=1, padx=10, pady=10)


    def create_theme_tab(self):
        """Styling and Themes Tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="   Styling & Themes   ")

        ttk.Label(tab, text="Select Theme:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.theme_selection = ttk.Combobox(tab, values=["Default", "Dark", "Light", "Seaborn"])
        self.theme_selection.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(tab, text="Apply Theme", command=self.apply_theme).grid(row=0, column=2, padx=10, pady=10)

    def create_export_tab(self):
        """Export Options Tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="   Export Options   ")

        # Export options
        ttk.Label(tab, text="Export Format:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.export_format = ttk.Combobox(tab, values=["PNG", "PDF"])
        self.export_format.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(tab, text="Export", command=self.export_plot).grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(tab, text="Resolution (DPI):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.dpi_entry = ttk.Entry(tab)
        self.dpi_entry.insert(0, "100")
        self.dpi_entry.grid(row=1, column=1, padx=10, pady=10)

    def create_database_tab(self):
        """Database Integration Tab."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="   Database Integration   ")

        ttk.Label(tab, text="Database Connection:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(tab, text="Connect to Database", command=self.connect_to_database).grid(row=0, column=1, padx=10, pady=10)

    def update_plot(self):
     """Redraw the plot with the current points."""
     self.ax.clear()
     self.ax.set_title("Advanced Plot")
     self.ax.set_xlabel("X-axis")
     self.ax.set_ylabel("Y-axis")

     x_data, y_data = zip(*self.points) if self.points else ([], [])
     self.ax.plot(
        x_data,
        y_data,
        marker=self.current_marker_style,
        color=self.current_line_color,
        linestyle=self.current_line_style,
        label="Data Points"

     )

     # Redraw persistent annotations
     for annotation in self.annotations:
            self.ax.add_artist(annotation)

     # Set the chart title and axis labels
     self.ax.set_title(self.current_chart_title)
     self.ax.set_xlabel(self.current_x_axis_label)
     self.ax.set_ylabel(self.current_y_axis_label)

     # Configure gridlines visibility
     self.ax.grid(self.current_show_gridlines)

     # Set the position of the legend
     self.ax.legend(loc=self.current_legend_position)

     self.canvas.draw()

    
    def show_tooltip(self, event):
     """Display tooltip ONLY on hover, NOT on clicks."""
     if event.inaxes != self.ax:
        return  # Ignore if outside the plot

     # Debug: Print when show_tooltip is triggered
     print(f"show_tooltip triggered: event.button = {event.button}")

     if event.button is not None:  
        print("Blocked tooltip creation because it was a click event.")
        return  # Ensures tooltips ONLY appear on hover

     for x, y in self.points:
        if abs(event.xdata - x) < 0.2 and abs(event.ydata - y) < 0.2:
            print(f"Tooltip added at: ({x}, {y})")
            if self.tooltip:
                self.tooltip.set_visible(False)  # Hide previous tooltip before adding a new one
            self.tooltip = self.ax.annotate(
                f"({x:.2f}, {y:.2f})",
                xy=(x, y),
                xytext=(10, 10),
                textcoords="offset points",
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"),
                fontsize=9
            )
            self.canvas.draw_idle()
            return

     # Hide tooltip if no match
     if self.tooltip:
        print("Hiding tooltip")
        self.tooltip.set_visible(False)
        self.canvas.draw_idle()


    
    def enable_tooltip_deletion(self):
     """Enable a right-click context menu to delete tooltips."""
     self.context_menu = tk.Menu(self.canvas.get_tk_widget(), tearoff=0)
     self.context_menu.add_command(label="Delete Tooltip", command=self.delete_tooltip)
    
     def on_right_click(event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

     self.canvas.get_tk_widget().bind("<Button-3>", on_right_click)


    def delete_tooltip(self):
     """Delete the selected or closest annotation, even if not visible."""
     if not self.annotations:
        return  # No annotations to delete

     # If an annotation was selected, delete it
     if hasattr(self, "selected_annotation") and self.selected_annotation:
        if self.selected_annotation in self.annotations:
            self.selected_annotation.remove()  # Remove from plot
            self.annotations.remove(self.selected_annotation)  # Remove from list
        self.selected_annotation = None
        self.canvas.draw_idle()
        return

     # If no annotation is selected, remove the closest one to the last click
     if hasattr(self, "last_click_coords"):
        x_click, y_click = self.last_click_coords
        closest_annotation = None
        min_distance = float("inf")

        for annotation in self.annotations:
            x, y = annotation.xy
            distance = (x - x_click) ** 2 + (y - y_click) ** 2  # Euclidean distance squared
            if distance < min_distance:
                min_distance = distance
                closest_annotation = annotation

        if closest_annotation:
            closest_annotation.remove()
            self.annotations.remove(closest_annotation)

     self.canvas.draw_idle()





    def zoom_in(self):
        """Zoom into the plot."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0] + (xlim[1] - xlim[0]) * 0.1, xlim[1] - (xlim[1] - xlim[0]) * 0.1])
        self.ax.set_ylim([ylim[0] + (ylim[1] - ylim[0]) * 0.1, ylim[1] - (ylim[1] - ylim[0]) * 0.1])
        self.canvas.draw()

    def zoom_out(self):
        """Zoom out of the plot."""
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0] - (xlim[1] - xlim[0]) * 0.1, xlim[1] + (xlim[1] - xlim[0]) * 0.1])
        self.ax.set_ylim([ylim[0] - (ylim[1] - ylim[0]) * 0.1, ylim[1] + (ylim[1] - ylim[0]) * 0.1])
        self.canvas.draw()

    # Continuing from the error and completing the implementation

    def reset_view(self):
        """Reset plot view to default."""
        self.ax.set_xlim([self.data['X'].min(), self.data['X'].max()])
        self.ax.set_ylim([self.data['Y'].min(), self.data['Y'].max()])
        self.canvas.draw()

    def apply_filter(self):
        """Apply filters to the data."""
        selected_filter = self.filter_type.get()
        if selected_filter == "Numeric Ranges":
            self.filtered_data = self.data[(self.data['Y'] > 10) & (self.data['Y'] < 30)]  # Example filter
            messagebox.showinfo("Filter Applied", "Numeric range filter applied!")
        elif selected_filter == "Outlier Detection":
            q1 = self.data['Y'].quantile(0.25)
            q3 = self.data['Y'].quantile(0.75)
            iqr = q3 - q1
            self.filtered_data = self.data[(self.data['Y'] >= q1 - 1.5 * iqr) & (self.data['Y'] <= q3 + 1.5 * iqr)]
            messagebox.showinfo("Filter Applied", "Outliers removed using IQR!")
        elif selected_filter == "Specific Values":
            selected_categories = [self.category_selection.get(i) for i in self.category_selection.curselection()]
            self.filtered_data = self.data[self.data['Category'].isin(selected_categories)]
            messagebox.showinfo("Filter Applied", f"Filtered by categories: {', '.join(selected_categories)}")
        elif selected_filter == "Boolean Filtering":
            self.filtered_data = self.data[(self.data['Y'] > 10) & (self.data['Category'] == 'A')]  # Example boolean
            messagebox.showinfo("Filter Applied", "Boolean filtering applied!")
        else:
            messagebox.showerror("Error", "Please select a valid filter type.")
        self.update_plot()

    def apply_transformation(self):
        """Apply transformations to the data."""
        selected_transformation = self.transformation_type.get()
        if selected_transformation == "Normalization":
            self.filtered_data['Y'] = (self.filtered_data['Y'] - self.filtered_data['Y'].min()) / (
                        self.filtered_data['Y'].max() - self.filtered_data['Y'].min())
            messagebox.showinfo("Transformation Applied", "Data normalized!")
        elif selected_transformation == "Aggregation (Sum)":
            self.filtered_data = self.filtered_data.groupby('Category', as_index=False).sum()
            messagebox.showinfo("Transformation Applied", "Data aggregated by sum!")
        elif selected_transformation == "Custom Expression":
            expression = self.custom_expression_entry.get()
            try:
                self.filtered_data['Y'] = self.filtered_data.eval(expression)
                messagebox.showinfo("Transformation Applied", f"Custom expression '{expression}' applied!")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid expression: {e}")
        else:
            messagebox.showerror("Error", "Please select a transformation type.")
        self.update_plot()

    def update_axes(self):
        """Update axes labels based on user input."""
        x_label = self.x_label_entry.get()
        y_label = self.y_label_entry.get()
        self.ax.set_xlabel(x_label if x_label else "X-axis")
        self.ax.set_ylabel(y_label if y_label else "Y-axis")
        self.canvas.draw()

    def apply_theme(self):
        """Apply a selected theme to the plot."""
        selected_theme = self.theme_selection.get()
        if selected_theme == "Default":
            self.figure.patch.set_facecolor("white")
            self.ax.set_facecolor("white")
        elif selected_theme == "Dark":
            self.figure.patch.set_facecolor("black")
            self.ax.set_facecolor("gray")
        elif selected_theme == "Light":
            self.figure.patch.set_facecolor("white")
            self.ax.set_facecolor("lightyellow")
        elif selected_theme == "Seaborn":
            self.ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
        else:
            messagebox.showerror("Error", "Invalid theme selected.")
        self.canvas.draw()

    def export_plot(self):
        """Export the current plot."""
        format = self.export_format.get()
        dpi = int(self.dpi_entry.get()) if self.dpi_entry.get().isdigit() else 100
        if format in ["PNG", "PDF"]:
            filepath = filedialog.asksaveasfilename(defaultextension=f".{format.lower()}",
                                                    filetypes=[(format, f"*.{format.lower()}")])
            if filepath:
                self.figure.savefig(filepath, dpi=dpi)
                messagebox.showinfo("Export Successful", f"Plot saved as {filepath}")
        else:
            messagebox.showerror("Error", "Please select a valid export format.")

    def connect_to_database(self):
        """Placeholder for database integration."""
        messagebox.showinfo("Database Connection", "Database connection feature not yet implemented.")


# Create the main application window
root = tk.Tk()
complex_app = ComplexPlotApp(root)
root.mainloop()

