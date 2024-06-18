from PIL import Image, ImageDraw, ImageFont
import random

# Paths to your three font sets using raw strings to handle backslashes
font_paths = [
    r"D:\Vedant Learnings\handwriting project\fonts\Playwrite_CO\PlaywriteCO-VariableFont_wght.ttf",
    r"D:\Vedant Learnings\handwriting project\fonts\Vedaa-Regular.ttf",
    r"D:\Vedant Learnings\handwriting project\fonts\Ved-Regular.ttf"
]

# Load fonts
fonts = [ImageFont.truetype(font_path, size=40) for font_path in font_paths]

def draw_text(text):
    # Create a blank image
    img = Image.new('RGB', (1000, 500), color='white')
    d = ImageDraw.Draw(img)
    
    x, y = 50, 50  # Starting position

    # Split the text into words
    words = text.split()

    # Alternate between fonts for each word
    for i, word in enumerate(words):
        font = fonts[i % len(fonts)]  # Cycle through fonts
        d.text((x, y), word, font=font, fill=(0, 0, 0))
        
        # Calculate width of the word for positioning the next word
        bbox = d.textbbox((x, y), word, font=font)
        word_width = bbox[2] - bbox[0]
        
        x += word_width + 10  # Add some spacing between words

    img.show()

# Example usage
draw_text("Hello, this is a test with different fonts!")
