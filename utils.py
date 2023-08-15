# Utils file for ChatGpt bot


# Libraries
import requests  # Make requests
import json      # Json function
import random    # Random functions
import os        # OS functions
import base64    # Base 64 tolls
import re        # Regular Expression


# Bot token to use
Token = "Your Token"


# Decode and format MIME mail
def Decode_MIME(mime_message: str) -> str:
    """
    Decode base64-encoded parts from a MIME message and remove HTML tags.
    
    Args:
        mime_message (str): The MIME message containing base64-encoded parts.

    Returns:
        str: The decoded and cleaned plain text content extracted from the MIME message.
    """
    
    base64_parts = re.findall(
        r'Content-Type: text/plain; charset=utf-8\r\nContent-Transfer-Encoding: base64\r\n\r\n(.*?)--', 
        mime_message, 
        re.DOTALL
    )


    # Decode base64 and remove HTML tags
    decoded_parts = []
    for part in base64_parts:
        decoded_part = base64.b64decode(part).decode('utf-8', errors='ignore')
        plain_text_part = re.sub(r'<.*?>', '', decoded_part)
        decoded_parts.append(plain_text_part)

    return "\n".join(decoded_parts)
    

# Escape markdown filter
def escape_markdown(string: str) -> str:
    """
    Function to escape markdown syntax
    
    Parameter:
        String to be escaped
    
    Returns:
        Filtered string
    """

    # Return escaped string
    return (
        string.replace("_", "\_").replace("*", "\*").replace("[", "\[")
        .replace("]", "\]").replace("(", "\(").replace(")", "\)")
        .replace("~", "\~").replace(">", "\>").replace("#", "\#")
        .replace("+", "\+").replace("-", "\-").replace("=", "\=")
        .replace("|", "\|").replace("{", "\{").replace("}", "\}")
        .replace(".", "\.").replace("!", "\!").replace(",", "\,")
    )


# Force private chat
def force_private(message: object) -> bool:
    """
    Function to force chat into private chat

    Parameter:
        Message object

    Returns:
        Boolean value
    """

    # Return Boolean statement
    if message.chat.type == "private":
        return True
    
    return False


# Smart random string generator
def Smart_Random_String(length: int) -> str:
    """
    Function to generate Smart random String
    
    Generates a random word string by alternating between 
       consonants and vowels. It uses the random.choice 
       function to randomly select characters from the 
       consonants or vowels strings

    Parameter:
        Length of string
    """
    
    # Initializing Vowels & Consonants 
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    
    # Initializing Random string
    random_string = ""

    # Generating random string
    while len(random_string) < length:

        # Working with Vowels & Consonants 
        if len(random_string) % 2 == 0:
            char = random.choice(consonants)
        else:
            char = random.choice(vowels)
        
        # Adding result to string
        random_string += char
    
    # Return final result
    return random_string[:length]


# Generate Email address
def Generate_Email(message: callable) -> str:
    """
    Function to generate temporary Email

    Generates temporary Email address less then one
       minute with access to Inbox

    Parameter:
        Bot message object (You don't need to pass anything)
    """

    # Error handling
    try:

        # Initializing Username and Password (Not important for user)
        addrs = Smart_Random_String(8)
        paswd = Smart_Random_String(8)

        # Get available domain names
        req1 = requests.get(url="https://api.mail.tm/domains", timeout=10).json()
        res1 = req1
        for key, val in res1.items():
            if key == "hydra:member":
                tmp = res1[key][0]

                # Check the Activity of domain name
                if tmp["isActive"]:
                    account_mail_name = tmp["domain"]

                    # Open user config file and add Email address
                    with open(
                        f"Accounts/{message.from_user.id}/mails/{addrs}@{account_mail_name}",
                        "w",
                    ) as data:
                        data.write(
                            f"account_addrs:\n"
                            f"account_psswd:\n"
                            f"account_token:\n"
                            f"account_creat:\n"
                            f"account_mail_name:{account_mail_name}\n"
                        )

        # Create account for username
        headers = {"Content-type": "application/json"}
        params = {"address": f"{addrs}@{account_mail_name}", "password": paswd}
        
        # Send request to api to create account
        req2 = requests.post(
            url="https://api.mail.tm/accounts", json=params, headers=headers, timeout=10
        )
        res2 = req2.json()

        # Fetch create time
        creat = " ".join(res2["createdAt"].split("T"))

        # Open user config file and add Username, Password and created time
        with open(
            f"Accounts/{message.from_user.id}/mails/{addrs}@{account_mail_name}", "w"
        ) as data:
            data.write(
                f"account_addrs:{addrs}\n"
                f"account_psswd:{paswd}\n"
                f"account_token:\n"
                f"account_creat:{creat}\n"
                f"account_mail_name:{account_mail_name}\n"
            )

        # Get token for Email to access to Mailbox
        req3 = requests.post(
            url="https://api.mail.tm/token", json=params, headers=headers, timeout=10
        )
        res3 = req3.json()
        token = res3["token"]

        # Open user config file and add Token to it
        with open(
            f"Accounts/{message.from_user.id}/mails/{addrs}@{account_mail_name}", "w"
        ) as data:
            data.write(
                f"account_addrs:{addrs}\n"
                f"account_psswd:{paswd}\n"
                f"account_token:{token}\n"
                f"account_creat:{creat}\n"
                f"account_mail_name:{account_mail_name}\n"
            )

        # Return the final result
        return (
            f"You Email Address is created and ready to use\.\nYou can request Inbox from Mail menu by pressing /mail again\.\n\n"
            f"▋`{addrs}@{account_mail_name}`"
        )

    except:
        # Return error message
        return f"An error occurred\! Please try again\."


# Load Mailbox
def Load_Mail_Box(token: str) -> tuple:
    """
    Function to Load mailbox by given Token

    Shows all messages from User Email's mailbox (Attachment are now supported)

    Parameter:
        Token
    """

    # Error handling
    try:

        # Send request to get mailbox
        headers = {"Authorization": f"Bearer {token}"}
        req1 = requests.get(
            url="https://api.mail.tm/messages", headers=headers, timeout=10
        )
        res1 = req1.json()

        # Get total messages
        messages_count = res1["hydra:totalItems"]
        
        # Return False result if mailbox is empty
        if messages_count == 0:
            return False, "Your inbox is empty! Try to fetch inbox again after minutes."
        
        # Otherwise fetch all messages from mailbox
        else:
            inboxes = []
            for message in res1["hydra:member"]:
                # Fetch sender information 
                message_from = (
                    f"From {message['from']['name']}\n{message['from']['address']}\n\n"
                )

                # Fetch subject and set No subject if there is no subject
                try:
                    message_subj = (
                        f"▋{message['subject']}\n"
                        if message["subject"] != ""
                        else "▋No Subject\n"
                    )
                except KeyError:
                    message_subj = f"▋No Subject\n"

                # Fetch message and set Empty message if there is no message
                try:
                    message_intr = Decode_MIME(requests.get(
                        url=f"https://api.mail.tm{message['downloadUrl']}", headers=headers, timeout=10
                    ).text)
                except KeyError:
                    message_intr = f"Message is Empty or could not get message."


                # add result to result list
                inboxes.append(message_from + message_subj + message_intr)
            
            # Return True and results
            return True, inboxes
    
    except:
        # Return False and error message
        return False, f"An error occurred! Please try again."
