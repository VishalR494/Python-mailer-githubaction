import smtplib
from email.mime.text import MIMEText  # MIMEText is a class that represents the text of the email
from email.mime.multipart import MIMEMultipart  # MIMEMultipart is a class that represents the email message itself
import os

def send_mail(workflow_name, repo_name, workflow_run_id):
    # Email details
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    # Email Message
    subject = f"Workflow {workflow_name} failed for repo {repo_name}"
    body = f"Hi, the workflow {workflow_name} failed for the repo {repo_name}. Please check the log for more details.\n\nMore details: \nRun ID: {workflow_run_id}"

    # Prepare email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the mail server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)  # Log in to the server
        text = msg.as_string()  # Convert the message to a string
        server.sendmail(sender_email, receiver_email, text)  # Send the email
        server.quit()  # Terminate the SMTP session

        print('Email sent successfully')
    except Exception as e:
        print(f'Error: {e}')

# Call the function with environment variables
send_mail(os.getenv('WORKFLOW_NAME'), os.getenv('REPO_NAME'), os.getenv('WORKFLOW_RUN_ID'))
