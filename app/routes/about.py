from fasthtml.common import *
from app.components.layout import Layout



def register_routes(rt):

    @rt("/about")
    def about():

       return Layout(

    H1("About TabulaFlow"),

    P("TabulaFlow is a free collection of spreadsheet utilities."),

    H2("Our Mission"),

    P("Make spreadsheet tools accessible to everyone."), 

    H2("Why we built it?"), 

    P("Because I felt like it"),

    H3("Our GitHub"), 
      
    H3("Support the Project"),

)