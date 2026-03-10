import pandas as pd


def file_transformation(file_content: bytes) -> str:
    full_text = file_content.decode("utf-8")
    return clean_log(full_text)


def clean_log(full_text: str) -> str:
    df = pd.DataFrame(full_text.splitlines(), columns=["lof_info"])
    keywords = "ERROR|CRITICAL|EXCEPTION|FAILED"
    filtered_df = df[df["lof_info"].str.contains(keywords, case=False, na=False)]
    clean_text = "\n".join(filtered_df["log_info"].to_list())

    if clean_text:
        return clean_text
    else:
        return None
