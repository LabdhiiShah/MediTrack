import easyocr

reader = easyocr.Reader(['en'])
result = reader.readtext('med2.jpg')

for detection in result:
    print(detection[1])