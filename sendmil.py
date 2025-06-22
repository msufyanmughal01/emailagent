from agents import function_tool
import os 
@function_tool
def send_mail(sender:str,to:str,sub:str,msg_plain:str)->str:
    from simplegmail import Gmail

    gmail = Gmail() # will open a browser window to ask you to log in and authenticate
    params = {
    "to": f"{to.lower()}",
    "sender": f"{sender.lower()}",
    "subject": f"{sub}",
    "msg_html": "<h1></h1><br />",
    "msg_plain": f"{msg_plain}",
    "signature": True  # use my account signature
    }
    message = gmail.send_message(**params)
    with open("send_email.txt","a", encoding="utf-8") as f :
        f.write(message.plain + "\n--\n")
        print("written in file")
    return message.plain or "email not send "


@function_tool
def save_mem(TEXT:str):
    """SAVE THE USER INFO IN A FILE THAT IS IMPORTANT YOU THINK THAT WILL USE AGAIN """ 
    with open("userinfo.txt","a") as f :
        f.write(TEXT + "\n--\n")
        print("written in file")

@function_tool
def load_mem():
      """retreive the user relative info that will use in this email"""  
      if not os.path.exists("userinfo.txt"):
          return "not file not found "
      with open("userinfo.txt","r") as f :
          return f.read()
    
@function_tool
def load_email():
      """retreive the email one by one and generate the reply """  
      if not os.path.exists("email.txt"):
          return "not file not found "
      with open("email.txt","r") as f :
          return f.read()    