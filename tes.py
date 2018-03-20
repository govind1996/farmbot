from PIL import Image
import requests
response = requests.get("http://tineye.com/images/widgets/mona.jpg", stream=True)
response.raw.decode_content = True
image = Image.open(response.raw)   
image.save("C:/Users/user/mona.jpg","JPEG")
