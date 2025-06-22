from agents import Agent, Runner ,set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
import os 
import chainlit as cl
from readmail import retrive
from dotenv import load_dotenv
from sendmil import save_mem,load_mem,send_mail
load_dotenv()
# enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
apikey = os.getenv("GEMINI_API_kEY")
Model = "gemini/gemini-2.0-flash"


greet = Agent(
    name = "greeting_agent",
    instructions="You generate polite, professional replies to a single email. Use information from memory if relevant. Return the draft reply as a string.",
    model= LitellmModel(model=Model, api_key=apikey),
    tools= [load_mem]
)
know = Agent(
    name = "knowledge_agent",
    instructions="Identify important user information in the email content and save it for future use using the save_mem tool.",
    model= LitellmModel(model=Model, api_key=apikey),
    tools= [save_mem]
)

mail = Agent(
    name = "mail_processing",
    instructions="Retrieve one unread email at a time and return its summary. If no emails remain, return 'No more emails'. Use the load_email tool if applicable, or fetch new emails.",
    model= LitellmModel(model=Model, api_key=apikey),
    tools= [retrive]
)
sen = Agent(
    name = "send_mail",
    instructions="Send the reply to the email using the send_mail tool after user approval. Return confirmation of the sent email.",
    model= LitellmModel(model=Model, api_key=apikey),
    tools= [send_mail]
)

Fagent = Agent(
    name = "frontend",
    instructions="""
You're the orchestrator agent managing the email response flow, processing one email at a time until no emails remain:

1. Call `mail_processing_agent` to fetch one unread email summary.
   - If the response is 'No more emails', stop and return 'All emails processed'.

2. If an email is retrieved:
   - Pass the email summary to `knowledge_agent` to extract and save any important information.
   - Pass the email summary to `greeting_agent` to generate a professional draft reply.

3. Present the draft reply to the user and ask:
   - "Do you want to tweak this draft reply? (Reply with 'yes' to provide changes, 'no' to proceed, or 'skip' to skip this email.)"

4. Handle user input:
   - If 'yes', accept the user's modified reply and store it as the final draft.
   - If 'no', use the original draft from `greeting_agent` as the final draft.
   - If 'skip', skip sending this email and proceed to the next email.

5. If not skipped, ask the user:
   - "Should I send this reply now? (Reply with 'yes' or 'no'.)"

6. Handle sending:
   - If 'yes', call `send_agent` to send the final reply.
   - If 'no', skip sending and proceed to the next email.

7. Repeat from step 1 until no more emails are available.

Return the status of each email processed (e.g., 'Email 1 sent', 'Email 1 skipped', 'All emails processed').

Note: Since this is a text-based interaction, assume user input will be provided sequentially for each prompt. Store the current email's state (e.g., draft reply, user input) temporarily to proceed correctly.
""",
    model= LitellmModel(model=Model, api_key=apikey),
    tools =[
        mail.as_tool(
            tool_name="mail_processing_agent",
            tool_description="Agent that retrieves one unread email."
        ),
        greet.as_tool(
            tool_name="greeting_agent",
            tool_description="Agent that drafts a professional reply for a single email."
        ),
        know.as_tool(
            tool_name="knowledge_agent",
            tool_description="Agent that stores user information found in emails for reuse."
        ),
        sen.as_tool(
            tool_name="send_agent",
            tool_description="Agent that sends the final reply after user confirmation."
        )

    ]

)
@cl.on_chat_start
async def hadle():
    cl.user_session.set("history",[])
    await cl.Message("hello jee....").send()

@cl.on_message
async def main(messa:cl.Message):
    history = cl.user_session.get("history")
    history.append({"role":"user","content":messa.content})
    result = await Runner.run(
    Fagent,
    input= history)
    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)
    await cl.Message(result.final_output).send()
