import streamlit as st
import fal_client
import os
import base64

st.set_page_config(page_title="Design Partner", layout="centered")
st.title("Joseph's Architectural AI")
st.markdown("Upload a SketchUp massing to generate a high-end proposal.")

api_key = st.text_input("Enter Fal.ai API Key:", type="password")
uploaded_file = st.file_uploader("Upload 3D Massing (JPEG/PNG)", type=["jpg", "jpeg", "png"])
prompt = st.text_area("Design Style:", value="Modern tropical architecture, dusk lighting, warm wood and concrete, hyperrealistic")

if st.button("Generate Proposal"):
    if not api_key:
        st.warning("Please enter your API key.")
    elif uploaded_file is None:
        st.warning("Please upload an image.")
    else:
        st.info("The cloud is rendering...")
        os.environ["FAL_KEY"] = api_key
        
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode('utf-8')
        image_uri = f"data:image/jpeg;base64,{base64_str}"
        
        try:
            # Using the most stable, single-purpose model for SketchUp lines
            result = fal_client.run(
                "fal-ai/t2i-adapter-sdxl-canny",
                arguments={
                    "prompt": prompt,
                    "image_url": image_uri,
                    "guidance_scale": 7.5,
                    "adapter_condition_scale": 0.8
                }
            )
            
            if 'images' in result and len(result['images']) > 0:
                st.success("Success!")
                st.image(result['images'][0]['url'])
            else:
                st.error("No image returned.")
                st.write(result)
                
        except Exception as e:
            st.error(f"Error: {e}")
