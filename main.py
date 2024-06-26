from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import tkinter as tk
from tkinter import filedialog
from threading import Timer

# Paths to your font sets using raw strings to handle backslashes
font_paths = [
    r"D:\Vedant Learnings\handwriting project\text-to-handwriting\fonts\Fontvver2-Regular.ttf",
    r"D:\Vedant Learnings\handwriting project\text-to-handwriting\fonts\Fontgv2Ver1-Regular.ttf"
]

# Load fonts with initial size
initial_font_size = 12
fonts = [ImageFont.truetype(font_path, size=initial_font_size) for font_path in font_paths]

# Global variables to store previous text, image, and list of characters with fonts
prev_text = ""
char_font_list = []  # List to store (character, font) tuples
font_size = initial_font_size  # Initialize font size
start_x = 72  # Initial starting x position
start_y = 74  # Initial starting y position
char_gap = 0.71  # Initial character gap multiplier
line_gap_series = [10.0]  # Initial line gap series
right_margin = 35  # Increased right margin
word_space = 10  # Initial word space

# Load the background lined page image
lined_page_path = r"D:\Vedant Learnings\handwriting project\text-to-handwriting\background\lined_page.png"
lined_page_image = Image.open(lined_page_path).convert("RGB")

# Initialize text_timer as None
text_timer = None

# Function to draw a character on the image using the provided font
def drawchar(d, x, y, char, font):
    bbox = d.textbbox((x, y), char, font=font)
    char_width = bbox[2] - bbox[0]
    d.text((x, y), char, font=font, fill=(0, 0, 0))  # Draw the character
    return char_width

# Function to draw text on an image
def draw_text_on_image():
    global img, char_font_list, lined_page_image, start_x, start_y, char_gap, line_gap_series, word_space

    # Create a copy of the background image
    img = lined_page_image.copy()

    d = ImageDraw.Draw(img)
    x, y = start_x, start_y  # Starting position from entry fields
    max_width, max_height = img.size
    line_index = 0

    # Iterate over each character and its font in the list
    for char, font in char_font_list:
        char_width = drawchar(d, x, y, char, font)

        # Move to the next line if the text exceeds the image width
        if x + char_width >= max_width - right_margin:  # Adjusted right margin
            x = start_x  # Reset x to the left margin from entry fields
            line_index += 1  # Increment line index

            # Use the corresponding line gap from the series, or the last value if we run out of values
            current_line_gap = line_gap_series[line_index] if line_index < len(line_gap_series) else line_gap_series[-1]
            y += font_size + current_line_gap  # Move y down to the next line

        # If y exceeds the image height, stop drawing
        if y + font_size + line_gap_series[-1] >= max_height:
            break

        x += char_width * char_gap  # Adjust spacing between characters

        # Add extra space after a word (if char is space)
        if char == ' ':
            x += word_space

    # Show the image in the tkinter window
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo

# Function to handle text change event with debounce
def on_text_changed(event):
    global char_font_list, prev_text, text_timer

    # Check if text_timer is None
    if text_timer:
        text_timer.cancel()

    # Start a new timer to process text after 700 milliseconds (adjust as needed)
    text_timer = Timer(0.7, process_text)
    text_timer.start()

def process_text():
    global char_font_list, prev_text

    # Get current text from entry widget
    text = text_widget.get("1.0", tk.END).strip()

    # Determine the position of the first change (deletion or addition)
    start_index = 0
    while start_index < len(prev_text) and start_index < len(text) and prev_text[start_index] == text[start_index]:
        start_index += 1

    # Remove tuples from char_font_list for deleted characters
    char_font_list = char_font_list[:start_index]

    # Insert tuples into char_font_list for added characters
    for char in text[start_index:]:
        char_font_list.append((char, random.choice(fonts)))

    prev_text = text
    draw_text_on_image()  # Update the image with the new text and fonts

# Function to handle font size change
def on_font_size_changed(event):
    global fonts, font_size, char_font_list, prev_text
    try:
        font_size = int(font_size_entry.get())
    except ValueError:
        font_size = initial_font_size

    fonts = [ImageFont.truetype(font_path, size=font_size) for font_path in font_paths]
    # Update char_font_list with new fonts based on current text
    char_font_list = [(char, random.choice(fonts)) for char in prev_text]
    draw_text_on_image()  # Redraw the text with the new font size

# Function to handle starting x position change
def on_start_x_changed(event):
    global start_x
    try:
        start_x = int(start_x_entry.get())
    except ValueError:
        start_x = 50  # Default value if input is invalid
    draw_text_on_image()  # Redraw the text with the new starting position

# Function to handle starting y position change
def on_start_y_changed(event):
    global start_y
    try:
        start_y = int(start_y_entry.get())
    except ValueError:
        start_y = 50  # Default value if input is invalid
    draw_text_on_image()  # Redraw the text with the new starting position

# Function to handle character gap change
def on_char_gap_changed(event):
    global char_gap
    try:
        char_gap = float(char_gap_entry.get())
    except ValueError:
        char_gap = 0.71  # Default value if input is invalid
    draw_text_on_image()  # Redraw the text with the new character gap

# Function to handle line gap change
def on_line_gap_changed(event):
    global line_gap_series
    try:
        line_gap_series = [float(gap) for gap in line_gap_entry.get().split()]
    except ValueError:
        line_gap_series = [10.0]  # Default value if input is invalid
    draw_text_on_image()  # Redraw the text with the new line gap series

# Function to handle word space change
def on_word_space_changed(event):
    global word_space
    try:
        word_space = int(word_space_entry.get())
    except ValueError:
        word_space = 10  # Default value if input is invalid
    draw_text_on_image()  # Redraw the text with the new word space

# Function to handle image download
def download_image():
    global img
    if img:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            # Determine file extension to save in appropriate format
            file_extension = file_path.split(".")[-1].lower()

            if file_extension == "png":
                img.save(file_path)
            elif file_extension == "jpg" or "jpeg":
                img.save(file_path, quality=100)  # Adjust quality as needed
            else:
                img.save(file_path)  # Default to PNG if extension is unrecognized

# GUI setup using tkinter
root = tk.Tk()
root.title("Live Text to Image Generator")

# Main frame to hold all widgets
main_frame = tk.Frame(root)
main_frame.pack(pady=10, padx=10, expand=True, fill="both")

# Frame for inputs and settings
input_frame = tk.Frame(main_frame)
input_frame.grid(row=0, column=0, sticky="nw")

# First row of inputs
font_size_label = tk.Label(input_frame, text="Font Size")
font_size_label.grid(row=0, column=0, padx=5, pady=5)
font_size_entry = tk.Entry(input_frame, width=10)
font_size_entry.grid(row=0, column=1, padx=5, pady=5)
font_size_entry.insert(0, str(initial_font_size))
font_size_entry.bind('<KeyRelease>', on_font_size_changed)

start_x_label = tk.Label(input_frame, text="Start X Position")
start_x_label.grid(row=0, column=2, padx=5, pady=5)
start_x_entry = tk.Entry(input_frame, width=10)
start_x_entry.grid(row=0, column=3, padx=5, pady=5)
start_x_entry.insert(0, str(start_x))
start_x_entry.bind('<KeyRelease>', on_start_x_changed)

start_y_label = tk.Label(input_frame, text="Start Y Position")
start_y_label.grid(row=0, column=4, padx=5, pady=5)
start_y_entry = tk.Entry(input_frame, width=10)
start_y_entry.grid(row=0, column=5, padx=5, pady=5)
start_y_entry.insert(0, str(start_y))
start_y_entry.bind('<KeyRelease>', on_start_y_changed)

# Second row of inputs
char_gap_label = tk.Label(input_frame, text="Character Gap Multiplier")
char_gap_label.grid(row=1, column=0, padx=5, pady=5)
char_gap_entry = tk.Entry(input_frame, width=10)
char_gap_entry.grid(row=1, column=1, padx=5, pady=5)
char_gap_entry.insert(0, str(char_gap))
char_gap_entry.bind('<KeyRelease>', on_char_gap_changed)

line_gap_label = tk.Label(input_frame, text="Line Gaps (space-separated)")
line_gap_label.grid(row=1, column=2, padx=5, pady=5)
line_gap_entry = tk.Entry(input_frame, width=10)
line_gap_entry.grid(row=1, column=3, padx=5, pady=5)
line_gap_entry.insert(0, ' '.join(map(str, line_gap_series)))
line_gap_entry.bind('<KeyRelease>', on_line_gap_changed)

word_space_label = tk.Label(input_frame, text="Word Space")
word_space_label.grid(row=1, column=4, padx=5, pady=5)
word_space_entry = tk.Entry(input_frame, width=10)
word_space_entry.grid(row=1, column=5, padx=5, pady=5)
word_space_entry.insert(0, str(word_space))
word_space_entry.bind('<KeyRelease>', on_word_space_changed)

# Text widget for text input
text_widget = tk.Text(main_frame, wrap="word", width=80, height=10)
text_widget.grid(row=1, column=0, pady=10, padx=5, sticky="nsew")
text_widget.bind('<KeyRelease>', on_text_changed)  # Bind key release event to update text

# Button for downloading the image
download_button = tk.Button(main_frame, text="Download Image", command=download_image)
download_button.grid(row=2, column=0, pady=10, padx=5, sticky="nw")

# Label to display generated image
image_label = tk.Label(main_frame)
image_label.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")

# Configure row and column weights for proper resizing
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(1, weight=1)

root.mainloop()
