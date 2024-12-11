import streamlit as st
from PyPDF2 import PdfReader
from llama_index import SimpleVectorStoreIndex, Document

# Function to extract text from a PDF
def extract_text_with_page_numbers(pdf_path):
    """Extract text from PDF with page numbers."""
    reader = PdfReader(pdf_path)
    page_text = {}
    for i, page in enumerate(reader.pages):
        page_text[i + 1] = page.extract_text()
    return page_text

# Function to build the index
def build_index(page_text):
    """Build a searchable index from extracted text."""
    documents = [Document(f"Page {page_number}: {text}") for page_number, text in page_text.items()]
    index = SimpleVectorStoreIndex.from_documents(documents)
    return index

# Function to query the index
def answer_question(index, question):
    """Query the index and return an answer."""
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return response

# Streamlit app interface
def main():
    st.title("Mahabharata Chatbot 📖")
    st.write("Upload the Mahabharata PDF, and ask any question. I'll provide the answer and the page number!")

    # Upload the PDF file
    pdf_file = st.file_uploader("Upload the Mahabharata PDF", type=["pdf"])
    if pdf_file is not None:
        # Extract text and build the index
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_text_with_page_numbers(pdf_file)
            index = build_index(pdf_text)
            st.success("PDF processed successfully! You can now ask questions.")

        # Ask questions
        question = st.text_input("Enter your question:")
        if st.button("Ask"):
            with st.spinner("Searching for an answer..."):
                response = answer_question(index, question)
                st.write(response)

if __name__ == "__main__":
    main()
