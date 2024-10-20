    import os
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    from PIL import Image

    # Convert message to binary
    def message_to_bin(message):
        print("binary message: ",''.join(format(ord(char), '08b') for char in message))
        return ''.join(format(ord(char), '08b') for char in message)

    # Convert binary to message
    def bin_to_message(binary_message):
        chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
        return ''.join(chr(int(char, 2)) for char in chars)

    # Encode the message into the image
    def encode_message(image_path, message, output_image_path):
        img = Image.open(image_path)
        img = img.convert('RGB')
        pixels = img.load()

        bin_message = message_to_bin(message) + '11111111'  # Adding the marker 11111111 at the end
        print("binary message: ",bin_message)
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

    # Decode the message from the image
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

                if bin_message[-8:]== '11111111' and len(bin_message)%8==0 :  # Check for the marker
                    return bin_to_message(bin_message[:-8])  # Remove the marker and convert to text

        return "No message found"

    # Main function
    def main():
        # Hide the Tkinter root window
        Tk().withdraw()

        # Prompt the user to select the image file
        print("Please select the image file you want to use:")
        image_path = askopenfilename(filetypes=[("PNG files", "*.png")])

        if not image_path:
            print("No image selected. Exiting...")
            return

        # Prompt the user to enter the secret message
        secret_message = input("Enter the secret message you want to hide: ")

        # Define the output image path in the same directory as the script
        output_image_path = os.path.join(os.getcwd(), 'encoded_image.png')

        # Encode the message into the image
        encode_result = encode_message(image_path, secret_message, output_image_path)
        print(encode_result)

        # Decode the message to verify encoding
        decoded_message = decode_message(output_image_path)
        print("Decoded message:", decoded_message)

    if __name__ == "__main__":
        main()
