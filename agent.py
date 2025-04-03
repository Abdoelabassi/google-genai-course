from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_community.utilities import SerpAPIWrapper
from langchain.chat_models import ChatVertexAI
import os
from dotenv import load_dotenv

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


@tool
def search(query: str):
    """Search the web for a query."""
    search = SerpAPIWrapper()
    return search.run(query)


@tool
def places(query: str):
    """Search for places using Google Places API."""
    places = GooglePlacesTool()
    return places.run(query)


model = ChatVertexAI(model="gemini-2.0-flash-001")
tools = [search, places]
query = "How many goals scored by Real Madrid yesterday during the Copa del Ray, and where was the match played?"

agent = create_react_agent(model, tools)
input = {"message": [("human", query)]}

for s in agent.stream(input, stream_mode="values"):
    message = s["message"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()
