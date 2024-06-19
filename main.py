from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import tkinter as tk

# Paths to your font sets using raw strings to handle backslashes
font_paths = [
    r"D:\Vedant Learnings\handwriting project\text-to-handwriting\fonts\QEJER.ttf",
    r"D:\Vedant Learnings\handwriting project\text-to-handwriting\fonts\QEJohnCaplin.ttf"
]

# Load fonts
fonts = [ImageFont.truetype(font_path, size=40) for font_path in font_paths]

# Global variables to store previous text, image, and list of characters with fonts
prev_text = ""
img = None
char_font_list = []  # List to store (character, font) tuples

# Function to draw a character on the image using the provided font
def drawchar(d, x, y, char, font):
    bbox = d.textbbox((x, y), char, font=font)
    char_width = bbox[2] - bbox[0]
    
    d.text((x, y), char, font=font, fill=(0, 0, 0))  # Draw the character
    
    return char_width

# Function to draw text on an image
def draw_text_on_image():
    global img, char_font_list
    
    # Create a blank image with white background
    img = Image.new('RGB', (1000, 500), color='white')
    
    d = ImageDraw.Draw(img)
    x, y = 50, 50  # Starting position
    max_width, max_height = img.size
    line_height = 50  # Adjust line height based on font size
    
    # Iterate over each character and its font in the list
    for char, font in char_font_list:
        char_width = drawchar(d, x, y, char, font)
        
        # Move to the next line if the text exceeds the image width
        if x + char_width >= max_width - 50:  # 50 is the right margin
            x = 50  # Reset x to the left margin
            y += line_height  # Move y down to the next line
        
        # If y exceeds the image height, stop drawing
        if y + line_height >= max_height:
            break
        
        x += char_width * 0.85  # Adjust spacing between characters
        
        # Add extra space after a word (if char is space)
        if char == ' ':
            x += 8
    
    # Show the image in the tkinter window
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo

# Function to handle text change event
def on_text_changed(event):
    global char_font_list, prev_text
    text = entry.get()  # Get current text from entry widget
    
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

# GUI setup using tkinter
root = tk.Tk()
root.title("Live Text to Image Generator")

# Entry widget for text input
entry = tk.Entry(root, width=80)
entry.pack(pady=10)
entry.bind('<KeyRelease>', on_text_changed)  # Bind key release event to update text

# Label to display generated image
image_label = tk.Label(root)
image_label.pack(pady=10)

root.mainloop()
