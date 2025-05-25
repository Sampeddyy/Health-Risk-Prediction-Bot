import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_exif_date_taken(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            return None
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == 'DateTimeOriginal':
                return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
    return None

def rename_photos_by_date(folder_path):
    supported_extensions = ('.jpg', '.jpeg', '.png')
    photos_with_dates = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_extensions):
            full_path = os.path.join(folder_path, filename)
            date_taken = get_exif_date_taken(full_path)
            if date_taken:
                photos_with_dates.append((full_path, date_taken))
            else:
                print(f"No EXIF date found for {filename}, skipping.")

    # Sort by date
    photos_with_dates.sort(key=lambda x: x[1])

    # Rename files
    for index, (file_path, _) in enumerate(photos_with_dates, start=1):
        ext = os.path.splitext(file_path)[1].lower()
        new_name = f"{index}{ext}"
        new_path = os.path.join(folder_path, new_name)
        print(f"Renaming {file_path} → {new_path}")
        os.rename(file_path, new_path)

# Run on your folder
rename_photos_by_date(r"D:\comic\nemisis\photos")
