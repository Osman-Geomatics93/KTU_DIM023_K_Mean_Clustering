# KTU_DIM023_K_Mean_Clustering
This program provides a GUI-based application using the "tkinter" library to perform various image processing tasks on both grayscale and color images
Key features include:

Image Loading: Users can load images in formats like JPG, PNG, BMP, TIFF, and more, including specialized .img raster files.
Image Display: Displays the original, grayscale, and K-means clustered versions of the loaded image.
Histogram Visualization: Plots histograms for color and grayscale images. For grayscale images, it also showcases K-means clustering centers.
K-means Clustering: Performs K-means clustering on the pixel intensities of grayscale images and RGB values of color images. The user can specify the number of clusters (K value).
K-means Center Locations: Plots the intensity values of the K-means centers for grayscale images.
Scatter Plot by Bands: Visualizes the relationship between RGB bands in a scatter plot format.
The GUI provides an intuitive interface with buttons for each functionality, along with an entry widget for the user to specify the K value for clustering. The backend image processing leverages libraries like PIL for image operations, numpy for numerical computations, matplotlib for plotting, and sklearn for K-means clustering.
