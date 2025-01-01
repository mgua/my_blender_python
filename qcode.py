#! python
# this code generates qrcodes 
# as a test it saves a simple file
#
# install requirements
# python -m pip install qrcode[pip]


import qrcode
from io import BytesIO

def generate_qr_bytes(data):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Create a bytes buffer
    buffer = BytesIO()
    
    # Save the image to the buffer in PNG format
    qr_image.save(buffer, format='PNG')
    
    # Get the bytes from the buffer
    image_bytes = buffer.getvalue()
    
    return image_bytes

# Example usage
if __name__ == "__main__":
    data_to_encode = "https://marco.guardigli.it"
    qr_bytes = generate_qr_bytes(data_to_encode)
    
    # Example: To verify the bytes were created
    print(f"QR code generated! Byte array length: {len(qr_bytes)} bytes")
    
    # Example: If you need to save the bytes to a file later
    output_file=r"C:\Users\mgua\my_blender_4.3\qrcode.png"  # r is to avoid backslash escaping role
    with open(output_file, 'wb') as f:
        f.write(qr_bytes)


