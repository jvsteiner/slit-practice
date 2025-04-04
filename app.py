import streamlit as st
import tempfile
import os
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

st.set_page_config(
    page_title="PDF to Markdown Converter", page_icon="📄", layout="wide"
)

st.title("PDF to Markdown Converter")
st.markdown("Upload a PDF file to convert it to Markdown format.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Converting PDF to Markdown..."):
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".pdf"
        ) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            # Initialize the PDFConverter
            converter = PdfConverter(artifact_dict=create_model_dict())

            # Convert PDF to Markdown
            rendered = converter(tmp_file_path)
            markdown_text, _, _ = text_from_rendered(rendered)

            # Display the markdown output
            st.subheader("Markdown Output")
            st.text_area("Markdown", markdown_text, height=400)

            # Provide a download button for the markdown
            st.download_button(
                label="Download Markdown",
                data=markdown_text,
                file_name=f"{uploaded_file.name.split('.')[0]}.md",
                mime="text/markdown",
            )

            # Display preview of the markdown
            st.subheader("Markdown Preview")
            st.markdown(markdown_text)

        except Exception as e:
            st.error(f"Error converting PDF: {str(e)}")
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
else:
    st.info("Please upload a PDF file to begin conversion.")

st.markdown("---")
st.markdown("Powered by Marker.pdf | Created with Streamlit")
