import streamlit as st
import fal_client
import os
import base64

# --- THE APP INTERFACE ---
st.set_page_config(page_title="Joseph's Design Partner", layout="centered")
st.title("Architectural AI Partner")
st.markdown("Upload a SketchUp massing to generate a high-end proposal.")

# 1. API Key Input
api_key = st.text_input("Enter Fal.ai API Key:", type="password")

# 2. File Uploader
uploaded_file = st.file_uploader("Upload 3D Massing (JPEG/PNG)", type=["jpg", "jpeg", "png"])

# 3. Design Prompt
prompt = st.text_area("Design Style:", value="Modern tropical architecture, dusk lighting, warm wood and concrete, hyperrealistic, high-end residential photography")

# --- THE ENGINE ---
if st.button("Generate Proposal"):
    if not api_key:
        st.warning("Please enter your API key first.")
    elif uploaded_file is None:
        st.warning("Please upload an image.")
    else:
        st.info("The cloud is rendering... Your Acer laptop is resting.")
        os.environ["FAL_KEY"] = api_key
        
        # Format the image for the cloud
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode('utf-8')
        image_uri = f"data:image/jpeg;base64,{base64_str}"
        
        try:
            # Using the verified 2026 Canny model ID
            result = fal_client.subscribe(
                "fal-ai/flux-lora-canny",
                arguments={
                    "prompt": prompt,
                    "image_url": image_uri,
                }
            )
            
            if 'image' in result:
                st.success("Generation Complete!")
                st.image(result['image']['url'], caption="AI Generated Proposal")
            elif 'images' in result:
                st.success("Generation Complete!")
                st.image(result['images'][0]['url'], caption="AI Generated Proposal")
            else:
                st.error("No image found. Check output below.")
                st.write(result)
            
        except Exception as e:
            st.error(f"Engine Error: {e}")
