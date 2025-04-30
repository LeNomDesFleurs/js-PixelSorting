import numpy as np
from PIL import Image, ImageDraw

def create_segmented_image(resolution, segments, angle_deg, output_path="output.png"):
    width, height = resolution
    image = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(image)

    angle_rad = np.deg2rad(angle_deg % 180)  # Normalize angle between 0-179
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)

    # Determine spacing between lines perpendicular to the direction
    if angle_deg % 180 == 0:
        spacing = height / segments
        for i in range(segments):
            y_start = int(i * spacing)
            y_end = int((i + 1) * spacing - 1)
            draw.rectangle([(0, y_start), (width - 1, y_end)], fill="white")
    elif angle_deg % 180 == 90:
        spacing = width / segments
        for i in range(segments):
            x_start = int(i * spacing)
            x_end = int((i + 1) * spacing - 1)
            draw.rectangle([(x_start, 0), (x_end, height - 1)], fill="white")
    else:
        # For arbitrary angles, fill white pixels in the direction
        diag = int(np.hypot(width, height))
        spacing = diag / segments

        for y in range(height):
            for x in range(width):
                # Project point (x, y) onto the direction vector (cos_a, sin_a)
                projection = x * cos_a + y * sin_a
                segment_index = int(projection // spacing)
                if projection >= 0 and (projection % spacing) > 1:
                    image.putpixel((x, y), (255, 255, 255))

    image.save(output_path)
    print(f"Image saved to {output_path}")

# Example usage
create_segmented_image((800, 600), 10, 45, "angled_output.png")