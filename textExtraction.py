import pdfplumber
from preprocessing import preprocess_text

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # Skip empty pages
                text += page_text.strip() + "\n"
    return text


# Example usage
book1_text = preprocess_text(extract_text_from_pdf("C:/Users/abdul/Downloads/Essential-Orthopaedics-by-Maheshwari.pdf"))
book2_text = preprocess_text(extract_text_from_pdf("C:/Users/abdul/Downloads/2015OKOJ.pdf"))
book3_text = preprocess_text(extract_text_from_pdf("C:/Users/abdul/Downloads/the-orthopaedic-physical-exam.pdf"))
all_text = book1_text + book2_text + book3_text
# Save to a file for later use
with open("combined_books.txt", "w", encoding="utf-8") as file:
    file.write(all_text)
