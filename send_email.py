# send_email.py - sends the email with the quote
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
import configparser
import time
import datetime
import get_quote


def email():
    config_path = Path(__file__).parent / "../quote_emailer/config.ini"
    log_path = Path(__file__).parent / "../quote_emailer/send_email.log"
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    config = configparser.ConfigParser()
    config.read_file(open(config_path))
    config_dict = dict(config.items('email_params'))

    subject = 'Quote of the Day'
    # body of email
    body_text = f'Quote of the Day:\r\n {get_quote.start()}'
    # HTML body of email
    body_html = f'''
    <html>
    <head></head>
    <body>
      <h1>Quote of the Day:</h1>
      <p>{get_quote.start()}</p>
    </body>
    </html>
                '''
    # Create SES resource
    client = boto3.client('ses', region_name=config_dict['region'])
    # send the email
    try:
        # Body of email
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    config_dict['recipient'],
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': config_dict['charset'],
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': config_dict['charset'],
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': config_dict['charset'],
                    'Data': subject,
                },
            },
            Source=config_dict['sender'],
        )
    # Errors
    except ClientError as e:
        with open(log_path, 'a') as log_file:
            log_file.write(f"\n\n{timestamp} {e.response['Error']['Message']}")
    else:
        with open(log_path, 'a') as log_file:
            log_file.write(f"{timestamp} Email sent! Recipient: "
                           f"{config_dict['recipient']} "
                           f"Message ID:\n{response['MessageId']}"
                           f"\n\n")


if __name__ == '__main__':
    email()
