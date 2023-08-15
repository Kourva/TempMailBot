#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# TempMail telegram bot
# Developed by Kourva
# Source code: https://github.com/Kourva/TempMailBot


# Libraries
import telebot                        # Bot API Library
import requests                       # Internet requests
import utils                          # Bot Utilities
import json                           # Json function
import os                             # OS functions
from telebot import types, util       # TeleBot utilities           
from telebot.util import quick_markup # Markup generator
from utils import Generate_Email      # Email generator
from utils import Load_Mail_Box       # Mail box loader


# Connect to bot
# Token placed in utils.py file. You can change it with your token
TempMailBot = telebot.TeleBot(utils.Token)
print(f"The Bot is online (id: {TempMailBot.get_me().id})...")


# Start message handler
@TempMailBot.message_handler(commands=["start", "restart"])
def start_command_handler(message: object) -> None:
    """
    Function   to   handle /start  & /restart  command
    Creates account for user and sends welcome message
    """

    # Search for user account that is exist or not
    if (ufile := f"{message.from_user.id}") in os.listdir("Accounts/"):
            
        # Send welcome back message to user
        TempMailBot.send_chat_action(
            chat_id=message.chat.id, 
            action="typing"
        )
        TempMailBot.reply_to(
            message=message,
            text=f"Welcome Back {message.from_user.first_name}.\nUse /mail for menu!",
        )

    # Continue if user is new member and create account for user
    else:

        # Send welcome message to new user
        TempMailBot.send_chat_action(
            chat_id=message.chat.id, 
            action="typing"
        )
        TempMailBot.reply_to(
            message=message,
            text=f"Welcome Dear {message.from_user.first_name}.\nUse /mail for menu!",
   
        )

        # Initialize user account's files
        os.mkdir(f"Accounts/{ufile}") 
        os.mkdir(f"Accounts/{ufile}/mails/")  # User Mails


# Mail command handler
@TempMailBot.message_handler(commands=["mail"])
def mail_generator_handler(message: object) -> None:
    """
    Function to handle /mail command
    Generates temporary mail with access to mailbox
    Use TempMail button in main menu options to see usage
    """
    
    # Force chat type to private. Skip if user is Owner
    if utils.force_private(message):

        # reply markup
        Markups = quick_markup(
            {
                "📥 New Email": {
                    "callback_data": "NewEmail"
                },
                "📬 Email List": {
                    "callback_data": "EmailList"
                },
                "📩 Email Inbox": {
                    "callback_data": "EMailBoxMenu"
                },
                "📤 Delete Email": {
                    "callback_data": "DelEMailMenu"
                },
                "❌ Close": {
                    "callback_data": "Close"
                },
            },
            row_width=2,
        )

        # Send mail menu to user
        TempMailBot.send_chat_action(
            chat_id=message.chat.id, 
            action="typing"
        )
        mail_menu_msg = TempMailBot.send_message(
            chat_id=message.chat.id,
            text=f"Welcome to mail menu.",
            reply_markup=Markups,
        )


# Callback query handler for buttons used in settings
@TempMailBot.callback_query_handler(func=lambda call: True)
def callback_query(call: object) -> None:
    """
    This function will handle the inline keyboards callback
    Show    results   and    Answer  the  callback  queries
    """
    
    # Initialize the IDs (User ID), (Chat ID), (Message ID)
    try:uid = call.from_user.id 
    except:pass

    try:cid = call.message.chat.id
    except:pass

    try:mid = call.message.message_id
    except:pass

    # Callback handler for Email Generator
    if call.data == "NewEmail":

        # Error handling
        try:
        
            # Answer query
            TempMailBot.answer_callback_query(
                call.id, 
                "Please wait..."
            )

            # Send Generating prompt to user
            new_mail_msg = TempMailBot.send_message(
                chat_id=cid,
                text=f"Generating E\-Mail\.\.\.\nIt can take up to minute\.\n",
                parse_mode="MarkdownV2",
            )
            
            # Fetch the result & send new Email to user
            result = "".join(Generate_Email(call))
            TempMailBot.edit_message_text(
                chat_id=cid,
                text=result,
                message_id=new_mail_msg.message_id,
                parse_mode="MarkdownV2",
                disable_web_page_preview=None,
            )

        except:

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "❌ Could not generate email! try again :(",
                show_alert=True
            )

    # Callback handler for Email list
    elif call.data == "EmailList":

        # Error handling
        try:

            # Create list to store buttons
            keyboard = []
            
            # Fetch all Emails from user account config file
            mails = sorted(os.listdir(f"Accounts/{uid}/mails/"))

            # Make button for each Email
            for mail in mails:
                keyboard.append(
                    [types.InlineKeyboardButton(f"📧 {mail}", callback_data=f"MailInfo_{mail}")],
                )

            # Add Close button
            keyboard.append(
                [types.InlineKeyboardButton("❌ Close", callback_data=f"Close")],
            )
            Markups = types.InlineKeyboardMarkup(keyboard)

            # Send Empty Email message if user don't have Emails
            if len(keyboard) == 1:
                TempMailBot.send_message(
                    chat_id=cid,
                    text="You don't have any Emails yet. Create new one from /mail menu\n\nYou can create Email up to 99.\nDue to Telegram limitation, you can't have more than 100 button in message!",
                    reply_markup=Markups,
                )

            # Otherwise show Email list to user
            else:
                TempMailBot.send_message(
                    chat_id=cid,
                    text="Here is list of your Emails! Click on each to see details.\n\nYou can create Email up to 99.\nDue to Telegram limitation, you can't have more than 100 button in message!",
                    reply_markup=Markups,
                )

            # Show hint prompt to user
            TempMailBot.answer_callback_query(call.id, "Its completely FREE :)")

        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )

    # Callback handler for Email information
    elif call.data.startswith("MailInfo"):

        # Error handling
        try:

            # Get Email ID from argument
            mail = call.data.split("_")[1]

            # Opens Email config file and fetch all information
            with open(f"Accounts/{uid}/mails/{mail}", "r") as data:
                infos = [
                    d.split("\n")[0].split(":", maxsplit=1)[1] for d in data.readlines()
                ]

                # Show information to user
                TempMailBot.answer_callback_query(
                    call.id,
                    f"▋Username: {infos[0]}\n▋Password: {infos[1]}\n▋Token: {infos[2][:20]}...\n▋Created: {infos[3]}\n▋Domain: {infos[4]}",
                    show_alert=True,
                )

        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )

    # Callback to handle Email Box menu
    elif call.data.startswith("EMailBoxMenu"):

        # Error handling
        try:

            # Get lost of Emails and make buttons for each (Sorted)
            keyboard = []
            mails = sorted(os.listdir(f"Accounts/{uid}/mails/"))
            for mail in mails:
                keyboard.append(
                    [types.InlineKeyboardButton(f"📧 {mail}", callback_data=f"EMailBox_{mail}")],
                )
            keyboard.append(
                [types.InlineKeyboardButton("❌ Close", callback_data=f"Close")],
            )
            Markups = types.InlineKeyboardMarkup(keyboard)

            # Send Email list for user to select
            TempMailBot.send_chat_action(
                chat_id=cid, 
                action="typing"
            )
            mailbox_msg = TempMailBot.send_message(
                chat_id=cid,
                text=f"Select Email to get Inbox\. All messages in your inbox will send here\.",
                parse_mode="MarkdownV2",
                reply_markup=Markups,
            )

        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )

    # Callback handler for Email Box results
    elif call.data.startswith("EMailBox_"):

        # Error handling
        try:

            # Get Email ID from argument
            mail = call.data.split("_")[1]
            
            # Open Email config to get Email token
            with open(f"Accounts/{uid}/mails/{mail}", "r") as data:
                
                # Fetch token from Email config
                token = data.readlines()[2].split("\n")[0].split(":", maxsplit=1)[1]
                
                # Fetch condition & Result after getting Email inbox
                cond, result = Load_Mail_Box(token)

                # If condition if false, send error result to user
                if not cond:
                    TempMailBot.answer_callback_query(
                        call.id,
                        result,
                        show_alert=True,
                    )
                    return

                # Otherwise if condition is true, get result
                else:
                    keyboard = []

                    # Send note message about attachments
                    TempMailBot.send_chat_action(
                        chat_id=cid, 
                        action="typing"
                    )
                    TempMailBot.send_message(
                        chat_id=cid,
                        text="Note that attachments are now supported. You can use this mail for simple OTP verification, or link verification",
                        disable_web_page_preview=True,
                    )

                    # Send All messages in User mail inbox
                    for masg in result:
                        TempMailBot.send_chat_action(
                            chat_id=cid, 
                            action="typing"
                        )
                        TempMailBot.send_message(
                            chat_id=cid, 
                            text=masg, 
                            disable_web_page_preview=True
                        )
        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )

    # Callback handler for Email deletion menu
    elif call.data == "DelEMailMenu":

        # Error handling
        try:

            # Show Email list for user to delete (Sorted)
            keyboard = []
            mails = sorted(os.listdir(f"Accounts/{uid}/mails/"))

            # Make button for each Email and add Delete & Cancel options
            for mail in mails:
                keyboard.append(
                    [types.InlineKeyboardButton(f"📧 {mail}", callback_data=f"DeleteMail_{mail}")],
                )
            Markups = types.InlineKeyboardMarkup(keyboard)
            Markups.add(
                (types.InlineKeyboardButton("⚠️ Delete all", callback_data="DelAllMails")),
                (types.InlineKeyboardButton("❌ Close", callback_data="Close")),
                row_width=2,
            )

            # Send the final result to user
            TempMailBot.send_chat_action(
                chat_id=cid, 
                action="typing"
            )
            mailbox_msg = TempMailBot.send_message(
                chat_id=cid,
                text=f"Select Email to Delete\. This action can not be restored so be careful\.",
                parse_mode="MarkdownV2",
                reply_markup=Markups,
            )


        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )

    # Callback handler for Email deletion prompt
    elif call.data.startswith("DeleteMail_"):

        # Error handling
        try:

            # Get Email ID from argument
            mail = call.data.split("_")[1]

            # Generates confirmation buttons
            keyboard = [
                [types.InlineKeyboardButton("⚠️ Delete", callback_data=f"DeleteYes_{mail}")],
                [types.InlineKeyboardButton("❌ Cancel", callback_data=f"DeleteNo_{mail}")],
            ]
            Markups = types.InlineKeyboardMarkup(keyboard)

            # Send confirmation message
            TempMailBot.send_chat_action(
                chat_id=cid, 
                action="typing"
            )
            mailbox_msg = TempMailBot.send_message(
                chat_id=cid,
                text=f"You sure you want delete this Email address?\n\n▋ {utils.escape_markdown(mail)}",
                parse_mode="MarkdownV2",
                reply_markup=Markups,
            )

        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )

    # Callback handler for Email deletion confirmation
    elif call.data.startswith("DeleteYes_"):

        # Error handling
        try:

            # Get Email ID from argument
            mail = call.data.split("_")[1]

            # Remove Email
            try:
                os.remove(f"Accounts/{uid}/mails/{mail}")
            except FileNotFoundError:
                # Send success message to user
                TempMailBot.answer_callback_query(
                    call.id, "You don't have this email!", show_alert=True
                )
            
            # Send success message to user
            TempMailBot.answer_callback_query(
                call.id, "Email removed successfully.", show_alert=True
            )

            # Delete message
            TempMailBot.delete_message(
                chat_id=cid, 
                message_id=mid
            )

        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )


    # Callback handler for Delete cancellation
    elif call.data.startswith("DeleteNo_"):

        # Error handling
        try:
        
            # Send cancellation message to user
            TempMailBot.answer_callback_query(
                call.id, 
                "Operation Cancelled.", 
                show_alert=True
            )
            # Delete message
            TempMailBot.delete_message(
                chat_id=cid, 
                message_id=mid
            )
    
        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )


    # Callback handler for all Email deletion confirm prompt
    elif call.data == "DelAllMails":

        # Error handling
        try:

            # Make confirm buttons
            keyboard = [
                [types.InlineKeyboardButton("⚠️ Delete", callback_data=f"DeleteAll_Yes")],
                [types.InlineKeyboardButton("❌ Cancel", callback_data=f"DeleteNo_")],
            ]
            Markups = types.InlineKeyboardMarkup(keyboard)

            # Send confirmation
            TempMailBot.send_chat_action(
                chat_id=cid, 
                action="typing"
            )
            mailbox_msg = TempMailBot.send_message(
                chat_id=cid,
                text=f"You sure you want delete All Email addresses?",
                parse_mode="MarkdownV2",
                reply_markup=Markups,
            )

        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )

    # Callback handler for all Email deletion confirm
    elif call.data == "DeleteAll_Yes":

        # Error handling
        try:
            
            # Gets Email list in user account and delete all
            for mail in os.listdir(f"Accounts/{uid}/mails/"):
                try:
                    os.remove(f"Accounts/{uid}/mails/{mail}")
                except FileNotFoundError:
                    pass
            
            # Send success message to user
            TempMailBot.answer_callback_query(
                call.id, 
                "All Emails removed successfully.", 
                show_alert=True
            )
            # Delete message
            TempMailBot.delete_message(
                chat_id=cid, 
                message_id=mid
            )
            

        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )

    # Callback handler for Close option
    elif call.data == "Close":


        # Error handling
        try:

            # Delete the message (Close)
            TempMailBot.delete_message(
                chat_id=cid, 
                message_id=mid
            )

        except Exception as e:
            print(e) # Log

            # Show error message
            TempMailBot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )


# Connect to  bot in  infinite polling mode
# Make   bot  connection       non     stop
# Skip      old    messages,  don't  update
if __name__ == "__main__":

    # Error handling 
    try:
        TempMailBot.infinity_polling(
            skip_pending=True, 
            none_stop=True,
        )

    # Except any error
    except: 
        print("Lost connection!")
