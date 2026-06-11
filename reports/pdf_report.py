import sqlite3
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

DB_PATH = "data/waste_management.db"

def generate_report():

    conn = sqlite3.connect(
        DB_PATH
    )

    df = pd.read_sql(
        "SELECT * FROM waste_data",
        conn
    )

    conn.close()

    pdf = SimpleDocTemplate(
        "outputs/Waste_Report.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Smart Waste Management Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1,20)
    )

    content.append(
        Paragraph(
            f"Total Records: {len(df)}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Average Fill: {round(df['fill_percentage'].mean(),2)}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Maximum Fill: {round(df['fill_percentage'].max(),2)}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Total Alerts: {len(df[df['alert']=='YES'])}",
            styles["Normal"]
        )
    )

    pdf.build(content)

    print(
        "PDF Report Generated"
    )

if __name__ == "__main__":
    generate_report()