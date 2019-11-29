from PIL import Image


def decodeImage(image):
    pixels = list(image.getdata())
    binary = ''.join([str(int(r >> 1 << 1 != r)) + str(int(g >> 1 << 1 != g)) + str(int(b >> 1 << 1 != b)) + str(
        int(a >> 1 << 1 != a)) for (r, g, b, a) in pixels])
    return binary


mes = decodeImage(Image.open("encoded-picture.png"))
message_file = open('decoded_message.txt', 'w+')
message_file.write(mes)
message_file.close()
