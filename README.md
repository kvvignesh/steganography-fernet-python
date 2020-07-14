# steganography-fernet-python

## Usage

Create a `virtualenv` and install the requirements:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, encrypt and decrypt your data with:

```
python steganography.py encrypt --key=key.key --img=input.png --file=README.md
python steganography.py decrypt --key=key.key --img=output.png --file=output.txt
```

To generate a key use the below command:

```
python steganography.py generate-key
```

## Steganography

Let’s understand what is steganography, digital images, pixels, and color models.

### What is steganography?

> [Steganography](https://en.wikipedia.org/wiki/Steganography) is the practice of concealing a file, message, image, or video within another file, message, image, or video.

### What is the advantage of steganography over cryptography?
> The advantage of steganography over [cryptography](https://en.wikipedia.org/wiki/Cryptography) alone is that the intended secret message does not attract attention to itself as an object of scrutiny. Plainly visible encrypted messages, no matter how unbreakable they are, arouse interest and may in themselves be incriminating in countries in which [encryption](https://en.wikipedia.org/wiki/Encryption) is illegal.

In other words, steganography is more discreet than cryptography when we want to send a secret information. On the other hand, the hidden message is easier to extract.


**You can check out the result in the following image**:

The below image is the original image used for the encrypting the data and storing into it

<p align="center"><img src="https://github.com/kvvignesh/steganography-fernet-python/raw/master/input.png" width="400" /> </p>

Below is the image where the data is stored in its pixel

<p align="center"><img src="https://github.com/kvvignesh/steganography-fernet-python/raw/master/output.png" width="400" /> </p>

As you can see in the image above, you can't find any difference between the both the images

## Limitations
- This program will **ONLY** work with PNG images. JPEG images have a specific compression issue that screws with the encryption algorithim.
- You can only encrypt a specific amount of characters within an image. The exact amount is based off the size of the image (one pixel is dedicated to each character).
- Currently, if you try with the color image the output will be a Black and White image.

If you want to try with color images, please visit [steganography-crypto](https://github.com/kvvignesh/steganography-crypto)


Licensing
------------------------
Please see the file named [LICENSE.md](LICENSE.md).
