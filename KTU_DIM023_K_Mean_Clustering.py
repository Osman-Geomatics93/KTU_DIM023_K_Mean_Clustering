#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.cluster import KMeans
import rasterio
from rasterio.plot import reshape_as_image

def browse_images():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.img")])
    if file_path:
        global color_img, gray_img
        if file_path.lower().endswith('.img'):
            with rasterio.open(file_path) as src:
                color_arr = reshape_as_image(src.read())
                color_arr = (color_arr * (255.0 / color_arr.max())).astype(np.uint8) # Add this line
                color_img = Image.fromarray(color_arr)
        else:
            color_img = Image.open(file_path)

        gray_img = ImageOps.grayscale(color_img)


def display_original_image():
    display_images(color_img, "Original Image")

def display_grayscale_image():
    display_images(gray_img, "Grayscale Image")

def display_kmeans_image():
    kmeans_image(gray_img, int(k_value_entry.get()))

def display_color_kmeans_image():
    kmeans_color_image(color_img, int(k_value_entry.get()))

def display_images(img, title):
    window = tk.Toplevel(root)
    window.title(title)

    photo = ImageTk.PhotoImage(img)

    label = tk.Label(window, image=photo)
    label.image = photo
    label.pack(padx=10, pady=10)

def display_histograms():
    histograms(color_img, gray_img, int(k_value_entry.get()))

def kmeans_image(gray_img, k_value):
    gray_arr = np.array(gray_img)
    kmeans = KMeans(n_clusters=k_value)
    pixel_values = gray_arr.reshape(-1, 1)
    kmeans.fit(pixel_values)
    labels = kmeans.labels_.reshape(gray_arr.shape)

    clustered_img = Image.fromarray((labels * 255 // (k_value - 1)).astype(np.uint8), mode='L')
    display_images(clustered_img, "K-means Clustered Image")

def kmeans_color_image(color_img, k_value):
    color_arr = np.array(color_img)
    kmeans = KMeans(n_clusters=k_value)
    pixel_values = color_arr.reshape(-1, 3)
    kmeans.fit(pixel_values)
    labels = kmeans.labels_.reshape(color_arr.shape[:2])

    clustered_arr = np.zeros_like(color_arr)
    for i in range(k_value):
        clustered_arr[labels == i] = kmeans.cluster_centers_[i]

    clustered_img = Image.fromarray(clustered_arr.astype(np.uint8))
    display_images(clustered_img, "K-means Clustered Color Image")

def histograms(color_img, gray_img, k_value):
    histogram_window = tk.Toplevel(root)
    histogram_window.title("Histograms")

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    # Color Image Histogram
    color_arr = np.array(color_img)
    colors = ("r", "g", "b")
    for i, color in enumerate(colors):
        axs[0].hist(color_arr[..., i].ravel(), bins=256, color=color, alpha=0.6)
    axs[0].set_title("Color Image Histogram")
    axs[0].legend(['Red', 'Green', 'Blue'])

    # Grayscale Image Histogram with K-means Clustering
    gray_arr = np.array(gray_img).ravel()
    axs[1].hist(gray_arr, bins=256, color='gray', alpha=0.6)

    kmeans = KMeans(n_clusters=k_value)
    kmeans.fit(gray_arr.reshape(-1, 1))
    centers = kmeans.cluster_centers_.squeeze()
    for center in centers:
        axs[1].axvline(center, color='r', linestyle='--')
    axs[1].set_title("Grayscale Image Histogram with K-means Clustering")
    axs[1].legend(['K-means Clustering'])

    canvas = FigureCanvasTkAgg(fig, master=histogram_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side="bottom", padx=10, pady=10)

def display_kmeans_centers():
    plot_kmeans_centers(gray_img, int(k_value_entry.get()))

def plot_kmeans_centers(gray_img, k_value):
    gray_arr = np.array(gray_img).ravel()
    kmeans = KMeans(n_clusters=k_value)
    kmeans.fit(gray_arr.reshape(-1, 1))
    centers = kmeans.cluster_centers_.squeeze()

    centers_window = tk.Toplevel(root)
    centers_window.title("K-means Center Locations")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(range(1, k_value + 1), centers, c='r', marker='o')
    ax.set_title("K-means Center Locations")
    ax.set_xlabel("Cluster Index")
    ax.set_ylabel("Intensity Value")

    canvas = FigureCanvasTkAgg(fig, master=centers_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side="bottom", padx=10, pady=10)

def display_scatter_by_group():
    scatter_by_group(color_img)

def scatter_by_group(color_img):
    color_arr = np.array(color_img)
    r_band = color_arr[..., 0].ravel()
    g_band = color_arr[..., 1].ravel()
    b_band = color_arr[..., 2].ravel()

    scatter_window = tk.Toplevel(root)
    scatter_window.title("Scatter Plot by Group (Bands)")

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(r_band, g_band, c='r', marker='.', alpha=0.6, label='Red')
    ax.scatter(g_band, b_band, c='g', marker='.', alpha=0.6, label='Green')
    ax.scatter(b_band, r_band, c='b', marker='.', alpha=0.6, label='Blue')
    ax.set_title("Scatter Plot by Group (Bands)")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=scatter_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side="bottom", padx=10, pady=10)

def main():
    global root, k_value_entry, color_img, gray_img
    root = tk.Tk()
    root.title("KTU-DIP023")

    browse_button = tk.Button(root, text="Browse Images", command=browse_images)
    browse_button.grid(row=0, column=0, padx=20, pady=20)

    original_button = tk.Button(root, text="Display Original Image", command=display_original_image)
    original_button.grid(row=1, column=0, padx=20, pady=10)

    grayscale_button = tk.Button(root, text="Display Grayscale Image", command=display_grayscale_image)
    grayscale_button.grid(row=2, column=0, padx=20, pady=10)

    histogram_button = tk.Button(root, text="Display Histograms", command=display_histograms)
    histogram_button.grid(row=3, column=0, padx=20, pady=10)

    kmeans_button = tk.Button(root, text="Display K-means Clustered Image", command=display_kmeans_image)
    kmeans_button.grid(row=4, column=0, padx=20, pady=10)

    kmeans_color_button = tk.Button(root, text="Display K-means Clustered Color Image", command=display_color_kmeans_image)
    kmeans_color_button.grid(row=5, column=0, padx=20, pady=10)

    kmeans_centers_button = tk.Button(root, text="Display K-means Center Locations", command=display_kmeans_centers)
    kmeans_centers_button.grid(row=6, column=0, padx=20, pady=10)

    scatter_group_button = tk.Button(root, text="Display Scatter Plot by Group (Bands)", command=display_scatter_by_group)
    scatter_group_button.grid(row=7, column=0, padx=20, pady=10)

    k_value_label = tk.Label(root, text="K value:")
    k_value_label.grid(row=8, column=0, sticky="e")

    k_value_entry = tk.Entry(root)
    k_value_entry.insert(0, "3")
    k_value_entry.grid(row=8, column=1, padx=(0, 20))

    root.mainloop()

if __name__ == "__main__":
    main()

