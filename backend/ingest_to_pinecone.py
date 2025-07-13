from dotenv import load_dotenv
load_dotenv()

import os
print("OPENAI_API_KEY loaded:", os.getenv("OPENAI_API_KEY"))

from extract_pdf import extract_text_from_pdf
from format_tickets import split_tickets, parse_ticket_block
from app.services.embeddings import generate_embedding, upsert_to_pinecone
import time

if __name__ == "__main__":
    # Step 1: Extract ticket text from original PDF
    text = extract_text_from_pdf("Salesforce_tickets_Agentforce.pdf")
    tickets = split_tickets(text)
    print(f"📦 Total tickets to embed: {len(tickets)}")

    # Step 2: Format and upload each ticket
    # Step 2: Process and upload each ticket
for i, block in enumerate(tickets):
    if not block.strip():
        print(f"⏭️ Skipping empty ticket-{i}")
        continue

    fields = parse_ticket_block(block)

    # Skip if 'request_details' is missing or empty
    if not fields.get("request_details", "").strip():
        print(f"⏭️ Skipping ticket-{i} due to missing 'request_details'")
        continue

    # Build content for embedding
    content = f"{fields.get('title', '')}\n{fields.get('request_details', '')}\n{fields.get('resolution_or_rootcause', '')}"

    try:
        embedding = generate_embedding(content)
        ticket_id = fields.get("it_ticket_number", f"ticket-{i}")

        # Upload to Pinecone with metadata
        upsert_to_pinecone(
            ticket_id,
            embedding,
            metadata={
                "ticket_number": ticket_id,
                "project_category": fields.get("project_category", ""),
                "record_type": fields.get("record_type", "")
            }
        )

        print(f"✅ Uploaded {ticket_id}")
        time.sleep(1)  # prevent rate limiting
    except Exception as e:
        print(f"❌ Failed on ticket-{i}: {e}")
