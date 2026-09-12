from fasthtml.common import *
from app.components.layout import Layout

def register_routes(rt):

    @rt("/contact")
    def contact():

       return Layout(

        H1("Contact"),

        P("Need help?"),

        A("GitHub"),

        A("Email")

)