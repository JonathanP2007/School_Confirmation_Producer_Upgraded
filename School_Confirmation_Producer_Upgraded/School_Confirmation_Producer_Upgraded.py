import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

current_time = datetime.now().strftime("%H:%M")
current_date = datetime.now().strftime("%d/%m/%Y")

def reversetext(text):
    return text[::-1]

# Input GIF file path
gif_path = 'defaultgif.gif'

# Collect inputs once
shem = reversetext(input("מה השם? "))
kita = reversetext(input("מה הכיתה? "))
kita_number = input("איזה מספר כיתה? ")
output_path = reversetext(shem) + '.gif'

if input("לבחור שעה בעצמך? (y/n) ") == "y":
    shaa = input("איזה שעה? ")
else:
    shaa = current_time
if input("לבחור תאריך בעצמך? (y/n) ") == "y":
    taarich = input("איזה תאריך? ")
else:
    taarich = current_date
if input("לבחור שעה נוכחית בעצמך? (y/n) ") == "y":
    time = input("איזה שעה? ")
else:
    time = current_time


# Load the GIF
with Image.open(gif_path) as img:
    frames = []
    frame_durations = []  # To keep track of frame durations

    # Read all frames of the GIF
    try:
        while True:
            frame = img.convert("RGBA")  # Convert to RGBA
            draw = ImageDraw.Draw(frame)

            font_path = "Alef-bold.ttf"
            number_font_path = "Roboto-Bold.ttf"
            font_size = 28
            number_size = 23
            shaa_size = 22
            time_size = 16
            font = ImageFont.truetype(font_path, font_size)
            number_font = ImageFont.truetype(number_font_path, number_size)
            shaa_font = ImageFont.truetype(number_font_path, shaa_size)
            time_font = ImageFont.truetype(number_font_path, time_size)

            # Calculate text bounding box
            shembox = draw.textbbox((0, 0), shem, font=font)
            shem_width = shembox[2] - shembox[0]

            kitabox = draw.textbbox((0, 0), kita, font=font)
            kita_width = kitabox[2] - kitabox[0]

            kita_numberbox = draw.textbbox((0, 0), kita_number, font=number_font)
            kita_number_width = kita_numberbox[2] - kita_numberbox[0]

            # Define text position
            image_width, image_height = frame.size
            shem_position = (image_width - shem_width - 145, 257)
            kita_position = (image_width - kita_width - 413, 258)
            kita_number_position = (image_width - kita_number_width - (440 if len(kita) != 1 else 423), 266)
            shaa_position = (22, 219)
            taarich_position = (252, 218)
            time_position = (25, 14)

            text_color_transparent = (0, 0, 0, 190)  # 50% opacity color for all texts

            # Create a new transparent layer for text
            text_layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_layer)

            # Draw all texts on the transparent layer
            text_draw.text(shem_position, shem, font=font, fill=text_color_transparent)
            text_draw.text(kita_position, kita, font=font, fill=text_color_transparent)
            text_draw.text(kita_number_position, kita_number, font=number_font, fill=text_color_transparent)
            text_draw.text(shaa_position, shaa, font=shaa_font, fill=text_color_transparent)
            text_draw.text(taarich_position, taarich, font=number_font, fill=text_color_transparent)
            text_draw.text(time_position, time, font=time_font, fill=text_color_transparent)

            # Composite the text layer onto the frame
            frame = Image.alpha_composite(frame, text_layer)

            frames.append(frame)

            # Store the duration of the current frame
            frame_durations.append(img.info['duration'])

            img.seek(img.tell() + 1)  # Move to the next frame
    except EOFError:
        pass  # End of GIF

    # Save the modified frames as a new GIF with original durations
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=frame_durations, loop=0)

print(f"GIF saved as {output_path}")
