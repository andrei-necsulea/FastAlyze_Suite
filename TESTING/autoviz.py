import tkinter as tk
from tkinter import ttk, Menu, filedialog
import numpy as np
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.backend_bases import MouseButton
from tkinter import colorchooser, simpledialog
from scipy.spatial import KDTree
import matplotlib.patches as patches
import os

# Try to import TkinterDnD for drag and drop support
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False
    print("TkinterDnD2 not found. Drag and drop functionality will be limited.")
    
    # Create a fallback class to avoid errors
    class TkinterDnD:
        @staticmethod
        def Tk():
            return tk.Tk()

class InteractivePlot:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Plot Editor")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Initialize points and data structures
        self.points = np.array([(1, 10), (2, 20), (3, 25), (4, 30)])  # Initial points as numpy array

        # Subplot related attributes
        self.subplot_fig = None
        self.subplot_gs = None
        self.subplots = {}
        self.subplot_data = {}
        self.point_labels = {}  # Dictionary for point labels
        self.annotations = {}  # Dictionary to store tooltips by point index
        self.dragging_idx = None  # Index of point being dragged
        self.is_dragging = False  # Flag to track dragging
        self.drag_start = None  # Position for drag start
        self.point_attributes = {}  # Store attributes like color and size per point

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

        # Create KDTree for point proximity detection
        self.update_kdtree()

        # Set up for subplot interaction
        self.is_resizing = False
        self.is_moving = False
        self.resize_start_pos = None
        self.selected_subplot = None
        self.resize_handle = None
        
        # For undo/redo functionality
        self.history = []
        self.future = []
        self.max_history = 20  # Maximum number of states to store
        
        # For drag and drop functionality
        self.drop_target = None

        # Create the plot tab and subplot view
        self.create_plot_tab()

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

        # Remove the annotation from the plot
        annotation.remove()

        # Remove from stored annotations
        del self.annotations[idx]

        # Redraw
        self.canvas.draw_idle()

    def edit_annotation(self, idx, annotation):
        """Edit the text of an annotation"""
        x, y = self.points[idx]
        current_text = annotation.get_text()

        # Simple dialog to edit text
        new_text = simpledialog.askstring("Edit Annotation", "Enter annotation text:",
                                        initialvalue=current_text)

        if new_text:  # If user didn't cancel
            # Save current state for undo
            self.save_state()

            # Update annotation text
            annotation.set_text(new_text)

            # Redraw
            self.canvas.draw_idle()

    def edit_label(self, label_type):
        """Edit plot labels (title, xlabel, ylabel) with font and color customization"""
        # Determine current values
        if label_type == "title":
            current_text = self.ax.get_title()
            current_fontdict = self.ax.title.get_fontdict()
        elif label_type == "xlabel":
            current_text = self.ax.get_xlabel()
            current_fontdict = self.ax.xaxis.label.get_fontdict()
        elif label_type == "ylabel":
            current_text = self.ax.get_ylabel()
            current_fontdict = self.ax.yaxis.label.get_fontdict()
        else:
            return

        # Get current font properties
        current_size = current_fontdict.get('size', 12)
        current_weight = current_fontdict.get('weight', 'normal')
        current_fontstyle = current_fontdict.get('style', 'normal')
        current_color = current_fontdict.get('color', 'black')

        # Create custom dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit {label_type.capitalize()}")
        dialog.geometry("400x350")

        # First row: text entry
        text_frame = ttk.Frame(dialog)
        text_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(text_frame, text="Text:").pack(side='left')
        text_var = tk.StringVar(value=current_text)
        text_entry = ttk.Entry(text_frame, textvariable=text_var, width=30)
        text_entry.pack(side='left', padx=5, fill='x', expand=True)

        # Second row: font size
        size_frame = ttk.Frame(dialog)
        size_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(size_frame, text="Size:").pack(side='left')
        size_var = tk.IntVar(value=current_size)
        size_combo = ttk.Combobox(size_frame, textvariable=size_var, 
                                 values=[8, 10, 12, 14, 16, 18, 20, 24, 28, 32])
        size_combo.pack(side='left', padx=5)

        # Third row: font style options
        style_frame = ttk.Frame(dialog)
        style_frame.pack(pady=10, padx=10, fill='x')

        # Bold and italic checkboxes
        bold_var = tk.BooleanVar(value=(current_weight == "bold"))
        italic_var = tk.BooleanVar(value=(current_fontstyle == "italic"))

        ttk.Checkbutton(style_frame, text="Bold", variable=bold_var).pack(side="left", padx=5)
        ttk.Checkbutton(style_frame, text="Italic", variable=italic_var).pack(side="left", padx=5)

        # Color picker
        color_frame = ttk.Frame(dialog)
        color_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(color_frame, text="Color:").pack(side='left')
        color_button = ttk.Button(color_frame, text="Choose Color", command=pick_custom_color)
        color_button.pack(side='left', padx=5)

        # Color display
        color_preview = tk.Canvas(color_frame, width=30, height=20, bg=current_color, relief="ridge", borderwidth=1)
        color_preview.pack(side='left', padx=5)
        
        # Store the current color
        color_var = tk.StringVar(value=current_color)

        # Preview frame
        preview_frame = ttk.LabelFrame(dialog, text="Preview")
        preview_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Preview canvas for rendering
        preview_canvas = tk.Canvas(preview_frame, bg='white', height=100)
        preview_canvas.pack(fill='both', expand=True)

        def pick_custom_color():
            color = colorchooser.askcolor(color_var.get())[1]
            if color:
                color_var.set(color)
                color_preview.config(bg=color)
                update_preview()

        def update_preview(*args):
            # Set up a figure for preview
            preview_fig = Figure(figsize=(4, 2), dpi=80)
            preview_ax = preview_fig.add_subplot(111)

            # Get current settings
            text = text_var.get()
            size = size_var.get()
            bold = "bold" if bold_var.get() else "normal"
            italic = "italic" if italic_var.get() else "normal"
            color = color_var.get()

            # Configure the fontdict
            fontdict = {
                'size': size,
                'weight': bold,
                'style': italic,
                'color': color
            }

            # Apply to the appropriate label in preview
            if label_type == "title":
                preview_ax.set_title(text, fontdict=fontdict)
            elif label_type == "xlabel":
                preview_ax.set_xlabel(text, fontdict=fontdict)
            elif label_type == "ylabel":
                preview_ax.set_ylabel(text, fontdict=fontdict)

            # Add some dummy data
            preview_ax.plot([0, 1, 2, 3], [0, 1, 4, 9])

            # Update canvas
            preview_canvas.delete("all")
            preview_canvas_widget = FigureCanvasTkAgg(preview_fig, master=preview_canvas)
            preview_canvas_widget.draw()
            preview_canvas_widget.get_tk_widget().pack(fill='both', expand=True)

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10, fill='x')

        ttk.Button(button_frame, text="Apply", command=apply_changes).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='right', padx=5)

        def apply_changes():
            # Save current state for undo
            self.save_state()

            # Get all settings
            text = text_var.get()
            size = size_var.get()
            bold = "bold" if bold_var.get() else "normal"
            italic = "italic" if italic_var.get() else "normal"
            color = color_var.get()

            # Configure the fontdict
            fontdict = {
                'size': size,
                'weight': bold,
                'style': italic,
                'color': color
            }

            # Store custom properties for persistence
            self.custom_labels[label_type] = fontdict

            # Apply to the appropriate label
            if label_type == "title":
                self.ax.set_title(text, fontdict=fontdict)
            elif label_type == "xlabel":
                self.ax.set_xlabel(text, fontdict=fontdict)
            elif label_type == "ylabel":
                self.ax.set_ylabel(text, fontdict=fontdict)

            # Redraw the canvas
            self.canvas.draw_idle()
            dialog.destroy()

        # Set up callbacks for live preview
        text_var.trace_add("write", update_preview)
        size_var.trace_add("write", update_preview)
        bold_var.trace_add("write", update_preview)
        italic_var.trace_add("write", update_preview)
        color_var.trace_add("write", update_preview)

        # Initial preview
        update_preview()

        # Make sure dialog is modal
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def on_press(self, event):
        """Handle mouse press events for panning, selecting, and context menu"""
        if not hasattr(event, 'button'):
            return

        if event.button == MouseButton.LEFT:
            # Check if press is on a point
            point_idx = self.get_point_index(event)
            if point_idx is not None:
                self.dragging_idx = point_idx
                self.is_dragging = True
                self.canvas.get_tk_widget().config(cursor="fleur")  # Change cursor to indicate dragging
                # Save state for undo
                self.save_state()
            else:
                # For panning, track starting position
                self.prev_x, self.prev_y = event.xdata, event.ydata

        elif event.button == MouseButton.RIGHT:
            # Check if right-clicking on an annotation
            for idx, ann in self.annotations.items():
                # Check if mouse position is near annotation position
                ax, ay = ann.xy
                # Use a reasonable distance threshold in data coordinates
                if event.inaxes == self.ax and abs(ax - event.xdata) < 0.1 and abs(ay - event.ydata) < 0.1:
                    self.show_context_menu(event, idx, ann)
                    return

            # If not on annotation, show general context menu
            self.show_tooltip_context_menu(event)

    def show_tooltip_context_menu(self, event):
        """Show a context menu for tooltip operations"""
        context_menu = Menu(self.root, tearoff=0)
        
        # Add common menu items
        context_menu.add_command(label="Add Point", command=self.add_point)
        context_menu.add_command(label="Reset Zoom", command=self.reset_zoom)
        context_menu.add_separator()
        
        # Toggle options
        context_menu.add_checkbutton(label="Show Grid", variable=self.grid_toggle_var, 
                                   command=self.toggle_grid)
        context_menu.add_checkbutton(label="Show Legend", variable=self.legend_toggle_var, 
                                   command=self.toggle_legend)
        context_menu.add_separator()
        
        # Undo/Redo
        context_menu.add_command(label="Undo", command=self.undo, state='normal' if self.history else 'disabled')
        context_menu.add_command(label="Redo", command=self.redo, state='normal' if self.future else 'disabled')
        
        # Display the menu at mouse position on canvas
        x = self.canvas.get_tk_widget().winfo_rootx() + event.x
        y = self.canvas.get_tk_widget().winfo_rooty() + event.y
        context_menu.post(x, y)

    def edit_tooltip_text(self):
        """Edit the text of the current tooltip"""
        if self.tooltip:
            current_text = self.tooltip.get_text()
            new_text = simpledialog.askstring("Edit Tooltip", "Enter tooltip text:", initialvalue=current_text)
            if new_text:
                self.tooltip.set_text(new_text)
                self.canvas.draw_idle()

    def on_motion(self, event):
        """Handle motion for panning the plot"""
        if not self.is_dragging and self.prev_x is not None and self.prev_y is not None:
            # Only handle panning if we're not dragging a point and prev_x/y are set
            if hasattr(event, 'xdata') and hasattr(event, 'ydata') and event.xdata is not None and event.ydata is not None:
                # Calculate the movement
                dx = event.xdata - self.prev_x
                dy = event.ydata - self.prev_y
                
                # Only act if the movement is significant
                if abs(dx) > 0.01 or abs(dy) > 0.01:
                    # Get current limits
                    x1, x2 = self.ax.get_xlim()
                    y1, y2 = self.ax.get_ylim()
                    
                    # Pan by moving all limits
                    self.ax.set_xlim(x1 - dx, x2 - dx)
                    self.ax.set_ylim(y1 - dy, y2 - dy)
                    
                    # Update the plot
                    self.canvas.draw_idle()
                    
                    # Update previous positions
                    self.prev_x, self.prev_y = event.xdata, event.ydata

    def on_mouse_scroll(self, event):
        """Handle mouse scroll for zooming"""
        if not hasattr(event, 'button'):
            return
            
        # Get the current mouse position for centering the zoom
        if not hasattr(event, 'xdata') or not hasattr(event, 'ydata') or event.xdata is None or event.ydata is None:
            return
            
        # Get current axis limits
        x1, x2 = self.ax.get_xlim()
        y1, y2 = self.ax.get_ylim()
        
        # Calculate center point - use mouse position
        center_x, center_y = event.xdata, event.ydata
        
        # Calculate current span
        x_span = x2 - x1
        y_span = y2 - y1
        
        # Determine zoom direction
        if event.button == 'up':  # Zoom in
            # Calculate new spans after zoom
            x_span_new = x_span / self.zoom_factor
            y_span_new = y_span / self.zoom_factor
        else:  # Zoom out
            # Calculate new spans after zoom
            x_span_new = x_span * self.zoom_factor
            y_span_new = y_span * self.zoom_factor
            
        # Calculate new limits keeping the mouse position fixed
        relative_x = (event.xdata - x1) / x_span
        relative_y = (event.ydata - y1) / y_span
        
        x1_new = event.xdata - relative_x * x_span_new
        x2_new = x1_new + x_span_new
        y1_new = event.ydata - relative_y * y_span_new
        y2_new = y1_new + y_span_new
        
        # Apply new limits
        self.ax.set_xlim(x1_new, x2_new)
        self.ax.set_ylim(y1_new, y2_new)
        
        # Update the plot
        self.canvas.draw_idle()
    
    def on_mouse_drag(self, event):
        """Handle mouse dragging for panning"""
        if self.prev_x is not None and self.prev_y is not None:
            self.on_motion(event)
            self.prev_x, self.prev_y = event.xdata, event.ydata

    def create_plot_tab(self):
        """Interactive Plot Tab with dynamic editing features."""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        
        # Split the tab into two rows
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill='x', padx=5, pady=5)
        
        # Settings panel
        settings_frame = ttk.LabelFrame(top_frame, text="Plot Settings")
        settings_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        # Line color dropdown
        ttk.Label(settings_frame, text="Line Color:").pack(anchor='w', padx=5, pady=2)
        color_frame = ttk.Frame(settings_frame)
        color_frame.pack(fill='x', padx=5, pady=2)
        
        color_values = ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "custom"]
        self.color_var = tk.StringVar(value=self.line_color)
        color_combo = ttk.Combobox(color_frame, textvariable=self.color_var, values=color_values, width=10)
        color_combo.pack(side='left')
        color_combo.bind("<<ComboboxSelected>>", self.change_line_color)
        
        color_picker_btn = ttk.Button(color_frame, text="Pick Color", command=self.open_color_picker)
        color_picker_btn.pack(side='left', padx=5)
        
        # Line style dropdown
        ttk.Label(settings_frame, text="Line Style:").pack(anchor='w', padx=5, pady=2)
        style_frame = ttk.Frame(settings_frame)
        style_frame.pack(fill='x', padx=5, pady=2)
        
        style_values = ["-", "--", "-.", ":", "custom"]
        self.style_var = tk.StringVar(value=self.line_style)
        style_combo = ttk.Combobox(style_frame, textvariable=self.style_var, values=style_values, width=10)
        style_combo.pack(side='left')
        style_combo.bind("<<ComboboxSelected>>", self.change_line_style)
        
        style_btn = ttk.Button(style_frame, text="Custom Style", command=self.open_line_style_window)
        style_btn.pack(side='left', padx=5)
        
        # Marker size slider
        ttk.Label(settings_frame, text="Marker Size:").pack(anchor='w', padx=5, pady=2)
        self.marker_size_var = tk.IntVar(value=self.marker_size)
        marker_slider = ttk.Scale(settings_frame, from_=1, to=30, variable=self.marker_size_var, 
                                 orient='horizontal', command=self.change_marker_size)
        marker_slider.pack(fill='x', padx=5, pady=2)
        
        # Toggle buttons frame
        toggle_frame = ttk.Frame(settings_frame)
        toggle_frame.pack(fill='x', padx=5, pady=10)
        
        # Grid toggle
        grid_chk = ttk.Checkbutton(toggle_frame, text="Show Grid", variable=self.grid_toggle_var, 
                                  command=self.toggle_grid)
        grid_chk.pack(anchor='w')
        
        # Legend toggle
        legend_chk = ttk.Checkbutton(toggle_frame, text="Show Legend", variable=self.legend_toggle_var, 
                                    command=self.toggle_legend)
        legend_chk.pack(anchor='w')
        
        # Legend customization button
        legend_btn = ttk.Button(toggle_frame, text="Customize Legend", command=self.customize_legend)
        legend_btn.pack(anchor='w', pady=5)
        
        # Live update toggle
        live_update_chk = ttk.Checkbutton(toggle_frame, text="Live Update", variable=self.live_update_var, 
                                    command=self.toggle_live_update)
        live_update_chk.pack(anchor='w')
        
        # Button panel
        button_frame = ttk.LabelFrame(top_frame, text="Actions")
        button_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        # Action buttons
        ttk.Button(button_frame, text="Add Point", command=self.add_point).pack(fill='x', padx=5, pady=5)
        ttk.Button(button_frame, text="Reset Plot", command=self.reset_plot).pack(fill='x', padx=5, pady=5)
        ttk.Button(button_frame, text="Zoom In", command=lambda: self.zoom(True)).pack(fill='x', padx=5, pady=5)
        ttk.Button(button_frame, text="Zoom Out", command=lambda: self.zoom(False)).pack(fill='x', padx=5, pady=5)
        ttk.Button(button_frame, text="Reset Zoom", command=self.reset_zoom).pack(fill='x', padx=5, pady=5)
        
        # Undo/Redo
        undo_frame = ttk.Frame(button_frame)
        undo_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(undo_frame, text="Undo", command=self.undo).pack(side='left', fill='x', expand=True)
        ttk.Button(undo_frame, text="Redo", command=self.redo).pack(side='left', fill='x', expand=True)
        
        # Plot frame (main plot area)
        self.plot_frame = ttk.LabelFrame(self.main_frame, text="Plot")
        self.plot_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create a matplotlib figure and add to UI
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Connect events
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('scroll_event', self.on_mouse_scroll)
        self.canvas.mpl_connect('pick_event', lambda event: None)  # Placeholder for pick events
        
        # Connect double-click for tooltips and label editing
        self.canvas.mpl_connect('button_press_event', self.on_double_click)
        
        # Plot the initial data
        self.update_plot()
        
        # Create tab for subplots
        self.create_subplot_tab()
        
        # Add to notebook
        self.notebook.add(self.main_frame, text="Interactive Plot")
        
    def create_subplot_tab(self):
        """Create tab for multiple subplot visualization."""
        self.subplot_tab = ttk.Frame(self.root)
        self.subplot_frame = ttk.LabelFrame(self.subplot_tab, text="Subplots")
        self.subplot_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Control panel frame at top
        control_frame = ttk.Frame(self.subplot_tab)
        control_frame.pack(fill='x', padx=5, pady=5, before=self.subplot_frame)
        
        # Add controls for subplots
        ttk.Button(control_frame, text="Add Subplot", command=self.add_new_subplot).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Reset Subplots", command=self.reset_subplots).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Export Plots", command=self.export_subplots).pack(side='left', padx=5)
        
        # Subplot configuration
        config_frame = ttk.LabelFrame(control_frame, text="Configuration")
        config_frame.pack(side='left', padx=10, fill='y')
        
        # Row and column configuration
        row_frame = ttk.Frame(config_frame)
        row_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(row_frame, text="Rows:").pack(side='left')
        self.rows_var = tk.IntVar(value=2)
        ttk.Spinbox(row_frame, from_=1, to=4, width=5, textvariable=self.rows_var).pack(side='left', padx=5)
        
        col_frame = ttk.Frame(config_frame)
        col_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(col_frame, text="Columns:").pack(side='left')
        self.cols_var = tk.IntVar(value=2)
        ttk.Spinbox(col_frame, from_=1, to=4, width=5, textvariable=self.cols_var).pack(side='left', padx=5)
        
        ttk.Button(config_frame, text="Apply Layout", 
                 command=self.apply_subplot_layout).pack(padx=5, pady=5)
        
        # Layout type
        layout_frame = ttk.LabelFrame(control_frame, text="Layout Type")
        layout_frame.pack(side='left', padx=10, fill='y')
        
        self.layout_var = tk.StringVar(value="grid")
        ttk.Radiobutton(layout_frame, text="Grid", variable=self.layout_var, 
                      value="grid").pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(layout_frame, text="Asymmetric", variable=self.layout_var, 
                      value="asymmetric").pack(anchor='w', padx=5, pady=2)
        
        # Initialize subplot figure with drag-and-drop support
        self.create_subplot_view()
        
        # Add the tab to notebook
        self.notebook.add(self.subplot_tab, text="Multi-Plot View")

    def create_subplot_view(self):
        """Create the subplot view with drag and drop capabilities."""
        # Create figure for subplots
        self.subplot_fig = Figure(figsize=(10, 8), dpi=100)
        
        # Create canvas
        self.subplot_canvas = FigureCanvasTkAgg(self.subplot_fig, master=self.subplot_frame)
        self.subplot_canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Connect events
        self.subplot_canvas.mpl_connect('button_press_event', self.on_subplot_press)
        self.subplot_canvas.mpl_connect('button_release_event', self.on_subplot_release)
        self.subplot_canvas.mpl_connect('motion_notify_event', self.on_subplot_motion)
        
        # Set up drag and drop functionality
        if HAS_DND:
            self.subplot_canvas.get_tk_widget().drop_target_register(DND_FILES)
            self.subplot_canvas.get_tk_widget().dnd_bind('<<Drop>>', self.on_subplot_drop)
        else:
            # Fallback method using standard file dialog
            ttk.Button(self.subplot_frame, text="Import Data", 
                     command=self.import_data_fallback).pack(pady=5)
        
        # Initialize subplots with some default examples
        self.create_default_subplots()
        
        # Set key press handler for the canvas
        self.root.bind('<KeyPress>', self.on_key_press)
        
    def on_key_press(self, event):
        """Handle key press events."""
        # Check for Ctrl+Z for undo
        if event.keysym == 'z' and (event.state & 0x4):  # 0x4 is the mask for Ctrl
            self.undo()
        # Check for Ctrl+Y for redo
        elif event.keysym == 'y' and (event.state & 0x4):
            self.redo()
        # Delete key to remove selected subplot
        elif event.keysym == 'Delete' and self.selected_subplot:
            self.delete_subplot(self.selected_subplot)
            
    def import_data_fallback(self):
        """Fallback method for importing data when drag-and-drop is not available."""
        filetypes = [
            ("Data files", "*.csv;*.xlsx;*.txt;*.json"),
            ("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
            ("NumPy arrays", "*.npy;*.npz"),
            ("All files", "*.*")
        ]
        file_path = filedialog.askopenfilename(title="Import Data", filetypes=filetypes)
        
        if file_path:
            # Find the target subplot based on user selection
            if self.subplot_fig.get_axes():
                # Show a dialog to select which subplot to use
                subplot_options = [f"Subplot {i+1}" for i, _ in enumerate(self.subplot_fig.get_axes())]
                subplot_choice = simpledialog.askinteger(
                    "Select Subplot", 
                    "Enter subplot number (1-{})".format(len(subplot_options)),
                    minvalue=1, maxvalue=len(subplot_options))
                
                if subplot_choice:
                    target_subplot = self.subplot_fig.get_axes()[subplot_choice-1]
                    self.handle_subplot_drop(file_path, target_subplot)
            else:
                # If no subplots exist, create one
                self.add_new_subplot()
                if self.subplot_fig.get_axes():
                    self.handle_subplot_drop(file_path, self.subplot_fig.get_axes()[0])

    def apply_subplot_layout(self):
        """Apply the specified layout to subplots."""
        rows = self.rows_var.get()
        cols = self.cols_var.get()
        layout_type = self.layout_var.get()
        
        # Clear the figure
        self.subplot_fig.clear()
        
        # Create new subplots based on layout type
        if layout_type == "grid":
            # Regular grid layout
            for i in range(rows * cols):
                self.subplot_fig.add_subplot(rows, cols, i + 1)
        else:
            # Asymmetric layout with GridSpec
            gs = GridSpec(rows, cols, figure=self.subplot_fig)
            
            # Create some varied layouts
            if rows >= 2 and cols >= 2:
                # Larger plot in upper left
                ax1 = self.subplot_fig.add_subplot(gs[0:2, 0:2])
                ax1.set_title("Main Plot")
                
                # Smaller plots on right and bottom
                remaining = []
                for i in range(2, cols):
                    ax = self.subplot_fig.add_subplot(gs[0, i])
                    ax.set_title(f"Plot {len(remaining)+2}")
                    remaining.append(ax)
                
                for i in range(2, cols):
                    ax = self.subplot_fig.add_subplot(gs[1, i])
                    ax.set_title(f"Plot {len(remaining)+2}")
                    remaining.append(ax)
                    
                for i in range(2, rows):
                    for j in range(cols):
                        ax = self.subplot_fig.add_subplot(gs[i, j])
                        ax.set_title(f"Plot {len(remaining)+2}")
                        remaining.append(ax)
            else:
                # Simple grid if rows or cols are too small
                for i in range(rows):
                    for j in range(cols):
                        self.subplot_fig.add_subplot(gs[i, j])
        
        # Add some sample data to each subplot
        for i, ax in enumerate(self.subplot_fig.get_axes()):
            x = np.linspace(0, 10, 100)
            ax.plot(x, np.sin(x + i))
            ax.grid(True)
            
            # Initialize plot type
            self.subplots[ax] = 'line'
        
        # Adjust layout
        self.subplot_fig.tight_layout()
        self.subplot_canvas.draw()

    def add_new_subplot(self):
        """Add a new subplot to the grid."""
        # Get current number of subplots
        num_subplots = len(self.subplot_fig.get_axes())
        
        # Calculate grid dimensions
        rows = max(1, int(np.sqrt(num_subplots + 1)))
        cols = max(1, int(np.ceil((num_subplots + 1) / rows)))
        
        # Clear and recreate all subplots
        self.subplot_fig.clear()
        
        # Create empty subplot data to preserve
        subplot_data_temp = {}
        for i, (subplot, plot_type) in enumerate(self.subplots.items()):
            subplot_data_temp[i] = {
                'type': plot_type,
                'data': self.subplot_data.get(subplot, {})
            }
        
        # Create new grid of subplots
        for i in range(num_subplots + 1):
            ax = self.subplot_fig.add_subplot(rows, cols, i + 1)
            
            # Restore data for existing subplots
            if i < num_subplots and i in subplot_data_temp:
                # Get the saved data
                saved = subplot_data_temp[i]
                plot_type = saved['type']
                data = saved['data']
                
                # Add data back to the subplot
                if 'x' in data and 'y' in data:
                    x_data = data['x']
                    y_data = data['y']
                    
                    if plot_type == 'line':
                        ax.plot(x_data, y_data)
                    elif plot_type == 'scatter':
                        ax.scatter(x_data, y_data)
                    elif plot_type == 'bar':
                        ax.bar(x_data, y_data)
                    elif plot_type == 'histogram':
                        ax.hist(y_data, bins=30)
                
                # Store the plot type
                self.subplots[ax] = plot_type
                self.subplot_data[ax] = data
            else:
                # Initialize new subplot with default data
                x = np.linspace(0, 10, 100)
                ax.plot(x, np.sin(x + i))
                ax.set_title(f"Subplot {i+1}")
                ax.grid(True)
                
                # Store plot type
                self.subplots[ax] = 'line'
        
        # Adjust layout
        self.subplot_fig.tight_layout()
        self.subplot_canvas.draw()

    def create_default_subplots(self):
        """Create default subplots with different types of plots."""
        self.subplot_fig.clear()
        
        # Create a 2x2 grid of subplots
        ax1 = self.subplot_fig.add_subplot(2, 2, 1)
        ax2 = self.subplot_fig.add_subplot(2, 2, 2)
        ax3 = self.subplot_fig.add_subplot(2, 2, 3)
        ax4 = self.subplot_fig.add_subplot(2, 2, 4)
        
        # Line plot
        x = np.linspace(0, 10, 100)
        ax1.plot(x, np.sin(x))
        ax1.set_title("Line Plot")
        ax1.grid(True)
        self.subplots[ax1] = 'line'
        self.subplot_data[ax1] = {'x': x, 'y': np.sin(x)}
        
        # Scatter plot
        x = np.random.rand(50)
        y = np.random.rand(50)
        ax2.scatter(x, y)
        ax2.set_title("Scatter Plot")
        ax2.grid(True)
        self.subplots[ax2] = 'scatter'
        self.subplot_data[ax2] = {'x': x, 'y': y}
        
        # Bar chart
        x = np.arange(5)
        y = np.random.randint(1, 20, 5)
        ax3.bar(x, y)
        ax3.set_title("Bar Chart")
        self.subplots[ax3] = 'bar'
        self.subplot_data[ax3] = {'x': x, 'y': y}
        
        # Histogram
        data = np.random.normal(0, 1, 1000)
        ax4.hist(data, bins=30)
        ax4.set_title("Histogram")
        self.subplots[ax4] = 'histogram'
        self.subplot_data[ax4] = {'x': np.arange(len(data)), 'y': data}
        
        # Adjust layout
        self.subplot_fig.tight_layout()
        self.subplot_canvas.draw()

    def on_subplot_drop(self, event):
        """Handle file drops onto subplots."""
        # Get the file path from the event
        file_path = event.data
        
        # Get mouse position relative to canvas
        x = event.widget.winfo_pointerx() - event.widget.winfo_rootx()
        y = event.widget.winfo_pointery() - event.widget.winfo_rooty()
        
        # Convert to figure coordinates
        for subplot in self.subplot_fig.get_axes():
            bbox = subplot.get_position()
            if bbox.contains(self.subplot_fig.transFigure.inverted().transform(
                (x/self.subplot_fig.dpi*self.subplot_fig.get_figwidth(),
                 y/self.subplot_fig.dpi*self.subplot_fig.get_figheight()))[0]):
                self.handle_subplot_drop(file_path, subplot)
                break

    def handle_subplot_drop(self, file_path, subplot):
        """Process dropped file for subplot."""
        try:
            if file_path.endswith('.csv') or file_path.endswith('.xlsx') or file_path.endswith('.txt'):
                # Load data from file
                if file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_path.endswith('.txt'):
                    # Try to guess delimiter for text files
                    df = pd.read_csv(file_path, sep=None, engine='python')

                # Create popup dialog for plot configuration
                plot_window = tk.Toplevel(self.root)
                plot_window.title("Plot Configuration")
                plot_window.geometry("450x500")
                plot_window.transient(self.root)
                plot_window.grab_set()  # Make window modal
                
                # Create frames for organization
                data_frame = ttk.LabelFrame(plot_window, text="Data Handling")
                data_frame.pack(fill="x", expand=False, padx=10, pady=5)
                
                plot_frame = ttk.LabelFrame(plot_window, text="Plot Type")
                plot_frame.pack(fill="x", expand=False, padx=10, pady=5)
                
                columns_frame = ttk.LabelFrame(plot_window, text="Column Selection")
                columns_frame.pack(fill="x", expand=False, padx=10, pady=5)
                
                options_frame = ttk.LabelFrame(plot_window, text="Plot Options")
                options_frame.pack(fill="x", expand=False, padx=10, pady=5)
                
                # Data handling options
                data_var = tk.StringVar(value="overwrite")
                ttk.Radiobutton(data_frame, text="Overwrite existing plot", variable=data_var, 
                               value="overwrite").pack(anchor="w", padx=20, pady=2)
                ttk.Radiobutton(data_frame, text="Append to existing data", variable=data_var, 
                               value="append").pack(anchor="w", padx=20, pady=2)
                
                # Plot type selection
                plot_var = tk.StringVar(value="line")
                
                plot_types = [
                    ("Line Plot", "line"),
                    ("Scatter Plot", "scatter"),
                    ("Bar Chart", "bar"),
                    ("Histogram", "histogram"),
                    ("Box Plot", "box"),
                    ("Pie Chart", "pie"),
                    ("Area Plot", "area"),
                    ("Step Plot", "step"),
                    ("Heatmap", "heatmap")
                ]
                
                # Create 3x3 grid of plot type options
                row, col = 0, 0
                for text, value in plot_types:
                    ttk.Radiobutton(plot_frame, text=text, variable=plot_var, 
                                   value=value).grid(row=row, column=col, sticky="w", padx=10, pady=2)
                    col += 1
                    if col > 2:  # 3 columns
                        col = 0
                        row += 1
                
                # Column selection widgets
                x_label = ttk.Label(columns_frame, text="X-Axis:")
                x_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
                
                x_var = tk.StringVar()
                x_combo = ttk.Combobox(columns_frame, textvariable=x_var, values=list(df.columns), width=20)
                x_combo.grid(row=0, column=1, sticky="w", padx=10, pady=5)
                if len(df.columns) > 0:
                    x_combo.current(0)
                
                y_label = ttk.Label(columns_frame, text="Y-Axis:")
                y_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
                
                y_var = tk.StringVar()
                y_combo = ttk.Combobox(columns_frame, textvariable=y_var, values=list(df.columns), width=20)
                y_combo.grid(row=1, column=1, sticky="w", padx=10, pady=5)
                if len(df.columns) > 1:
                    y_combo.current(1)
                elif len(df.columns) > 0:
                    y_combo.current(0)
                
                # Additional options for plots
                # Color selection
                color_label = ttk.Label(options_frame, text="Color:")
                color_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
                
                color_var = tk.StringVar(value="blue")
                color_choices = ["blue", "green", "red", "cyan", "magenta", "yellow", "black"]
                color_combo = ttk.Combobox(options_frame, textvariable=color_var, values=color_choices, width=10)
                color_combo.grid(row=0, column=1, sticky="w", padx=10, pady=5)
                
                # Line/marker style for line and scatter plots
                style_label = ttk.Label(options_frame, text="Style:")
                style_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
                
                style_var = tk.StringVar(value="-")
                style_choices = ["-", "--", "-.", ":", "None"]
                style_combo = ttk.Combobox(options_frame, textvariable=style_var, values=style_choices, width=10)
                style_combo.grid(row=1, column=1, sticky="w", padx=10, pady=5)
                
                # Grid toggle
                grid_var = tk.BooleanVar(value=True)
                grid_check = ttk.Checkbutton(options_frame, text="Show Grid", variable=grid_var)
                grid_check.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)
                
                # Title for the plot
                title_label = ttk.Label(options_frame, text="Title:")
                title_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
                
                title_var = tk.StringVar(value=os.path.basename(file_path))
                title_entry = ttk.Entry(options_frame, textvariable=title_var, width=30)
                title_entry.grid(row=3, column=1, columnspan=2, sticky="w", padx=10, pady=5)
                
                # Function to apply settings and create plot
                def apply_plot_settings():
                    # Get all settings
                    mode = data_var.get()
                    plot_type = plot_var.get()
                    
                    # Get selected columns
                    x_col = x_var.get()
                    y_col = y_var.get()
                    
                    # Plot options
                    color = color_var.get()
                    style = style_var.get()
                    use_grid = grid_var.get()
                    plot_title = title_var.get()
                    
                    # Prepare data
                    if x_col in df.columns and y_col in df.columns:
                        x_data = df[x_col]
                        y_data = df[y_col]
                    else:
                        # Fallback if columns not found
                        x_data = df.iloc[:, 0] if len(df.columns) > 0 else np.arange(len(df))
                        y_data = df.iloc[:, 1] if len(df.columns) > 1 else df.iloc[:, 0]
                    
                    # Clear the plot if overwriting
                    if mode == "overwrite":
                        subplot.clear()
                        
                        # Store the plot type for future reference
                        self.subplots[subplot] = plot_type
                        
                        # Create plot based on type
                        if plot_type == 'line':
                            subplot.plot(x_data, y_data, color=color, linestyle=style, label=y_col)
                        elif plot_type == 'scatter':
                            subplot.scatter(x_data, y_data, color=color, label=y_col)
                        elif plot_type == 'bar':
                            subplot.bar(x_data, y_data, color=color, label=y_col)
                        elif plot_type == 'histogram':
                            subplot.hist(y_data, bins=30, color=color, alpha=0.7, label=y_col)
                        elif plot_type == 'box':
                            # For box plots, can select multiple columns
                            subplot.boxplot(df[[y_col]].values, labels=[y_col])
                        elif plot_type == 'pie':
                            # For pie, use categories and values
                            subplot.pie(y_data, labels=None if len(x_data) > 10 else x_data, 
                                       autopct='%1.1f%%', colors=plt.cm.tab10.colors)
                        elif plot_type == 'area':
                            subplot.fill_between(x_data, y_data, alpha=0.5, color=color, label=y_col)
                        elif plot_type == 'step':
                            subplot.step(x_data, y_data, color=color, linestyle=style, label=y_col)
                        elif plot_type == 'heatmap':
                            # Use more columns for heatmap if available
                            if len(df.columns) > 5:
                                data_matrix = df.iloc[:10, :10].values  # Limit size for performance
                                im = subplot.imshow(data_matrix, cmap='viridis')
                                subplot.figure.colorbar(im, ax=subplot)
                            else:
                                messagebox.showinfo("Limited Data", 
                                                 "Heatmap works best with matrix-like data (>5 columns)")
                                subplot.text(0.5, 0.5, "Need more columns for heatmap", 
                                           ha='center', va='center', transform=subplot.transAxes)
                        
                        # Store the data
                        self.subplot_data[subplot] = {'x': x_data, 'y': y_data}
                    
                    else:  # Append mode
                        if subplot in self.subplot_data:
                            current_data = self.subplot_data[subplot]
                            
                            # Only certain plot types support appending
                            if self.subplots.get(subplot) in ['line', 'scatter', 'step']:
                                # Append the data
                                try:
                                    new_x = pd.concat([current_data['x'], x_data])
                                    new_y = pd.concat([current_data['y'], y_data])
                                    
                                    # Update the plot
                                    subplot.clear()
                                    
                                    if self.subplots[subplot] == 'line':
                                        subplot.plot(new_x, new_y, color=color, linestyle=style, label=y_col)
                                    elif self.subplots[subplot] == 'scatter':
                                        subplot.scatter(new_x, new_y, color=color, label=y_col)
                                    elif self.subplots[subplot] == 'step':
                                        subplot.step(new_x, new_y, color=color, linestyle=style, label=y_col)
                                    
                                    # Update stored data
                                    self.subplot_data[subplot] = {'x': new_x, 'y': new_y}
                                except Exception as e:
                                    messagebox.showerror("Append Error", 
                                                     f"Could not append data: {str(e)}\nFalling back to overwrite.")
                                    # Fall back to overwrite
                                    subplot.clear()
                                    if self.subplots[subplot] == 'line':
                                        subplot.plot(x_data, y_data, color=color, linestyle=style, label=y_col)
                                    elif self.subplots[subplot] == 'scatter':
                                        subplot.scatter(x_data, y_data, color=color, label=y_col)
                                    elif self.subplots[subplot] == 'step':
                                        subplot.step(x_data, y_data, color=color, linestyle=style, label=y_col)
                                    self.subplot_data[subplot] = {'x': x_data, 'y': y_data}
                            else:
                                messagebox.showinfo("Append Not Supported", 
                                                 f"Append not supported for {self.subplots.get(subplot)} plots.\nOverwriting instead.")
                                # Fall back to overwrite for unsupported types
                                subplot.clear()
                                if plot_type == 'line':
                                    subplot.plot(x_data, y_data, color=color, linestyle=style, label=y_col)
                                elif plot_type == 'scatter':
                                    subplot.scatter(x_data, y_data, color=color, label=y_col)
                                elif plot_type == 'bar':
                                    subplot.bar(x_data, y_data, color=color, label=y_col)
                                self.subplots[subplot] = plot_type
                                self.subplot_data[subplot] = {'x': x_data, 'y': y_data}
                        else:
                            # No existing data, treat as overwrite
                            subplot.clear()
                            if plot_type == 'line':
                                subplot.plot(x_data, y_data, color=color, linestyle=style, label=y_col)
                            elif plot_type == 'scatter':
                                subplot.scatter(x_data, y_data, color=color, label=y_col)
                            self.subplots[subplot] = plot_type
                            self.subplot_data[subplot] = {'x': x_data, 'y': y_data}
                    
                    # Apply common styling
                    subplot.set_title(plot_title)
                    subplot.grid(use_grid)
                    
                    # Add axis labels if not pie chart
                    if plot_type != 'pie':
                        subplot.set_xlabel(x_col)
                        subplot.set_ylabel(y_col)
                    
                    # Add legend for most plot types
                    if plot_type not in ['pie', 'box', 'heatmap']:
                        subplot.legend()
                    
                    # Update the canvas
                    self.subplot_canvas.draw()
                    plot_window.destroy()
                
                # Apply button at bottom
                ttk.Button(plot_window, text="Apply", command=apply_plot_settings).pack(pady=15)
                
            elif file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Handle image files - show them in a subplot
                subplot.clear()
                try:
                    from PIL import Image
                    img = Image.open(file_path)
                    subplot.imshow(np.array(img))
                    subplot.axis('off')  # Turn off axis for images
                    subplot.set_title(os.path.basename(file_path))
                    self.subplot_canvas.draw()
                except ImportError:
                    img = plt.imread(file_path)
                    subplot.imshow(img)
                    subplot.axis('off')
                    subplot.set_title(os.path.basename(file_path))
                    self.subplot_canvas.draw()
                    
            elif file_path.lower().endswith(('.npy', '.npz')):
                # Handle NumPy data files
                try:
                    data = np.load(file_path)
                    subplot.clear()
                    
                    if file_path.endswith('.npz'):
                        # For .npz files, show options to choose which array to plot
                        keys = list(data.keys())
                        chosen_key = simpledialog.askstring(
                            "Choose Array", f"Available arrays: {', '.join(keys)}\nEnter array name:")
                        
                        if chosen_key and chosen_key in keys:
                            array_data = data[chosen_key]
                        else:
                            array_data = data[keys[0]]  # default to first array
                    else:
                        array_data = data
                    
                    # Plot based on dimensions
                    if array_data.ndim == 1:
                        subplot.plot(array_data)
                    elif array_data.ndim == 2:
                        if min(array_data.shape) <= 10:  # Treat as X,Y data if one dimension is small
                            if array_data.shape[0] <= 10:
                                for i in range(array_data.shape[0]):
                                    subplot.plot(array_data[i], label=f'Series {i+1}')
                            else:
                                for i in range(array_data.shape[1]):
                                    subplot.plot(array_data[:, i], label=f'Series {i+1}')
                            subplot.legend()
                        else:  # Treat as image/heatmap
                            subplot.imshow(array_data, cmap='viridis')
                            plt.colorbar(subplot.imshow(array_data, cmap='viridis'), ax=subplot)
                    
                    subplot.set_title(os.path.basename(file_path))
                    subplot.grid(True)
                    self.subplot_canvas.draw()
                    
                except Exception as e:
                    messagebox.showerror("NumPy Load Error", f"Error loading NumPy file: {str(e)}")
            
            else:
                messagebox.showinfo("Unsupported File", 
                                  f"File type not supported: {os.path.basename(file_path)}\nSupported types: CSV, Excel, TXT, image files, and NumPy arrays")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def delete_subplot(self, subplot):
        """Delete a selected subplot."""
        if subplot not in self.subplot_fig.get_axes():
            return
            
        # Remove the subplot
        self.subplot_fig.delaxes(subplot)
        
        # Clear data
        if subplot in self.subplots:
            del self.subplots[subplot]
        if subplot in self.subplot_data:
            del self.subplot_data[subplot]
            
        # Reset selection
        self.selected_subplot = None
        
        # Redraw all remaining subplots in a grid
        self.rearrange_subplots()
        
    def rearrange_subplots(self):
        """Rearrange subplots after deletion or addition."""
        # Save existing subplot data
        existing_subplots = []
        for ax in self.subplot_fig.get_axes():
            if ax in self.subplots:
                existing_subplots.append({
                    'type': self.subplots[ax],
                    'data': self.subplot_data.get(ax, {}),
                    'title': ax.get_title(),
                    'xlabel': ax.get_xlabel(),
                    'ylabel': ax.get_ylabel()
                })
        
        # Clear figure
        self.subplot_fig.clear()
        
        # Recreate grid
        num_subplots = len(existing_subplots)
        if num_subplots == 0:
            # Add a default subplot if none exist
            ax = self.subplot_fig.add_subplot(111)
            ax.set_title("Empty Plot")
            self.subplots[ax] = 'line'
            self.subplot_canvas.draw()
            return
            
        # Calculate new grid layout
        rows = int(np.ceil(np.sqrt(num_subplots)))
        cols = int(np.ceil(num_subplots / rows))
        
        # Recreate each subplot
        for i, subplot_data in enumerate(existing_subplots):
            ax = self.subplot_fig.add_subplot(rows, cols, i + 1)
            
            # Restore plot type and data
            plot_type = subplot_data['type']
            data = subplot_data['data']
            
            # Set labels
            ax.set_title(subplot_data['title'])
            ax.set_xlabel(subplot_data['xlabel'])
            ax.set_ylabel(subplot_data['ylabel'])
            
            # Restore data
            if 'x' in data and 'y' in data:
                x_data = data['x']
                y_data = data['y']
                
                if plot_type == 'line':
                    ax.plot(x_data, y_data)
                elif plot_type == 'scatter':
                    ax.scatter(x_data, y_data)
                elif plot_type == 'bar':
                    ax.bar(x_data, y_data)
                elif plot_type == 'histogram':
                    ax.hist(y_data, bins=30)
                
                # Add grid if needed
                ax.grid(True)
                
            # Store plot type and data
            self.subplots[ax] = plot_type
            self.subplot_data[ax] = data
            
        # Adjust layout
        self.subplot_fig.tight_layout()
        self.subplot_canvas.draw()

    def reset_subplots(self):
        """Reset all subplots to their default state."""
        # Confirm reset
        if messagebox.askyesno("Reset Subplots", "Are you sure you want to reset all subplots?"):
            # Clear all data
            self.subplots.clear()
            self.subplot_data.clear()
            
            # Create default subplots
            self.create_default_subplots()

    def export_subplots(self):
        """Export all subplots as separate files."""
        # Create a directory selector
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        
        if not export_dir:
            return
            
        # Get file format
        formats = [("PNG", "png"), ("PDF", "pdf"), ("SVG", "svg"), ("JPEG", "jpg")]
        format_window = tk.Toplevel(self.root)
        format_window.title("Export Format")
        format_window.transient(self.root)
        format_window.grab_set()
        
        # Format selection
        ttk.Label(format_window, text="Select export format:").pack(padx=10, pady=10)
        
        format_var = tk.StringVar(value="png")
        for text, value in formats:
            ttk.Radiobutton(format_window, text=text, variable=format_var, value=value).pack(anchor='w', padx=20)
        
        # DPI selection for raster formats
        dpi_frame = ttk.Frame(format_window)
        dpi_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(dpi_frame, text="DPI (for PNG/JPEG):").pack(side='left')
        dpi_var = tk.IntVar(value=300)
        ttk.Spinbox(dpi_frame, from_=72, to=600, width=5, textvariable=dpi_var).pack(side='left', padx=5)
        
        # Export button
        def do_export():
            fmt = format_var.get()
            dpi = dpi_var.get()
            
            try:
                # Export each subplot
                for i, ax in enumerate(self.subplot_fig.get_axes()):
                    # Create a new figure for this subplot
                    fig = Figure(figsize=(8, 6), dpi=dpi)
                    new_ax = fig.add_subplot(111)
                    
                    # Copy content from the original subplot
                    for line in ax.lines:
                        new_ax.plot(line.get_xdata(), line.get_ydata(), 
                                    color=line.get_color(), 
                                    linestyle=line.get_linestyle(),
                                    marker=line.get_marker(),
                                    linewidth=line.get_linewidth())
                    
                    for collection in ax.collections:
                        if hasattr(collection, 'get_offsets'):  # Scatter plots
                            offsets = collection.get_offsets()
                            if len(offsets) > 0:
                                new_ax.scatter(offsets[:, 0], offsets[:, 1], 
                                              color=collection.get_facecolor()[0])
                    
                    # Copy basic properties
                    new_ax.set_title(ax.get_title())
                    new_ax.set_xlabel(ax.get_xlabel())
                    new_ax.set_ylabel(ax.get_ylabel())
                    new_ax.grid(ax.get_grid())
                    
                    # Set limits
                    new_ax.set_xlim(ax.get_xlim())
                    new_ax.set_ylim(ax.get_ylim())
                    
                    # Save figure
                    filename = f"subplot_{i+1}.{fmt}"
                    filepath = os.path.join(export_dir, filename)
                    fig.savefig(filepath, format=fmt, dpi=dpi, bbox_inches='tight')
                
                messagebox.showinfo("Export Complete", 
                                  f"Successfully exported {len(self.subplot_fig.get_axes())} subplots to {export_dir}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting subplots: {str(e)}")
            
            format_window.destroy()
        
        ttk.Button(format_window, text="Export", command=do_export).pack(pady=10)

    def on_subplot_press(self, event):
        """Handle mouse press events for subplot resizing and repositioning."""
        if not event.inaxes:
            return
            
        self.dragging = True
        self.resize_subplot = event.inaxes
        self.resize_start = (event.x, event.y)
        
        # Store the subplot for selection highlighting
        self.selected_subplot = event.inaxes
        
        # Detect edges for resize vs. reposition
        pos = self.resize_subplot.get_position()
        subplot_width = pos.width * self.subplot_fig.get_figwidth() * self.subplot_fig.dpi
        subplot_height = pos.height * self.subplot_fig.get_figheight() * self.subplot_fig.dpi
        
        # Get the subplot boundaries in pixels
        x0 = pos.x0 * self.subplot_fig.get_figwidth() * self.subplot_fig.dpi
        y0 = pos.y0 * self.subplot_fig.get_figheight() * self.subplot_fig.dpi
        x1 = x0 + subplot_width
        y1 = y0 + subplot_height
        
        # Edge detection - check if near edge (within 15 pixels)
        edge_threshold = 15
        near_right = abs(event.x - x1) < edge_threshold
        near_bottom = abs(event.y - y1) < edge_threshold
        near_left = abs(event.x - x0) < edge_threshold
        near_top = abs(event.y - y0) < edge_threshold
        
        # Determine action type
        if (near_right and near_bottom) or (near_left and near_top):
            self.action_type = "resize"  # Corner resize (diagonal)
            if near_right and near_bottom:
                self.resize_edge = "bottom-right"
            else:
                self.resize_edge = "top-left"
            self.subplot_canvas.get_tk_widget().config(cursor="sizing")
        elif near_right or near_left:
            self.action_type = "resize_width"  # Horizontal resize
            self.resize_edge = "right" if near_right else "left"
            self.subplot_canvas.get_tk_widget().config(cursor="sb_h_double_arrow")
        elif near_bottom or near_top:
            self.action_type = "resize_height"  # Vertical resize
            self.resize_edge = "bottom" if near_bottom else "top"
            self.subplot_canvas.get_tk_widget().config(cursor="sb_v_double_arrow")
        else:
            self.action_type = "move"  # Move entire subplot
            self.subplot_canvas.get_tk_widget().config(cursor="fleur")

    def on_subplot_release(self, event):
        """Handle mouse release events for subplot resizing."""
        self.dragging = False
        self.resize_subplot = None
        self.resize_start = None
        self.action_type = None
        self.resize_edge = None
        self.subplot_canvas.get_tk_widget().config(cursor="")  # Reset cursor

    def on_subplot_motion(self, event):
        """Handle mouse motion events for subplot resizing and repositioning."""
        if not self.dragging or not self.resize_subplot:
            return
            
        # Calculate movement amount
        dx = event.x - self.resize_start[0]
        dy = event.y - self.resize_start[1]
        
        # Convert to figure coordinates
        dx_fig = dx / self.subplot_fig.dpi / self.subplot_fig.get_figwidth()
        dy_fig = dy / self.subplot_fig.dpi / self.subplot_fig.get_figheight()
        
        # Get current position
        pos = self.resize_subplot.get_position()
        
        # Apply changes based on action type
        if self.action_type == "resize":
            # Diagonal resize (bottom-right or top-left corner)
            if self.resize_edge == "bottom-right":
                new_pos = [pos.x0, pos.y0, 
                          max(0.1, pos.width + dx_fig),  # Minimum width of 10%
                          max(0.1, pos.height + dy_fig)]  # Minimum height of 10%
            else:  # top-left
                new_pos = [min(pos.x0 + dx_fig, pos.x0 + pos.width - 0.1),  # Stay within right edge
                          min(pos.y0 + dy_fig, pos.y0 + pos.height - 0.1),  # Stay within bottom edge
                          max(0.1, pos.width - dx_fig),
                          max(0.1, pos.height - dy_fig)]
                          
        elif self.action_type == "resize_width":
            # Horizontal resize
            if self.resize_edge == "right":
                new_pos = [pos.x0, pos.y0, 
                          max(0.1, pos.width + dx_fig),  # Minimum width of 10%
                          pos.height]
            else:  # left edge
                new_pos = [min(pos.x0 + dx_fig, pos.x0 + pos.width - 0.1),  # Stay within right edge
                          pos.y0,
                          max(0.1, pos.width - dx_fig),
                          pos.height]
                
        elif self.action_type == "resize_height":
            # Vertical resize
            if self.resize_edge == "bottom":
                new_pos = [pos.x0, pos.y0, 
                          pos.width,
                          max(0.1, pos.height + dy_fig)]  # Minimum height of 10%
            else:  # top edge
                new_pos = [pos.x0,
                          min(pos.y0 + dy_fig, pos.y0 + pos.height - 0.1),  # Stay within bottom edge
                          pos.width,
                          max(0.1, pos.height - dy_fig)]
                
        elif self.action_type == "move":
            # Move the entire subplot
            # Ensure it stays within figure boundaries (0 to 1)
            new_x0 = max(0, min(1 - pos.width, pos.x0 + dx_fig))
            new_y0 = max(0, min(1 - pos.height, pos.y0 + dy_fig))
            new_pos = [new_x0, new_y0, pos.width, pos.height]
            
        # Update the position 
        self.resize_subplot.set_position(new_pos)
        
        # Set the current point as the new start point
        self.resize_start = (event.x, event.y)
        
        # Redraw the canvas
        self.subplot_canvas.draw_idle()

    def zoom(self, zoom_in=True):
        """Zoom in or out on the plot"""
        # Get current axis limits
        x1, x2 = self.ax.get_xlim()
        y1, y2 = self.ax.get_ylim()
        
        # Calculate center point
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        # Calculate current span
        x_span = x2 - x1
        y_span = y2 - y1
        
        if zoom_in:
            # Calculate new spans after zoom in
            x_span_new = x_span / self.zoom_factor
            y_span_new = y_span / self.zoom_factor
        else:
            # Calculate new spans after zoom out
            x_span_new = x_span * self.zoom_factor
            y_span_new = y_span * self.zoom_factor
            
        # Calculate new limits centered on the original center
        x1_new = center_x - x_span_new / 2
        x2_new = center_x + x_span_new / 2
        y1_new = center_y - y_span_new / 2
        y2_new = center_y + y_span_new / 2
        
        # Apply new limits
        self.ax.set_xlim(x1_new, x2_new)
        self.ax.set_ylim(y1_new, y2_new)
        
        # Update the plot
        self.canvas.draw_idle()

    def reset_zoom(self):
        """Reset zoom to original view"""
        # Find data limits
        min_x = np.min(self.points[:, 0])
        max_x = np.max(self.points[:, 0])
        min_y = np.min(self.points[:, 1])
        max_y = np.max(self.points[:, 1])
        
        # Add padding (10%)
        x_padding = (max_x - min_x) * 0.1
        y_padding = (max_y - min_y) * 0.1
        
        # Set limits
        self.ax.set_xlim(min_x - x_padding, max_x + x_padding)
        self.ax.set_ylim(min_y - y_padding, max_y + y_padding)
        
        # Update the plot
        self.canvas.draw_idle()

    def reset_plot(self):
        """Reset the plot to its initial state"""
        # Confirm reset
        if messagebox.askyesno("Reset Plot", "Are you sure you want to reset the plot to its initial state?"):
            # Reset points to initial state
            self.points = self.initial_points.copy()
            self.update_kdtree()
            
            # Clear annotations
            for ann in self.annotations.values():
                ann.remove()
            self.annotations.clear()
            
            # Reset styles to initial values
            self.line_style = self.initial_line_style
            self.line_color = self.initial_line_color
            self.marker_size = self.initial_marker_size
            
            # Update style variables
            self.color_var.set(self.line_color)
            self.style_var.set(self.line_style)
            self.marker_size_var.set(self.marker_size)
            
            # Reset toggles
            self.grid_toggle_var.set(False)
            self.legend_toggle_var.set(False)
            
            # Stop live update if running
            if self.live_update_var.get():
                self.toggle_live_update()
                
            # Update the plot
            self.update_plot()
            
            # Reset zoom
            self.reset_zoom()

    def toggle_grid(self):
        """Toggle gridlines on/off"""
        self.ax.grid(self.grid_toggle_var.get())
        self.canvas.draw_idle()

    def toggle_legend(self):
        """Toggle legend display on/off"""
        if self.legend_toggle_var.get():
            self.ax.legend().set_visible(True)
        else:
            if self.ax.get_legend():
                self.ax.get_legend().set_visible(False)
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
            if not self.live_update_var.get():
                return
                
            # Add noise to points
            self.points = self.points + np.random.normal(0, 0.1, self.points.shape)
            self.update_kdtree()
            
            # Update annotations if they exist
            for point_idx, ann in self.annotations.items():
                x, y = self.points[point_idx]
                ann.xy = (x, y)
                ann.set_text(f"({x:.2f}, {y:.2f})")
                
            # Update the plot
            self.update_plot()
            
            # Schedule next update
            self.live_update_task_id = self.root.after(100, update)
            
        # Start the updates
        self.live_update_task_id = self.root.after(100, update)

    def stop_live_update(self):
        """Stop live updating of the plot"""
        if self.live_update_task_id:
            self.root.after_cancel(self.live_update_task_id)
            self.live_update_task_id = None

    def change_line_color(self, event=None):
        """Change the line color based on combobox selection"""
        # Save current state for undo
        self.save_state()
        
        color = self.color_var.get()
        if color == "custom":
            self.open_color_picker()
        else:
            self.line_color = color
            self.update_plot()

    def change_line_style(self, event=None):
        """Change the line style based on combobox selection"""
        # Save current state for undo
        self.save_state()
        
        style = self.style_var.get()
        if style == "custom":
            self.open_line_style_window()
        else:
            self.line_style = style
            self.update_plot()

    def change_marker_size(self, event=None):
        """Change marker size based on slider value"""
        # Save current state for undo
        self.save_state()
        
        self.marker_size = self.marker_size_var.get()
        self.update_plot()

    def open_color_picker(self):
        """Open a color picker and update the line color"""
        color = colorchooser.askcolor(self.line_color)[1]
        if color:
            self.line_color = color
            # Update the dropdown to show "custom"
            self.color_var.set("custom")
            self.update_plot()

    def open_line_style_window(self):
        """Open a pop-up window to enter a custom line style"""
        style_window = tk.Toplevel(self.root)
        style_window.title("Custom Line Style")
        style_window.geometry("300x150")
        
        ttk.Label(style_window, text="Enter custom line style:").pack(pady=5)
        
        examples_frame = ttk.Frame(style_window)
        examples_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(examples_frame, text="Examples: '-' (solid), '--' (dashed),\n'-.' (dash-dot), ':' (dotted),\nor a tuple like (0, (1, 1))").pack()
        
        style_var = tk.StringVar(value=self.line_style)
        style_entry = ttk.Entry(style_window, textvariable=style_var, width=20)
        style_entry.pack(pady=5)
        
        def apply_style():
            """Apply the entered line style"""
            try:
                # Try to evaluate as tuple if it's formatted like one
                new_style = style_var.get()
                if '(' in new_style and ')' in new_style:
                    new_style = eval(new_style)
                    
                # Test if the style is valid by plotting
                test_fig = Figure(figsize=(1, 1))
                test_ax = test_fig.add_subplot(111)
                test_ax.plot([0, 1], [0, 1], linestyle=new_style)
                
                # If we get here, the style is valid
                self.line_style = new_style
                self.style_var.set("custom")
                self.update_plot()
                style_window.destroy()
            except Exception as e:
                messagebox.showerror("Invalid Style", f"Error: {str(e)}\nPlease enter a valid line style.")
        
        ttk.Button(style_window, text="Apply", command=apply_style).pack(pady=10)
        
        # Make dialog modal
        style_window.transient(self.root)
        style_window.grab_set()
        self.root.wait_window(style_window)

    def customize_legend(self):
        """Popup window for manual legend customization"""
        legend_window = tk.Toplevel(self.root)
        legend_window.title("Customize Legend")
        legend_window.geometry("350x250")
        
        # Location options
        loc_frame = ttk.LabelFrame(legend_window, text="Location")
        loc_frame.pack(fill='x', padx=10, pady=5)
        
        locations = [
            ("Best (Auto)", "best"),
            ("Upper Right", "upper right"),
            ("Upper Left", "upper left"),
            ("Lower Left", "lower left"),
            ("Lower Right", "lower right"),
            ("Center", "center")
        ]
        
        loc_var = tk.StringVar(value="best")
        row, col = 0, 0
        for text, value in locations:
            ttk.Radiobutton(loc_frame, text=text, variable=loc_var, value=value).grid(
                row=row, column=col, sticky='w', padx=5, pady=2)
            col += 1
            if col > 1:  # 2 columns
                col = 0
                row += 1
        
        # Title and properties
        props_frame = ttk.LabelFrame(legend_window, text="Properties")
        props_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(props_frame, text="Title:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        title_var = tk.StringVar(value="")
        ttk.Entry(props_frame, textvariable=title_var).grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        
        # Font size
        ttk.Label(props_frame, text="Font Size:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        fontsize_var = tk.IntVar(value=10)
        ttk.Spinbox(props_frame, from_=6, to=20, width=5, textvariable=fontsize_var).grid(
            row=1, column=1, sticky='w', padx=5, pady=2)
        
        # Frame options
        frame_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(props_frame, text="Show Frame", variable=frame_var).grid(
            row=2, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        
        shadow_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(props_frame, text="Show Shadow", variable=shadow_var).grid(
            row=3, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        
        # Preview button
        ttk.Button(legend_window, text="Preview", 
                 command=lambda: self.apply_legend(preview=True, 
                                                 loc=loc_var.get(),
                                                 title=title_var.get(),
                                                 fontsize=fontsize_var.get(),
                                                 frameon=frame_var.get(),
                                                 shadow=shadow_var.get())).pack(pady=5)
        
        # Apply button
        ttk.Button(legend_window, text="Apply", 
                 command=lambda: [self.apply_legend(preview=False,
                                                  loc=loc_var.get(),
                                                  title=title_var.get(),
                                                  fontsize=fontsize_var.get(),
                                                  frameon=frame_var.get(),
                                                  shadow=shadow_var.get()),
                                 legend_window.destroy()]).pack(pady=5)

    def apply_legend(self, preview=False, **kwargs):
        """Apply legend changes with preview option"""
        # Save current state for undo if not just previewing
        if not preview:
            self.save_state()
            
        # Toggle legend on if it's not already
        if not self.legend_toggle_var.get():
            self.legend_toggle_var.set(True)
            
        # Apply changes and redraw
        legend = self.ax.legend(**kwargs)
        self.canvas.draw_idle()

    def add_point(self):
        """Add a new point to the plot"""
        # Save current state for undo
        self.save_state()
        
        # Get current axis limits
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        # Create a new random point within the visible area
        new_x = np.random.uniform(xlim[0], xlim[1])
        new_y = np.random.uniform(ylim[0], ylim[1])
        
        # Add to points array
        self.points = np.vstack([self.points, [new_x, new_y]])
        self.update_kdtree()
        
        # Update the plot
        self.update_plot()

    def save_state(self):
        """Save current state for undo functionality"""
        # Create a state dictionary
        state = {
            'points': self.points.copy(),
            'annotations': {idx: ann.get_text() for idx, ann in self.annotations.items()},
            'line_style': self.line_style,
            'line_color': self.line_color,
            'marker_size': self.marker_size,
            'grid': self.grid_toggle_var.get(),
            'legend': self.legend_toggle_var.get()
        }
        
        # Add to history, limited to max size
        self.history.append(state)
        if len(self.history) > self.max_history:
            self.history.pop(0)
            
        # Clear future when a new action is performed
        self.future = []

    def undo(self):
        """Undo the last action"""
        if not self.history:
            messagebox.showinfo("Undo", "Nothing to undo")
            return
            
        # Get current state
        current_state = {
            'points': self.points.copy(),
            'annotations': {idx: ann.get_text() for idx, ann in self.annotations.items()},
            'line_style': self.line_style,
            'line_color': self.line_color,
            'marker_size': self.marker_size,
            'grid': self.grid_toggle_var.get(),
            'legend': self.legend_toggle_var.get()
        }
        
        # Move current state to future
        self.future.append(current_state)
        
        # Restore previous state
        prev_state = self.history.pop()
        self.points = prev_state['points'].copy()
        self.update_kdtree()
        
        # Clear current annotations
        for ann in self.annotations.values():
            ann.remove()
        self.annotations.clear()
        
        # Restore annotations
        for idx, text in prev_state['annotations'].items():
            if idx < len(self.points):
                x, y = self.points[idx]
                ann = self.ax.annotate(
                    text,
                    xy=(x, y),
                    xytext=(10, 10),
                    textcoords="offset points",
                    fontsize=9,
                    color='black',
                    bbox=dict(boxstyle="round", fc="yellow", alpha=0.7),
                    arrowprops=dict(arrowstyle="->"),
                    zorder=1000
                )
                self.annotations[idx] = ann
        
        # Restore styles
        self.line_style = prev_state['line_style']
        self.line_color = prev_state['line_color']
        self.marker_size = prev_state['marker_size']
        
        # Update style variables
        self.color_var.set(self.line_color if self.line_color in ["blue", "green", "red", "cyan", "magenta", "yellow", "black"] else "custom")
        self.style_var.set(self.line_style if self.line_style in ["-", "--", "-.", ":"] else "custom")
        self.marker_size_var.set(self.marker_size)
        
        # Restore toggles
        self.grid_toggle_var.set(prev_state['grid'])
        self.legend_toggle_var.set(prev_state['legend'])
        
        # Update the plot
        self.update_plot()

    def redo(self):
        """Redo the last undone action"""
        if not self.future:
            messagebox.showinfo("Redo", "Nothing to redo")
            return
            
        # Get current state
        current_state = {
            'points': self.points.copy(),
            'annotations': {idx: ann.get_text() for idx, ann in self.annotations.items()},
            'line_style': self.line_style,
            'line_color': self.line_color,
            'marker_size': self.marker_size,
            'grid': self.grid_toggle_var.get(),
            'legend': self.legend_toggle_var.get()
        }
        
        # Move current state to history
        self.history.append(current_state)
        
        # Restore future state
        future_state = self.future.pop()
        self.points = future_state['points'].copy()
        self.update_kdtree()
        
        # Clear current annotations
        for ann in self.annotations.values():
            ann.remove()
        self.annotations.clear()
        
        # Restore annotations
        for idx, text in future_state['annotations'].items():
            if idx < len(self.points):
                x, y = self.points[idx]
                ann = self.ax.annotate(
                    text,
                    xy=(x, y),
                    xytext=(10, 10),
                    textcoords="offset points",
                    fontsize=9,
                    color='black',
                    bbox=dict(boxstyle="round", fc="yellow", alpha=0.7),
                    arrowprops=dict(arrowstyle="->"),
                    zorder=1000
                )
                self.annotations[idx] = ann
        
        # Restore styles
        self.line_style = future_state['line_style']
        self.line_color = future_state['line_color']
        self.marker_size = future_state['marker_size']
        
        # Update style variables
        self.color_var.set(self.line_color if self.line_color in ["blue", "green", "red", "cyan", "magenta", "yellow", "black"] else "custom")
        self.style_var.set(self.line_style if self.line_style in ["-", "--", "-.", ":"] else "custom")
        self.marker_size_var.set(self.marker_size)
        
        # Restore toggles
        self.grid_toggle_var.set(future_state['grid'])
        self.legend_toggle_var.set(future_state['legend'])
        
        # Update the plot
        self.update_plot()

    def update_plot(self):
        """Update the entire plot with current settings"""
        # Clear the axis
        self.ax.clear()
        
        # Plot the points
        self.plot_points()
        
        # Add custom labels if they exist
        for label_type, fontdict in self.custom_labels.items():
            if label_type == "title":
                self.ax.set_title(self.ax.get_title(), fontdict=fontdict)
            elif label_type == "xlabel":
                self.ax.set_xlabel(self.ax.get_xlabel(), fontdict=fontdict)
            elif label_type == "ylabel":
                self.ax.set_ylabel(self.ax.get_ylabel(), fontdict=fontdict)
        
        # Add grid if toggled
        self.ax.grid(self.grid_toggle_var.get())
        
        # Add legend if toggled
        if self.legend_toggle_var.get():
            self.ax.legend()
            
        # Redraw canvas
        self.canvas.draw_idle()

    def plot_points(self):
        """Plot points and connecting lines with current styles"""
        # Default labels if not set
        if not self.ax.get_title():
            self.ax.set_title("Interactive Plot")
        if not self.ax.get_xlabel():
            self.ax.set_xlabel("X-axis")
        if not self.ax.get_ylabel():
            self.ax.set_ylabel("Y-axis")
            
        # Plot the line connecting points
        self.ax.plot(self.points[:, 0], self.points[:, 1], 
                   linestyle=self.line_style, 
                   color=self.line_color, 
                   marker='o', 
                   markersize=self.marker_size, 
                   label="Data Points")
        
        # Recreate annotations if they exist
        new_annotations = {}
        for idx, ann in self.annotations.items():
            if idx < len(self.points):
                x, y = self.points[idx]
                new_ann = self.ax.annotate(
                    ann.get_text(),
                    xy=(x, y),
                    xytext=(10, 10),
                    textcoords="offset points",
                    fontsize=9,
                    color='black',
                    bbox=dict(boxstyle="round", fc="yellow", alpha=0.7),
                    arrowprops=dict(arrowstyle="->"),
                    zorder=1000
                )
                new_annotations[idx] = new_ann
        
        # Update annotations
        self.annotations = new_annotations

def main():
    # Create root window using TkinterDnD if available
    if HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
        
    root.title("AutoViz - Advanced Data Visualization")
    root.geometry("1200x800")
    
    # Create the interactive plot application
    app = InteractivePlot(root)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()