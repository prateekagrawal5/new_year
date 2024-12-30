import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Predefined image path (You can replace it with your own image path)
PREDEFINED_IMAGE_PATH = "NYFS.jpg"
DATA_TYPE_PATH = "Montserrat-Regular.ttf"

def add_name_to_image(image_path, first_name, middle_name, last_name):
    # Open the image
    image = Image.open(image_path)
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Define the font (ensure Montserrat font file is in your directory)
    font = ImageFont.truetype(DATA_TYPE_PATH, 60)
    
    # Concatenate the full name
    full_name = f"{first_name} {middle_name} {last_name}"
    
    # Get the size of the image
    image_width, image_height = image.size
    
    # Calculate the bounding box of the text
    text_bbox = draw.textbbox((0, 0), full_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate the text position to center it
    text_x = (image_width - text_width) // 2
    text_y = 710
    text_position = (text_x, text_y)
    
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Adjust for more boldness if needed
    for offset in offsets:
        draw.text((text_position[0] + offset[0], text_position[1] + offset[1]),
                  full_name, fill="White", font=font)
    # # Add text to the image
    # draw.text(text_position, full_name, fill="White", font=font)
    
    return image


# Streamlit App
st.title("Create & download your personalized New Year Greeting Card")

# Collect user input for the name
st.subheader("Enter Your Name")
first_name = st.text_input("First Name", placeholder="Enter your first name")
middle_name = st.text_input("Middle Name", placeholder="Enter your middle name")
last_name = st.text_input("Last Name", placeholder="Enter your last name")

if st.button("Generate Greeting"):
    if first_name and last_name:  # Ensure at least first and last name are provided
        # Generate the personalized image
        personalized_image = add_name_to_image(
            PREDEFINED_IMAGE_PATH, first_name, middle_name, last_name
        )
        
        # Display the image
        st.image(personalized_image, caption="Your Personalized New Year Greeting)
        
        # Convert image to bytes for download
        img_byte_arr = io.BytesIO()
        personalized_image.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()
        
        # Provide a download link
        st.download_button(
            label="Download Image",
            data=img_byte_arr,
            file_name="personalized_image.png",
            mime="image/png",
        )
    else:
        st.error("Please enter at least your first and last name.")
