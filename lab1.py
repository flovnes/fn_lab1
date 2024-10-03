import matplotlib.pyplot as plt
import random
import math
# import tkinter as tk
import ttkbootstrap as tk

from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Window(themename="darkly")
# root = tk.Tk()

def euclid(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def manhet(p1, p2):
    return sum(abs(a - b) for a, b in zip(p1, p2))

def minkov(p1, p2, p=3):
    return sum(abs(a - b) ** p for a, b in zip(p1, p2)) ** (1/p)

def kmeans(points, k, i_lim=100, chosen_metric='euclid', p=3):
    if chosen_metric == 'euclid':
        metric = euclid
    elif chosen_metric == 'manhet':
        metric = manhet
    elif chosen_metric == 'minkov':
        metric = lambda x, y: minkov(x, y, p)

    centroids = random.sample(points, k)
    
    for _ in range(i_lim):
        clusters = [[] for _ in range(k)]
        for point in points:
            distances = [metric(point, centroid) for centroid in centroids]
            closest_centroid_idx = distances.index(min(distances))
            clusters[closest_centroid_idx].append(point)
        
        new_centroids = []
        for cluster in clusters:
            if cluster:
                new_centroid = tuple(sum(coord) / len(cluster) for coord in zip(*cluster))
                new_centroids.append(new_centroid)
            else:
                new_centroids.append(random.choice(points))
        
        if new_centroids == centroids:
            break
        
        centroids = new_centroids
    
    return clusters, centroids

def plot(cords, n_clusters=8, chosen_metric='euclid', p=3):
    clusters, centroids = kmeans(cords, n_clusters, chosen_metric=chosen_metric, p=p)
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 8))

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'pink', 'brown', 'gray', 'olive', 'cyan']

    for i, cluster in enumerate(clusters):
        x, y = zip(*cluster) if cluster else ([], [])
        ax.scatter(x, y, 
                   color=colors[i % len(colors)], 
                   marker="$"+str(i+1)+"$", 
                   s=100, 
                   label=f'Cluster {i+1}')

    x, y = zip(*centroids)
    ax.scatter(x, y, color='yellow', marker='*', s=200, label='cluster centers')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'{chosen_metric} metric')

    ax.legend()
    ax.grid(False)

    return fig

def generate_random_points(n, min_val=0, max_val=20):
    return [(random.uniform(min_val, max_val), random.uniform(min_val, max_val)) for _ in range(n)]

def run_clustering():
    n_points = int(points_entry.get())
    n_clusters = int(clusters_entry.get())
    metric = metric_var.get()
    p_value = int(p_entry.get())

    random_points = generate_random_points(n_points)
    fig = plot(random_points, n_clusters=n_clusters, chosen_metric=metric, p=p_value)

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

root.title("Lab1")

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="points").grid(row=0, column=0)
points_entry = tk.Entry(input_frame)
points_entry.grid(row=0, column=1)
points_entry.insert(0, "100")

tk.Label(input_frame, text="clusters").grid(row=1, column=0)
clusters_entry = tk.Entry(input_frame)
clusters_entry.grid(row=1, column=1)
clusters_entry.insert(0, "8")

tk.Label(input_frame, text="distance").grid(row=2, column=0)
metric_var = tk.StringVar(value="euclid")
tk.OptionMenu(input_frame, metric_var,"euclid","euclid", "manhet", "minkov").grid(row=2, column=1)

tk.Label(input_frame, text="p = ").grid(row=3, column=0)
p_entry = tk.Entry(input_frame)
p_entry.grid(row=3, column=1)
p_entry.insert(0, "3")

tk.Button(input_frame, text="Run", command=run_clustering).grid(row=4, columnspan=2)

canvas_frame = tk.Frame(root)
canvas_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=1)

root.mainloop()