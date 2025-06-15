from simplegmail import Gmail
from simplegmail.query import construct_query

gmail = Gmail() 

query_params_1 = {
    "newer_than": (2, "day"),
    "unread": True,
    "labels":"unread"
}

messages = gmail.get_messages(query=construct_query(query_params_1))

for message in messages:
    print("message sender", message.sender)
    print("message subject", message.subject)  
    print("message date", message.date) 
    print("message userid", message.user_id) 
    print("message snippet", message.snippet) 
    print("message plain", message.plain) 

    with open("email.txt","a") as f :
        if message.plain:
            if len(message.plain) < 10000:
                f.write(message.sender +"\n"+"subject"+ message.subject+"\n"+ "plain text "+ message.plain)


