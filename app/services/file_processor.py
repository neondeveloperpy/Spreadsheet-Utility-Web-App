import pandas as pd
from pathlib import Path
import uuid

# Processes Excel and CSV files
# needed by file modificatio functions 

def load_dataframe(file): 
    if isinstance(file, Path): # To process a temp file path or an actual uploaded file
        filename = file.name
        source = file

    else:
        filename = file.filename
        source = file.file


    if filename.endswith(".csv"):
        return pd.read_csv(source)

    elif filename.endswith(".xlsx"):
        return pd.read_excel(source)

    else:
        raise ValueError("Unsupported file type")


async def save_uploaded_file(file):
    extension = Path(file.filename).suffix
    temp_filename = f"{uuid.uuid4().hex}.{extension}"
    temp_path = Path("temp") / temp_filename
    temp_path.parent.mkdir(exist_ok=True)
    
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())

    return temp_path