from fasthtml.common import * 

def Loading(message="Processing..."):

    return Div(

        P(message),

        cls="!text-center py-8"

    )