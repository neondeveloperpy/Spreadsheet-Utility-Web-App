from pathlib import Path
import uuid
import pandas as pd


def save_dataframe1(df, original_filename):

    extension = Path(original_filename).suffix.lower()

    filename = f"{uuid.uuid4()}{extension}"

    output_path = Path("temp") / filename

    output_path.parent.mkdir(exist_ok=True)


    if extension == ".csv":

        df.to_csv(
            output_path,
            index=False
        )

    elif extension == ".xlsx":


        df.to_excel(
            output_path,
            index=False
        )

    else:
        raise ValueError("Unsupported format")


    return output_path


def save_dataframe(
    df,
    original_filename,
    output_format,
    operation
):

    original = Path(original_filename)

    stem = original.stem

    unique = uuid.uuid4().hex[:8]

    filename = f"{stem}_{operation}_{unique}.{output_format}"

    output_path = Path("temp") / filename

    output_path.parent.mkdir(parents=True,
                             exist_ok=True)

    if output_format == "csv":

        df.to_csv(
            output_path,
            index=False
        )

    elif output_format == "xlsx":

        df.to_excel(
            output_path,
            index=False
        )

    else:

        raise ValueError("Unsupported output format")

    return output_path