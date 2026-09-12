from fasthtml.common import * 
from app.components.layout import Layout
from app.components.tool_page import ToolPage
from app.components.shared import UploadBox
from app.components.shared import PrimaryButton
from app.services.file_processor import load_dataframe
from app.services.file_output import save_dataframe
from app.dataframes.cleaners import remove_empty_columns_func
from app.services.file_processor import save_uploaded_file
from app.components.layout import DataTable
from app.components.file_info import FileInfo
from app.components.tookworkspcae import ToolWorkSpace
from app.components.tool_controls import ToolControls
from pathlib import Path


def register_routes(rt): 

    @rt("/remove-empty-columns", methods=["GET"])
    def remove_empty_columns():

        return Layout(
        
                ToolPage(
        
                    "Remove Empty Columns",
        
                    "Remove empty columns from your spreadsheet.",

                    Div(
                    UploadBox(
                        PrimaryButton("Upload"),

                        accept=".csv,.xlsx", 
                        action="/remove-empty-columns",
                        method="post",
                        hx_post="/remove-empty-columns",
                        hx_target="#tool-workspace",
                        hx_swap="innerHTML",
                        ),
                    id="tool-workspace"
                    )
                )
            )

    @rt("/remove-empty-columns", methods=["POST"])
    async def remove_empty_columns_post(request):

        form = await request.form()

        file = form["file"]

        if not file:
            return "No file uploaded"

        temp_path = await save_uploaded_file(file)

        df = load_dataframe(temp_path)

        file.file.seek(0, 2) 
        size = file.file.tell()              
        file.file.seek(0)

        return ToolWorkSpace(

            FileInfo(
                filename=file.filename,
                rows=len(df),
                columns=len(df.columns),
                size=f"{size/ 1024:.1f} KB"
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
                    H3("Ready to Clean",
                        cls="font-semibold text-gray-900!"
                    ),

                    P(
                    "Remove empty columns from your file.",
                    cls="text-sm text-gray-500 mt-1!"
                    )
                ),
                        
                    Form(
                    Button("Remove Empty Columns", 
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
                    action="/remove-empty-columns/convert"
                    )   
                )
        )



    @rt("/remove-empty-columns/convert", methods=["POST"])
    async def remove_empty_columns_convert(request):

        form = await request.form()
        
        temp_file = form["temp_file"]

        df = load_dataframe(Path(temp_file))
        
        df = remove_empty_columns_func(df)

        output_path = save_dataframe(
                    df,
                    Path(temp_file).name,
                    output_format=Path(temp_file).suffix[1:],
                    operation="cleaned"
        
                )
        
        return FileResponse(
                    output_path, 
                    filename=f"cleaned_{output_path.name}"
                )