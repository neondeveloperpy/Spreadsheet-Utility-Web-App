from app.components.layout import Layout
from app.components.shared import PrimaryButton
from fasthtml.common import *

def register_routes(rt):

    @rt("/not-found")
    def not_found():

       return Layout(

        H1("404"),

        P("Page not found."),

        PrimaryButton("Go Home")

)