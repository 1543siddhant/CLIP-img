import streamlit as st
import cv2
import google.generativeai as genai
import tempfile

# Configure Google Gemini API
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit App
def main():
    st.set_page_config(page_title="Video Description Generation with Gemini")
    st.title("Video Description Generation with Gemini")

    # Video file uploader
    video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

    # Text input for the prompt
    prompt = st.text_input("Enter your description prompt (e.g., 'Provide a summary of the events in this video'):")

    if video_file is not None and prompt:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(video_file.read())
            video_path = temp_file.name

        # Extract video details
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            st.error("Error: Could not open video.")
            return

        # Get video details (resolution, duration, etc.)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = f"{width}x{height}"

        # Display video information
        st.write(f"Video Resolution: {resolution}")
        st.write(f"Video Duration: {duration:.2f} seconds")
        st.write(f"Frames: {frame_count}, FPS: {fps:.2f}")

        cap.release()

        # Perform the description generation using Gemini API
        with st.spinner("Generating video description..."):
            try:
                # Upload video file to Gemini
                video = genai.upload_file(video_path)

                # Generate description
                response = gemini_model.generate_content([video, prompt])
                video_description = response.text

                # Display the generated description
                st.success("Video Description Generated!")
                st.write("### Video Description:")
                st.write(video_description)

            except Exception as e:
                st.error(f"Error generating video description: {e}")

if __name__ == "__main__":
    main()
