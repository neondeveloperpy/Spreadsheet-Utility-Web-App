from fasthtml.common import * 


def Section(*content):

    return Div(

        *content,

        cls="!max-w-6xl mx-auto py-12"

    )