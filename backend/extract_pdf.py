# extract_pdf.py
import PyPDF2

def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        print(f"PDF has {len(reader.pages)} pages")
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":
    pdf_path = "Salesforce_tickets_Agentforce.pdf"  # replace with your path
    full_text = extract_text_from_pdf(pdf_path)
    print(full_text[:1000])  # Preview first 1000 characters
