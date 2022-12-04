from openpyxl import load_workbook
from datetime import datetime


def make_excel(path) -> None:
    filename: str = path.split("/")[-1]  # exract filename from path
    wb = load_workbook("TempTemplate.xlsx")
    ws = wb.active
    # ws.title = filename
    datum: list[int] = [int(x) for x in filename.split("-")]
    with open(path, "r") as f:
        for i, line in enumerate(f):
            if i != 0:
                for j, item in enumerate(line.split(";")):
                    if j == 0:
                        kdy: list[int] = [int(x) for x in item.split(":")]
                        ws.cell(row=i + 1, column=j + 1, value=datetime(*datum, *kdy))  # type: ignore # nevím, prostě se tomu něco nelíbí
                    elif j == 1:
                        ws.cell(
                            row=i + 1, column=j + 1, value=float(item.replace(",", "."))
                        )
    wb.save(f"{path}.xlsx")


if __name__ == "__main__":
    make_excel("WIP/2022-12-04")
