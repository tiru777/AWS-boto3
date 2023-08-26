import boto3
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ses_client = boto3.client('ses')


def create_email():
    """
    After run this file and verify in your email box
    """
    response = ses_client.verify_email_address(
        EmailAddress='thirumalareddy797@gmail.com'
    )

    return response


def list_identify():
    response = ses_client.list_identities(
        IdentityType='EmailAddress'
    )

    return response['Identities']


def email_create_template():
    response = ses_client.create_template(
        Template={
            'TemplateName': 'GurudevaTemplate',
            'SubjectPart': 'Welcome to the course',
            'TextPart': 'Thanks for buying the course',
            'HtmlPart': 'Thanks for buying the course'
        }
    )

    return response


def get_email_template():
    """
    response = ses_client.get_template(
        TemplateName='CustomTemplate'
    )

    pprint(response['Template'])
    """

    response = ses_client.list_templates()
    return response


def delete_email_template():
    response = ses_client.delete_template(
        TemplateName='GurudevaTemplate'
    )
    return response


def send_email():
    resp = ses_client.send_templated_email(
        Source='thirumalareddy797@gmail.com',
        Destination={
            'ToAddresses': ['thirumalareddy797@gmail.com', 'thirumalareddy1111@outlook.com'],
            'CcAddresses': ['thirumalareddy797@gmail.com']
        },
        ReplyToAddresses=['thirumalareddy797@gmail.com'],
        Template='GurudevaTemplate',
        TemplateData='{"replace":"value"}'
    )

    return resp


CHARSET = 'UTF-8'
destination_address = {
    "ToAddresses": [
        "thirumalareddy797@gmail.com",
        "thirumalareddy1111@outlook.com"
    ]
}
source = "thirumalareddy797@gmail.com"
plain_txt_message = {
    "Body": {
        "Text": {
            "Charset": CHARSET,
            "Data": "Thanks for sending this the course"
        }
    },
    "Subject": {
        "Charset": CHARSET,
        "Data": "AWS Course with Python & Boto3"
    }
}


def send_plain_text_or_html_without_template(destination, message, source_address):
    response = ses_client.send_email(
        Destination=destination,
        Message=message,
        Source=source_address
    )

    return response


def send_html_code_without_template():
    html_email_content = """
            <html>
                <head></head>
                <h1 style='text_align:center'>AWS with Python & Boto3</h1>
                <p style='color:red'>Welcome to the course and thanks for buying the course</p>
            </html>

        """
    plain_html_message = {
        "Body": {
            "Html": {
                "Charset": CHARSET,
                "Data": html_email_content
            }
        },
        "Subject": {
            "Charset": CHARSET,
            "Data": "AWS Course with Python & Boto3"
        }
    }
    response = send_plain_text_or_html_without_template(destination_address, plain_html_message, source)
    return response


def send_attachment_simple_email():

        msg = MIMEMultipart()

        msg["Subject"] = "This is python with aws learning"
        msg["From"] = "thirumalareddy797@gmail.com"
        msg["To"] = "thirumalareddy1111@outlook.com"

        body = MIMEText("Aws with Python & Boto3, Thanks for buying the course")
        msg.attach(body)

        filename = "tiru resume.pdf"

        with open(filename, "rb") as f:
            part = MIMEApplication(f.read())
            part.add_header("Content-Disposition",
                            "attachment",
                            filename=filename)

        msg.attach(part)

        response = ses_client.send_raw_email(
            Source="thirumalareddy797@gmail.com",
            Destinations=['thirumalareddy1111@outlook.com'],
            RawMessage={"Data": msg.as_string()}

        )

        return response


# print(create_email())
# print(list_identify())
# print(email_create_template())
# print(get_email_template())
# print(delete_email_template())
# print(send_email())
# print(send_plain_text_or_html_without_template(destination_address, plain_txt_message, source))
# print(send_html_code_without_template())
# print(send_attachment_simple_email())
