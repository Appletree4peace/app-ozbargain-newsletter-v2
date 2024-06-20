from module_gmail_sender.gmail_sender import GmailSender
import os

def main():
    # read the message
    sender = GmailSender(os.path.join(os.path.dirname(__file__), 'gcp-svc-acc-key-gmail.json'))
    regex_str = 'OzBargain'
    messages = sender.list_messages('admin@cloudelivery.com.au', fr'{regex_str}', 10)
    message = sender.get_message('admin@cloudelivery.com.au', messages[0]['id'])

    # dump to output.html file
    output_file_path = os.path.join(os.path.dirname(__file__), 'publish', 'output.html')
    with open(output_file_path, 'w') as f:
        f.write(message)

if __name__ == '__main__':
    main()