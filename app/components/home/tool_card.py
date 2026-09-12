from fasthtml.common import * 
from app.components.shared import PrimaryButton

def ToolCard(

    title,

    description,

    href,

    icon="📄"

    ):

    return Div(

        H2(icon, 
           cls="text-2xl"),

        H3(title, 
           cls="text-xl text-gray-200"), 

        P(description, 
          cls="text-sm text-blue-200"), 

        A("Open", href=href, 
          cls="mt-4 font-semibold inline-block !bg-blue-600 !hover:bg-blue-500 !text-white px-4 py-2 rounded-md"), 

        cls="""
        border 
        rounded-xl
        p-6
        shadow-sm
        hover:shadow-md
        transition
        """

    )