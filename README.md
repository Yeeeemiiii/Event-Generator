Written by Yẹmí

# ICS Event Generator with Embedded PDF

A local Python tool to generate an `.ics` calendar file with a fully embedded PDF attachment (encoded in Base64). 

This script is highly useful for generating event tickets that you want to send directly to iOS users. When sent via iMessage, Apple Calendar parses the embedded Base64 PDF perfectly, showing the event details and the ticket natively in a single tap.

### 📝 Features
* Converts any PDF into an inline Base64 attachment.
* Automatically handles iCalendar strict line-folding requirements (RFC 5545).
* Escapes commas in location data to prevent parsing errors.
* Generates unique event UIDs automatically.

### 🚀 Usage

1. Clone this repository to your local machine.
2. Place the PDF you want to embed (e.g., `sample_ticket.pdf`) in the root directory.
3. Open `generate_ics.py` and modify the variables at the bottom of the script under the **Configuration & Execution** section:
    ```python
    INPUT_PDF = 'sample_ticket.pdf'
    OUTPUT_ICS = 'event_invite.ics'

    EVENT_INFO = {
        'summary': 'Your Event Title',
        'dtstart': 'YYYYMMDDThhmmss', 
        'dtend': 'YYYYMMDDThhmmss',
        'location': 'Event Location',
        'description': 'Event Description'
    }
    ```
4. Run the script:
    ```bash
    python3 generate_ics.py
    ```
5. An `.ics` file will be generated in your directory. You can drop this file directly into iMessage or an email client to send to your recipients.

### ⚠️ Compatibility Note
While valid under the iCalendar specification, many web-based calendars (like Google Calendar) and some Outlook versions silently strip Base64 inline attachments due to size. This tool is best utilized for direct-to-device delivery (like sending via iMessage to an iPhone/Mac). 

---
Written by Yẹmí
