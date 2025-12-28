#!/usr/bin/env python3
"""Generate Open Graph preview image for Write Toba website."""

from PIL import Image, ImageDraw, ImageFont
import sys

# Image dimensions (Facebook's recommended size)
WIDTH = 1200
HEIGHT = 630

# Colors
BACKGROUND = "#1a1f36"  # Dark blue background
TEXT_COLOR = "#ffffff"  # White text
ACCENT_COLOR = "#4f46e5"  # Indigo accent

# Batak Toba text
BATAK_TEXT = "ᯅ ᯖ ᯂ᯲ ᯖᯬ ᯅ"
APP_NAME = "Write Toba"
TAGLINE = "Learn Batak Toba Script"

def create_og_image():
    """Create the Open Graph preview image."""
    # Create image with background color
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(img)
    
    # Try to load a font that supports Batak script
    # Fall back to default if not available
    font_sizes = {
        'batak': 180,
        'title': 80,
        'tagline': 40
    }
    
    try:
        # Try to use system fonts that might support Batak script
        # macOS often has good Unicode support in system fonts
        batak_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", font_sizes['batak'])
    except:
        try:
            batak_font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", font_sizes['batak'])
        except:
            # Fallback to default
            batak_font = ImageFont.load_default()
            print("Warning: Using default font. Batak characters may not display correctly.", file=sys.stderr)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_sizes['title'])
        tagline_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_sizes['tagline'])
    except:
        title_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
    
    # Calculate positions for centered text
    # Batak text
    batak_bbox = draw.textbbox((0, 0), BATAK_TEXT, font=batak_font)
    batak_width = batak_bbox[2] - batak_bbox[0]
    batak_x = (WIDTH - batak_width) // 2
    batak_y = 150
    
    # Title
    title_bbox = draw.textbbox((0, 0), APP_NAME, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (WIDTH - title_width) // 2
    title_y = 380
    
    # Tagline
    tagline_bbox = draw.textbbox((0, 0), TAGLINE, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_x = (WIDTH - tagline_width) // 2
    tagline_y = 480
    
    # Draw decorative line above Batak text
    line_y = 100
    line_margin = 300
    draw.rectangle([line_margin, line_y, WIDTH - line_margin, line_y + 4], fill=ACCENT_COLOR)
    
    # Draw decorative line below tagline
    line_y = 550
    draw.rectangle([line_margin, line_y, WIDTH - line_margin, line_y + 4], fill=ACCENT_COLOR)
    
    # Draw text
    draw.text((batak_x, batak_y), BATAK_TEXT, font=batak_font, fill=TEXT_COLOR)
    draw.text((title_x, title_y), APP_NAME, font=title_font, fill=TEXT_COLOR)
    draw.text((tagline_x, tagline_y), TAGLINE, font=tagline_font, fill=TEXT_COLOR)
    
    # Save the image
    output_path = "og-image.png"
    img.save(output_path, "PNG", optimize=True)
    print(f"Successfully created {output_path}")
    print(f"Image size: {WIDTH}x{HEIGHT} pixels")

if __name__ == "__main__":
    try:
        create_og_image()
    except Exception as e:
        print(f"Error creating image: {e}", file=sys.stderr)
        sys.exit(1)
