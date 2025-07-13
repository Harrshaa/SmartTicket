# format_tickets.py

from extract_pdf import extract_text_from_pdf
import re

def split_tickets(raw_text):
    return re.split(r"\bit_ticket_number\s*:", raw_text)[1:]  # skip header

def parse_ticket_block(block):
    fields = {}
    current_key = None
    lines = block.strip().split('\n')

    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip().lower()
         
            value = value.strip()
            fields[key] = value
            current_key = key
        elif current_key and line.strip():
            # Handle multiline field values
            fields[current_key] += " " + line.strip()

    return fields


def format_for_embedding(fields):
    title = fields.get("title", "")
    summary = fields.get("generalized_request_summary", "")
    request = fields.get("request_details", "")
    resolution = fields.get("resolution_or_rootcause", "")
    return f"Title: {title}\nSummary: {summary}\nRequest: {request}\nResolution: {resolution}"

if __name__ == "__main__":
    text = extract_text_from_pdf("Salesforce_tickets_Agentforce.pdf")
    blocks = split_tickets(text)
    print(f"Extracted {len(blocks)} tickets")

    for i, block in enumerate(blocks[:2]):  # Show first 2 tickets
        data = parse_ticket_block(block)
        chunk = format_for_embedding(data)
        print(f"\n--- Ticket {i+1} ---\n{chunk}")
