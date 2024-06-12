import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter
import json

# Image Constants
outputSize = 6000  # Resolution in pixesl.  It should be greater than the print size x resolution to make sure the cropped images are big enough.
numSubdivisions = 30  # Number of divisions between each color change (higher is smoother).  Minimum is 1, there is no max, but it starts to get weird at high levels
gaussianBlurRadius = 50  # Radius for Gaussian blur.  Set to 0 to disable.  Works best with higher subdivisions

# Print Constants
printSize = 8  # Export print size in inches
printResolution = 350  # Resolution in DPI
cutoutThickness = 7  # Thickness of the cutout ring in pixels.  Default: 7
cutoutColor = (0, 0, 0)  # Color of the cutout ring.  Default: black
inner_cutout_width_in = 0.25  # Inner cutout diameter in inches


# Function to complete the color degrees array
def complete_color_degrees(array):
    modified_array = array.copy()
    
    # Calculate degrees if not provided
    if all('degree' not in color for color in modified_array):
        num_colors = len(modified_array)
        degree_step = 360 / num_colors
        for i, color in enumerate(modified_array):
            color['degree'] = i * degree_step
    
    first_entry = modified_array[0].copy()
    
    # Modify the degree of the first entry
    modified_array[0]['degree'] = 0
    
    # Create a copy of the first entry and modify the degree to 360
    last_entry = first_entry.copy()
    last_entry['degree'] = 360
    
    modified_array.append(last_entry)
    return modified_array



# Define the color palettes.  Mark palette as True if you'd like to export it.
color_palettes = {
    'bright_rainbow': {
        'description': 'A bright and vibrant set of rainbow colors',
        'export': True,
        'colors': [
            {'name': 'Yellow', 'color': '#eedd00'},
            {'name': 'Orange', 'color': '#ee9944'},
            {'name': 'Pink', 'color': '#c53f65'},
            {'name': 'Lavender', 'color': '#8346c1'},
            {'name': 'Blue', 'color': '#3366bb'},
            {'name': 'Sky Blue', 'color': '#0099cc'},
            {'name': 'Cyan', 'color': '#22ccbb'},
            {'name': 'Green', 'color': '#99dd55'}
        ]
    },
    'seasons_1': {
        'description': 'Retro set of season colors',
        'export': True,
        'colors': [
            {'name': 'Yellow', 'color': '#ffd43a'},
            {'name': 'Orange', 'color': '#FD8111'},
            {'name': 'Blue', 'color': '#9bb2db'},
            {'name': 'Green', 'color': '#4d884e'}
        ]
    },
    'vintage_rainbow_1': {
        'description': 'A vintage set of rainbow colors',
        'export': True,
        'colors': [
            {'name': 'Yellow', 'color': '#D8D7B9'},
            {'name': 'Pink', 'color': '#C17E9B'},
            {'name': 'Blue', 'color': '#7397AA'},
            {'name': 'Green', 'color': '#87B191'}
        ]
    },
    'vintage_rainbow_2': {
        'description': 'A vintage set of rainbow colors',
        'export': True,
        'colors': [
            {'name': 'Yellow', 'color': '#D8D7B9'},
            {'name': 'Orange', 'color': '#CDAB81'},
            {'name': 'Blue', 'color': '#7397AA'},
            {'name': 'Green', 'color': '#87B191'}
        ]
    },
    'vintage_rainbow_3': {
        'description': 'A vintage set of rainbow colors',
        'export': True,
        'colors': [
            {'name': 'Light Yellow', 'color': '#FBD773'},
            {'name': 'Peach', 'color': '#F8A479'},
            {'name': 'Pink', 'color': '#C85B8A'},
            {'name': 'Purple', 'color': '#8A4495'},
            {'name': 'Olive', 'color': '#657665'},
            {'name': 'Green', 'color': '#7F9F8F'}
        ]
    },
    'google_brand': {
        'description': 'Google brand colors',
        'export': True,
        'colors': [
            {'name': 'Yellow', 'color': '#FBBC05'},
            {'name': 'Red', 'color': '#EA4335'},
            {'name': 'Blue', 'color': '#4285F4'},
            {'name': 'Green', 'color': '#34A853'}
        ]
    },
    'pastel_mixed': {
        'description': 'A mixed set of pastel colors',
        'export': True,
        'colors': [
            {'name': 'Yellow', 'color': '#E0EBC5'},
            {'name': 'Pink', 'color': '#E2BAE8'},
            {'name': 'Purple', 'color': '#A096D1'},
            {'name': 'Green', 'color': '#9BD4B3'}
        
        ]
    }
}


# Convert hex color to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Generate radial gradient image
def generate_radial_gradient(colors, output_size, num_subdivisions):
    img = Image.new('RGB', (output_size, output_size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    center = output_size // 2
    radius = center
    
    for i in range(len(colors) - 1):
        start_color = hex_to_rgb(colors[i]['color'])
        end_color = hex_to_rgb(colors[i + 1]['color'])
        start_angle = colors[i]['degree']
        end_angle = colors[i + 1]['degree']
        
        angle_step = (end_angle - start_angle) / num_subdivisions
        
        for j in range(num_subdivisions):
            t = j / num_subdivisions
            interp_color = (
                int(start_color[0] * (1 - t) + end_color[0] * t),
                int(start_color[1] * (1 - t) + end_color[1] * t),
                int(start_color[2] * (1 - t) + end_color[2] * t),
            )
            draw.pieslice(
                [0, 0, output_size, output_size],
                start=start_angle + j * angle_step,
                end=start_angle + (j + 1) * angle_step,
                fill=interp_color,
            )
    
    return img


# Loop through each palette and export if selected
for palette_name, palette in color_palettes.items():
    if palette['export']:
        selected_palette = palette
        completed_color_degrees = complete_color_degrees(selected_palette['colors'])

        # Generate the image
        gradient_image = generate_radial_gradient(completed_color_degrees, outputSize, numSubdivisions)
        gradient_image = gradient_image.rotate(90, expand=True)  # Rotate the image 90 degrees counter-clockwise

        # Apply Gaussian blur if the radius is greater than 0
        if gaussianBlurRadius > 0:
            gradient_image = gradient_image.filter(ImageFilter.GaussianBlur(gaussianBlurRadius))

        # Save the image with a timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_root = f"{timestamp} - radial_gradient ({palette_name})"

        image_filename = f"{file_root}.png"
        gradient_image.save(image_filename)
        gradient_image.show()

        # Export settings to a text file in JSON format
        settings = {
            'outputSize': outputSize,
            'numSubdivisions': numSubdivisions,
            'gaussianBlurRadius': gaussianBlurRadius,
            'selected_palette_name': palette_name,
            'selected_palette': selected_palette
        }

        settings_filename = f"{file_root}.txt"
        with open(settings_filename, 'w') as settings_file:
            json.dump(settings, settings_file, indent=4)

        # Crop the image to the size for the new printed resolution
        printWidth = printSize * printResolution
        crop_box = (
            (outputSize - printWidth) // 2,
            (outputSize - printWidth) // 2,
            (outputSize + printWidth) // 2,
            (outputSize + printWidth) // 2
        )
        cropped_image = gradient_image.crop(crop_box)

        # Create a mask to fill corners with white
        mask = Image.new('L', (printWidth, printWidth), 255)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse(
            [(cutoutThickness, cutoutThickness), (printWidth - cutoutThickness, printWidth - cutoutThickness)],
            fill=0
        )
        white_layer = Image.new('RGB', (printWidth, printWidth), (255, 255, 255))
        cropped_image.paste(white_layer, (0, 0), mask)

        # Draw the centered rings on top of the cropped image
        draw = ImageDraw.Draw(cropped_image)
        center = printWidth // 2
        outer_radius = center
        inner_radius = center - cutoutThickness

        # Draw outer ring
        draw.ellipse(
            [(center - outer_radius, center - outer_radius), (center + outer_radius, center + outer_radius)],
            outline=cutoutColor,
            width=cutoutThickness
        )

        # Calculate inner cutout width in pixels
        inner_cutout_width_px = inner_cutout_width_in * printResolution
        inner_cutout_radius = inner_cutout_width_px // 2

        # Draw inner ring
        draw.ellipse(
            [(center - inner_cutout_radius, center - inner_cutout_radius), (center + inner_cutout_radius, center + inner_cutout_radius)],
            fill=(255, 255, 255),
            outline=cutoutColor,
            width=cutoutThickness
        )

        # Save the cropped image with the ring
        cropped_image_filename = f"{file_root}_print_ready.png"
        cropped_image.save(cropped_image_filename)
        cropped_image.show()

        print(f"Image saved as {image_filename}")
        print(f"Settings saved as {settings_filename}")
        print(f"Cropped image saved as {cropped_image_filename}")
