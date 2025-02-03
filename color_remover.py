#!/usr/bin/env python3
# encoding: utf-8

r"""
# Color Remover Tool

A powerful command-line tool for manipulating colors in images. This tool provides functionality
to process images by removing or replacing colors, with support for multiple image formats
including PNG, JPG, and GIF.

## Features

- Remove all colors except black and white
- Remove specific colors using RGB or hex format
- Replace removed colors with custom colors
- Support for multiple image formats (PNG, JPG, GIF)
- Preserve transparency in images
- Easy-to-use command line interface

## Usage Examples

1. Basic usage (removes all colors except black and white):
   ```bash
   python color_remover.py input.png output.png
   ```

2. Remove a specific color (supports both RGB and hex format):
   ```bash
   python color_remover.py input.jpg output.jpg --target-color "255,0,0"
   # or using hex format
   python color_remover.py input.jpg output.jpg --target-color "#ff0000"
   ```

3. Replace with a custom color:
   ```bash
   python color_remover.py input.gif output.gif --replacement-color "#00ff00"
   ```

4. Keep only black and white pixels:
   ```bash
   python color_remover.py input.png output.png --bw-only
   ```

# Installation

1. Ensure you have Python 3.6 or higher installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

# License

This script is released under the [WTFPL License](https://en.wikipedia.org/wiki/WTFPL).
"""

from rich import print
from rich import traceback
from rich import pretty
from rich.console import Console
import typer
from PIL import Image, ImageSequence
from typing import Optional, Tuple
import os

pretty.install()
traceback.install()
console = Console()

app = typer.Typer(
    add_completion=False,
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Image Color Remover Tool",
    epilog="To get help about the script, call it with the --help option."
)

def is_color_match(pixel: Tuple[int, ...], target_color: Tuple[int, ...]) -> bool:
    """Check if a pixel matches a target color, handling both RGB and RGBA."""
    return pixel[:3] == target_color[:3]

def process_image(
    input_path: str,
    output_path: str,
    target_color: Optional[Tuple[int, int, int]] = None,
    replacement_color: Tuple[int, int, int] = (255, 255, 255),
    keep_only_bw: bool = False
) -> None:
    """
    Process an image by removing/replacing colors.

    Args:
        input_path: Path to input image
        output_path: Path to save processed image
        target_color: Specific color to remove (if None and keep_only_bw is False, removes all colors)
        replacement_color: Color to use for replacement
        keep_only_bw: If True, keeps only black and white pixels
    """
    # Get file extension
    _, ext = os.path.splitext(input_path.lower())

    with Image.open(input_path) as im:
        if ext == '.gif':
            frames = []
            for frame in ImageSequence.Iterator(im):
                processed_frame = process_single_frame(
                    frame, target_color, replacement_color, keep_only_bw
                )
                frames.append(processed_frame)

            # Save as GIF
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                loop=im.info.get('loop', 0),
                duration=im.info.get('duration', 100),
                disposal=2
            )
        else:
            # Process single image
            processed_image = process_single_frame(
                im, target_color, replacement_color, keep_only_bw
            )
            processed_image.save(output_path)

def process_single_frame(
    image: Image.Image,
    target_color: Optional[Tuple[int, int, int]],
    replacement_color: Tuple[int, int, int],
    keep_only_bw: bool
) -> Image.Image:
    """Process a single image or frame."""
    # Convert to RGBA for consistent processing
    frame_rgba = image.convert("RGBA")
    pixels = frame_rgba.getdata()
    new_pixels = []

    for px in pixels:
        if keep_only_bw:
            # Keep only black or white pixels
            if (px[0], px[1], px[2]) in [(0, 0, 0), (255, 255, 255)]:
                new_pixels.append(px)
            else:
                new_pixels.append((*replacement_color, px[3]))
        elif target_color is not None:
            # Remove specific color
            if is_color_match(px, target_color):
                new_pixels.append((*replacement_color, px[3]))
            else:
                new_pixels.append(px)
        else:
            # Remove all colors except black and white
            if (px[0], px[1], px[2]) in [(0, 0, 0), (255, 255, 255)]:
                new_pixels.append(px)
            else:
                new_pixels.append((*replacement_color, px[3]))

    frame_rgba.putdata(new_pixels)
    return frame_rgba

def parse_color(color_str: str) -> Tuple[int, int, int]:
    """
    Parse a color string in either RGB format ('255,0,0') or hex format ('#RRGGBB').

    Args:
        color_str: Color string in either 'R,G,B' or '#RRGGBB' format

    Returns:
        Tuple of (R, G, B) values

    Raises:
        ValueError: If the color string format is invalid
    """
    color_str = color_str.strip()

    # Handle hex format
    if color_str.startswith('#'):
        if len(color_str) != 7:  # #RRGGBB format should be 7 chars
            raise ValueError("Hex color must be in #RRGGBB format")
        try:
            # Convert hex to RGB
            r = int(color_str[1:3], 16)
            g = int(color_str[3:5], 16)
            b = int(color_str[5:7], 16)
            return (r, g, b)
        except ValueError:
            raise ValueError("Invalid hex color format")

    # Handle RGB format
    try:
        r, g, b = map(int, color_str.split(','))
        if not all(0 <= x <= 255 for x in (r, g, b)):
            raise ValueError("RGB values must be between 0 and 255")
        return (r, g, b)
    except ValueError:
        raise ValueError("Color must be in either R,G,B format (e.g., '255,0,0') or hex format (e.g., '#ff0000')")


#
# Main command
#
@app.command()
def main(
    input_file: str = typer.Argument(..., help="Input image file (PNG, JPG, or GIF)"),
    output_file: str = typer.Argument(..., help="Output image file"),
    target_color: Optional[str] = typer.Option(
        None,
        "--target-color", "-t",
        help="Color to remove in R,G,B format (e.g., '255,0,0') or hex format (e.g., '#ff0000')"
    ),
    replacement_color: str = typer.Option(
        "255,255,255",
        "--replacement-color", "-r",
        help="Color to replace with in R,G,B format (e.g., '255,0,0') or hex format (e.g., '#ff0000')"
    ),
    keep_only_bw: bool = typer.Option(
        False,
        "--bw-only", "-b",
        help="Keep only black and white pixels, remove all other colors"
    )
):
    """Process an image by removing or replacing colors."""
    try:
        # Parse colors from string to tuples
        replacement_rgb = parse_color(replacement_color)
        target_rgb = parse_color(target_color) if target_color else None

        # Validate input file
        if not os.path.exists(input_file):
            console.print(f"[red]Error: Input file '{input_file}' does not exist.[/red]")
            raise typer.Exit(1)

        # Process the image
        process_image(
            input_file,
            output_file,
            target_rgb,
            replacement_rgb,
            keep_only_bw
        )

        console.print(f"[green]Successfully processed image and saved to '{output_file}'[/green]")

    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def doc(
    title: str = typer.Option("Color Remover Tool", help="The title of the document"),
    toc: bool = typer.Option(False, help="Whether to create a table of contents"),
) -> None:
    """Generate documentation for the Color Remover Tool."""
    # Start building the documentation
    doc_parts = []

    # Add title
    doc_parts.append(f"# {title}\n")

    # Add main description from module docstring
    if __doc__:
        doc_parts.append(__doc__.strip() + "\n")

    # Add table of contents if requested
    if toc:
        doc_parts.append("## Table of Contents\n")
        doc_parts.append("- [Features](#features)")
        doc_parts.append("- [Installation](#installation)")
        doc_parts.append("- [Usage Examples](#usage-examples)")
        doc_parts.append("- [License](#license)\n")

    # Print the documentation
    console.print("\n".join(doc_parts))


#
# Use main as default command
#
if __name__ == "__main__":
    import sys
    from typer.main import get_command

    # Get all available command names
    commands = get_command(app).commands
    command_names = {cmd_name.lower() for cmd_name in commands.keys()}

    # If no command is provided or the first argument isn't a command,
    # insert the default command
    if len(sys.argv) == 1 or (
        len(sys.argv) > 1 and
        sys.argv[1].lower() not in command_names
    ):
        sys.argv.insert(1, "main")

    app()