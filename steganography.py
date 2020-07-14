
import click
import cv2
from cryptography.fernet import Fernet
import os

class Steganography(object):

    @staticmethod
    def __to_bit_generator(msg):
        """Converts a message into a generator which returns 1 bit of the message each time.
        :param msg: Message from input file
        :return: Iterator.
        """

        for c in (msg):
            o = ord(c)
            for i in range(8):
                yield (o & (1 << i)) >> i
                
    @staticmethod
    def __read_file_as_bytes(file):
        """Reads the file.
        :param file: Input file
        :return: bytes.
        """
        
        file = open(file, 'rb')
        data = file.read()
        file.close()
        return data

    @staticmethod
    def __read_file_as_str(file):
        """Reads the file.
        :param file: Input file
        :return: str.
        """
        
        return open(file, "r").read()

    @staticmethod
    def write_file(file, data):
        """Reads the file.
        :param file: Output file name
        :param data: bytes that needs to be written in the file
        """
        
        file_output = open(file, "w")
        file_output.write(data)
        file_output.close()

    @staticmethod
    def encrypt(key, img, file):
        """Merge two images. The second one will be merged into the first one.
        :param key: Key that needs for encryption
        :param img: Image used to store data
        :param file: File which has the text data
        :return: A new encrypted image.
        """

        # Read the file which has the text data
        data = Steganography.__read_file_as_str(file)
    
        # Encrypt the text data using the key
        f = Fernet(Steganography.__read_file_as_bytes(key))
        encrypted = f.encrypt(data.encode())
    
        # Create a generator for the hidden message
        hidden_message = Steganography.__to_bit_generator(encrypted.decode())

        # Read the original image
        image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

        x = 0
        for h in range(len(image)):
            for w in range(len(image[0])):
                try:
                    x = next(hidden_message)
                except StopIteration as e:
                    x = 0
                # Write the hidden message into the least significant bit
                image[h][w] = (image[h][w] & ~1) | x
        
        return image

    @staticmethod
    def decrypt(key, img):
        """Extract the data from the image
        :param key: Key used for encryption.
        :param img: The input image.
        :return: Extracted text data from image
        """

        # Read the image and try to restore the message
        image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        i = 0
        bits = ''
        chars = []
        for row in image:
            for pixel in row:
                bits = str(pixel & 0x01) + bits
                i += 1
                if(i == 8):
                    chars.append(chr(int(bits, 2)))
                    i = 0
                    bits = ''

        f = Fernet(Steganography.__read_file_as_bytes(key))
        decrypted = f.decrypt(''.join(chars).replace("\x00", "").encode())
        return decrypted.decode()


@click.group()
def main():
    pass


@main.command()
def generate_key():
    key = Fernet.generate_key()
    file = open('key.key', 'wb')
    file.write(key)
    file.close()


@main.command()
@click.option('--key', required=True, type=str, help='Key that needs to be used for encryption')
@click.option('--img', required=True, type=str, help='Image that is used to hide data')
@click.option('--file', required=True, type=str, help='Text file which needs to be stored into the image')
@click.option('--output', required=False, type=str, help='Output image name')
def encrypt(key, img, file, output):
    filename, file_extension = os.path.splitext(img)
    encrypted_image = Steganography.encrypt(key, img, file)
    cv2.imwrite(output + file_extension if output is not None and len(output) > 0 else "output" + file_extension, encrypted_image)


@main.command()
@click.option('--key', required=True, type=str, help='Key that used during encryption')
@click.option('--img', required=True, type=str, help='Image that has the data stored')
@click.option('--file', required=True, type=str, help='Output file name with extension')
def decrypt(key, img, file):
    decrypted_text = Steganography.decrypt(key, img)
    Steganography.write_file(file, decrypted_text)


if __name__ == '__main__':
    main()
