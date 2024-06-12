# Radial Gradient Image Generator

This project generates radial gradient images based on predefined color palettes and exports high-resolution images suitable for printing. It also includes functionality to add cutout rings for easy circular cutting.

## Features

- Generate radial gradient images with customizable subdivisions and Gaussian blur.
- Export multiple images and settings files based on selected color palettes.
- Crop images to a specified print resolution and size.
- Add cutout rings for easy circular cutting.
- Export images with timestamped filenames and associated settings in JSON format.

## Requirements

- Python 3.6+
- NumPy
- Matplotlib
- Pillow

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MST8K-code/Radial-Gradient-O-Matic.git
    cd Radial-Gradient-O-Matic
    ```

2. Install the required packages:
    ```bash
    pip install numpy matplotlib pillow
    ```

## Usage

1. Update the `color_palettes` dictionary in the script to define your color palettes. Set `export` to `True` for palettes you want to export.

2. Adjust the constants in the script to fit your needs:
    - `outputSize`: Resolution in pixels. It should be greater than `printSize * printResolution` to ensure the cropped images are big enough.
    - `numSubdivisions`: Number of divisions between each color change. Minimum is 1.
    - `gaussianBlurRadius`: Radius for Gaussian blur. Set to 0 to disable.
    - `printSize`: Export print size in inches.
    - `printResolution`: Resolution in DPI.
    - `cutoutThickness`: Thickness of the cutout ring in pixels.
    - `cutoutColor`: Color of the cutout ring.
    - `inner_cutout_width_in`: Inner cutout diameter in inches.

3. Run the script:
    ```bash
    python generate_radial_gradient.py
    ```

4. The script will generate images and settings files for each selected palette. The files will be saved in the same directory with timestamped filenames.

## Example Color Palettes

The `color_palettes` dictionary includes several predefined palettes:

```python
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
    ...
}
