from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from datetime import datetime

def CompressImage(f, filename=None):
    try:
        name = str(f).split('.')[0]
        if filename:
            name = filename
        image = Image.open(f)
        thumbnail = BytesIO()
        # Default quality is quality=75
        image.save(thumbnail, format='JPEG', quality=65)
        thumbnail.seek(0)
        newImage = InMemoryUploadedFile(thumbnail,
                                   None,
                                   name + ".jpg",
                                   'image/jpeg',
                                   thumbnail.tell(),
                                   None)
        return newImage
    except Exception as e:
        return e

def convert_date(date):
    date = datetime.strptime(date, '%d-%m-%Y')
    converted = date.strftime('%Y-%m-%d')

    return converted