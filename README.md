# Image Steganography using Least Significant Bit (LSB) in Python

## Table of Contents
1. [Introduction to Steganography](#introduction-to-steganography)
2. [Description](#description)
3. [Features](#features)
4. [Prerequisites](#prerequisites)
5. [How It Works](#how-it-works)
    1. [Converting Message to Binary](#1-converting-message-to-binary)
    2. [Encoding the Message into the Image](#2-encoding-the-message-into-the-image)
    3. [Decoding the Message from the Image](#3-decoding-the-message-from-the-image)
    4. [File Dialog for Image Selection](#4-file-dialog-for-image-selection)
6. [Running the Script](#running-the-script)
7. [Example](#example)
8. [License](#license)

## Introduction to Steganography

**Steganography** is the practice of hiding secret information within a non-suspicious file, message, or image, making it appear normal. Unlike encryption, where the content of the message is scrambled, steganography focuses on keeping the very existence of the message hidden. For example, a simple image could contain a hidden message without altering its visible appearance.

In digital steganography, information is often embedded in image, audio, or video files. A popular method involves modifying the least significant bits (LSB) of the pixel values in an image, which doesn't affect the overall appearance of the image but can store binary data.

This project uses LSB steganography to hide a secret message within the red color channel of a PNG image.

## Description

This Python script allows you to hide a secret message inside a PNG image by manipulating the least significant bit (LSB) of the red channel in each pixel. The encoded message is appended with a marker `11111111` to indicate the end of the message, and the message is retrieved by decoding the LSBs of the red channel from the image.

The script uses Python’s `Pillow` library for image manipulation and `tkinter` to open a file selection dialog for ease of use.

## Features

- **Encode a secret message** into the red component of a PNG image.
- **Marker-based decoding** to identify where the message ends.
- Error handling to ensure only valid binary messages (multiples of 8 bits) are decoded.

## Prerequisites

To run this script, you need to have the following installed:
- Python 3.x
- `Pillow` library for image handling
- `tkinter` for file dialog handling

You can install the required dependencies using:

```bash
pip install Pillow
```

## How It Works

### 1. Converting Message to Binary
The message you wish to hide is converted to its binary representation. Each character is converted to its corresponding 8-bit binary equivalent.

```python
def message_to_bin(message):
    return ''.join(format(ord(char), '08b') for char in message)
```

### 2. Encoding the Message into the Image
- Each pixel's red value is modified by changing its least significant bit (LSB) to represent a bit of the secret message.
- The marker `11111111` is appended to the binary message to signify its end.
- The modified image is saved in the same directory as the script under the name `encoded_image.png`.

```python
def encode_message(image_path, message, output_image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    bin_message = message_to_bin(message) + '11111111'  # Adding the marker 11111111 at the end
    message_len = len(bin_message)
    width, height = img.size
    idx = 0

    for y in range(height):
        for x in range(width):
            if idx < message_len:
                r, g, b = pixels[x, y]
                r_bin = format(r, '08b')  # Convert red component to binary
                r_bin = r_bin[:-1] + bin_message[idx]  # Replace the LSB with the message bit
                r = int(r_bin, 2)
                pixels[x, y] = (r, g, b)
                idx += 1
            else:
                img.save(output_image_path)
                return "Message encoded and saved to " + output_image_path
```

### 3. Decoding the Message from the Image
- The LSBs of the red values in the image are extracted to retrieve the binary message.
- The process stops once the marker `11111111` is detected, ensuring we only extract the secret message.
- The script also ensures that the decoded binary is a multiple of 8 bits to avoid errors.

```python
def decode_message(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    width, height = img.size
    bin_message = ''

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bin_message += format(r, '08b')[-1]  # Get the least significant bit

            if bin_message[-8:]== '11111111' and len(bin_message)%8==0:  # Check for the marker
                return bin_to_message(bin_message[:-8])  # Remove the marker and convert to text
    return "No message found"
```

### 4. File Dialog for Image Selection
The script prompts the user to select an image file (PNG) using `tkinter`'s file dialog.

```python
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()  # Hide the Tkinter root window
image_path = askopenfilename(filetypes=[("PNG files", "*.png")])
```

## Running the Script

1. Clone the repository:
    ```bash
    git clone https://github.com/eng-MohamedFayed/Image-Steganography
    cd Image-Steganography
    ```

2. Install the required dependencies:
    ```bash
    pip install Pillow
    ```

3. Run the script:
    ```bash
    python stegano.py
    ```

4. When prompted:
    - Select a PNG image.
    - Enter the secret message you wish to hide.

5. The output image (`encoded_image.png`) will be saved in the same directory as the script, and the secret message will be automatically decoded to verify successful encoding.

## Example

```
Please select the image file you want to use:
Enter the secret message you want to hide: "hi I am mystique"
Message encoded and saved to encoded_image.png
Decoded message: hi I am mystique
```

## License

This project is licensed under the MIT License.
