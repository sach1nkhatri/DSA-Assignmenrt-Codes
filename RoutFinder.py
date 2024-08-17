import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from operator import itemgetter

class RouteOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Delivery Route Optimizer")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        # Initialize data
        self.delivery_points = []
        self.graph = nx.Graph()

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Frame for input options
        input_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, borderwidth=2, relief="groove")
        input_frame.pack(fill="x")

        # Import Delivery Points Button
        self.import_button = tk.Button(input_frame, text="Import Delivery Points", command=self.import_points,
                                       bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), relief="raised")
        self.import_button.pack(pady=10, side="top", fill="x")

        # Manual Entry Button
        self.manual_button = tk.Button(input_frame, text="Enter Delivery Points", command=self.manual_entry,
                                       bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), relief="raised")
        self.manual_button.pack(pady=10, side="top", fill="x")

        # Algorithm Selection
        tk.Label(input_frame, text="Select Algorithm:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5, side="top")
        self.algorithm_var = tk.StringVar(value="dijkstra")
        algorithms = ["dijkstra", "tsp"]
        for algo in algorithms:
            tk.Radiobutton(input_frame, text=algo.capitalize(), variable=self.algorithm_var, value=algo,
                           bg="#ffffff", font=("Helvetica", 12)).pack(pady=2, side="top")

        # Vehicle Capacity and Distance Constraints
        tk.Label(input_frame, text="Vehicle Capacity:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5, side="top")
        self.capacity_entry = tk.Entry(input_frame, font=("Helvetica", 12))
        self.capacity_entry.pack(pady=5, side="top")

        tk.Label(input_frame, text="Max Distance (km):", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5, side="top")
        self.distance_entry = tk.Entry(input_frame, font=("Helvetica", 12))
        self.distance_entry.pack(pady=5, side="top")

        # Optimize Button
        self.optimize_button = tk.Button(input_frame, text="Optimize Route", command=self.optimize_route,
                                         bg="#FF5722", fg="white", font=("Helvetica", 12, "bold"), relief="raised")
        self.optimize_button.pack(pady=20, side="top", fill="x")

        # Frame for Route Visualization
        self.canvas_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.canvas_frame.pack(fill="both", expand=True)

        # Result Display
        self.result_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, borderwidth=2, relief="groove")
        self.result_frame.pack(fill="x")

        self.result_label = tk.Label(self.result_frame, text="", bg="#ffffff", font=("Helvetica", 12))
        self.result_label.pack()

    def import_points(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                lines = file.readlines()
                self.delivery_points = [tuple(map(str.strip, line.split(','))) for line in lines]
                self.update_graph()

    def manual_entry(self):
        num_points = simpledialog.askinteger("Input", "How many delivery points?")
        if num_points:
            self.delivery_points = []
            for _ in range(num_points):
                address = simpledialog.askstring("Input", "Enter address:")
                priority = simpledialog.askinteger("Input", "Enter priority:")
                self.delivery_points.append((address, priority))
            self.update_graph()

    def update_graph(self):
        self.graph.clear()
        for i, (address, _) in enumerate(self.delivery_points):
            self.graph.add_node(i, label=address)

        # Sort delivery points based on priority (higher priority first)
        sorted_points = sorted(enumerate(self.delivery_points), key=lambda x: x[1][1], reverse=True)
        for i, (addr, _) in sorted_points:
            for j in range(i):
                # Adding edges with weights influenced by priorities
                self.graph.add_edge(i, j, weight=np.random.randint(1, 10) + self.delivery_points[i][1])

    def optimize_route(self):
        if not self.delivery_points:
            messagebox.showwarning("No Points", "Please import or enter delivery points.")
            return

        try:
            capacity = int(self.capacity_entry.get())
            max_distance = int(self.distance_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numerical values for constraints.")
            return

        algorithm = self.algorithm_var.get()
        route = []

        if algorithm == "dijkstra":
            # Find shortest path (Dijkstra)
            if len(self.delivery_points) > 1:
                source = 0
                target = len(self.delivery_points) - 1
                path = nx.dijkstra_path(self.graph, source, target, weight='weight')
                route = path
                total_distance = sum(self.graph[u][v]['weight'] for u, v in zip(path, path[1:]))
        elif algorithm == "tsp":
            # Find optimal route for TSP
            path = nx.approximation.traveling_salesman_problem(self.graph, cycle=True)
            route = path
            total_distance = sum(self.graph[u][v]['weight'] for u, v in zip(path, path[1:]))

        # Update result display
        route_str = " -> ".join(f"Node {node} (Priority: {self.delivery_points[node][1]})" for node in route)
        self.result_label.config(text=f"Optimized Route: {route_str}\nTotal Distance: {total_distance}")

        self.visualize_route(route)

    def visualize_route(self, route):
        # Clear previous widgets in the canvas frame
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # Create a new figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Draw the graph
        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(self.graph, pos, with_labels=True, node_size=800, node_color="#00BCD4", font_size=12,
                font_color="white", edge_color="#FFC107", width=2, ax=ax)
        nx.draw_networkx_edges(self.graph, pos, edgelist=[(route[i], route[i+1]) for i in range(len(route)-1)],
                               edge_color='red', width=3, ax=ax)
        
        # Remove axis
        ax.axis('off')

        # Embed Matplotlib figure into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = RouteOptimizerApp(root)
    root.mainloop()
