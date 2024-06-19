from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import tkinter as tk

# Paths to your font sets using raw strings to handle backslashes
font_paths = [
    r"D:\Vedant Learnings\handwriting project\fonts\Vedaa-Regular.ttf",
    r"D:\Vedant Learnings\handwriting project\fonts\Ved-Regular.ttf"
]

# Load fonts
fonts = [ImageFont.truetype(font_path, size=40) for font_path in font_paths]

# Global variables to store previous text, image, and available fonts
prev_text = ""
img = None
available_fonts = fonts[:]  # Copy of fonts list for use in drawchar()

# Function to draw text on an image using available fonts
def drawchar(d, x, y, char, available_fonts):
    # Select a random font from available_fonts
    font = random.choice(available_fonts)
    
    bbox = d.textbbox((x, y), char, font=font)
    char_width = bbox[2] - bbox[0]
    
    d.text((x, y), char, font=font, fill=(0, 0, 0))  # Draw the character
    
    return char_width

# Function to draw text on an image
def draw_text_on_image(text):
    global prev_text, img, available_fonts
    
    # Only update if text has changed
    if text == prev_text:
        return
    
    prev_text = text
    
    # Create a blank image with white background if img is None
    if img is None:
        img = Image.new('RGB', (1000, 500), color='white')
    
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), img.size], fill='white')  # Clear previous drawing
    
    x, y = 50, 50  # Starting position
    max_width, max_height = img.size
    line_height = 50  # Adjust line height based on font size
    
    # Iterate over each character in the text
    for char in text:
        char_width = drawchar(d, x, y, char, available_fonts)
        
        # Move to the next line if the text exceeds the image width
        if x + char_width >= max_width - 50:  # 50 is the right margin
            x = 50  # Reset x to the left margin
            y += line_height  # Move y down to the next line
        
        # If y exceeds the image height, stop drawing
        if y + line_height >= max_height:
            break
        
        x += char_width * 0.6999  # Adjust spacing between characters
        
        # Add extra space after a word (if char is space)
        if char == ' ':
            x += 10
    
    # Show the image in the tkinter window
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo

# Function to handle text change event
def on_text_changed(event):
    global available_fonts
    text = entry.get()  # Get current text from entry widget
    
    # Update available_fonts based on fonts listt
    available_fonts = fonts[:]

    draw_text_on_image(text)  # Update the image with the new text


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
