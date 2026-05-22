import base64
import uuid
from datetime import datetime

def create_ics_with_pdf(pdf_filename, output_filename, event_details):
    """
    Reads a PDF, encodes it to Base64, and embeds it inside an .ics calendar file.
    """
    
    # 1. Read and Encode the PDF
    # Opens the specified PDF in binary reading mode ('rb') and converts it to a Base64 string.
    try:
        with open(pdf_filename, 'rb') as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: Could not find '{pdf_filename}'. Please ensure the file is in the same directory.")
        return

    # 2. Format the Attachment Property
    # iCalendar requires specific formatting for attachments. We define the MIME type and encoding.
    attach_line = f"ATTACH;FMTTYPE=application/pdf;ENCODING=BASE64;VALUE=BINARY:{encoded_string}"

    # 3. Line Folding Function
    # The iCalendar specification (RFC 5545) strictly limits line lengths to 75 characters.
    # This function breaks up the Base64 string and prefixes continuation lines with a space.
    def fold_line(text):
        lines = [text[:75]]
        text = text[75:]
        while text:
            lines.append(' ' + text[:74])
            text = text[74:]
        return '\r\n'.join(lines)

    folded_attachment = fold_line(attach_line)

    # 4. Generate Timestamps and Unique IDs
    # DTSTAMP is the creation time. UID ensures the calendar event is uniquely identified.
    creation_time = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    unique_id = f"event-{uuid.uuid4()}@local"

    # Escape commas in the location string to prevent parsing errors in Apple Calendar / Outlook
    location = event_details.get('location', '').replace(',', '\\,')

    # 5. Construct the ICS Content
    # Assembling the VCALENDAR and VEVENT components with standard \r\n line endings.
    ics_content = (
        f"BEGIN:VCALENDAR\r\n"
        f"VERSION:2.0\r\n"
        f"BEGIN:VEVENT\r\n"
        f"UID:{unique_id}\r\n"
        f"DTSTAMP:{creation_time}\r\n"
        f"DTSTART:{event_details['dtstart']}\r\n"
        f"DTEND:{event_details['dtend']}\r\n"
        f"SUMMARY:{event_details['summary']}\r\n"
        f"LOCATION:{location}\r\n"
        f"DESCRIPTION:{event_details['description']}\r\n"
        f"{folded_attachment}\r\n"
        f"END:VEVENT\r\n"
        f"END:VCALENDAR"
    )

    # 6. Write the File
    # Saves the final string as an .ics file encoded in UTF-8.
    with open(output_filename, 'w', encoding='utf-8', newline='') as f:
        f.write(ics_content)
        
    print(f"Successfully created: {output_filename}")

# ==========================================
# CONFIGURATION & EXECUTION
# ==========================================
if __name__ == "__main__":
    # Define your file paths
    INPUT_PDF = 'sample_ticket.pdf'
    OUTPUT_ICS = 'event_invite.ics'

    # Define your event details
    # Date Format: YYYYMMDDThhmmss (e.g., 20260702T200000)
    EVENT_INFO = {
        'summary': 'Your Event Title Here',
        'dtstart': '20260101T180000',
        'dtend': '20260101T210000',
        'location': 'Event Venue Name, City, Zip',
        'description': 'Description of the event or attached documents.'
    }

    # Run the generator
    create_ics_with_pdf(INPUT_PDF, OUTPUT_ICS, EVENT_INFO)