from fasthtml.common import * 

def ToolGrid(*cards):

    return Div(

        *cards,

        cls="!grid grid-cols-3 gap-6"

    )