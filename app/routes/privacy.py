from fasthtml.common import *
from app.components.layout import Layout

def register_routes(rt):

    @rt("/privacy")
    def privacy():

       return Layout(

        H1("Privacy Policy"),

        H2("Your Files Stay Private"),

        H2("No Account Required"),

        H2("No Personal Data Collected")

)