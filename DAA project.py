import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Graph class implementing Kruskal's MST algorithm
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def addEdge(self, u, v, w):
        if u >= self.V or v >= self.V or u < 0 or v < 0:
            raise ValueError(f"Vertices {u} and {v} are out of range for a graph with {self.V} vertices.")
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    def KruskalMST(self):
        result = []
        i = 0
        e = 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = [node for node in range(self.V)]
        rank = [0] * self.V
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)

        minimumCost = sum([weight for u, v, weight in result])
        return result, minimumCost

# GUI Application
class KruskalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kruskal's MST Algorithm")
        self.root.geometry("550x600")
        self.edge_list = []
        
        # Title
        title_label = tk.Label(root, text="Kruskal's MST Algorithm", font=("Helvetica", 18, "bold"), fg="#003366")
        title_label.pack(pady=10)

        # Frame for Vertices and Edges input
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10, padx=20, fill="x")

        # Number of Vertices
        tk.Label(input_frame, text="Number of Vertices:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.vertices_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=5)
        self.vertices_entry.grid(row=0, column=1, padx=5, pady=5)

        # Edge Input
        tk.Label(input_frame, text="Edge (u, v, weight):", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.u_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=5)
        self.u_entry.grid(row=1, column=1, padx=5, pady=5)
        self.v_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=5)
        self.v_entry.grid(row=1, column=2, padx=5, pady=5)
        self.w_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=5)
        self.w_entry.grid(row=1, column=3, padx=5, pady=5)

        # Buttons to add edge and clear edges
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        add_edge_button = tk.Button(button_frame, text="Add Edge", command=self.add_edge, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        add_edge_button.grid(row=0, column=0, padx=10)
        clear_edges_button = tk.Button(button_frame, text="Clear Edges", command=self.clear_edges, bg="#f44336", fg="white", font=("Helvetica", 12))
        clear_edges_button.grid(row=0, column=1, padx=10)

        # Edge List Display
        self.edge_list_display = tk.Text(root, height=8, width=40, font=("Helvetica", 12))
        self.edge_list_display.pack(pady=10)
        self.edge_list_display.insert(tk.END, "Edges:\n")
        self.edge_list_display.config(state="disabled")

        # Calculate MST Button
        calculate_mst_button = tk.Button(root, text="Calculate MST", command=self.calculate_mst, bg="#2196F3", fg="white", font=("Helvetica", 14))
        calculate_mst_button.pack(pady=15)

        # Result Display
        self.result_label = tk.Label(root, text="", font=("Helvetica", 12), fg="#003366")
        self.result_label.pack(pady=10)

    def add_edge(self):
        try:
            u = int(self.u_entry.get())
            v = int(self.v_entry.get())
            w = int(self.w_entry.get())
            vertices = int(self.vertices_entry.get()) if self.vertices_entry.get().isdigit() else 0
            if u >= vertices or v >= vertices or u < 0 or v < 0:
                messagebox.showerror("Invalid Edge", f"Vertices {u} and {v} are out of range for a graph with {vertices} vertices.")
                return
            self.edge_list.append((u, v, w))
            self.display_edges()
            self.u_entry.delete(0, tk.END)
            self.v_entry.delete(0, tk.END)
            self.w_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integer values for u, v, and weight.")

    def clear_edges(self):
        self.edge_list = []
        self.display_edges()

    def display_edges(self):
        self.edge_list_display.config(state="normal")
        self.edge_list_display.delete(1.0, tk.END)
        self.edge_list_display.insert(tk.END, "Edges:\n")
        for u, v, w in self.edge_list:
            self.edge_list_display.insert(tk.END, f"{u} -- {v} == {w}\n")
        self.edge_list_display.config(state="disabled")

    def calculate_mst(self):
        try:
            vertices = int(self.vertices_entry.get())
            self.graph = Graph(vertices)
            for u, v, w in self.edge_list:
                self.graph.addEdge(u, v, w)
            mst, minimumCost = self.graph.KruskalMST()

            result_text = "Edges in the MST:\n"
            for u, v, weight in mst:
                result_text += f"{u} -- {v} == {weight}\n"
            result_text += f"\nMinimum Cost of MST: {minimumCost}"
            self.result_label.config(text=result_text)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of vertices.")
        except IndexError:
            messagebox.showerror("MST Error", "Ensure the graph has enough edges to form a spanning tree.")

# Run the app
root = tk.Tk()
app = KruskalApp(root)
root.mainloop()
