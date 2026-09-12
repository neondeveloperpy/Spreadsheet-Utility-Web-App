from fasthtml.common import * 
from app.components.layout import Layout
from app.components.tool_page import ToolPage
from app.components.shared import UploadBox
from app.components.shared import PrimaryButton
from app.dataframes.converters import excel_to_csv_func
from app.services.file_output import save_dataframe
from app.services.file_processor import save_uploaded_file
from app.services.file_processor import load_dataframe
from app.components.layout import DataTable
from app.components.file_info import FileInfo
from app.components.tookworkspcae import ToolWorkSpace
from app.components.tool_controls import ToolControls
import pandas as pd 

def register_routes(rt): 

    @rt("/excel-to-csv", methods=["GET"])
    def excel_to_csv():

        return Layout(

        ToolPage(
                "EXCEL to CSV",
                "Convert EXCEL workbooks into CSV files",

                Div(
                UploadBox(
                    PrimaryButton("Upload"),

                    accept=".xlsx",
                    action="/excel-to-csv", 
                    method="post",
                    hx_post="/excel-to-csv",
                    hx_target="#tool-workspace",
                    hx_swap="innerHTML",
                    ),
                id="tool-workspace"
                )
            )
        )
    

    @rt("/excel-to-csv", methods=["POST"])
    async def excel_to_csv_post(request): 

        form = await request.form()

        file = form["file"]
        
        if not file:
            return "No file uploaded"

        temp_path = await save_uploaded_file(file)

        df = load_dataframe(temp_path)

        # Get file size 
        file.file.seek(0, 2) 
        size = file.file.tell()              
        file.file.seek(0)

        #df = pd.read_excel(file.file)
        
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

            Form(
            Button("Convert to CSV", 
                    type="submit",
            
                    cls=(
                        "bg-blue-600 hover:bg-blue-700 "
                        "text-white px-4 py-2 rounded-lg!"
                        )
                    ),
            
                    Input(
                    type="hidden",
                    name="temp_file",
                    value=str(temp_path)
                            ),
                    method="post",
                    action="/excel-to-csv/convert"

                        )   
                    )
                )
            

    @rt("/excel-to-csv/convert", methods=["POST"])
    async def excel_to_csv_convert(request): 
        form = await request.form()
        
        temp_file = form["temp_file"]
                
        df = load_dataframe(Path(temp_file))

        output_path = save_dataframe(
            df,
            Path(temp_file).name,
            output_format="csv",
            operation="converted"
                    )
                
        return FileResponse(
            output_path,
            filename=output_path.name
                        )
        
         
    