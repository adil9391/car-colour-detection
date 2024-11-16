import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


# Function to map RGB values to color names
def get_color_name(rgb):
    colors = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "gray": (128, 128, 128),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "pink": (255, 192, 203),
    }

    # Find the closest color name
    closest_color = min(colors.keys(), key=lambda key: np.linalg.norm(np.array(colors[key]) - np.array(rgb)))
    return closest_color


def load_image():
    global img_path
    img_path = filedialog.askopenfilename(title="Select an Image",
                                          filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if img_path:
        img = Image.open(img_path)
        img = img.resize((400, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel.configure(image=img)
        panel.image = img
        detect_color(img_path)


def detect_color(image_path):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize image for easier processing
    image = cv2.resize(image, (100, 100))

    # Reshape image to a 2D array of pixels
    pixels = image.reshape(-1, 3)

    # Calculate the most common color
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    dominant_color = unique_colors[counts.argmax()]

    # Get the color name
    color_name = get_color_name(dominant_color)

    # Convert to hexadecimal color code
    color_hex = "#{:02x}{:02x}{:02x}".format(dominant_color[0], dominant_color[1], dominant_color[2])

    result_label.config(text=f'Dominant Color: {color_name} ({color_hex})', bg=color_hex)


# Set up the main GUI window
root = Tk()
root.title("Car Color Detection")
root.geometry("500x400")

panel = Label(root)
panel.pack(pady=10)

load_button = Button(root, text="Load Image", command=load_image)
load_button.pack(pady=10)

result_label = Label(root, text="Dominant Color: ", font=("Helvetica", 14))
result_label.pack(pady=20)

root.mainloop()
