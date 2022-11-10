from PIL import Image

image = Image.open ("yolov5_deploy-main\ImagesAttendance\Sanket.jpg")
with open(image,"rb") as img:
    df = img.read()
    print(img)