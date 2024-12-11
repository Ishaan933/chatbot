with open("app.py", "w") as f:
    f.write("""
import streamlit as st
from PyPDF2 import PdfReader
from llama_index.indices import GPTVectorStoreIndex
from llama_index import Document

# Extract Text from PDF
def extract_text_with_page_numbers(pdf_path):
    reader = PdfReader(pdf_path)
    page_text = {}
    for i, page in enumerate(reader.pages):
        page_text[i + 1] = page.extract_text()
    return page_text

# Build the Index
def build_index(page_text):
    documents = [Document(f"Page {page_number}: {text}") for page_number, text in page_text.items()]
    index = GPTVectorStoreIndex.from_documents(documents)
    return index

# Answer Questions
def answer_question(index, question):
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return response

def main():
    st.title("Mahabharata Chatbot 📖")
    st.write("Ask any question about the Mahabharata, and I'll provide the answer along with the page number!")

    pdf_file = st.file_uploader("Upload the Mahabharata PDF", type=["pdf"])
    if pdf_file is not None:
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_text_with_page_numbers(pdf_file)
            index = build_index(pdf_text)
            st.success("PDF processed successfully! You can now ask questions.")

        question = st.text_input("Enter your question:")
        if st.button("Ask"):
            with st.spinner("Searching for an answer..."):
                response = answer_question(index, question)
                st.write(response)

if __name__ == "__main__":
    main()
""")
