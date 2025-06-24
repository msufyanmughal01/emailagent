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
You're the orchestrator agent""",
    model= LitellmModel(model=Model, api_key=apikey),
    tools =[
        mail.as_tool(
            tool_name="mail_processing_agent",
            tool_description="Agent that retrieves unread email."
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

    ])
@cl.on_message
async def main(meas:cl.Message):
    email_runner = await Runner.run(
        Fagent,
        f"check today's email and print the email"
    )
    intial_output = email_runner.final_output
    await cl.Message(f"initial output: {intial_output}").send()
    email_generater = Runner.run(
        Fagent,
        f"generate the reply for this email and print it {intial_output} also print the sender details  and this is the commands {meas.content} the user will be or be not send to you if he want to tweak the reply you generated"
    )
    await cl.Message(f"second output: {email_generater.final_output}").send()


