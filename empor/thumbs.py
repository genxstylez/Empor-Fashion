from PIL import Image
import hashlib
from django.core.files.base import ContentFile
import cStringIO

def generate_crop(file, ext, x1, y1, x2, y2):
    image = Image.open(file)

    # ImageOps compatible mode
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    cropped = image.crop((x1,y1,x2,y2))

    if image.size != (40,40):
        cropped = thumb_resize(image, ext, 40, 40)

    else:
        imagefile = cStringIO.StringIO()
        filename = hashlib.md5(imagefile.getvalue()).hexdigest()+ '.' + ext
        if ext.upper() == 'JPG':
                ext = 'JPEG'
        image.save(imagefile, ext, quality=95)
        content = ContentFile(imagefile.getvalue())
        image = (filename, content)

    return cropped

def thumb_resize(file, ext, dimension1, dimension2=None):
    if isinstance(file, Image.Image):
        image = file
    else:
        image = Image.open(file)

    sizes = image.size
    ratio = sizes[0] / dimension1
    if not dimension2:
        dimension2 = sizes[1]/ratio 
    image = image.resize((dimension1, dimension2), Image.ANTIALIAS)

    io = cStringIO.StringIO()
    if ext.upper() == 'JPG':
        ext = 'JPEG'
    image.save(io, ext, quality=95)
    content = ContentFile(io.getvalue())
    filename = hashlib.md5(io.getvalue()).hexdigest()+ '.' + ext

    return (filename, content)
