import pandas as pd
import glob
from PIL import Image, ImageOps
from io import BytesIO
from IPython.display import HTML, display  
import base64

def getInfoAboutImgFromDir(dirPath):
    # Збираємо тільки зображення з розширенням .jpg і .png
    file_paths = glob.glob(f'{dirPath}/*.jpg') + glob.glob(f'{dirPath}/*.png')
    
    if not file_paths:
        print("No image files found in the directory.")
        return pd.DataFrame()
    
    image_data = []
    
    for file in file_paths:
        try:
            with Image.open(file) as img:
                original_size = img.size
                
                # Масштабуємо зображення до 200x200
                img_resized = img.resize((200, 200))
                
                # Зміна кольору на відтінки сірого
                img_gray = ImageOps.grayscale(img_resized)
                
                # Зберігаємо зображення у форматі base64 для HTML-виводу
                buffered = BytesIO()
                img_gray.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                
                image_data.append({
                    'file_path': file,
                    'original_size': original_size,
                    'resized_size': img_resized.size,
                    'mean_color': img_gray.getextrema(),
                    'image': f'<img src="data:image/png;base64,{img_str}" width="100" height="100">'
                })
                
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    # Створюємо DataFrame з інформацією про зображення
    df = pd.DataFrame(image_data)
    
    # Повертаємо DataFrame з HTML-виводом зображень
    return HTML(df.to_html(escape=False))

# Виклик функції
dir_path = r'C:\Users\\tboim\Desktop\\Учеба\\3курс\\Обробка даних Python\\Лабораторна робота №4\\ImgAndNotImg'
display(getInfoAboutImgFromDir(dir_path))