import requests
from io import StringIO
r =requests.get('file:///F:/py/Decaptcha/images/aa0.gif')
img =Image.open(imgbuf)