import tkinter as tk
from tkinter import ttk, Menu, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseButton
from tkinter import colorchooser, simpledialog
from scipy.spatial import KDTree
import matplotlib.patches as patches
import os
import pandas as pd
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

class InteractivePlot:
    def __init__(self):
        # Create main window using TkinterDnD
        self.root = TkinterDnD.Tk()
        self.root.title("Interactive Plot Editor")
        
        # Enhanced subplot management
        self.subplots = {}  # Format: {id: {'ax': ax, 'fig': fig, 'canvas': canvas, 'state': {...}}}
        self.active_subplot = None
        self.subplot_states = {}  # Track state for each subplot
        
        # Initialize drag and drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_file_drop)
        
        # Create notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # Initialize points and data structures
        self.points = np.array([(1, 10), (2, 20), (3, 25), (4, 30)])  # Initial points as numpy array
        self.point_labels = {}  # Dictionary for point labels
        self.annotations = {}  # Dictionary to store tooltips by point index
        self.dragging_idx = None  # Index of point being dragged
        self.is_dragging = False  # Flag to track dragging
        self.drag_start = None  # Position for drag start
        self.point_attributes = {}  # Store attributes like color and size per point

        # Track active plot elements (main or subplot)
        self.active_figure = None
        self.active_ax = None
        self.active_canvas = None

        # Custom label properties for persistent formatting
        self.custom_labels = {}

        # Default Styles
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
        self.initial_points = np.array([(1, 10), (2, 20), (3, 25), (4, 30)])  # Save the original state
        self.points = self.initial_points.copy()

        # Store original axis limits
        self.original_xlim = (0, 10)
        self.original_ylim = (0, 35)

        # Create KDTree for point proximity detection
        self.update_kdtree()

        # Undo/Redo functionality
        self.history = []  # Stack for undo operations
        self.redo_stack = []  # Stack for redo operations

        # Create initial plot tab
        self.create_plot_tab()

        # Add tab switching handler
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_switch)

    def update_kdtree(self):
        """Update the KDTree with current points"""
        if len(self.points) > 0:
            self.kdtree = KDTree(self.points)
        else:
            self.kdtree = None

    def on_mouse_move(self, event):
        """Handle moving and dragging of points and annotations."""
        if not hasattr(event, 'xdata') or not hasattr(event, 'ydata') or event.xdata is None or event.ydata is None:
            return

        # Store current limits to prevent chart movement
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Handle dragging a point
        if self.dragging_idx is not None:
            # Update the point position
            self.points[self.dragging_idx] = np.array([event.xdata, event.ydata])
            self.update_kdtree()

            # Update the scatter plot with new positions
            self.update_plot()

            # If this point has an annotation, update it too
            if self.dragging_idx in self.annotations:
                ann = self.annotations[self.dragging_idx]
                x, y = self.points[self.dragging_idx]

                # Update annotation position and text
                ann.xy = (x, y)
                ann.set_text(f"({x:.2f}, {y:.2f})")

            # Ensure axes don't change
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)

            # Redraw
            self.canvas.draw_idle()

    # on_click has been replaced by on_press and on_double_click methods
    # which provide more specific handling of different mouse interactions

    def on_release(self, event):
        """Handle mouse release events"""
        # Reset drag state
        self.dragging_idx = None
        self.is_dragging = False
        self.prev_x, self.prev_y = None, None

        # Reset cursor if it was changed
        self.canvas.get_tk_widget().config(cursor="")

    def on_hover(self, event):
        """This function is now disabled, tooltips should only appear when double-clicking on points."""
        # We now only create tooltips when double-clicking, not on hover
        return

    def update_tooltip_for_point(self, point_index, point_coords):
        """Create or update tooltip for a specific point"""
        # Remove existing tooltip
        self.remove_tooltip()

        # Create a new tooltip very close to the point
        self.tooltip = self.ax.annotate(
            f"({point_coords[0]:.2f}, {point_coords[1]:.2f})",
            xy=(point_coords[0], point_coords[1]),
            xytext=(point_coords[0] + 0.02, point_coords[1] + 0.02),  # Position closer to the point
            fontsize=9, 
            color='blue',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'),
            zorder=1000  # Ensure tooltip is on top
        )

        # Store which point this tooltip is for
        self.tooltip.point_index = point_index

        # Make the tooltip permanent so it won't disappear during hover
        self.tooltip.permanent = True

    def remove_tooltip(self):
        """Safely remove tooltip from plot"""
        if self.tooltip:
            try:
                self.tooltip.remove()
            except:
                # If removal fails, just make it invisible
                if hasattr(self.tooltip, 'set_visible'):
                    self.tooltip.set_visible(False)
            self.tooltip = None

    def on_tooltip_double_click(self, event):
        """Start dragging a tooltip on double-click"""
        if not event.dblclick or not self.tooltip:
            return

        # Safe alternative to contains() - check if click is near the tooltip position
        tooltip_xy = getattr(self.tooltip, 'xy', None)
        if tooltip_xy is not None:
            # Check if double-click is near tooltip
            tx, ty = tooltip_xy
            # Use a reasonable distance threshold
            if abs(tx - event.xdata) < 0.1 and abs(ty - event.ydata) < 0.1:
                self.dragging_tooltip = True

    def get_point_index(self, event):
        """Get index of the point closest to the event position"""
        if not hasattr(event, 'xdata') or not hasattr(event, 'ydata') or event.xdata is None or event.ydata is None:
            return None

        if self.kdtree is not None:
            distance, index = self.kdtree.query([event.xdata, event.ydata])
            if distance < 0.2:  # Threshold for being close to a point
                return index
        return None

    def on_double_click(self, event):
        """Handle double-click for editing labels and creating tooltips on points"""
        if not event.dblclick:
            return

        # Only handle left button double-clicks
        if event.button != MouseButton.LEFT:
            return

        # Title, X-axis and Y-axis labels detection
        # Check for special areas outside the main plot area
        if not hasattr(event, 'inaxes') or event.inaxes is None:
            # Get figure dimensions
            fig_width = self.figure.get_figwidth() * self.figure.dpi
            fig_height = self.figure.get_figheight() * self.figure.dpi

            # Check position relative to the figure
            # Title area (top center)
            title_area = plt.Rectangle((fig_width*0.3, fig_height*0.9), fig_width*0.4, fig_height*0.1)
            if title_area.contains_point((event.x, event.y)):
                self.edit_label("title")
                return

            # X-axis label area (bottom center)
            xlabel_area = plt.Rectangle((fig_width*0.3, 0), fig_width*0.4, fig_height*0.1)
            if xlabel_area.contains_point((event.x, event.y)):
                self.edit_label("xlabel")
                return

            # Y-axis label area (middle left)
            ylabel_area = plt.Rectangle((0, fig_height*0.3), fig_width*0.1, fig_height*0.4)
            if ylabel_area.contains_point((event.x, event.y)):
                self.edit_label("ylabel")
                return

        # Alternate text-based approach for more reliability
        try:
            # Get text objects in the figure
            for artist in self.figure.get_children():
                if isinstance(artist, plt.Text):
                    # Check text content to identify labels
                    text = artist.get_text()
                    if text == self.ax.get_title():
                        # Title was clicked
                        self.edit_label("title")
                        return
                    elif text == self.ax.get_xlabel():
                        # X-axis label was clicked
                        self.edit_label("xlabel")
                        return
                    elif text == self.ax.get_ylabel():
                        # Y-axis label was clicked
                        self.edit_label("ylabel")
                        return
        except (AttributeError, TypeError):
            # If there's an error with the checks, continue with point check
            pass

        # Check if we're inside the plot area for checking points
        point_idx = None
        if hasattr(event, 'inaxes') and event.inaxes == self.ax:
            # Check if double-clicking on a point
            point_idx = self.get_point_index(event)

        if point_idx is not None and point_idx not in self.annotations:
            self.add_annotation(point_idx)

    def add_annotation(self, point_idx):
        """Add a tooltip annotation to a specific point"""
        # Save current state for undo
        self.save_state()

        x, y = self.points[point_idx]

        # Create the annotation
        ann = self.ax.annotate(
            f"({x:.2f}, {y:.2f})",
            xy=(x, y),
            xytext=(10, 10),
            textcoords="offset points",
            fontsize=9,
            color='black',
            bbox=dict(boxstyle="round", fc="yellow", alpha=0.7),
            arrowprops=dict(arrowstyle="->"),
            zorder=1000  # Ensure tooltip is on top
        )

        # Store the annotation
        self.annotations[point_idx] = ann

        # Redraw
        self.canvas.draw_idle()

    def show_context_menu(self, event, annotation_idx, annotation):
        """Show context menu for tooltip operations"""
        context_menu = Menu(self.root, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda: self.edit_annotation(annotation_idx, annotation))
        context_menu.add_command(label="Delete", command=lambda: self.delete_annotation(annotation_idx, annotation))

        # Display the menu at mouse position on canvas
        x = self.canvas.get_tk_widget().winfo_rootx() + event.x
        y = self.canvas.get_tk_widget().winfo_rooty() + event.y
        context_menu.post(x, y)

    def delete_annotation(self, idx, annotation):
        """Delete a tooltip annotation"""
        # Save current state for undo
        self.save_state()

        # Remove annotation from plot
        annotation.remove()
        del self.annotations[idx]

        # Redraw
        self.canvas.draw_idle()

    def edit_annotation(self, idx, annotation):
        """Edit the text of an annotation"""
        # Get current text
        current_text = annotation.get_text()

        # Ask for new text
        new_text = simpledialog.askstring("Edit Tooltip", "Enter new tooltip text:",
                                        initialvalue=current_text)

        if new_text:
            # Update the tooltip text
            annotation.set_text(new_text)
            self.canvas.draw_idle()

    def edit_label(self, label_type):
        """Edit plot labels (title, xlabel, ylabel) with font and color customization"""
        # Create a custom dialog for advanced label editing
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit {label_type.capitalize()}")
        edit_window.geometry("400x350")
        edit_window.grab_set()  # Make the dialog modal

        # Store current attributes
        current_text = ""
        current_fontsize = 12
        current_color = "black"
        current_fontweight = "normal"
        current_fontstyle = "normal"

        # Get current settings based on label type
        if label_type == "title":
            current_text = self.ax.get_title()
            title_props = self.ax.title.get_fontproperties()
            if title_props:
                current_fontsize = self.ax.title.get_fontsize()
                current_color = self.ax.title.get_color()
                current_fontweight = self.ax.title.get_weight() or "normal"
                current_fontstyle = self.ax.title.get_style() or "normal"
        elif label_type == "xlabel":
            current_text = self.ax.get_xlabel()
            xlabel_props = self.ax.xaxis.label.get_fontproperties()
            if xlabel_props:
                current_fontsize = self.ax.xaxis.label.get_fontsize()
                current_color = self.ax.xaxis.label.get_color()
                current_fontweight = self.ax.xaxis.label.get_weight() or "normal"
                current_fontstyle = self.ax.xaxis.label.get_style() or "normal"
        elif label_type == "ylabel":
            current_text = self.ax.get_ylabel()
            ylabel_props = self.ax.yaxis.label.get_fontproperties()
            if ylabel_props:
                current_fontsize = self.ax.yaxis.label.get_fontsize()
                current_color = self.ax.yaxis.label.get_color()
                current_fontweight = self.ax.yaxis.label.get_weight() or "normal"
                current_fontstyle = self.ax.yaxis.label.get_style() or "normal"

        # Text entry
        ttk.Label(edit_window, text=f"Enter {label_type} text:").pack(pady=(10, 5), padx=10, anchor="w")
        text_entry = ttk.Entry(edit_window, width=40)
        text_entry.pack(pady=(0, 10), padx=10, fill="x")
        text_entry.insert(0, current_text)

        # Font size
        ttk.Label(edit_window, text="Font Size:").pack(pady=(5, 0), padx=10, anchor="w")
        size_frame = ttk.Frame(edit_window)
        size_frame.pack(pady=(0, 10), padx=10, fill="x")

        font_size_var = tk.IntVar(value=int(current_fontsize))
        font_sizes = [8, 10, 12, 14, 16, 18, 20, 24]
        for size in font_sizes:
            rb = ttk.Radiobutton(size_frame, text=str(size), variable=font_size_var, value=size)
            rb.pack(side="left", padx=3)

        # Font style
        style_frame = ttk.Frame(edit_window)
        style_frame.pack(pady=(5, 10), padx=10, fill="x")

        bold_var = tk.BooleanVar(value=(current_fontweight == "bold"))
        italic_var = tk.BooleanVar(value=(current_fontstyle == "italic"))

        ttk.Checkbutton(style_frame, text="Bold", variable=bold_var).pack(side="left", padx=5)
        ttk.Checkbutton(style_frame, text="Italic", variable=italic_var).pack(side="left", padx=5)

        # Color selection
        color_frame = ttk.Frame(edit_window)
        color_frame.pack(pady=(5, 10), padx=10, fill="x")

        ttk.Label(color_frame, text="Color:").pack(side="left", padx=5)
        color_var = tk.StringVar(value=current_color)
        color_options = ["black", "blue", "red", "green", "purple", "orange", "custom"]
        color_combo = ttk.Combobox(color_frame, textvariable=color_var, values=color_options, state="readonly", width=10)
        color_combo.pack(side="left", padx=5)

        # Custom color picker function
        def pick_custom_color():
            # Using colorchooser dialog
            color = colorchooser.askcolor(initialcolor=color_var.get())
            if color and color[1]:  # color is ((r,g,b), hexcode)
                color_var.set(color[1])

        ttk.Button(color_frame, text="Custom Color", command=pick_custom_color).pack(side="left", padx=5)

        # Preview frame
        preview_frame = ttk.LabelFrame(edit_window, text="Preview")
        preview_frame.pack(pady=10, padx=10, fill="both", expand=True)

        preview_label = ttk.Label(preview_frame, text=current_text, anchor="center")
        preview_label.pack(pady=10, fill="both", expand=True)

        # Update preview function
        def update_preview(*args):
            # Get current settings
            text = text_entry.get()
            size = font_size_var.get()
            weight = "bold" if bold_var.get() else "normal"
            style = "italic" if italic_var.get() else "normal"
            color = color_var.get()

            # Update preview label with custom font
            font_config = ("TkDefaultFont", size, weight + " " + style)
            preview_label.config(text=text, font=font_config, foreground=color)

        # Connect update function to all variables
        text_entry.bind("<KeyRelease>", update_preview)
        font_size_var.trace_add("write", update_preview)
        bold_var.trace_add("write", update_preview)
        italic_var.trace_add("write", update_preview)
        color_var.trace_add("write", update_preview)

        # Initialize preview
        update_preview()

        # Buttons
        button_frame = ttk.Frame(edit_window)
        button_frame.pack(pady=10, fill="x")

        def apply_changes():
            # Get all the values
            text = text_entry.get()
            size = font_size_var.get()
            weight = "bold" if bold_var.get() else "normal"
            style = "italic" if italic_var.get() else "normal"
            color = color_var.get()

            # Store the customized label settings
            if not hasattr(self, 'custom_labels'):
                self.custom_labels = {}

            # Save all settings
            self.custom_labels[label_type] = {
                'text': text,
                'fontsize': size,
                'color': color,
                'fontweight': weight,
                'fontstyle': style
            }

            # Save current state for undo
            self.save_state()

            # Apply settings based on label type
            if label_type == "title":
                self.ax.set_title(text, fontsize=size, color=color, fontweight=weight, fontstyle=style)
            elif label_type == "xlabel":
                self.ax.set_xlabel(text, fontsize=size, color=color, fontweight=weight, fontstyle=style)
            elif label_type == "ylabel":
                self.ax.set_ylabel(text, fontsize=size, color=color, fontweight=weight, fontstyle=style)

            edit_window.destroy()
            self.canvas.draw_idle()

        ttk.Button(button_frame, text="Apply", command=apply_changes).pack(side="right", padx=10)
        ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side="right", padx=10)

    def on_press(self, event):
        """Handle mouse press events"""
        if not hasattr(event, 'xdata') or not hasattr(event, 'ydata') or event.xdata is None or event.ydata is None:
            return

        # Right-click for context menu functionality
        if event.button == MouseButton.RIGHT:
            # Create context menu
            context_menu = tk.Menu(self.root, tearoff=0)
            
            # Add activation options
            context_menu.add_command(
                label="Activate Main Plot",
                command=lambda: self.activate_main_plot()
            )
            
            # Add all subplot options
            for subplot_id in self.subplots.keys():
                context_menu.add_command(
                    label=f"Activate {subplot_id}",
                    command=lambda id=subplot_id: self.set_active_subplot(id)
                )
                
            # Add separator
            context_menu.add_separator()
            
            # Add point functionality if clicking on a point
            point_idx = self.get_point_index(event)
            if point_idx is not None:
                context_menu.add_command(
                    label="Delete Point",
                    command=lambda: self.delete_point(point_idx)
                )
                context_menu.add_command(
                    label="Edit Point",
                    command=lambda: self.edit_point(point_idx)
                )
                context_menu.add_separator()
            
            # Add general plot options
            context_menu.add_command(
                label="Add Point Here", 
                command=lambda: self.add_point(event.xdata, event.ydata)
            )
            context_menu.add_command(
                label="Toggle Grid",
                command=lambda: self.toggle_grid()
            )
                
            # Show menu at mouse position
            try:
                if hasattr(event, 'guiEvent'):
                    context_menu.tk_popup(event.guiEvent.x_root, event.guiEvent.y_root)
                else:
                    # Fallback if guiEvent not available
                    x = self.canvas.get_tk_widget().winfo_rootx() + event.x
                    y = self.canvas.get_tk_widget().winfo_rooty() + event.y
                    context_menu.tk_popup(x, y)
            except Exception as e:
                print(f"Menu error: {e}")
            finally:
                context_menu.grab_release()
            
            return
            
        # Rest of press handling...
        # Middle button for panning
        if event.button == MouseButton.MIDDLE:
            self.prev_x, self.prev_y = event.xdata, event.ydata
            self.canvas.get_tk_widget().config(cursor="fleur")  # Change cursor for panning

        # Left-click to start dragging points
        elif event.button == MouseButton.LEFT:
            # First check for point near cursor
            point_idx = self.get_point_index(event)
            if point_idx is not None:
                self.dragging_idx = point_idx
                return

    def activate_main_plot(self):
        """Activate main plot and switch to first tab"""
        self.active_subplot = None
        self.notebook.select(0)
        
        # Highlight main plot
        if hasattr(self, 'ax'):
            for spine in self.ax.spines.values():
                spine.set_color('red')
                
        # Reset subplot highlights
        for subplot in self.subplots.values():
            if 'ax' in subplot:
                for spine in subplot['ax'].spines.values():
                    spine.set_color('black')
                    
        # Force redraw
        if hasattr(self, 'canvas'):
            self.canvas.draw_idle()

    def on_motion(self, event):
        """Handle motion for panning the plot"""
        if not hasattr(event, 'xdata') or not hasattr(event, 'ydata') or event.xdata is None or event.ydata is None:
            return

        # Pan the plot if middle button is pressed
        if event.button == MouseButton.MIDDLE and self.prev_x is not None and self.prev_y is not None:
            dx = event.xdata - self.prev_x
            dy = event.ydata - self.prev_y

            # Get current axis limits
            x_min, x_max = self.ax.get_xlim()
            y_min, y_max = self.ax.get_ylim()

            # Update limits (move in opposite direction of mouse)
            self.ax.set_xlim(x_min - dx, x_max - dx)
            self.ax.set_ylim(y_min - dy, y_max - dy)

            # Redraw canvas
            self.canvas.draw_idle()

    def on_mouse_scroll(self, event):
        """Handle mouse scroll for zooming"""
        if not hasattr(event, 'xdata') or not hasattr(event, 'ydata') or event.xdata is None or event.ydata is None:
            return

        # Get current axis limits
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()

        # Zoom factor
        factor = 0.9 if event.button == 'up' else 1.1

        # Calculate new limits centered on mouse position
        x_center = event.xdata
        y_center = event.ydata

        x_min_new = x_center - (x_center - x_min) * factor
        x_max_new = x_center + (x_max - x_center) * factor
        y_min_new = y_center - (y_center - y_min) * factor
        y_max_new = y_center + (y_max - y_center) * factor

        # Set new limits
        self.ax.set_xlim(x_min_new, x_max_new)
        self.ax.set_ylim(y_min_new, y_max_new)

        # Redraw canvas
        self.canvas.draw_idle()

    def on_mouse_drag(self, event):
        """Handle mouse dragging for panning"""
        if event.button == MouseButton.MIDDLE and self.prev_x is not None and self.prev_y is not None:
            self.on_motion(event)
            self.prev_x, self.prev_y = event.xdata, event.ydata

    def create_properties_controls(self, parent_frame, subplot_id=None):
        """Create controls for a specific subplot"""
        controls_frame = ttk.Frame(parent_frame, relief=tk.RIDGE, borderwidth=2)
        controls_frame.pack(side="bottom", fill="x", pady=5)

        # Title/Label controls
        label_frame = ttk.Frame(controls_frame)
        label_frame.pack(side="top", fill="x", pady=2)
        
        ttk.Label(label_frame, text="Title:").pack(side="left")
        self.title_entry = ttk.Entry(label_frame)
        self.title_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        ttk.Label(label_frame, text="X Label:").pack(side="left")
        self.xlabel_entry = ttk.Entry(label_frame)
        self.xlabel_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        ttk.Label(label_frame, text="Y Label:").pack(side="left")
        self.ylabel_entry = ttk.Entry(label_frame)
        self.ylabel_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Update button
        update_btn = ttk.Button(label_frame, text="Update", command=lambda: self.update_labels(subplot_id))
        update_btn.pack(side="right", padx=5)
        
        # Style controls (existing implementation)
        # First row of buttons
        buttons_frame1 = ttk.Frame(controls_frame)
        buttons_frame1.pack(side="top", fill="x", pady=2)

        ttk.Button(buttons_frame1, text="Add Point", command=self.add_point).pack(side="left", padx=5)
        ttk.Button(buttons_frame1, text="Undo", command=self.undo).pack(side="left", padx=5)
        ttk.Button(buttons_frame1, text="Redo", command=self.redo).pack(side="left", padx=5)

        # Zoom controls
        ttk.Button(buttons_frame1, text="Zoom In", command=lambda: self.zoom(True)).pack(side="left", padx=5)
        ttk.Button(buttons_frame1, text="Zoom Out", command=lambda: self.zoom(False)).pack(side="left", padx=5)
        ttk.Button(buttons_frame1, text="Reset Zoom", command=self.reset_zoom).pack(side="left", padx=5)
        ttk.Button(buttons_frame1, text="Reset", command=self.reset_plot).pack(side="left", padx=5)

        # Second row of controls
        controls_frame2 = ttk.Frame(controls_frame)
        controls_frame2.pack(side="top", fill="x", pady=2)

        # Line Color
        ttk.Label(controls_frame2, text="Line Color:").pack(side="left", padx=5)
        self.line_color_combo = ttk.Combobox(controls_frame2, values=["blue", "red", "green", "black", "Custom"], state="readonly", width=8)
        self.line_color_combo.pack(side="left", padx=5)
        self.line_color_combo.set(self.line_color)
        self.line_color_combo.bind("<<ComboboxSelected>>", self.change_line_color)

        ttk.Button(controls_frame2, text="Custom Color", command=self.open_color_picker).pack(side="left", padx=5)

        # Line Style
        ttk.Label(controls_frame2, text="Line Style:").pack(side="left", padx=5)
        self.line_style_combo = ttk.Combobox(controls_frame2, values=["-", "--", "-.", ":", "Custom"], state="readonly", width=5)
        self.line_style_combo.pack(side="left", padx=5)
        self.line_style_combo.set(self.line_style)
        self.line_style_combo.bind("<<ComboboxSelected>>", self.change_line_style)

        ttk.Button(controls_frame2, text="Custom Style", command=self.open_line_style_window).pack(side="left", padx=5)

        # Third row of controls
        controls_frame3 = ttk.Frame(controls_frame)
        controls_frame3.pack(side="top", fill="x", pady=2)

        # Marker size adjustment
        ttk.Label(controls_frame3, text="Marker Size:").pack(side="left", padx=5)
        self.marker_size_slider = ttk.Scale(controls_frame3, from_=5, to=50, orient="horizontal", length=150, command=self.change_marker_size)
        self.marker_size_slider.set(self.marker_size)
        self.marker_size_slider.pack(side="left", padx=5)

        # Toggle checkboxes
        ttk.Checkbutton(controls_frame3, text="Live Update", variable=self.live_update_var, command=self.toggle_live_update).pack(side="left", padx=5)
        ttk.Checkbutton(controls_frame3, text="Grid", variable=self.grid_toggle_var, command=self.toggle_grid).pack(side="left", padx=5)
        ttk.Checkbutton(controls_frame3, text="Legend", variable=self.legend_toggle_var, command=self.toggle_legend).pack(side="left", padx=5)
        ttk.Button(controls_frame3, text="Edit Legend", command=self.customize_legend).pack(side="left", padx=5)
        ttk.Button(controls_frame3, text="Add Subplot", command=self.add_subplot).pack(side="left", padx=5)

        # Fourth row - Data Management Controls
        controls_frame4 = ttk.Frame(controls_frame)
        controls_frame4.pack(side="top", fill="x", pady=2)

        # Import/Export buttons
        ttk.Button(controls_frame4, text="Import Data", command=self.show_import_dialog).pack(side="left", padx=5)
        ttk.Button(controls_frame4, text="Export Plot", command=self.show_export_dialog).pack(side="left", padx=5)
        
        # Filter dropdown
        ttk.Label(controls_frame4, text="Filter:").pack(side="left", padx=5)
        self.filter_combo = ttk.Combobox(controls_frame4, values=["None", "Numeric Range", "Outliers"], state="readonly", width=12)
        self.filter_combo.pack(side="left", padx=5)
        self.filter_combo.set("None")
        
        ttk.Button(controls_frame4, text="Apply Filter", command=self.apply_filter).pack(side="left", padx=5)

        # Initialize with current values if subplot exists
        if subplot_id and subplot_id in self.subplot_states:
            state = self.subplot_states[subplot_id]
            self.title_entry.insert(0, state['title'])
            self.xlabel_entry.insert(0, state['xlabel'])
            self.ylabel_entry.insert(0, state['ylabel'])
            
            if hasattr(self, 'line_color_combo'):
                self.line_color_combo.set(state['line_color'])
            if hasattr(self, 'line_style_combo'):
                self.line_style_combo.set(state['line_style'])
            if hasattr(self, 'marker_size_slider'):
                self.marker_size_slider.set(state['marker_size'])

    def update_labels(self, subplot_id):
        """Update labels for a specific subplot"""
        if subplot_id in self.subplot_states:
            self.subplot_states[subplot_id].update({
                'title': self.title_entry.get(),
                'xlabel': self.xlabel_entry.get(),
                'ylabel': self.ylabel_entry.get()
            })
            
            # Update both views
            self.update_main_view()
            self.subplots[subplot_id]['canvas'].draw_idle()
            
            # If this is the active subplot, update controls
            if self.active_subplot == subplot_id:
                self.set_active_subplot(subplot_id)

    def on_tab_switch(self, event=None):
        """Handle tab switching or manual activation"""
        # If called manually (not from event), switch to first tab
        if event is None:
            self.notebook.select(0)
            
        current_tab = self.notebook.index(self.notebook.select())
        
        if current_tab == 0:
            # Main plot tab
            self.active_subplot = None
            
            # Highlight main plot
            if hasattr(self, 'ax'):
                for spine in self.ax.spines.values():
                    spine.set_color('red')
            
            # Reset subplot highlights
            for subplot in self.subplots.values():
                if hasattr(subplot, 'ax'):
                    for spine in subplot['ax'].spines.values():
                        spine.set_color('black')
        else:
            # Subplot tab
            subplot_id = list(self.subplots.keys())[current_tab - 1]
            self.set_active_subplot(subplot_id)
            
            # Reset main plot highlight
            if hasattr(self, 'ax'):
                for spine in self.ax.spines.values():
                    spine.set_color('black')

    def set_active_subplot(self, subplot_id):
        """Properly activate subplot with full state update"""
        if subplot_id in self.subplots:
            self.active_subplot = subplot_id
            subplot = self.subplots[subplot_id]
            
            # Switch to the subplot tab
            subplot_index = list(self.subplots.keys()).index(subplot_id)
            self.notebook.select(subplot_index + 1)  # +1 for main tab offset
            
            # Clear all borders
            for s_id, s_data in self.subplots.items():
                for spine in s_data['ax'].spines.values():
                    spine.set_color('black')
            
            # Clear main plot border
            if hasattr(self, 'ax'):
                for spine in self.ax.spines.values():
                    spine.set_color('black')
            
            # Highlight active subplot
            for spine in subplot['ax'].spines.values():
                spine.set_color('red')
            
            # Also highlight the subplot in the main view
            if hasattr(self, 'figure'):
                # Find this subplot in the main figure
                for i, ax in enumerate(self.figure.axes):
                    if i == list(self.subplots.keys()).index(subplot_id) + 1:  # +1 for main plot
                        for spine in ax.spines.values():
                            spine.set_color('red')
                
            # Update control values from state
            state = self.subplot_states[subplot_id]
            if hasattr(self, 'title_entry'):
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, state['title'])
            if hasattr(self, 'xlabel_entry'):
                self.xlabel_entry.delete(0, tk.END)
                self.xlabel_entry.insert(0, state['xlabel'])
            if hasattr(self, 'ylabel_entry'):
                self.ylabel_entry.delete(0, tk.END)
                self.ylabel_entry.insert(0, state['ylabel'])
            
            # Force redraw
            subplot['canvas'].draw_idle()
            if hasattr(self, 'canvas'):
                self.canvas.draw_idle()

    def edit_subplot(self, subplot_id):
        """Handle subplot editing with proper synchronization"""
        if subplot_id in self.subplots:
            # Get current control values
            new_title = self.title_entry.get() if hasattr(self, 'title_entry') else ""
            
            # Update state
            self.subplot_states[subplot_id].update({
                'title': new_title,
                # Add other properties here
            })
            
            # Update both views
            self.update_main_view()
            self.subplots[subplot_id]['canvas'].draw_idle()

    def save_state(self):
        """Save current state for undo functionality"""
        # Deep copy custom labels to ensure we store a complete snapshot
        custom_labels_copy = {}
        if hasattr(self, 'custom_labels'):
            for key, value in self.custom_labels.items():
                custom_labels_copy[key] = value.copy()

        state = {
            'points': self.points.copy(),
            'line_color': self.line_color,
            'line_style': self.line_style,
            'marker_size': self.marker_size,
            'custom_labels': custom_labels_copy
        }
        self.history.append(state)
        # Clear redo stack after a new action
        self.redo_stack = []

    def undo(self):
        """Undo the last action"""
        if len(self.history) > 0:
            # Deep copy custom labels for current state
            custom_labels_copy = {}
            if hasattr(self, 'custom_labels'):
                for key, value in self.custom_labels.items():
                    custom_labels_copy[key] = value.copy()

            # Save current state to redo stack
            current_state = {
                'points': self.points.copy(),
                'line_color': self.line_color,
                'line_style': self.line_style,
                'marker_size': self.marker_size,
                'custom_labels': custom_labels_copy
            }
            self.redo_stack.append(current_state)

            # Restore previous state
            previous_state = self.history.pop()
            self.points = previous_state['points'].copy()
            self.line_color = previous_state['line_color']
            self.line_style = previous_state['line_style']
            self.marker_size = previous_state['marker_size']

            # Restore custom labels if they exist in the saved state
            if 'custom_labels' in previous_state:
                self.custom_labels = previous_state['custom_labels']

            # Update UI
            self.line_color_combo.set(self.line_color)
            self.line_style_combo.set(self.line_style)
            self.marker_size_slider.set(self.marker_size)

            # Update KDTree and plot
            self.update_kdtree()
            self.update_plot()

    def redo(self):
        """Redo the last undone action"""
        if len(self.redo_stack) > 0:
            # Deep copy custom labels for current state
            custom_labels_copy = {}
            if hasattr(self, 'custom_labels'):
                for key, value in self.custom_labels.items():
                    custom_labels_copy[key] = value.copy()

            # Save current state to history
            current_state = {
                'points': self.points.copy(),
                'line_color': self.line_color,
                'line_style': self.line_style,
                'marker_size': self.marker_size,
                'custom_labels': custom_labels_copy
            }
            self.history.append(current_state)

            # Restore next state
            next_state = self.redo_stack.pop()
            self.points = next_state['points'].copy()
            self.line_color = next_state['line_color']
            self.line_style = next_state['line_style']
            self.marker_size = next_state['marker_size']

            # Restore custom labels if they exist in the saved state
            if 'custom_labels' in next_state:
                self.custom_labels = next_state['custom_labels']

            # Update UI
            self.line_color_combo.set(self.line_color)
            self.line_style_combo.set(self.line_style)
            self.marker_size_slider.set(self.marker_size)

            # Update KDTree and plot
            self.update_kdtree()
            self.update_plot()

    def update_plot(self):
        """Update the entire plot with current settings"""
        # Just call plot_points which now handles everything needed for a proper update
        # This prevents duplicate code and ensures consistent behavior
        self.plot_points()

    def plot_points(self):
        """Plot points and connecting lines with current styles"""
        if len(self.points) == 0:
            return

        # Store current limits and labels
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Store current label properties before clearing
        title_text = self.ax.get_title() or "Advanced Plot"
        xlabel_text = self.ax.get_xlabel() or "X-axis"
        ylabel_text = self.ax.get_ylabel() or "Y-axis"

        # Store custom label properties if they exist
        custom_title_props = {}
        custom_xlabel_props = {}
        custom_ylabel_props = {}

        # Check if we have saved custom label settings
        if hasattr(self, 'custom_labels'):
            if 'title' in self.custom_labels:
                custom_title_props = self.custom_labels['title']
                title_text = custom_title_props.get('text', title_text)
            if 'xlabel' in self.custom_labels:
                custom_xlabel_props = self.custom_labels['xlabel']
                xlabel_text = custom_xlabel_props.get('text', xlabel_text)
            if 'ylabel' in self.custom_labels:
                custom_ylabel_props = self.custom_labels['ylabel']
                ylabel_text = custom_ylabel_props.get('text', ylabel_text)

        # Clear current plot
        self.ax.clear()

        # Re-apply labels with custom settings if available
        if custom_title_props:
            self.ax.set_title(title_text, 
                             fontsize=custom_title_props.get('fontsize', 12),
                             color=custom_title_props.get('color', 'black'),
                             fontweight=custom_title_props.get('fontweight', 'normal'),
                             fontstyle=custom_title_props.get('fontstyle', 'normal'))
        else:
            self.ax.set_title(title_text)

        if custom_xlabel_props:
            self.ax.set_xlabel(xlabel_text,
                              fontsize=custom_xlabel_props.get('fontsize', 10),
                              color=custom_xlabel_props.get('color', 'black'),
                              fontweight=custom_xlabel_props.get('fontweight', 'normal'),
                              fontstyle=custom_xlabel_props.get('fontstyle', 'normal'))
        else:
            self.ax.set_xlabel(xlabel_text)

        if custom_ylabel_props:
            self.ax.set_ylabel(ylabel_text,
                              fontsize=custom_ylabel_props.get('fontsize', 10),
                              color=custom_ylabel_props.get('color', 'black'),
                              fontweight=custom_ylabel_props.get('fontweight', 'normal'),
                              fontstyle=custom_ylabel_props.get('fontstyle', 'normal'))
        else:
            self.ax.set_ylabel(ylabel_text)

        # Extract x and y coordinates
        x = self.points[:, 0]
        y = self.points[:, 1]

        # Plot line and points
        self.ax.plot(x, y, linestyle=self.line_style, color=self.line_color, marker='o', 
                     markersize=self.marker_size/2, markerfacecolor=self.line_color)

        # Highlight dragging point if any
        if self.dragging_idx is not None and self.dragging_idx < len(self.points):
            self.ax.plot(self.points[self.dragging_idx, 0], self.points[self.dragging_idx, 1], 
                        'o', markersize=self.marker_size/1.5, markerfacecolor='yellow', 
                        markeredgecolor='red', markeredgewidth=2)

        # Restore all annotations
        for idx, ann in list(self.annotations.items()):
            if idx < len(self.points):  # Make sure the point still exists
                x, y = self.points[idx]

                # Update annotation position and text
                ann.xy = (x, y)
                ann.set_text(f"({x:.2f}, {y:.2f})")

        # Apply grid if enabled
        self.ax.grid(self.grid_toggle_var.get())

        # Apply legend if enabled
        if self.legend_toggle_var.get():
            if hasattr(self, 'legend_labels'):
                if hasattr(self, 'legend_position'):
                    self.ax.legend(self.legend_labels, loc=self.legend_position)
                else:
                    self.ax.legend(self.legend_labels)
            else:
                self.ax.legend([f"Data {i+1}" for i in range(len(self.points))])

        # Restore original view limits
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)

        # Draw only what's needed without changing axis limits
        self.canvas.draw_idle()

    def add_point(self, x=None, y=None):
        """Add point to active subplot or main plot"""
        if self.active_subplot and self.active_subplot in self.subplots:
            subplot = self.subplots[self.active_subplot]
            
            # Ensure points exist in subplot
            if 'points' not in subplot:
                subplot['points'] = np.array([]).reshape(0, 2)
                
            # Add point to both subplot and state
            if x is None or y is None:
                x_min, x_max = subplot['ax'].get_xlim()
                y_min, y_max = subplot['ax'].get_ylim()
                new_x = np.random.uniform(x_min, x_max)
                new_y = np.random.uniform(y_min, y_max)
            else:
                new_x = x
                new_y = y
                
            new_point = np.array([[new_x, new_y]])
            subplot['points'] = np.vstack([subplot['points'], new_point])
            self.subplot_states[self.active_subplot]['points'] = subplot['points'].copy()
            
            # Update the subplot
            subplot['ax'].plot(new_x, new_y, 'o')
            subplot['canvas'].draw_idle()
            
            # Update main view
            self.update_main_view()
        else:
            # Add to main plot
            if x is None or y is None:
                x_min, x_max = self.ax.get_xlim()
                y_min, y_max = self.ax.get_ylim()
                new_x = np.random.uniform(x_min, x_max)
                new_y = np.random.uniform(y_min, y_max)
            else:
                new_x = x
                new_y = y
                
            if len(self.points) == 0:
                self.points = np.array([[new_x, new_y]])
            else:
                self.points = np.vstack([self.points, [new_x, new_y]])
                
            self.update_kdtree()
            self.update_plot()

    def handle_file_drop(self, event):
        """Handle dropped files on the plot area"""
        file_path = event.data.strip('{}')
        if not os.path.exists(file_path):
            return
            
        # Get mouse position to determine target subplot
        x, y = self.root.winfo_pointerxy()
        target = self.get_subplot_at_position(x, y)
        
        if target:
            self.show_data_import_dialog(file_path, target)
        
    def get_subplot_at_position(self, x, y):
        """Find which subplot contains given screen coordinates"""
        for widget in self.root.winfo_children():
            if widget.winfo_contain(x, y):
                if hasattr(widget, 'subplot_id'):
                    return widget.subplot_id
        return None
        
    def show_data_import_dialog(self, file_path, subplot_id):
        """Show dialog for data import options"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Import Data")
        
        tk.Label(dialog, text=f"Import {os.path.basename(file_path)} to:").pack(pady=10)
        
        plot_type_var = tk.StringVar(value="line")
        tk.Label(dialog, text="Plot Type:").pack()
        tk.OptionMenu(dialog, plot_type_var, 
                     "line", "scatter", "bar", "histogram", 
                     "pie", "heatmap", "3d").pack()
                     
        import_mode = tk.StringVar(value="replace")
        tk.Label(dialog, text="Import Mode:").pack()
        tk.Radiobutton(dialog, text="Replace Existing", variable=import_mode, value="replace").pack()
        tk.Radiobutton(dialog, text="Append Data", variable=import_mode, value="append").pack()
        
        def handle_import():
            try:
                data = self.load_data_file(file_path)
                self.plot_data(subplot_id, data, plot_type_var.get(), import_mode.get())
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import data: {str(e)}")
        
        tk.Button(dialog, text="Import", command=handle_import).pack(pady=10)
        
    def load_data_file(self, file_path):
        """Load data from various file formats"""
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
            
    def plot_data(self, subplot_id, data, plot_type, mode):
        """Plot data in specified subplot"""
        self.save_state()
        ax = self.subplots[subplot_id]['ax']
        
        if mode == "replace":
            ax.clear()
            
        if plot_type == "line":
            ax.plot(data.iloc[:,0], data.iloc[:,1])
        elif plot_type == "scatter":
            ax.scatter(data.iloc[:,0], data.iloc[:,1])
        elif plot_type == "bar":
            ax.bar(data.iloc[:,0], data.iloc[:,1])
        elif plot_type == "histogram":
            ax.hist(data.iloc[:,0])
        elif plot_type == "pie":
            ax.pie(data.iloc[:,1], labels=data.iloc[:,0])
        elif plot_type == "heatmap":
            ax.imshow(data.values, cmap='viridis')
        elif plot_type == "3d":
            from mpl_toolkits.mplot3d import Axes3D
            if not hasattr(ax, 'projection') or ax.projection != '3d':
                self.figure.delaxes(ax)
                ax = self.figure.add_subplot(ax.get_geometry(), projection='3d')
                self.subplots[subplot_id]['ax'] = ax
            ax.plot_trisurf(data.iloc[:,0], data.iloc[:,1], data.iloc[:,2])
            
        self.update_plot()

    def show_import_dialog(self):
        """Show file dialog for importing data"""
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )
        if file_path:
            self.import_data(file_path)

    def import_data(self, file_path):
        """Import data from file and plot it"""
        try:
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file_path)
            else:
                messagebox.showerror("Error", "Unsupported file format")
                return
            
            # Clear existing points
            self.points = np.empty((0, 2))
            
            # Convert to points array (assuming first two columns are x,y)
            if len(data.columns) >= 2:
                self.points = data.iloc[:, :2].values
                self.update_kdtree()
                self.update_plot()
                messagebox.showinfo("Success", f"Imported {len(self.points)} data points")
            else:
                messagebox.showerror("Error", "Data file must have at least 2 columns")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {str(e)}")

    def show_export_dialog(self):
        """Show dialog for exporting plot"""
        file_path = filedialog.asksaveasfilename(
            title="Save Plot As",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            self.export_plot(file_path)

    def export_plot(self, file_path):
        """Export current plot to file"""
        try:
            if file_path.endswith('.png'):
                self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
            elif file_path.endswith('.pdf'):
                self.figure.savefig(file_path, bbox_inches='tight')
            messagebox.showinfo("Success", f"Plot saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export plot: {str(e)}")

    def apply_filter(self):
        """Apply selected filter to the data"""
        filter_type = self.filter_combo.get()
        if filter_type == "None":
            # Reset to original points
            if hasattr(self, 'original_points'):
                self.points = self.original_points.copy()
        elif filter_type == "Numeric Range":
            # Store original points before filtering
            if not hasattr(self, 'original_points'):
                self.original_points = self.points.copy()
            
            # Simple range filter (can be enhanced with a dialog)
            x_min, x_max = np.min(self.points[:,0]), np.max(self.points[:,0])
            y_min, y_max = np.min(self.points[:,1]), np.max(self.points[:,1])
            
            # Filter points within middle 50% range
            x_range = x_max - x_min
            y_range = y_max - y_min
            mask = (self.points[:,0] > x_min + 0.25*x_range) & \
                   (self.points[:,0] < x_min + 0.75*x_range) & \
                   (self.points[:,1] > y_min + 0.25*y_range) & \
                   (self.points[:,1] < y_min + 0.75*y_range)
            self.points = self.original_points[mask]
        elif filter_type == "Outliers":
            # Store original points before filtering
            if not hasattr(self, 'original_points'):
                self.original_points = self.points.copy()
                
            # Simple outlier removal using IQR
            q1 = np.percentile(self.points[:,1], 25)
            q3 = np.percentile(self.points[:,1], 75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5*iqr
            upper_bound = q3 + 1.5*iqr
            
            mask = (self.points[:,1] >= lower_bound) & (self.points[:,1] <= upper_bound)
            self.points = self.original_points[mask]
        
        self.update_kdtree()
        self.update_plot()

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

        # Initial plot
        self.update_plot()

        # Add properties controls
        self.create_properties_controls(tab)

        # Connect canvas events for interactivity
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('scroll_event', self.on_mouse_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_double_click)

        # Initialize for panning
        self.prev_x, self.prev_y = None, None

    def add_subplot(self):
        """Add new synchronized subplot"""
        subplot_id = f"subplot_{len(self.subplots) + 1}"
        
        # Create edit tab
        edit_tab = ttk.Frame(self.notebook)
        self.notebook.add(edit_tab, text=f"Edit {len(self.subplots) + 1}")
        
        # Create figure and canvas for edit view
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, edit_tab)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Initialize subplot state with points
        self.subplot_states[subplot_id] = {
            'points': self.points.copy(),  # Initialize with current points
            'title': f"Subplot {len(self.subplots) + 1}",
            'xlabel': "X-axis",
            'ylabel': "Y-axis",
            'line_color': 'blue',
            'line_style': '-',
            'marker_size': 8
        }
        
        # Store references with proper structure
        self.subplots[subplot_id] = {
            'fig': fig,
            'ax': ax,
            'canvas': canvas,
            'tab': edit_tab,
            'points': self.points.copy()  # Also store points in subplot dict
        }
        
        # Add controls to edit tab
        self.create_properties_controls(edit_tab, subplot_id)
        
        # Update main view
        self.update_main_view()
        
        # Set as active
        self.set_active_subplot(subplot_id)
        
    def update_main_view(self):
        """Synchronize all subplots with main view"""
        if not hasattr(self, 'figure'):
            return
            
        self.figure.clear()
        
        # Recreate main plot with all subplots
        cols = min(3, len(self.subplots) + 1)
        rows = (len(self.subplots) + cols) // cols
        
        # Main plot
        self.ax = self.figure.add_subplot(rows, cols, 1)
        self.plot_points()
        
        # Subplots
        for i, (subplot_id, subplot) in enumerate(self.subplots.items(), start=2):
            ax = self.figure.add_subplot(rows, cols, i)
            state = self.subplot_states[subplot_id]
            
            # Plot points with subplot's style
            if len(state['points']) > 0:
                ax.plot(state['points'][:,0], state['points'][:,1],
                       color=state['line_color'],
                       linestyle=state['line_style'],
                       marker='o',
                       markersize=state['marker_size'])
            
            # Apply subplot's labels
            ax.set_title(state['title'])
            ax.set_xlabel(state['xlabel'])
            ax.set_ylabel(state['ylabel'])
        
        self.canvas.draw()
        
    def toggle_grid(self):
        """Toggle gridlines on/off"""
        self.ax.grid(self.grid_toggle_var.get())
        self.canvas.draw_idle()

    def toggle_legend(self):
        """Toggle legend display on/off"""
        if self.legend_toggle_var.get():
            # Use custom labels if they exist, otherwise generate default ones
            labels = getattr(self, 'legend_labels', [f"Data {i+1}" for i in range(len(self.points))])

            # Apply legend with position settings if they exist
            if hasattr(self, 'legend_position'):
                self.ax.legend(labels, **self.legend_position)
            else:
                self.ax.legend(labels, loc='best')
        else:
            # Remove legend if exists
            if self.ax.get_legend():
                self.ax.get_legend().remove()

        self.canvas.draw_idle()

    def toggle_live_update(self):
        """Toggle live update of the plot"""
        if self.live_update_var.get():
            self.start_live_update()
        else:
            self.stop_live_update()

    def start_live_update(self):
        """Start live updating of the plot"""
        def update():
            if self.live_update_var.get():
                # Add small random movement to points
                if len(self.points) > 0:
                    noise = np.random.normal(0, 0.1, self.points.shape)
                    self.points = self.points + noise
                    self.update_kdtree()
                    self.plot_points()

                # Schedule next update
                self.live_update_task_id = self.root.after(100, update)

        # Start the update loop
        update()

    def stop_live_update(self):
        """Stop live updating of the plot"""
        if self.live_update_task_id:
            self.root.after_cancel(self.live_update_task_id)
            self.live_update_task_id = None

    def change_line_color(self, event=None):
        """Change the line color based on combobox selection"""
        selected_color = self.line_color_combo.get()
        if selected_color != "Custom":
            self.line_color = selected_color
            self.update_plot()

    def change_line_style(self, event=None):
        """Change the line style based on combobox selection"""
        selected_style = self.line_style_combo.get()
        if selected_style != "Custom":
            self.line_style = selected_style
            self.update_plot()

    def change_marker_size(self, event=None):
        """Change marker size based on slider value"""
        self.marker_size = self.marker_size_slider.get()
        self.update_plot()

    def open_color_picker(self):
        """Open a color picker and update the line color"""
        color_code = colorchooser.askcolor(title="Choose Line Color")[1]  # Get hex code
        if color_code:  # If the user picked a color, update it
            self.line_color = color_code
            self.line_color_combo.set("Custom")  # Show "Custom" in dropdown
            self.update_plot()

    def open_line_style_window(self):
        """Open a pop-up window to enter a custom line style"""
        style_window = tk.Toplevel(self.root)
        style_window.title("Custom Line Style")
        style_window.geometry("250x150")

        ttk.Label(style_window, text="Enter Line Style:").pack(pady=5)
        style_entry = ttk.Entry(style_window)
        style_entry.pack(pady=5)

        def apply_style():
            """Apply the entered line style"""
            new_style = style_entry.get()
            if new_style:
                self.line_style = new_style
                self.line_style_combo.set("Custom")  # Show "Custom" in dropdown
                self.update_plot()
            style_window.destroy()

        ttk.Button(style_window, text="Apply", command=apply_style).pack(pady=10)

    def customize_legend(self):
        """Popup window for manual legend customization"""
        self.legend_popup = tk.Toplevel(self.root)
        self.legend_popup.title("Customize Legend")
        self.legend_popup.geometry("400x800")  # Increased height
        self.legend_popup.minsize(400, 800)  # Increased minimum height
        self.legend_popup.grab_set()  # Make window modal
        self.legend_popup.resizable(False, False)  # Fixed size window

        # Main container with padding
        main_frame = ttk.Frame(self.legend_popup, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Labels section with scrollbar
        labels_frame = ttk.LabelFrame(main_frame, text="Legend Labels")
        labels_frame.pack(fill="x", pady=(0, 10))
        labels_frame.pack(pady=10, padx=5, fill="x")

        # Scrollable frame for labels
        canvas = tk.Canvas(labels_frame)
        scrollbar = ttk.Scrollbar(labels_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Legend entries
        self.legend_entries = []
        for i in range(len(self.points)):
            frame = ttk.Frame(scrollable_frame)
            frame.pack(pady=2, fill="x", padx=5)

            ttk.Label(frame, text=f"Label {i+1}:").pack(side="left", padx=5)
            entry = ttk.Entry(frame, width=30)
            entry.pack(side="left", expand=True, fill="x", padx=5)
            default_label = f"Data {i+1}"
            current_label = default_label
            if hasattr(self, 'legend_labels') and i < len(self.legend_labels):
                current_label = self.legend_labels[i]
            entry.insert(0, current_label)
            self.legend_entries.append(entry)

        canvas.pack(side="left", fill="both", expand=True, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Position section
        position_frame = ttk.LabelFrame(self.legend_popup, text="Legend Position")
        position_frame.pack(pady=10, padx=5, fill="x")

        # Position dropdown
        self.legend_position_var = tk.StringVar(value=getattr(self, 'legend_position', 'best'))
        ttk.Label(position_frame, text="Preset Positions:").pack(pady=5)

        legend_positions = [
            "best", "upper right", "upper left", "lower left", "lower right",
            "right", "center left", "center right", "lower center", "upper center", "center"
        ]

        position_combo = ttk.Combobox(position_frame, textvariable=self.legend_position_var, 
                                    values=legend_positions, state="readonly")
        position_combo.pack(pady=5)

        # Custom coordinates
        custom_frame = ttk.LabelFrame(self.legend_popup, text="Custom Position")
        custom_frame.pack(pady=10, padx=5, fill="x")

        # X coordinate
        x_frame = ttk.Frame(custom_frame)
        x_frame.pack(fill="x", pady=5)
        ttk.Label(x_frame, text="X Position (0-1):").pack(side="left", padx=5)
        self.legend_x_var = tk.DoubleVar(value=0.5)
        x_scale = ttk.Scale(x_frame, from_=0, to=1, orient="horizontal", 
                           variable=self.legend_x_var)
        x_scale.pack(side="left", expand=True, fill="x", padx=5)

        # Y coordinate
        y_frame = ttk.Frame(custom_frame)
        y_frame.pack(fill="x", pady=5)
        ttk.Label(y_frame, text="Y Position (0-1):").pack(side="left", padx=5)
        self.legend_y_var = tk.DoubleVar(value=0.5)
        y_scale = ttk.Scale(y_frame, from_=0, to=1, orient="horizontal", 
                           variable=self.legend_y_var)
        y_scale.pack(side="left", expand=True, fill="x", padx=5)

        # Preview button
        ttk.Button(self.legend_popup, text="Preview", 
                  command=lambda: self.apply_legend(preview=True)).pack(pady=5)

        # Apply button
        ttk.Button(self.legend_popup, text="Apply", 
                  command=lambda: self.apply_legend(preview=False)).pack(pady=5)

    def apply_legend(self, preview=False):
        """Apply legend changes with preview option"""
        # Get the labels
        self.legend_labels = [entry.get() for entry in self.legend_entries]
        
        # Get position
        position = self.legend_position_var.get()
        
        # Remove existing legend
        if self.ax.get_legend():
            self.ax.get_legend().remove()
            
        # Create a list of dummy lines for each point
        lines = [plt.Line2D([0], [0], color=self.line_color, linestyle=self.line_style, 
                          marker='o', markersize=self.marker_size/2) for _ in range(len(self.points))]
        
        # Apply legend with new settings
        if hasattr(self, 'legend_x_var') and hasattr(self, 'legend_y_var'):
            bbox = (self.legend_x_var.get(), self.legend_y_var.get())
            self.ax.legend(lines, self.legend_labels, bbox_to_anchor=bbox)
        else:
            self.ax.legend(lines, self.legend_labels, loc=position)
            
        # Store settings
        self.legend_position = position
        
        # Enable legend toggle
        self.legend_toggle_var.set(True)
        
        # Update display
        self.canvas.draw_idle()
        
        # Close window if not preview
        if not preview:
            self.legend_popup.destroy()

    def add_subplot(self):
        """Add new synchronized subplot"""
        subplot_id = f"subplot_{len(self.subplots) + 1}"
        
        # Create edit tab
        edit_tab = ttk.Frame(self.notebook)
        self.notebook.add(edit_tab, text=f"Edit {len(self.subplots) + 1}")
        
        # Create figure and canvas for edit view
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, edit_tab)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Initialize subplot state
        self.subplot_states[subplot_id] = {
            'points': self.points.copy(),
            'title': f"Subplot {len(self.subplots) + 1}",
            'xlabel': "X-axis",
            'ylabel': "Y-axis",
            'line_color': 'blue',
            'line_style': '-',
            'marker_size': 8
        }
        
        # Store references
        self.subplots[subplot_id] = {
            'fig': fig,
            'ax': ax,
            'canvas': canvas,
            'tab': edit_tab,
            'points': self.points.copy()
        }
        
        # Add controls to edit tab
        self.create_properties_controls(edit_tab, subplot_id)
        
        # Update main view
        self.update_main_view()
        
        # Set as active
        self.set_active_subplot(subplot_id)
        
    def update_main_view(self):
        """Synchronize all subplots with main view"""
        if not hasattr(self, 'figure'):
            return
            
        self.figure.clear()
        
        # Recreate main plot with all subplots
        cols = min(3, len(self.subplots) + 1)
        rows = (len(self.subplots) + cols) // cols
        
        # Main plot
        self.ax = self.figure.add_subplot(rows, cols, 1)
        self.plot_points()
        
        # Subplots
        for i, (subplot_id, subplot) in enumerate(self.subplots.items(), start=2):
            ax = self.figure.add_subplot(rows, cols, i)
            state = self.subplot_states[subplot_id]
            
            # Plot points with subplot's style
            if len(state['points']) > 0:
                ax.plot(state['points'][:,0], state['points'][:,1],
                       color=state['line_color'],
                       linestyle=state['line_style'],
                       marker='o',
                       markersize=state['marker_size'])
            
            # Apply subplot's labels
            ax.set_title(state['title'])
            ax.set_xlabel(state['xlabel'])
            ax.set_ylabel(state['ylabel'])
        
        self.canvas.draw()
        
    def zoom(self, zoom_in=True):
        """Zoom in or out on the plot"""
        factor = 0.9 if zoom_in else 1.1

        # Get current axis limits
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()

        # Calculate center
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2

        # Calculate new limits centered on current view
        x_min_new = x_center - (x_center - x_min) * factor
        x_max_new = x_center + (x_max - x_center) * factor
        y_min_new = y_center - (y_center - y_min) * factor
        y_max_new = y_center + (y_max - y_center) * factor

        # Set new limits
        self.ax.set_xlim(x_min_new, x_max_new)
        self.ax.set_ylim(y_min_new, y_max_new)

        # Redraw canvas
        self.canvas.draw_idle()

    def reset_zoom(self):
        """Reset zoom to original view"""
        if hasattr(self, 'original_xlim') and hasattr(self, 'original_ylim'):
            self.ax.set_xlim(self.original_xlim)
            self.ax.set_ylim(self.original_ylim)
            self.canvas.draw_idle()

    def reset_plot(self):
        """Reset the plot to its initial state"""
        # Save current state for undo
        self.save_state()

        # Reset points to initial state
        self.points = self.initial_points.copy()
        self.update_kdtree()

        # Reset styles to defaults
        self.line_color = self.initial_line_color
        self.line_style = self.initial_line_style
        self.marker_size = self.initial_marker_size

        # Reset custom labels
        self.custom_labels = {}

        # Update UI elements
        self.line_color_combo.set(self.line_color)
        self.line_style_combo.set(self.line_style)
        self.marker_size_slider.set(self.marker_size)

        # Reset axes to original view
        self.reset_zoom()

        # Update plot
        self.update_plot()

# Update main block
if __name__ == "__main__":
    app = InteractivePlot()
    app.root.geometry("800x600")
    app.root.mainloop()