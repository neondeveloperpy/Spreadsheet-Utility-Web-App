import pandas as pd 
from pathlib import Path
import uuid 
from io import BytesIO

def csv_to_excel_func(file):

    df = pd.read_csv(file)

    filename = f"{uuid.uuid4()}.xlsx" # Gives each file a unique ID to avoid collisions

    output_path = Path("temp") / filename 

    output_path.parent.mkdir(exist_ok=True)

    df.to_excel(output_path, index=False)

    return output_path

def excel_to_csv_func(file):

    df = pd.read_excel(file)

    filename = f"{uuid.uuid4()}.csv"

    output_path = Path("temp") / filename 
    
    output_path.parent.mkdir(exist_ok=True)

    df.to_csv(output_path, index=False)

    return output_path