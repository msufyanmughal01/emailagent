from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
import os 
from readmail import retrive
from dotenv import load_dotenv
load_dotenv()
set_tracing_disabled(disabled=True)
apikey = os.getenv("GEMINI_API_kEY")
Model = "gemini/gemini-2.0-flash"
Fagent = Agent(
    name = "assitant",
    instructions="you are the helpful agent",
    model= LitellmModel(model=Model, api_key=apikey),
    tools=[retrive]
)

result = Runner.run_sync(
    Fagent,
    f"retrieve emails from the last 2 days and is the eroor occured print the exect error ",
)
print(result.final_output)