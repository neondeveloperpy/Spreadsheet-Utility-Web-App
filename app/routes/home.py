from fasthtml.common import *
from app.components.layout import Layout
from app.components.layout import Section 
from app.components.home import Hero 
from app.components.home import ToolGrid 
from app.components.home import ToolCard 
from app.utilis.tool_registry import TOOLS 
from dataclasses import dataclass


@dataclass
class Tool:
    slug: str
    title: str
    description: str
    icon: str
    accept: str
    button: str
    category: str

cards = [
    ToolCard(
        title=tool["title"],
        description=tool["description"],
        href=f'/{tool["slug"]}',
        icon=tool["icon"]
    )
    for tool in TOOLS
]

def register_routes(rt):

    @rt("/")
    def home():

       return Layout(

           Hero(), 

           Section(
               
            H2("Popular Tools", 
               cls="text-2xl font-bold "),

            Br(),

            ToolGrid(*cards)
               
           ), 

           Section(

            H2("Why TabulaFlow?",
               cls="text-2xl font-bold"),

            P("It's Fast.", 
              cls="text-sm text-gray-100 "),

            P("It's Free.", 
              cls="text-sm text-gray-100 "),

            P("It's Privacy Friendly.", 
              cls="text-sm text-gray-100 ")
               
           )
           
       )