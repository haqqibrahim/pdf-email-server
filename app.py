from flask import Flask, render_template, request
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
import requests

app = Flask(__name__)

EXPRESS_SERVER_URL = 'http://localhost:3000'  # Replace with your Express server URL

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Extract data from the form
    full_name = request.form['full_name']
    email = request.form['email']
    receiver_email = request.form['receiver_email']
    address = request.form['address']

    # Generate PDF
    pdf_filename = f'{full_name}_info.pdf'
    pdf_path = generate_pdf_file(full_name, email, receiver_email, address, pdf_filename)

    # Send PDF to Express server
    send_pdf_to_express(receiver_email, pdf_path)

    return f'PDF generated successfully and sent to Express server.'

def generate_pdf_file(full_name, email, receiver_email, address, filename):
    pdf_path = os.path.join('static', filename)  # Save PDF in the 'static' folder
    
    # Create a PDF document
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
    story = []

    # Add title
    title_style = ParagraphStyle(
        'Title',
        parent=getSampleStyleSheet()['Title'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.blue,
    )
    title = Paragraph("Personal Information", title_style)
    story.append(title)
    story.append(Spacer(1, 12))

    # Add content
    content_style = ParagraphStyle(
        'BodyText',
        parent=getSampleStyleSheet()['BodyText'],
        fontSize=12,
        textColor=colors.black,
    )
    content = Paragraph(
        f"Full Name: {full_name}<br/>"
        f"Email: {email}<br/>"
        f"Receiver Email: {receiver_email}<br/>"
        f"Address: {address}",
        content_style
    )
    story.append(content)

    # Build the PDF document
    pdf.build(story)
    
    return pdf_path

def send_pdf_to_express(receiver_email, pdf_path):
    # Prepare the files to be sent
    files = {'pdf': open(pdf_path, 'rb')}

    # Make a POST request to the Express server
    response = requests.post(f'{EXPRESS_SERVER_URL}/send-email-with-attachment', data={'email': receiver_email}, files=files)

    # Print the response from the Express server (for debugging)
    print(response.text)

if __name__ == '__main__':
    app.run(debug=True)
