<h1 align="center">
    <img align='left' src="https://github.com/Kourva/TempMailBot/assets/118578799/d2fe9f8c-89ca-436d-bf57-ffc2c67f772c" width=200 height=200/>
    <h2>TempMail Telegram Bot </h2>
  <p><b>Make unlimited emails just in minute with access to mailbox!</b></p>
  <p><i>Usable for <b>Verification</b> codes and messages, <b>support MIME</b>!</i></p>
</h1>

<br><br>

# ▋New Features
+ Support MIME messages (Link verification)
+ Added emoji to buttons.

# ▋Features
Bot creates account for every user joins the bot.
+ **/mail** command to manage your account.
+ **Smart username generator** to generate readable usernames.
+ can **List all mails** and **Show information** for each.
+ can **Delete All/One** email when user don't want email anymore.
+ can **Show all inbox messages** in user email.
+ uses **Inline keyboard** instead of normal keyboard.

each user can have up to **100** mails, because Telegram does't allow us to use more than **100** buttons in each message<br>
Also note that now you can access to attachments (like confirm links) from your mailbox. you can use this for simple **conversation** or **OTP verification** and even **MIME messages**.

<br>

# ▋Clone Repository
To get started, first you need to **clone** this repository from github into your machine:
```bash
git clone https://github.com/Kourva/TempMailBot
```
and if you dont have git you can install it from your package manager!

<br>

# ▋Install Requirements
Then you have to install requirements before running bot
1. Navigate to bot directory
2. Install requirements using pip
```bash
cd TempMailBot
```
```bash
pip install -r requirements.txt
```
This will install **pyTelegamBotAPI** and **Requests** for you

<br>

# ▋Config your token
Now you have to get create bot from [BotFather](https://t.me/BotFather) **(If you don't have)** and take your **Token** to starts working with your bot.<br>
After getting **Token** from **BotFather** replace the Token in `utils.py` in line **12** as follows:
```python
# Bot token to use
Token = "6146793572:AAE7fbH29UPOKzlHlp0YDr9o06o_NdD4DBk"
```
> This is just an example Token. Use yours instead

<br>

# ▋Launch the bot
Now you are ready to launch your bot in polling mode inside your terminal using python
```bash
python main.py
```
You can also use **proxychains** to run your bot via **Tor** proxy
```bash
proxycahins python main.py
```
Or in quiet mode
```bash
proxychains -q python main.py
```
To install proxychains install `proxychains-ng` and then edit the config file in `/etc/proxychains.conf`.<br>
In config file comment the `strict_chain` and un-comment `dynamic_chain` and its ready to use.
<br>

# ▋TOR new IP address
If you got any denied requests that blocked your Ip address, you can renew your IP
```bash
sudo killall -HUP tor
```
<br>

# Thanks <3
> Dont forget to star this repository if you made it helpful!
