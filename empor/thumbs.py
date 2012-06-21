from PIL import Image
import hashlib
import os
from cStringIO import StringIO
from django.core.files import File

def generate_crop(file, ext, x1, y1, x2, y2):
    image = Image.open(file)

    # ImageOps compatible mode
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    image = image.crop((x1,y1,x2,y2))

    if image.size != (40,40):
        image = thumb_resize(image, ext, 40, 40)

    else:
        imagefile = StringIO()
        filename = hashlib.md5(imagefile.getvalue()).hexdigest()+ '.' + ext
        imagefile = open(os.path.join('/tmp',filename), 'w')
        image.save(imagefile)
        imagefile = open(os.path.join('/tmp',filename), 'r')
        content = File(imagefile)
        image = (filename, content)

    return image

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

    imagefile = StringIO()
    filename = hashlib.md5(imagefile.getvalue()).hexdigest()+ '.' + ext
    imagefile = open(os.path.join('/tmp',filename), 'w')
    image.save(imagefile)
    imagefile = open(os.path.join('/tmp',filename), 'r') 
    content = File(imagefile)

    return (filename, content)
