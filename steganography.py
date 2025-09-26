from PIL import Image

def encode_text(input_image_path, secret_text, output_image_path):
    img = Image.open(input_image_path)
    encoded = img.copy()
    width, height = img.size
    index = 0

    secret_text += "====="  # delimiter to mark end
    binary_secret = ''.join(format(ord(i), '08b') for i in secret_text)

    for row in range(height):
        for col in range(width):
            if index < len(binary_secret):
                r, g, b = img.getpixel((col, row))
                r = (r & ~1) | int(binary_secret[index])  # store bit in R
                encoded.putpixel((col, row), (r, g, b))
                index += 1
            else:
                encoded.save(output_image_path)
                return

def decode_text(stego_image_path):
    img = Image.open(stego_image_path)
    width, height = img.size
    binary_data = ""
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            binary_data += str(r & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_text = ""
    for byte in all_bytes:
        decoded_text += chr(int(byte, 2))
        if decoded_text.endswith("====="):
            return decoded_text[:-5]
    return decoded_text
