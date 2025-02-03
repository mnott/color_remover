# Color Remover Tool

# Introduction

This is a command-line tool for manipulating colors in images. This tool provides functionality
to process images by removing or replacing colors, with support for multiple image formats
including PNG, JPG, and GIF.

## Features

- Remove all colors except black and white
- Remove specific colors using RGB or hex format
- Replace removed colors with custom colors
- Support for multiple image formats (PNG, JPG, GIF)
- Preserve transparency in images
- Configurable color matching tolerance
- Easy-to-use command line interface

## Usage Examples

1. Basic usage (removes all colors except black and white):
   ```bash
   python color_remover.py input.png output.png
   ```

2. Remove a specific color (supports both RGB and hex format):
   ```bash
   python color_remover.py input.jpg output.jpg -s "255,0,0"
   # or using hex format
   python color_remover.py input.jpg output.jpg -s "#ff0000"
   ```

3. Replace with a custom color:
   ```bash
   python color_remover.py input.gif output.gif -s "#ff0000" -r "#00ff00"
   ```

4. Keep only black and white pixels:
   ```bash
   python color_remover.py input.png output.png --bw
   ```

5. Adjust color matching tolerance:
   ```bash
   python color_remover.py input.png output.png -s "#ff0000" -t 40
   ```

## Options

```
-s, --search TEXT      Color to remove in R,G,B format (e.g., '255,0,0') or hex format (e.g., '#ff0000')
-r, --replace TEXT     Color to replace with (default: white)
-b, --bw, --bw-only    Keep only black and white pixels
-t, --tolerance INT    Color matching tolerance (0-255, default: 30)
```

# Installation

1. Ensure you have Python 3.6 or higher installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

# License

This script is released under the [WTFPL License](https://en.wikipedia.org/wiki/WTFPL).

