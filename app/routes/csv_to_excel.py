from fasthtml.common import * 
from app.components.layout import Layout
from app.components.tool_page import ToolPage
from app.components.shared import UploadBox
from app.components.shared import PrimaryButton
from app.dataframes.converters import csv_to_excel_func # no longer in use 
from app.services.file_output import save_dataframe
from app.services.file_processor import load_dataframe
from app.services.file_processor import save_uploaded_file
from app.components.layout import DataTable
from app.components.file_info import FileInfo
from app.components.tookworkspcae import ToolWorkSpace
from app.components.tool_controls import ToolControls
import pandas as pd
from pathlib import Path
import uuid

def register_routes(rt):

    @rt("/csv-to-excel", methods=["GET"])
    def csv_to_excel():

        return Layout(

        ToolPage(
            "CSV to EXCEL", 
            "Convert CSV Files into EXCEL Files", 


        Div(
            UploadBox(
                PrimaryButton("Upload"),


                accept=".csv",
                action="/csv-to-excel",
                method="post",
                hx_post="/csv-to-excel",
                hx_target="#tool-workspace",
                hx_swap="innerHTML",

                    ), 
                id="tool-workspace"
                ) 
            )  
        )

    @rt("/csv-to-excel", methods=["POST"])
    async def csv_to_excel_post(request):

        form = await request.form()

        file = form["file"] # Represents the saved uploaded file 

        temp_path = await save_uploaded_file(file) # Represents the temporary file created to store the uploaded file

        df = load_dataframe(temp_path)

        # Get file size 
        file.file.seek(0, 2) 
        size = file.file.tell()               
        file.file.seek(0)

        return ToolWorkSpace(

                FileInfo(
                    filename=file.filename,
                    rows=len(df),
                    columns=len(df.columns),
                    size=f"{size / 1024:.1f} KB"
                ),

                Div(

                H3("Preview",
                   cls="text-lg font-semibold text-gray-900 mb-3"),

                
                DataTable(df),

                    cls=(
                        "bg-white border border-gray-200 "
                        "rounded-xl p-5 shadow-sm")
                                                                  

                ),


                ToolControls(
                    Div(
                    H3("Ready to Convert",
                       cls="font-semibold text-gray-900!"
                       ),
                    P(
                        "Convert your CSV file to Excel.",
                        cls="text-sm text-gray-500 mt-1!"
                    )
                ),
                    

                Div(
                Form(
                PrimaryButton("Convert to Excel"),

                Input(
                type="hidden",
                name="temp_file",
                value=str(temp_path)
                ),

                method="post",
                action="/csv-to-excel/convert",
                cls="m-0!"
                ),
                    cls="shrink-0"
                    )
                )
            )
        


    @rt("/csv-to-excel/convert", methods=["POST"])
    async def csv_to_excel_convert(request):
        form = await request.form()

        temp_file = form["temp_file"]
        
        df = load_dataframe(Path(temp_file))

        output_path = save_dataframe(
            df,
            Path(temp_file).name,
            output_format="xlsx",
            operation="converted"
                )

        return FileResponse(
            output_path,
            filename=output_path.name
        )

