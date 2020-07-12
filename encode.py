import cv2
from cryptography.fernet import Fernet

def to_bit_generator(msg):
    """Converts a message into a generator which returns 1 bit of the message each time."""
    for c in (msg):
        o = ord(c)
        for i in range(8):
            yield (o & (1 << i)) >> i

def main():
    file = open('key.key', 'rb')
    key = file.read() # The key will be type bytes
    file.close()

    data = open("README.md", "r").read()

    f = Fernet(key)
    encrypted = f.encrypt(data.encode())

    # Create a generator for the hidden message
    hidden_message = to_bit_generator(encrypted.decode())
    # Read the original image
    img = cv2.imread('input.png', cv2.IMREAD_GRAYSCALE)
    x = 0
    for h in range(len(img)):
        for w in range(len(img[0])):
            try:
                x = next(hidden_message)
            except StopIteration as e:
                x = 0
            # Write the hidden message into the least significant bit
            img[h][w] = (img[h][w] & ~1) | x
    # Write out the image with hidden message
    cv2.imwrite("output.png", img)

if __name__ == "__main__":
	main()
