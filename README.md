# Text Image Generator with Multiple Fonts

## Requirements

- Python (version 3.6 or higher)
- PIL (Python Imaging Library), which can be installed via pip:

## Setup

### 1. Download Fonts

- Download and place your three font files (`PlaywriteCO-VariableFont_wght.ttf`, `PlaywriteSK-VariableFont_wght.ttf`, and `PlaywriteUSTrad-VariableFont_wght.ttf`) in a directory accessible from your Python environment.

### 2. Update Font Paths

- In the Python script (`text_image_generator.py`), update the `font_paths` list with the absolute paths to your downloaded font files.

## Usage

### 1. Run the Script

- Execute the Python script (`text_image_generator.py`).

### 2. Input Text

- Enter the text you want to visualize. Each word in the text will be rendered using a different font from the three specified font sets.

### 3. View Output

- The script will display the generated image with the text rendered in various fonts.

## Example

```python
# Example usage in the script
draw_text("Hello, this is a test with different fonts!")

This README structure separates each section using hash characters (`#`) to clearly outline the requirements, setup instructions, usage guidelines, example usage, and additional notes for your text image generator script. Adjust the content and organization as necessary based on your specific project requirements.
