from PIL import Image
img = Image.open('aa0.gif',mode='wr') 
img = img.convert("RGBA") 
pixdata = img.load() 
width,height = img.size
print('imgsize: %dx %d' % (width, height))
print('pixel[2,4]:', pixdata[2, 4]) #eg,(0xD3,0xD3,0xD3,0xFF)