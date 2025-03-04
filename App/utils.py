from PIL import Image, ImageFilter

def remove_watermark(image_path, watermark_area):
    # Open the image
    image = Image.open(image_path)
    
    # Crop the watermark area (assuming it's a rectangle)
    cropped_area = image.crop(watermark_area)
    
    # Apply a blur filter to the watermark area
    blurred_area = cropped_area.filter(ImageFilter.GaussianBlur(10))
    
    # Paste the blurred area back into the image
    image.paste(blurred_area, watermark_area)
    
    # Save the new image
    image.save("image_without_watermark.jpg")
