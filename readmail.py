from simplegmail.query import construct_query
from agents import function_tool
@function_tool
def retrive(time:int,unit:str):
    """
    Retrieve recent unread emails.

    Parameters:
    - time (int): How many time units back to search (e.g., 2).
    - unit (str): The unit of time (e.g., 'day', 'month', 'year').

    Example:
    retrive(time=2, unit="day")  # gets unread emails from the last 2 days
You are retrieving recent unread emails.

If the user says:
- "check today's emails" → treat as (time=1, unit="day")
- "check this week" or "last 7 days" → treat as (time=7, unit="day")
- "this month" → treat as (time=1, unit="month")

DO NOT ask the user to be specific. Make a smart guess and continue.

Your job:
- Use the time and unit to fetch unread emails.
- Return each email one by one (as a list of summaries).
- Use clear and polite English only.
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
    
    message = messages[0]
    if len(message.plain) < 10000:
            summery = f"""
            EMAIL:
message sender: {message.sender}
message date: {message.date}
message subject: {message.subject}
message snippet: {message.snippet}
message plain: {message.plain.strip()}
            
"""
    # Write to file for record-keeping
            with open("email.txt", "a", encoding="utf-8") as f:
                f.write(summery + "\n++++++++++++++\n")
                print("Written to file")

            return summery

    return "No more emails"