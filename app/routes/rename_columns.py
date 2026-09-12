from app.components.layout import Layout
from app.components.tool_page import ToolPage
from app.components.shared import UploadBox
from app.components.shared import PrimaryButton
from fasthtml.common import *
from app.services.file_processor import load_dataframe
from app.services.file_output import save_dataframe
from app.dataframes.transformers import rename_columns_func
from app.services.file_processor import save_uploaded_file
from app.components.layout import DataTable
from app.components.file_info import FileInfo
from app.components.tookworkspcae import ToolWorkSpace
from app.components.tool_controls import ToolControls

def RenameColumnsControls(
    df,
    temp_path
):
    inputs = []

    for column in df.columns:
        inputs.append(
            Div(
                Div(
                    Label(
                        "Current Name",
                        cls="text-xs text-gray-500"
                    ),
                    P(
                        str(column),
                        cls="font-medium text-gray-900 truncate"
                    ),
                ),

                Div(
                    Label(
                        "New Name",
                        cls="text-xs text-gray-500"
                    ),
                    Input(
                        type="text",
                        name=f"column_{column}",
                        value=str(column),
                        cls=(
                            "w-full! bg-gray-50 border border-gray-300 "
                            "rounded-lg! px-3 py-2"
                        )
                    ),
                ),

                cls=(
                    "grid grid-cols-1 md:grid-cols-2 "
                    "gap-3 items-center"
                )
            )
        )

    return ToolControls(
        Form(
            H3(
                "Rename Columns",
                cls="text-lg font-semibold text-gray-900 mb-5"
            ),

            Div(
                *inputs,
                cls="space-y-4"
            ),

            Input(
                type="hidden",
                name="temp_file",
                value=str(temp_path)
            ),

            Input(
                type="hidden",
                name="original_filename",
            ),

            Div(
                PrimaryButton("Rename Columns"),
                cls="mt-5"
            ),

            method="post",
            action="/rename-columns/apply",
            hx_post="/rename-columns/apply",
            hx_target="#datatable-preview",
            hx_swap="innerHTML"
        )
    )

def DownloadControls(temp_path):
    return ToolControls(
        Div(
            Div(
                H3(
                    "Your file is ready",
                    cls="font-semibold text-gray-900"
                ),
                P(
                    "Download the updated spreadsheet.",
                    cls="text-sm text-gray-500 mt-1"
                )
            ),

            Form(
                PrimaryButton(
                    "Download File"
                ),

                Input(
                    type="hidden",
                    name="temp_file",
                    value=str(temp_path)
                ),

                method="post",
                action="/download"
            )
        )
    )

def register_routes(rt):

    @rt("/rename-columns", methods=["GET"])
    def rename_columns():

        return Layout(
        
                ToolPage(
        
                    "Rename Columns",
        
                    "Rename Columns in your spreadsheet.",

                    Div(
                    UploadBox(
                        PrimaryButton("Upload"),
                        accept=".csv,.xlsx",
                        action="/rename-columns",
                        method="post",
                        hx_post="/rename-columns",
                        hx_target="#tool-workspace",
                        hx_swap="innerHTML",
                    ),
                    id="tool-workspace"
                )
            )
        )
    
    

    @rt("/rename-columns", methods=["POST"])
    async def rename_columns_post(request):

        form = await request.form()

        file = form["file"]

        if not file:
            return "No file uploaded"

        temp_path = await save_uploaded_file(file)

        df = load_dataframe(Path(temp_path))

        file.file.seek(0, 2) 
        size = file.file.tell()              
        file.file.seek(0)
        
        return ToolWorkSpace(

                FileInfo(
                    file.filename,
                    rows=len(df),
                    columns=len(df.columns),
                    size=f"{size/1024:.1f} KB"
                ),

                Div(
                    H3("Preview",
                       cls="text-lg font-semibold text-gray-900 mb-3"),

                    DataTable(df),

                     cls=(
                        "bg-white border border-gray-200 "
                        "rounded-xl p-5 shadow-sm"),

                    id="datatable-preview"
                ),

                RenameColumnsControls(
                    df,
                    temp_path
                ),

                
        )

    @rt("/rename-columns/apply", methods=["POST"])
    async def rename_columns_apply(request):
        form = await request.form()

        temp_file = form["temp_file"]

        df = load_dataframe(Path(temp_file))

        mapping = {}

        for column in df.columns:
            new_name = form.get(f"column_{column}")

            if new_name:
                mapping[column] = new_name

        df = rename_columns_func(df, mapping)

        output_path = save_dataframe(
        df,
        Path(temp_file).name,
        output_format=Path(temp_file).suffix[1:],
        operation="renamed"
        )

        return Div(
                    H3("Preview",
                    cls="text-lg font-semibold text-gray-900 mb-3"),
        
                    DataTable(df),

                    Div(
                    DownloadControls(output_path),
                    cls="mt-1.5"
                    ),

                    cls="space-x-1"
        
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
