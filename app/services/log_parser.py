import pandas as pd
from app.constants import KEYWORDS


def file_transformation(file_content: bytes) -> str:
    full_text = file_content.decode("utf-8")
    return clean_log(full_text)


def clean_log(full_text: str) -> str:
    df = pd.DataFrame(full_text.splitlines(), columns=["log_info"])
    filtered_df = df[df["log_info"].str.contains(KEYWORDS, case=False, na=False)]
    clean_text = "\n".join(filtered_df["log_info"].to_list())

    if clean_text:
        return clean_text
    else:
        return None
