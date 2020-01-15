from PIL import Image

imageName="2"
im = Image.open(imageName+'.jpg')
im.save(imageName+'.png')