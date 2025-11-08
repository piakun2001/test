import qrcode
import pandas as pd
import os

# Read the CSV file
df = pd.read_csv('test_program.csv')  # Replace 'your_file.csv' with your CSV file name

# Create output directory if it doesn't exist
if not os.path.exists('qr_codes'):
    os.makedirs('qr_codes')

# Generate QR code for each row in the CSV
for index, row in df.iterrows():
    # Convert row data to string
    data = str(row.to_dict())
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to QR code
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image from QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image
    qr_image.save(f'qr_codes/qr_code_{index}.png')

print("QR codes have been generated successfully!")