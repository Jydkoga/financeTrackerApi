import cv2
import pytesseract
import json
from PIL import Image


def extract_receipt_text(image_path):
    """
    Parses the image at the given path and extracts text using OCR.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        dict: A dictionary containing the extracted text.
    """
    try:
        # Load the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to read.")

        # Convert the image to RGB format for PIL
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # threshold to improve OCR accuracy
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Use pytesseract to extract text from the image
        raw_text = pytesseract.image_to_string(thresh)

        # Return the raw text 
        return raw_text
    
    except Exception as e:
        return {"error": str(e)}
    

def parse_receipt_text(raw_text):
    lines = raw_text.strip().split('\n')
    items = []
    total = None

    for line in lines:
        print(f"Processing line: {line.strip()}")
        if not line.strip():
            continue
        if "total" in line.lower():
            print(f"Processing total line: {line.strip()}")
            if "subtotal" in line.lower() or "tax" in line.lower():
                print(f"Skipping line: {line.strip()}")
            else:
              # Attempt to extract the total amount from the line
              try:
                  print(f"Extracting total from line: {line.strip()}")
                  total = float(''.join(c for c in line if c.isdigit() or c == '.' or c == '-'))
              except:
                  print(f"Could not extract total from line: {line.strip()}")
                  pass
        elif any(char.isdigit() for char in line):
            parts = line.split()
            name = ' '.join(parts[:-1])
            try:
                price = float(parts[-1])
                items.append({"item": name, "price": price})
            except:
                continue

    return {
        "items": items,
        "total": total
    }

def save_to_json(data, filename='receipt.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

image_path = 'receipt.jpg'  # Change to your receipt image path
text = extract_receipt_text(image_path)
structured_data = parse_receipt_text(text)
save_to_json(structured_data)

print("Extracted JSON:")
print(json.dumps(structured_data, indent=2))

