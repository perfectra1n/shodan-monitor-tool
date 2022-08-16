import yagmail
import questionary
import json

class QuickMailer():
    def __init__(self, to_mail:str):
        self.secrets_items = ["from_email", "from_email_password", "smtp_server", "smtp_port"]
        self.send_email_to = to_mail
        self.load_secrets()


    def send_email(self, subject:str = "Custom Quick Emailer", body="", files:list=[]):

        body = "This is a quick emailer.\n\n"

        self.yag.send(to=self.send_email_to, subject=subject, body=body, files=files)
        return "Email sent!"

    def load_secrets(self):
        """Load the secrets from the secrets.json file
        """

        changed = False

        with open('secrets.json') as f:
            secrets = json.load(f)
        for item in self.secrets_items:
            if item not in secrets:
                secrets[item] = questionary.text(f"Please enter the value for item {item}").ask()
                changed = True
        
        # If the secrets have changed, write them to the file
        if changed:
            self.write_secrets(secrets)

        self.yag = yagmail.SMTP(self.email, self.password, self.smtp_server, self.smtp_port)

    def write_secrets(self, secrets):
        with open('secrets.json', 'w') as f:
            json.dump(secrets, f)