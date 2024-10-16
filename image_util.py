import os
from PIL import Image, ImageEnhance, ImageFilter

# Directory to save processed images
PROCESSED_FOLDER = 'processed'
if not os.path.exists(PROCESSED_FOLDER):
  os.makedirs(PROCESSED_FOLDER)

def convert_to_warm_tone(file_path, brightness=1.0, contrast=1.2):
  with Image.open(file_path) as img:
    if img.mode != "RGB":
      img = img.convert("RGB")
    
    # 添加暖色調：通過調整紅色和黃色的比例
    r, g, b = img.split()
    r = r.point(lambda i: i * 1.1)  # 增加紅色通道
    b = b.point(lambda i: i * 0.95)  # 減少藍色通道
    img = Image.merge('RGB', (r, g, b))

    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)

    # 保存處理過的圖片
    filename = os.path.basename(file_path)
    processed_filename = filename.replace('.jpg', '_processed.jpg')
    processed_file_path = os.path.join(PROCESSED_FOLDER, processed_filename)
    
    img.save(processed_file_path)

  return processed_file_path