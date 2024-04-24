import csv
import pandas as pd

fileToParseName = "DD'24 EXTENDED EXCOM.xlsx"

fileToParse = pd.ExcelFile(fileToParseName)

sheetToParseArray = fileToParse.parse(fileToParse.sheet_names[0]).to_numpy()


def getHeadDetails(competitionName):
    for line in sheetToParseArray:
        if (
            str(line[4]).lower().strip() == "head"
            and str(line[0]).lower().lstrip().rstrip()
            == competitionName.lower().lstrip().rstrip()
        ):
            return line


def getCoHeadDetails(competitionName):
    for i in range(len(sheetToParseArray)):
        line = sheetToParseArray[i]
        # Look for the correct competition group
        if (
            str(line[4]).lower().strip() == "head"
            and str(line[0]).lower().lstrip().rstrip()
            == competitionName.lower().lstrip().rstrip()
        ):
            # Once group found, look for co head
            j = 0
            while str(sheetToParseArray[i + j][4]).lower().lstrip().rstrip() != "":
                if (
                    str(sheetToParseArray[i + j][4]).lower().lstrip().rstrip()
                    == "co head"
                    or str(sheetToParseArray[i + j][4]).lower().lstrip().rstrip()
                    == "co-head"
                ):
                    return sheetToParseArray[i + j]
                j += 1


print(getCoHeadDetails("Seminar"))

# with open("employee_birthday.txt") as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=",")
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             print(
#                 f"\t{row[0]} works in the {row[1]} department, and was born in {row[2]}."
#             )
#             line_count += 1
#     print(f"Processed {line_count} lines.")
