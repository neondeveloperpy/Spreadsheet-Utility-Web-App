from app.components.layout import Layout
from app.components.tool_page import ToolPage
from app.components.shared import UploadBox
from app.components.shared import PrimaryButton
from app.components.layout import DataTable
from app.components.file_info import FileInfo
from app.services.file_processor import load_dataframe
from app.components.tookworkspcae import ToolWorkSpace
from app.components.tool_controls import ToolControls
from app.services.file_processor import save_uploaded_file
from app.dataframes.transformers import sort_rows_func
from app.services.file_output import save_dataframe
from fasthtml.common import *

def SortRowsControls(df, temp_path, original_filename):
    options = [
        Option(
            str(column),
            value=str(column)
        )
        for column in df.columns
    ]

    return ToolControls(
        Div(
            H3(
                "Sort Rows",
                cls="text-lg font-semibold text-gray-900"
            ),
            P(
                "Choose a column and sort order.",
                cls="text-sm text-gray-500 mt-1"
            )
        ),

        Form(
            Div(
                Div(
                    Label(
                        "Column",
                        cls="text-sm font-medium text-gray-700"
                    ),
                    Select(
                        *options,
                        name="column",
                        cls="w-full!"
                    ),
                    cls="space-y-2"
                ),

                Div(
                    Label(
                        "Order",
                        cls="text-sm font-medium text-gray-700"
                    ),
                    Select(
                        Option(
                            "Ascending",
                            value="ascending",
                            selected=True
                        ),
                        Option(
                            "Descending",
                            value="descending"
                        ),
                        name="order",
                        cls="w-full!"
                    ),
                    cls="space-y-2"
                ),

                cls="grid grid-cols-1 md:grid-cols-2 gap-4"
            ),

            Input(
                type="hidden",
                name="temp_file",
                value=str(temp_path)
            ),

            Input(
                type="hidden",
                name="original_filename",
                value=original_filename
            ),

            Div(
                PrimaryButton("Sort Rows"),
                cls="pt-1"
            ),

            method="post",
            action="/sort-rows/apply",
            hx_post="/sort-rows/apply",
            hx_target="#datatable-preview",
            hx_swap="innerHTML"
        )
    )

def DownloadControls(output_path):
    return Div(
        H3(
            "Your file is ready",
            cls="font-semibold text-gray-900"
        ),
        P(
            "Download the sorted spreadsheet.",
            cls="text-sm text-gray-500 mt-1"
        ),
        Form(
            PrimaryButton("Download File"),
            Input(
                type="hidden",
                name="temp_file",
                value=str(output_path)
            ),
            method="post",
            action="/download"
        ),
        cls="bg-white border border-gray-200 rounded-xl! px-5 py-4 shadow-sm!"
    )

def register_routes(rt):

    @rt("/sort-rows", methods=["GET"])
    def sort_rows():

        return Layout(
        
                ToolPage(
        
                    "Sort Rows",
        
                    "Sort rows in your spreadsheet.",

                    Div(
                    UploadBox(
                        PrimaryButton("Sort Rows"),
                        accept=".csv,.xlsx", 
                        action="/sort-rows",   
                        method="post",
                        hx_post="/sort-rows",
                        hx_target="#tool-workspace",
                        hx_swap="innerHTML"
                    ),
                    id="tool-workspace"
                    )
                )
            )

    @rt("/sort-rows", methods=["POST"])
    async def sort_rows_post(request):

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

        return ToolWorkSpace(

            FileInfo(file.filename,
                     rows=len(df),
                     columns=len(df.columns),
                     size=f"{size / 1024:.1f} KB"
                     ),

            Div(
                H3("Preview",
                    cls="text-lg font-semibold text-gray-900 mb-3"),

                DataTable(df), 

                cls="bg-white border border-gray-200 rounded-xl p-5 shadow-sm!",

                id="datatable-preview"

                ),

                SortRowsControls(
                df,
                temp_path,
                file.filename
                )

            )

    @rt("/sort-rows/apply", methods=["POST"])
    async def sort_rows_apply(request):
        form = await request.form()

        temp_file = form["temp_file"]
        original_filename = form["original_filename"]

        column = form.get("column")
        order = form.get("order")

        if not column:
            return "Please select a column."

        if order not in {"ascending", "descending"}:
            return "Invalid sort order."

        df = load_dataframe(Path(temp_file))

        if column not in df.columns:
            return "Invalid column."

        ascending = order == "ascending"

        df = sort_rows_func(
            df,
            column,
            ascending
        )

        output_path = save_dataframe(
            df,
            original_filename,
            output_format=Path(temp_file).suffix[1:],
            operation="sorted"
        )

        return ToolWorkSpace(
        Div(
            H3(
                "Preview",
                cls="text-lg font-semibold text-gray-900 mb-3"
            ),
            DataTable(df),
            #cls="bg-white border border-gray-200 rounded-xl p-5 shadow-sm!",
        ),

        DownloadControls(
            output_path
        )
        )

    @rt("/download", methods=["POST"])
    async def download(request):
        form = await request.form()

        temp_file = form["temp_file"]
        path = Path(temp_file)

        return FileResponse(
        path,
        filename=path.name
        )
            
        
    