import os
from PIL import Image, ImageEnhance, ImageFilter

# Directory to save processed images
PROCESSED_FOLDER = 'processed'
if not os.path.exists(PROCESSED_FOLDER):
  os.makedirs(PROCESSED_FOLDER)

def convert_to_warm_tone(file_path):
  with Image.open(file_path) as img:
    if img.mode != "RGB":
      img = img.convert("RGB")

    img = ImageEnhance.Color(img).enhance(1.0)
    img = ImageEnhance.Brightness(img).enhance(1.2)
    img = ImageEnhance.Contrast(img).enhance(1.0)
    img = ImageEnhance.Sharpness(img).enhance(1.5)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    
    # Extract the filename and create the new processed file path
    filename = os.path.basename(file_path)
    processed_filename = filename.replace('.jpg', '_processed.jpg')
    processed_file_path = os.path.join(PROCESSED_FOLDER, processed_filename)
    
    img.save(processed_file_path)

  return processed_file_path