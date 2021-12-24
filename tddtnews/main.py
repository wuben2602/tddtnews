
from emailcreator.emailRender import emailRender
from emailsender.emailSender import emailSender
from tddtgui.app import TDDTGui

import argparse

def publish():
    """ generates newsletter and sends it to the proper addresses.
        This is almost the same as the publish function called by TDDTGui and
        functions as the CLI version of this application

    Raises:
        TDDTEmailException: 
    """
    # get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('template', type=str, help="template to be emailed out")
    parser.add_argument('sendto', nargs='+', type=str, help="email or emails to be sent to ")
    parser.add_argument('-t','--tddt', help = "removes check for tddt.org emails")
    args = parser.parse_args()
    
    # error checking / parsing of emails using simple regex
    for email in args.sendto:
        if not args.tddt:
            try:
                if "@tddt.org" not in email:
                    raise TDDTEmailException(email)
            except TDDTEmailException as e:
                print(e)
                print("Excluding email:" + e.email)
    email_list = ",".join(args.sendto)
    
    # render email
    constructor = emailRender(args.template + ".jinja")
    subject = f"The New Lion Dance Beat. Vol {constructor.volume} No {constructor.number}"
    
    # send email
    sender = emailSender()
    sender.send_message(
        sender.create_message(
            email_list, # comma seperated list of email addresses to send to
            None, # sender - should be none
            subject, # subject
            None, # ccs - should be none
            constructor.render() # html as a string
        )
    )
    
    # update volume and number TODO

def gui():
    tddtgui = TDDTGui()
    tddtgui.start()
    
class TDDTEmailException(Exception):
    
    def __init__(self, email):
        self.email = email
        message = "TDDTEmailException: " + self.email + " doesn't come in the form of email@tddt.org"
        super().__init__(message)
        