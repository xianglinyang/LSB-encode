from PIL import Image
import base64


def makeImageEven(image):
    pixels = list(image.getdata())
    evenPixels = [(r >> 1 << 1, g >> 1 << 1, b >> 1 << 1, a >> 1 << 1) for [r, g, b, a] in pixels]
    evenImage = Image.new(image.mode, image.size)
    evenImage.putdata(evenPixels)
    return evenImage


def constLenBin(int):
    binary = "0" * (8 - (len(bin(int)) - 2)) + bin(int).replace('0b', '')
    return binary


def encodeDataInImage(image, data):
    evenImage = makeImageEven(image)
    binary = ''.join(map(constLenBin, bytearray(data, 'utf-8')))
    if len(binary) > len(image.getdata()) * 4:
        raise Exception("Error: Can't encode more than" + len(evenImage.getdata()) * 4 + " bits in this image. ")
    encodedPixels = [(r + int(binary[index * 4 + 0]), g + int(binary[index * 4 + 1]), b + int(binary[index * 4 + 2]),
                      a + int(binary[index * 4 + 3])) if index * 4 < len(binary) else (r, g, b, a) for
                     index, (r, g, b, a) in enumerate(list(evenImage.getdata()))]
    encodedImage = Image.new(evenImage.mode, evenImage.size)
    encodedImage.putdata(encodedPixels)
    return encodedImage


def binaryToInt(binary):
    sum = 0
    for i in range(8):
        sum = (sum << 1) + int(binary[i])
    return sum


def binaryToString(binary):
    index = 0
    string = []
    while index < len(binary):
        string.append(chr(binaryToInt(binary[index : index + 8])))
        index = index + 8
    return ''.join(string)


def pictureEncode(url):
    with open(url, 'rb') as f:
        f_str = str(base64.b64encode(f.read()), encoding='utf-8')
    return f_str


def pictureDecode(data):
    file_str = open('decodeImage.png', 'wb')
    file_str.write(base64.b64decode(data))
    file_str.close()


def decodeImage(image):
    pixels = list(image.getdata())
    binary = ''.join([str(int(r >> 1 << 1 != r)) + str(int(g >> 1 << 1 != g)) + str(int(b >> 1 << 1 != b)) + str(
        int(t >> 1 << 1 != t)) for (r, g, b, t) in pixels])
    locationDoubleNull = binary.find('0000000000000000')
    endIndex = locationDoubleNull + (
                8 - (locationDoubleNull % 8)) if locationDoubleNull % 8 != 0 else locationDoubleNull
    data = binaryToString(binary[0:endIndex])
    return data

#encode
url='target.png'
data = pictureEncode(url)
encodeDataInImage(Image.open("original-picture.png"), data).save('encodeImage.png')
#decode
str = bytes(decodeImage(Image.open("encodeImage.png")), encoding='utf-8')
pictureDecode(str)
