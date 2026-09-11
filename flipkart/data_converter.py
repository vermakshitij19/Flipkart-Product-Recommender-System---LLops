import os
import pandas as pd
from langchain_core.documents import Document


class DataConverter:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def verify(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(
                f"File not found: {self.file_path}"
            )

        if not self.file_path.endswith(".csv"):
            raise ValueError("File must be a CSV file")

    def convert(self):

        # Verify file
        self.verify()

        # Read CSV
        df = pd.read_csv(self.file_path)

        # Verify required columns
        required_columns = ["product_title", "review"]

        for column in required_columns:
            if column not in df.columns:
                raise ValueError(
                    f"Required column '{column}' not found in CSV"
                )

        # Select required columns
        df = df[required_columns]

        # Convert rows into LangChain Documents
        docs = [
            Document(
                page_content=str(row["review"]),
                metadata={
                    "product_name": str(row["product_title"])
                }
            )
            for _, row in df.iterrows()
        ]

        return docs