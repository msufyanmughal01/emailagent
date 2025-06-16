from simplegmail.query import construct_query
from agents import function_tool

@function_tool
def retrive(time:int,unit:str):
    """
    Retrieve recent unread emails.

    Parameters:
    - time (int): How many time units back to search (e.g., 2).
    - unit (str): The unit of time (e.g., 'day', 'hour', 'minute').

    Example:
    retrive(time=2, unit="day")  # gets unread emails from the last 2 days
    """
    from simplegmail import Gmail
    gmail = Gmail() 

    query_params_1 = {
        "newer_than": (time, unit.lower()),
        "unread": True,
        "labels":"unread"
    }

    messages = gmail.get_messages(query=construct_query(query_params_1))
    
    if not messages:
        print("No messages found")
        return "No recent emails found."
    
    email_summarize = []

    for message in messages:
        print("message sender", message.sender)
        print("message subject", message.subject)  
        print("message date", message.date) 
        print("message userid", message.user_id) 
        print("message snippet", message.snippet) 
        print("message plain", message.plain) 
        if len(message.plain) < 10000:
            summery = f"""
message sender: {message.sender}
message date: {message.date}
message subject: {message.subject}
message snippet: {message.snippet}
message plain: {message.plain}
"""
            email_summarize.append(summery)

            with open("email.txt","a", encoding="utf-8") as f :
                    f.write(summery + "\n--\n")
                    print("written in file")
    return "\n".join(email_summarize) or "email not found "



