import tkinter as tk
from tkinter import ttk, Menu, filedialog, simpledialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseButton
from tkinter import colorchooser
from scipy.spatial import KDTree
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import pandas as pd
import os
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import io
from PIL import Image, ImageTk


class SubplotManager:
    """Manages subplot configuration and data"""
    def __init__(self, fig, master):
        self.fig = fig
        self.master = master
        self.subplots = {}  # Store subplot info by ID
        self.next_id = 1    # For generating unique subplot IDs
        self.active_subplot = None
        self.gs = gridspec.GridSpec(2, 2, figure=self.fig)  # Default 2x2 grid
        self.grid_rows = 2
        self.grid_cols = 2
    
    def add_subplot(self, subplot_type="line", row=0, col=0, rowspan=1, colspan=1):
        """Add a new subplot to the figure"""
        subplot_id = f"subplot_{self.next_id}"
        self.next_id += 1
        
        # Create the subplot in the specified position
        ax = self.fig.add_subplot(self.gs[row:row+rowspan, col:col+colspan])
        
        # Store subplot info
        self.subplots[subplot_id] = {
            'ax': ax,
            'type': subplot_type,
            'row': row,
            'col': col,
            'rowspan': rowspan,
            'colspan': colspan,
            'data': {'x': np.array([1, 2, 3, 4]), 'y': np.array([10, 20, 30, 40])},
            'title': f"Subplot {len(self.subplots) + 1}",
            'xlabel': "X-axis",
            'ylabel': "Y-axis",
            'annotations': {},
            'style': {
                'line_color': 'blue',
                'line_style': '-',
                'marker_size': 10,
                'grid': False,
                'legend': False
            }
        }
        
        # Set active subplot
        self.active_subplot = subplot_id
        
        # Initialize the plot based on type
        self.update_subplot(subplot_id)
        
        return subplot_id
    
    def update_grid(self, rows, cols):
        """Update the gridspec layout"""
        self.grid_rows = rows
        self.grid_cols = cols
        
        # Store current subplot data
        saved_subplots = {}
        for subplot_id, info in self.subplots.items():
            saved_subplots[subplot_id] = {
                'type': info['type'],
                'data': info['data'],
                'title': info['title'],
                'xlabel': info['xlabel'],
                'ylabel': info['ylabel'],
                'annotations': info['annotations'],
                'style': info['style']
            }
        
        # Clear figure and reset GridSpec
        self.fig.clear()
        self.gs = gridspec.GridSpec(rows, cols, figure=self.fig)
        
        # Recreate subplots - for now, just place them in order
        # In a more advanced version, this would preserve positions if possible
        self.subplots = {}
        row, col = 0, 0
        
        for subplot_id, info in saved_subplots.items():
            new_id = subplot_id  # Preserve original ID
            ax = self.fig.add_subplot(self.gs[row, col])
            
            self.subplots[new_id] = {
                'ax': ax,
                'type': info['type'],
                'row': row,
                'col': col,
                'rowspan': 1,
                'colspan': 1,
                'data': info['data'],
                'title': info['title'],
                'xlabel': info['xlabel'],
                'ylabel': info['ylabel'],
                'annotations': info['annotations'],
                'style': info['style']
            }
            
            # Move to next cell
            col += 1
            if col >= cols:
                col = 0
                row += 1
                if row >= rows:
                    break  # No more space for subplots
            
            # Update the plot
            self.update_subplot(new_id)
        
        self.fig.tight_layout()
        return True
    
    def remove_subplot(self, subplot_id):
        """Remove a subplot by ID"""
        if subplot_id in self.subplots:
            # Remove from figure
            self.fig.delaxes(self.subplots[subplot_id]['ax'])
            # Remove from our tracking
            del self.subplots[subplot_id]
            # Reset active subplot if needed
            if self.active_subplot == subplot_id:
                self.active_subplot = next(iter(self.subplots)) if self.subplots else None
            return True
        return False
    
    def get_subplot_at_position(self, x, y):
        """Find which subplot contains the given figure coordinates"""
        for subplot_id, info in self.subplots.items():
            ax = info['ax']
            if ax.contains_point((x, y)):
                return subplot_id
        return None
    
    def update_subplot(self, subplot_id):
        """Update a subplot with current data and settings"""
        if subplot_id not in self.subplots:
            return False
        
        info = self.subplots[subplot_id]
        ax = info['ax']
        data = info['data']
        style = info['style']
        
        # Clear axis but keep it in the figure
        ax.clear()
        
        # Set labels
        ax.set_title(info['title'])
        ax.set_xlabel(info['xlabel'])
        ax.set_ylabel(info['ylabel'])
        
        # Apply grid setting
        ax.grid(style['grid'])
        
        # Plot data based on subplot type
        if info['type'] == 'line':
            ax.plot(data['x'], data['y'], 
                   color=style['line_color'], 
                   linestyle=style['line_style'], 
                   marker='o', 
                   markersize=style['marker_size']/2)
        
        elif info['type'] == 'scatter':
            ax.scatter(data['x'], data['y'], 
                      s=style['marker_size'], 
                      c=style['line_color'])
        
        elif info['type'] == 'bar':
            ax.bar(data['x'], data['y'], 
                  color=style['line_color'])
        
        elif info['type'] == 'histogram':
            ax.hist(data['y'], bins=10, 
                   color=style['line_color'])
        
        elif info['type'] == 'pie':
            # Pie chart needs positive values
            positive_values = np.maximum(data['y'], 0.1)
            ax.pie(positive_values, labels=[f"{x}" for x in data['x']])
        
        elif info['type'] == 'area':
            ax.fill_between(data['x'], data['y'], 
                           color=style['line_color'], 
                           alpha=0.5)
        
        # Restore annotations
        for idx, ann_info in info['annotations'].items():
            ann = ax.annotate(
                ann_info['text'],
                xy=ann_info['xy'],
                xytext=ann_info['xytext'],
                textcoords="offset points",
                fontsize=9,
                color='black',
                bbox=dict(boxstyle="round", fc="yellow", alpha=0.7),
                arrowprops=dict(arrowstyle="->")
            )
        
        # Highlight active subplot
        if subplot_id == self.active_subplot:
            for spine in ax.spines.values():
                spine.set_linewidth(2)
                spine.set_color('red')
        else:
            for spine in ax.spines.values():
                spine.set_linewidth(1)
                spine.set_color('black')
        
        return True
    
    def update_data(self, subplot_id, new_data, append=False):
        """Update subplot data, with option to append or replace"""
        if subplot_id not in self.subplots:
            return False
        
        info = self.subplots[subplot_id]
        
        if append and 'x' in new_data and 'y' in new_data:
            # Append data
            info['data']['x'] = np.append(info['data']['x'], new_data['x'])
            info['data']['y'] = np.append(info['data']['y'], new_data['y'])
        else:
            # Replace data
            info['data'] = new_data
        
        # Update the plot
        self.update_subplot(subplot_id)
        return True
    
    def resize_subplot(self, subplot_id, row, col, rowspan, colspan):
        """Resize and reposition a subplot"""
        if subplot_id not in self.subplots:
            return False
        
        # Get current info
        info = self.subplots[subplot_id]
        
        # Check if new position is valid
        if (row + rowspan > self.grid_rows) or (col + colspan > self.grid_cols):
            return False
        
        # Check for overlap with other subplots
        for sid, sinfo in self.subplots.items():
            if sid == subplot_id:
                continue
            
            # Check for overlap
            if (sinfo['row'] < row + rowspan and sinfo['row'] + sinfo['rowspan'] > row and
                sinfo['col'] < col + colspan and sinfo['col'] + sinfo['colspan'] > col):
                return False
        
        # Update position
        info['row'] = row
        info['col'] = col
        info['rowspan'] = rowspan
        info['colspan'] = colspan
        
        # Remove old axis
        self.fig.delaxes(info['ax'])
        
        # Create new axis with updated position
        info['ax'] = self.fig.add_subplot(self.gs[row:row+rowspan, col:col+colspan])
        
        # Update plot
        self.update_subplot(subplot_id)
        return True
    
    def change_subplot_type(self, subplot_id, new_type):
        """Change the type of a subplot"""
        if subplot_id in self.subplots:
            self.subplots[subplot_id]['type'] = new_type
            self.update_subplot(subplot_id)
            return True
        return False


class DataProcessor:
    """Class to handle data import and processing"""
    
    @staticmethod
    def load_data_from_file(file_path):
        """Load data from various file formats"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext == '.xlsx' or file_ext == '.xls':
                df = pd.read_excel(file_path)
            elif file_ext == '.txt' or file_ext == '.dat':
                # Try different delimiters
                try:
                    df = pd.read_csv(file_path, sep='\t')
                except:
                    try:
                        df = pd.read_csv(file_path, sep=',')
                    except:
                        df = pd.read_csv(file_path, sep=' ', skipinitialspace=True)
            elif file_ext == '.json':
                df = pd.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            # Try to determine x and y columns
            if len(df.columns) >= 2:
                x_col = df.columns[0]
                y_col = df.columns[1]
            else:
                # If only one column, use index as x
                x_col = None
                y_col = df.columns[0]
            
            # Extract data as numpy arrays
            if x_col:
                x_data = df[x_col].to_numpy()
            else:
                x_data = df.index.to_numpy()
            
            y_data = df[y_col].to_numpy()
            
            return {'x': x_data, 'y': y_data, 'df': df, 'columns': df.columns.tolist()}
        
        except Exception as e:
            print(f"Error loading data: {e}")
            return None


class SubplotTypeSelector(tk.Toplevel):
    """Dialog for selecting subplot type"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add New Subplot")
        self.geometry("350x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        self.selected_type = tk.StringVar(value="line")
        
        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create type options with images
        ttk.Label(main_frame, text="Select Plot Type:").pack(anchor=tk.W, pady=(0, 10))
        
        # Grid for plot type buttons
        type_frame = ttk.Frame(main_frame)
        type_frame.pack(fill=tk.BOTH, expand=True)
        
        # Plot type options (simulated with text for now)
        plot_types = [
            ("Line", "line"), 
            ("Scatter", "scatter"), 
            ("Bar", "bar"),
            ("Histogram", "histogram"), 
            ("Pie", "pie"), 
            ("Area", "area")
        ]
        
        # Create a 3x2 grid of plot type options
        for i, (label, value) in enumerate(plot_types):
            row = i // 2
            col = i % 2
            
            # Frame for each option
            opt_frame = ttk.Frame(type_frame, borderwidth=2, relief="groove", padding=5)
            opt_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Radio button
            radio = ttk.Radiobutton(opt_frame, text=label, value=value, variable=self.selected_type)
            radio.pack(anchor=tk.W)
            
            # Here you'd add an image representing the plot type
            # For now we'll use a label as placeholder
            img_label = ttk.Label(opt_frame, text=f"[{label} preview]", width=15, anchor=tk.CENTER)
            img_label.pack(pady=10)
        
        # Configure grid
        for i in range(2):
            type_frame.columnconfigure(i, weight=1)
        for i in range(3):
            type_frame.rowconfigure(i, weight=1)
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
    
    def ok(self):
        self.result = self.selected_type.get()
        self.destroy()
    
    def cancel(self):
        self.result = None
        self.destroy()
    
    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.result


class SubplotPositionDialog(tk.Toplevel):
    """Dialog for editing subplot position and size"""
    def __init__(self, parent, current_row=0, current_col=0, current_rowspan=1, current_colspan=1, max_rows=2, max_cols=2):
        super().__init__(parent)
        self.title("Edit Subplot Position")
        self.geometry("300x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        self.max_rows = max_rows
        self.max_cols = max_cols
        
        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Position controls
        pos_frame = ttk.LabelFrame(main_frame, text="Position")
        pos_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Row position
        row_frame = ttk.Frame(pos_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="Row:").pack(side=tk.LEFT)
        self.row_var = tk.IntVar(value=current_row)
        row_spin = ttk.Spinbox(row_frame, from_=0, to=max_rows-1, textvariable=self.row_var, width=5)
        row_spin.pack(side=tk.LEFT, padx=5)
        
        # Column position
        col_frame = ttk.Frame(pos_frame)
        col_frame.pack(fill=tk.X, pady=5)
        ttk.Label(col_frame, text="Column:").pack(side=tk.LEFT)
        self.col_var = tk.IntVar(value=current_col)
        col_spin = ttk.Spinbox(col_frame, from_=0, to=max_cols-1, textvariable=self.col_var, width=5)
        col_spin.pack(side=tk.LEFT, padx=5)
        
        # Size controls
        size_frame = ttk.LabelFrame(main_frame, text="Size")
        size_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Row span
        rowspan_frame = ttk.Frame(size_frame)
        rowspan_frame.pack(fill=tk.X, pady=5)
        ttk.Label(rowspan_frame, text="Row Span:").pack(side=tk.LEFT)
        self.rowspan_var = tk.IntVar(value=current_rowspan)
        rowspan_spin = ttk.Spinbox(rowspan_frame, from_=1, to=max_rows, textvariable=self.rowspan_var, width=5)
        rowspan_spin.pack(side=tk.LEFT, padx=5)
        
        # Column span
        colspan_frame = ttk.Frame(size_frame)
        colspan_frame.pack(fill=tk.X, pady=5)
        ttk.Label(colspan_frame, text="Column Span:").pack(side=tk.LEFT)
        self.colspan_var = tk.IntVar(value=current_colspan)
        colspan_spin = ttk.Spinbox(colspan_frame, from_=1, to=max_cols, textvariable=self.colspan_var, width=5)
        colspan_spin.pack(side=tk.LEFT, padx=5)
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
        
        # Validate inputs when they change
        self.row_var.trace_add("write", self.validate)
        self.col_var.trace_add("write", self.validate)
        self.rowspan_var.trace_add("write", self.validate)
        self.colspan_var.trace_add("write", self.validate)
    
    def validate(self, *args):
        """Validate that the position and size are within bounds"""
        try:
            row = self.row_var.get()
            col = self.col_var.get()
            rowspan = self.rowspan_var.get()
            colspan = self.colspan_var.get()
            
            # Check bounds
            if row + rowspan > self.max_rows:
                self.rowspan_var.set(self.max_rows - row)
            
            if col + colspan > self.max_cols:
                self.colspan_var.set(self.max_cols - col)
        except:
            pass  # Ignore validation errors during editing
    
    def ok(self):
        self.result = {
            'row': self.row_var.get(),
            'col': self.col_var.get(),
            'rowspan': self.rowspan_var.get(),
            'colspan': self.colspan_var.get()
        }
        self.destroy()
    
    def cancel(self):
        self.result = None
        self.destroy()
    
    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.result


class DataColumnSelector(tk.Toplevel):
    """Dialog for selecting which columns to use for x and y data"""
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.title("Select Data Columns")
        self.geometry("300x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.result = None
        self.columns = columns
        
        # Main frame
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # X column selection
        x_frame = ttk.Frame(main_frame)
        x_frame.pack(fill=tk.X, pady=5)
        ttk.Label(x_frame, text="X Column:").pack(side=tk.LEFT)
        self.x_var = tk.StringVar()
        x_combo = ttk.Combobox(x_frame, textvariable=self.x_var, values=['index'] + columns, state="readonly")
        x_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        if columns:
            self.x_var.set('index' if len(columns) == 1 else columns[0])
        
        # Y column selection
        y_frame = ttk.Frame(main_frame)
        y_frame.pack(fill=tk.X, pady=5)
        ttk.Label(y_frame, text="Y Column:").pack(side=tk.LEFT)
        self.y_var = tk.StringVar()
        y_combo = ttk.Combobox(y_frame, textvariable=self.y_var, values=columns, state="readonly")
        y_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        if columns:
            self.y_var.set(columns[0])
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
    
    def ok(self):
        self.result = {
            'x_col': self.x_var.get(),
            'y_col': self.y_var.get()
        }
        self.destroy()
    
    def cancel(self):
        self.result = None
        self.destroy()
    
    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.result


class InteractivePlot(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack(fill=tk.BOTH, expand=True)
        
        # Main notebook for multiple tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create main plot tab
        self.create_plot_tab()
        
        # Set up drag and drop
        self.setup_drag_drop()
        
        # Initialize tooltips
        self.tooltip = None
        
        # Variables for tracking subplot resizing
        self.resize_mode = False
        self.resize_subplot = None
        self.resize_start_pos = None
        
        # State tracking
        self.dragging_point = None
        self.prev_x, self.prev_y = None, None
        
        # Create KDTree for point proximity detection
        self.points = np.array([(1, 10), (2, 20), (3, 25), (4, 30)])
        self.update_kdtree()
    
    def setup_drag_drop(self):
        """Set up drag and drop functionality
        self.root.drop_target_register('*')
        self.root.dnd_bind('<<Drop>>', self.on_drop)
        """
        pass
    
    def on_drop(self, event):
        """Handle file drop events"""
        try:
            # Get the dropped data
            data = event.data
            
            # Check if it's a file path
            if os.path.isfile(data):
                # Process the dropped file
                self.process_dropped_file(data, event)
        except Exception as e:
            messagebox.showerror("Drop Error", f"Error processing dropped file: {str(e)}")
    
    def process_dropped_file(self, file_path, event):
        """Process a dropped data file"""
        # Try to load the data
        data = DataProcessor.load_data_from_file(file_path)
        
        if data:
            # Find which subplot was dropped on
            # Convert from screen coordinates to figure coordinates
            x = event.x_root - self.figure_canvas.winfo_rootx()
            y = event.y_root - self.figure_canvas.winfo_rooty()
            
            # Convert to figure coordinates
            inv = self.figure.transFigure.inverted()
            fig_coords = inv.transform((x, y))
            
            # Find the subplot at this position
            subplot_id = self.subplot_manager.get_subplot_at_position(*fig_coords)
            
            if subplot_id:
                # Ask if we should append or overwrite data
                response = messagebox.askyesnocancel(
                    "Data Import",
                    f"Do you want to append this data to the existing subplot?\n\nYes: Append\nNo: Overwrite\nCancel: Abort",
                    icon=messagebox.QUESTION
                )
                
                if response is not None:  # Not cancelled
                    # Select which columns to use if the data has multiple columns
                    if len(data['df'].columns) > 1:
                        column_selector = DataColumnSelector(self.root, data['columns'])
                        column_result = column_selector.show()
                        
                        if column_result:
                            # Extract selected columns
                            x_col = column_result['x_col']
                            y_col = column_result['y_col']
                            
                            if x_col == 'index':
                                x_data = data['df'].index.to_numpy()
                            else:
                                x_data = data['df'][x_col].to_numpy()
                            
                            y_data = data['df'][y_col].to_numpy()
                            
                            # Update subplot with selected data
                            self.subplot_manager.update_data(
                                subplot_id, 
                                {'x': x_data, 'y': y_data}, 
                                append=response  # True for append, False for overwrite
                            )
                            self.figure_canvas.draw_idle()
                    else:
                        # Use data as is
                        self.subplot_manager.update_data(
                            subplot_id, 
                            {'x': data['x'], 'y': data['y']}, 
                            append=response  # True for append, False for overwrite
                        )
                        self.figure_canvas.draw_idle()
            else:
                messagebox.showinfo("Drop Location", "Please drop on a specific subplot")
        else:
            messagebox.showerror("Data Error", "Could not load data from the dropped file")
    
    def update_kdtree(self):
        """Update the KDTree with current points"""
        if len(self.points) > 0:
            self.kdtree = KDTree(self.points)
        else:
            self.kdtree = None
    
    def create_plot_tab(self):
        """Create the main interactive plot tab with subplots"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="   Interactive Plot   ")
        
        # Create a matplotlib figure for interactive plotting
        self.figure = Figure(figsize=(8, 6), dpi=100)
        
        # Initialize subplot manager
        self.subplot_manager = SubplotManager(self.figure, self)
        
        # Add initial subplot
        self.subplot_manager.add_subplot()
        
        # Embed the figure in the GUI
        self.figure_canvas = FigureCanvasTkAgg(self.figure, tab)
        self.canvas_widget = self.figure_canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Create navigation toolbar

        toolbar_frame = ttk.Frame(tab)
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, toolbar_frame)

        self.toolbar.update()
        
        # Controls Frame
        controls_frame = ttk.Frame(tab, relief=tk.RIDGE, borderwidth=2)
        controls_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        # Grid for subplots
        grid_frame = ttk.LabelFrame(controls_frame, text="Grid")
        grid_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        grid_inner = ttk.Frame(grid_frame)
        grid_inner.pack(padx=5, pady=5)
        
        ttk.Label(grid_inner, text="Rows:").grid(row=0, column=0, padx=2)
        self.rows_var = tk.IntVar(value=2)
        rows_spin = ttk.Spinbox(grid_inner, from_=1, to=4, width=3, textvariable=self.rows_var)
        rows_spin.grid(row=0, column=1, padx=2)
        
        ttk.Label(grid_inner, text="Cols:").grid(row=0, column=2, padx=2)
        self.cols_var = tk.IntVar(value=2)
        cols_spin = ttk.Spinbox(grid_inner, from_=1, to=4, width=3, textvariable=self.cols_var)
        cols_spin.grid(row=0, column=3, padx=2)
        
        ttk.Button(grid_inner, text="Update Grid", command=self.update_grid).grid(row=0, column=4, padx=5)
        
        # Subplot controls frame
        subplot_frame = ttk.LabelFrame(controls_frame, text="Subplot")
        subplot_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        subplot_inner = ttk.Frame(subplot_frame)
        subplot_inner.pack(padx=5, pady=5)
        
        ttk.Button(subplot_inner, text="Add", command=self.add_subplot).grid(row=0, column=0, padx=2)
        ttk.Button(subplot_inner, text="Remove", command=self.remove_subplot).grid(row=0, column=1, padx=2)
        ttk.Button(subplot_inner, text="Position", command=self.edit_subplot_position).grid(row=0, column=2, padx=2)
        ttk.Button(subplot_inner, text="Type", command=self.change_subplot_type).grid(row=0, column=3, padx=2)
        
        # Style controls frame
        style_frame = ttk.LabelFrame(controls_frame, text="Style")
        style_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        style_inner = ttk.Frame(style_frame)
        style_inner.pack(padx=5, pady=5)
        
        ttk.Button(style_inner, text="Color", command=self.set_color).grid(row=0, column=0, padx=2)
        ttk.Button(style_inner, text="Grid", command=self.toggle_grid).grid(row=0, column=1, padx=2)
        
        # Data frame
        data_frame = ttk.LabelFrame(controls_frame, text="Data")
        data_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        data_inner = ttk.Frame(data_frame)
        data_inner.pack(padx=5, pady=5)
        
        ttk.Button(data_inner, text="Import", command=self.import_data).grid(row=0, column=0, padx=2)
        ttk.Button(data_inner, text="Edit", command=self.edit_data).grid(row=0, column=1, padx=2)
        
        # File operations frame
        file_frame = ttk.LabelFrame(controls_frame, text="File")
        file_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        file_inner = ttk.Frame(file_frame)
        file_inner.pack(padx=5, pady=5)
        
        ttk.Button(file_inner, text="Save", command=self.save_figure).grid(row=0, column=0, padx=2)
        ttk.Button(file_inner, text="Export", command=self.export_data).grid(row=0, column=1, padx=2)
        
        # Annotation frame
        annotation_frame = ttk.LabelFrame(controls_frame, text="Annotate")
        annotation_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        annotation_inner = ttk.Frame(annotation_frame)
        annotation_inner.pack(padx=5, pady=5)
        
        ttk.Button(annotation_inner, text="Add", command=self.add_annotation).grid(row=0, column=0, padx=2)
        ttk.Button(annotation_inner, text="Edit", command=self.edit_annotation).grid(row=0, column=1, padx=2)
        
        # Setup event handlers
        self.figure_canvas.mpl_connect('button_press_event', self.on_click)
        self.figure_canvas.mpl_connect('button_release_event', self.on_release)
        self.figure_canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.figure_canvas.mpl_connect('scroll_event', self.on_scroll)
    
    def update_grid(self):
        """Update the grid layout based on user input"""
        rows = self.rows_var.get()
        cols = self.cols_var.get()
        
        # Update the subplot manager's grid
        if self.subplot_manager.update_grid(rows, cols):
            # Redraw the figure
            self.figure.tight_layout()
            self.figure_canvas.draw_idle()
        else:
            messagebox.showerror("Grid Update Error", "Could not update grid to specified dimensions")
    
    def add_subplot(self):
        """Add a new subplot via dialog"""
        # Show type selector dialog
        type_selector = SubplotTypeSelector(self.root)
        subplot_type = type_selector.show()
        
        if subplot_type:
            # Get available grid position
            row, col = 0, 0
            found = False
            
            for r in range(self.subplot_manager.grid_rows):
                for c in range(self.subplot_manager.grid_cols):
                    # Check if this position is already occupied
                    occupied = False
                    for _, info in self.subplot_manager.subplots.items():
                        if (info['row'] <= r < info['row'] + info['rowspan'] and 
                            info['col'] <= c < info['col'] + info['colspan']):
                            occupied = True
                            break
                    
                    if not occupied:
                        row, col = r, c
                        found = True
                        break
                
                if found:
                    break
            
            if found:
                # Add the subplot
                subplot_id = self.subplot_manager.add_subplot(subplot_type, row, col)
                
                # Update the figure
                self.figure.tight_layout()
                self.figure_canvas.draw_idle()
            else:
                messagebox.showinfo("Grid Full", "No space available in current grid. Please adjust grid size.")
    
    def remove_subplot(self):
        """Remove the active subplot"""
        if self.subplot_manager.active_subplot:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this subplot?"):
                # Remove the subplot
                self.subplot_manager.remove_subplot(self.subplot_manager.active_subplot)
                
                # Update the figure
                self.figure.tight_layout()
                self.figure_canvas.draw_idle()
        else:
            messagebox.showinfo("No Selection", "Please select a subplot first")
    
    def edit_subplot_position(self):
        """Edit the position and size of the active subplot"""
        if self.subplot_manager.active_subplot:
            info = self.subplot_manager.subplots[self.subplot_manager.active_subplot]
            
            # Show position dialog
            position_dialog = SubplotPositionDialog(
                self.root,
                current_row=info['row'],
                current_col=info['col'],
                current_rowspan=info['rowspan'],
                current_colspan=info['colspan'],
                max_rows=self.subplot_manager.grid_rows,
                max_cols=self.subplot_manager.grid_cols
            )
            
            result = position_dialog.show()
            
            if result:
                # Update the subplot position
                if self.subplot_manager.resize_subplot(
                    self.subplot_manager.active_subplot,
                    result['row'], result['col'],
                    result['rowspan'], result['colspan']
                ):
                    # Update the figure
                    self.figure.tight_layout()
                    self.figure_canvas.draw_idle()
                else:
                    messagebox.showerror("Position Error", "Could not position subplot as requested. Check for overlap.")
        else:
            messagebox.showinfo("No Selection", "Please select a subplot first")
    
    def change_subplot_type(self):
        """Change the type of the active subplot"""
        if self.subplot_manager.active_subplot:
            # Show type selector dialog
            type_selector = SubplotTypeSelector(self.root)
            subplot_type = type_selector.show()
            
            if subplot_type:
                # Change the subplot type
                self.subplot_manager.change_subplot_type(self.subplot_manager.active_subplot, subplot_type)
                
                # Update the figure
                self.figure_canvas.draw_idle()
        else:
            messagebox.showinfo("No Selection", "Please select a subplot first")
    
    def set_color(self):
        """Set the color for the active subplot"""
        if self.subplot_manager.active_subplot:
            info = self.subplot_manager.subplots[self.subplot_manager.active_subplot]
            current_color = info['style']['line_color']
            
            # Show color picker
            color = colorchooser.askcolor(initial=current_color)
            
            if color[1]:  # If a color was selected
                # Update the subplot style
                info['style']['line_color'] = color[1]
                self.subplot_manager.update_subplot(self.subplot_manager.active_subplot)
                
                # Update the figure
                self.figure_canvas.draw_idle()
        else:
            messagebox.showinfo("No Selection", "Please select a subplot first")
    
    def toggle_grid(self):
        """Toggle grid visibility for the active subplot"""
        if self.subplot_manager.active_subplot:
            info = self.subplot_manager.subplots[self.subplot_manager.active_subplot]
            
            # Toggle grid state
            info['style']['grid'] = not info['style']['grid']
            self.subplot_manager.update_subplot(self.subplot_manager.active_subplot)
            
            # Update the figure
            self.figure_canvas.draw_idle()
        else:
            messagebox.showinfo("No Selection", "Please select a subplot first")
    
    def import_data(self):
        """Import data from a file"""
        if self.subplot_manager.active_subplot:
            # Show file dialog
            file_path = filedialog.askopenfilename(
                title="Select Data File",
                filetypes=(
                    ("CSV files", "*.csv"),
                    ("Excel files", "*.xlsx *.xls"),
                    ("Text files", "*.txt *.dat"),
                    ("JSON files", "*.json"),
                    ("All files", "*.*")
                )
            )
            
            if file_path:
                # Load the data
                data = DataProcessor.load_data_from_file(file_path)
                
                if data:
                    # Ask if we should append or overwrite data
                    response = messagebox.askyesnocancel(
                        "Data Import",
                        "Do you want to append this data to the existing subplot?\n\nYes: Append\nNo: Overwrite\nCancel: Abort",
                        icon=messagebox.QUESTION
                    )
                    
                    if response is not None:  # Not cancelled
                        # Select which columns to use if the data has multiple columns
                        if len(data['df'].columns) > 1:
                            column_selector = DataColumnSelector(self.root, data['columns'])
                            column_result = column_selector.show()
                            
                            if column_result:
                                # Extract selected columns
                                x_col = column_result['x_col']
                                y_col = column_result['y_col']
                                
                                if x_col == 'index':
                                    x_data = data['df'].index.to_numpy()
                                else:
                                    x_data = data['df'][x_col].to_numpy()
                                
                                y_data = data['df'][y_col].to_numpy()
                                
                                # Update subplot with selected data
                                self.subplot_manager.update_data(
                                    self.subplot_manager.active_subplot, 
                                    {'x': x_data, 'y': y_data}, 
                                    append=response  # True for append, False for overwrite
                                )
                                self.figure_canvas.draw_idle()
                        else:
                            # Use data as is
                            self.subplot_manager.update_data(
                                self.subplot_manager.active_subplot, 
                                {'x': data['x'], 'y': data['y']}, 
                                append=response  # True for append, False for overwrite
                            )
                            self.figure_canvas.draw_idle()
                else:
                    messagebox.showerror("Data Error", "Could not load data from the selected file")
        else:
            messagebox.showinfo("No Selection", "Please select a subplot first")
    
    def edit_data(self):
        """Open a dialog to manually edit data points"""
        if self.subplot_manager.active_subplot:
            info = self.subplot_manager.subplots[self.subplot_manager.active_subplot]
            data = info['data']
            
            # TODO: Implement a data editor dialog here
            messagebox.showinfo("Not Implemented", "Data editing dialog not yet implemented.")
        else:
            messagebox.showinfo("No Selection", "Please select a subplot first")
    
    def save_figure(self):
        """Save the figure to a file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Figure",
            defaultextension=".png",
            filetypes=(
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PDF files", "*.pdf"),
                ("SVG files", "*.svg"),
                ("All files", "*.*")
            )
        )
        
        if file_path:
            try:
                self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Save Success", f"Figure saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving figure: {str(e)}")
    
    def export_data(self):
        """Export data from subplots to a file"""
        if not self.subplot_manager.subplots:
            messagebox.showinfo("No Data", "No subplots to export data from")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Data",
            defaultextension=".csv",
            filetypes=(
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            )
        )
        
        if file_path:
            try:
                # Create a dictionary to hold data from all subplots
                export_data = {}
                
                for subplot_id, info in self.subplot_manager.subplots.items():
                    title = info['title'].replace(" ", "_")
                    export_data[f"{title}_x"] = info['data']['x']
                    export_data[f"{title}_y"] = info['data']['y']
                
                # Convert to DataFrame
                df = pd.DataFrame(export_data)
                
                # Export based on file extension
                file_ext = os.path.splitext(file_path)[1].lower()
                
                if file_ext == '.csv':
                    df.to_csv(file_path, index=False)
                elif file_ext == '.xlsx':
                    df.to_excel(file_path, index=False)
                elif file_ext == '.json':
                    df.to_json(file_path, orient='records')
                else:
                    df.to_csv(file_path, index=False)
                
                messagebox.showinfo("Export Success", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")
    
    def add_annotation(self):
        """Add an annotation to the active subplot"""
        if self.subplot_manager.active_subplot:
            # Get text for annotation
            text = simpledialog.askstring("Annotation", "Enter annotation text:")
            
            if text:
                info = self.subplot_manager.subplots[self.subplot_manager.active_subplot]
                ax = info['ax']
                
                # Add annotation at center of visible axes
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                x = (xlim[0] + xlim[1]) / 2
                y = (ylim[0] + ylim[1]) / 2
                
                # Generate annotation ID
                ann_id = len(info['annotations']) + 1
                
                # Store annotation info
                info['annotations'][ann_id] = {
                    'text': text,
                    'xy': (x, y),
                    'xytext': (30, 30)  # Offset from point
                }
                
                # Update the subplot
                self.subplot_manager.update_subplot(self.subplot_manager.active_subplot)
                self.figure_canvas.draw_idle()
                
                # Enter annotation move mode
                messagebox.showinfo("Annotation", "Click and drag to position the annotation")
        else:
            messagebox.showinfo("No Selection", "Please select a subplot first")
    
    def edit_annotation(self):
        """Edit annotations on the active subplot"""
        if self.subplot_manager.active_subplot:
            info = self.subplot_manager.subplots[self.subplot_manager.active_subplot]
            
            if not info['annotations']:
                messagebox.showinfo("No Annotations", "This subplot has no annotations to edit")
                return
            
            # TODO: Implement annotation editor dialog
            messagebox.showinfo("Not Implemented", "Annotation editing dialog not yet implemented.")
        else:
            messagebox.showinfo("No Selection", "Please select a subplot first")
    
    def on_click(self, event):
        """Handle mouse click events"""
        if event.inaxes is None:
            return
        
        # Find which subplot was clicked
        for subplot_id, info in self.subplot_manager.subplots.items():
            if info['ax'] == event.inaxes:
                # Set as active subplot
                self.subplot_manager.active_subplot = subplot_id
                self.subplot_manager.update_subplot(subplot_id)
                self.figure_canvas.draw_idle()
                
                # Check if we're close to a data point for dragging
                if event.button == MouseButton.LEFT:
                    # Get data points in display space
                    x_data = info['data']['x']
                    y_data = info['data']['y']
                    
                    # Convert data coordinates to display coordinates
                    display_coords = np.array([event.inaxes.transData.transform((x, y)) 
                                            for x, y in zip(x_data, y_data)])
                    
                    # Find closest point
                    click_coords = np.array([event.x, event.y])
                    distances = np.sqrt(np.sum((display_coords - click_coords)**2, axis=1))
                    
                    if len(distances) > 0:
                        closest_idx = np.argmin(distances)
                        min_dist = distances[closest_idx]
                        
                        # If click is close enough to a point
                        if min_dist < 10:  # Threshold in pixels
                            self.dragging_point = {
                                'subplot_id': subplot_id,
                                'idx': closest_idx
                            }
                break
    
    def on_release(self, event):
        """Handle mouse release events"""
        self.dragging_point = None
        self.resize_mode = False
        self.resize_subplot = None
        self.resize_start_pos = None
    
    def on_motion(self, event):
        """Handle mouse motion events"""
        if event.inaxes is None:
            return
        
        # Handle data point dragging
        if self.dragging_point:
            subplot_id = self.dragging_point['subplot_id']
            idx = self.dragging_point['idx']
            
            if subplot_id in self.subplot_manager.subplots:
                info = self.subplot_manager.subplots[subplot_id]
                
                # Convert display coordinates to data coordinates
                data_coords = event.inaxes.transData.inverted().transform((event.x, event.y))
                
                # Update the data point
                info['data']['x'][idx] = data_coords[0]
                info['data']['y'][idx] = data_coords[1]
                
                # Redraw the subplot
                self.subplot_manager.update_subplot(subplot_id)
                self.figure_canvas.draw_idle()
    
    def on_scroll(self, event):
        """Handle mouse scroll events"""
        if event.inaxes is None:
            return
        
        # Find which subplot was scrolled
        for subplot_id, info in self.subplot_manager.subplots.items():
            if info['ax'] == event.inaxes:
                # Adjust marker size on scroll
                if event.button == 'up':
                    info['style']['marker_size'] = min(info['style']['marker_size'] + 1, 20)
                else:
                    info['style']['marker_size'] = max(info['style']['marker_size'] - 1, 1)
                
                # Update the subplot
                self.subplot_manager.update_subplot(subplot_id)
                self.figure_canvas.draw_idle()
                break


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interactive Plot Builder")
        self.geometry("1024x768")
        
        # Create menu bar
        self.create_menu()
        
        # Create main interactive plot
        self.plot = InteractivePlot(self)
    
    def create_menu(self):
        """Create the application menu bar"""
        menu_bar = Menu(self)
        
        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_project)
        file_menu.add_command(label="Open", command=self.open_project)
        file_menu.add_command(label="Save", command=self.save_project)
        file_menu.add_command(label="Save As", command=self.save_project_as)
        file_menu.add_separator()
        file_menu.add_command(label="Export Figure", command=self.export_figure)
        file_menu.add_command(label="Export Data", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Grid Settings", command=self.edit_grid)
        edit_menu.add_command(label="Figure Settings", command=self.edit_figure)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        # Data menu
        data_menu = Menu(menu_bar, tearoff=0)
        data_menu.add_command(label="Import Data", command=self.import_data)
        data_menu.add_command(label="Generate Test Data", command=self.generate_test_data)
        menu_bar.add_cascade(label="Data", menu=data_menu)
        
        # Help menu
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menu_bar)
    
    def new_project(self):
        """Create a new project"""
        if messagebox.askyesno("New Project", "Create a new project? Any unsaved changes will be lost."):
            # Reset the plot
            self.plot.destroy()
            self.plot = InteractivePlot(self)
    
    def open_project(self):
        """Open a saved project file"""
        file_path = filedialog.askopenfilename(
            title="Open Project",
            filetypes=(("Plot Builder Project", "*.pbp"), ("All files", "*.*"))
        )
        
        if file_path:
            try:
                # Implementation would load project data
                messagebox.showinfo("Not Implemented", "Project loading not yet implemented")
            except Exception as e:
                messagebox.showerror("Open Error", f"Error opening project: {str(e)}")
    
    def save_project(self):
        """Save the current project"""
        # Implementation would save project data
        messagebox.showinfo("Not Implemented", "Project saving not yet implemented")
    
    def save_project_as(self):
        """Save the current project with a new name"""
        file_path = filedialog.asksaveasfilename(
            title="Save Project As",
            defaultextension=".pbp",
            filetypes=(("Plot Builder Project", "*.pbp"), ("All files", "*.*"))
        )
        
        if file_path:
            try:
                # Implementation would save project data
                messagebox.showinfo("Not Implemented", "Project saving not yet implemented")
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving project: {str(e)}")
    
    def export_figure(self):
        """Export the current figure"""
        self.plot.save_figure()
    
    def export_data(self):
        """Export data from the current plot"""
        self.plot.export_data()
    
    def edit_grid(self):
        """Edit grid settings"""
        # Implementation would show a grid settings dialog
        messagebox.showinfo("Not Implemented", "Grid settings dialog not yet implemented")
    
    def edit_figure(self):
        """Edit figure settings"""
        # Implementation would show a figure settings dialog
        messagebox.showinfo("Not Implemented", "Figure settings dialog not yet implemented")
    
    def import_data(self):
        """Import data into the current plot"""
        self.plot.import_data()
    
    def generate_test_data(self):
        """Generate test data for the current plot"""
        # Implementation would generate test data
        messagebox.showinfo("Not Implemented", "Test data generation not yet implemented")
    
    def show_documentation(self):
        """Show application documentation"""
        # Implementation would show documentation
        messagebox.showinfo("Documentation", "Documentation not yet available")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", "Interactive Plot Builder\nVersion 1.0\n\nA powerful tool for creating and editing interactive plots.")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()