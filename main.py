import csv
import pandas as pd

fileToParseName = "DD'24 EXTENDED EXCOM.xlsx"

fileToParse = pd.ExcelFile(fileToParseName)

sheetToParseArray = fileToParse.parse(fileToParse.sheet_names[0]).to_numpy()

generalCompetitionsHeadData = {
    "Sketching Competition": ["", "Areeba", "21K-4855", "0332 2301088"],
    "Calligraphy Competition": ["", "Kashmala", "21K-3579", "0331 2316078"],
    "Speed Typing Competition": ["", "Saleha", "21K-4918", "0301 3367064"],
    "Reels Competition": ["", "Rafay Akbar", "21K-4766", "0319 8337338"],
    "Origami Competition": ["", "Arooba", "22K-4083", "0333 3462501"],
}

generalHeadData = ["", "Syed Abdul Rehman", "21K-3156", "0335-3278656"]
generalCoHeadData = ["", "Jahanzaib", "21K-3361", "0332 0272311"]


def getHeadDetails(competitionName):
    for line in sheetToParseArray:
        if (
            str(line[4]).lower().strip() == "head"
            and str(line[0]).lower().lstrip().rstrip()
            == competitionName.lower().lstrip().rstrip()
        ):
            return line

    # if not found in other competitions, look in general
    for competition in generalCompetitionsHeadData.keys():
        if (
            str(competition).lower().lstrip().rstrip()
            == str(competitionName).lower().lstrip().rstrip()
        ):
            return generalCompetitionsHeadData[competition]

    return generalHeadData


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
            return []

    # if not found in other competitions, look in general
    for competition in generalCompetitionsHeadData.keys():
        if (
            str(competition).lower().lstrip().rstrip()
            == str(competitionName).lower().lstrip().rstrip()
        ):
            return []

    # if there is no head in generals for the competition, return general co head
    return generalCoHeadData


def getMailFromID(id):
    id = str(id)

    year = id.split("-")[0][:-1]
    letter = id.split("-")[0][-1].lower()
    rollNum = id.split("-")[1]

    mail = f"{letter}{year}{rollNum}@nu.edu.pk"

    return mail


oldParticipantsDataFileName = "filtered_participants_data.csv"
newParticipantsDataFileName = "participants_with_heads_data.csv"

dataAsList = []

with open(oldParticipantsDataFileName) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        dataAsList.append(row)
        line_count += 1

# Set headings
dataAsList[0].append("Head_name")
dataAsList[0].append("Head_id")
dataAsList[0].append("Head_email")
dataAsList[0].append("Head_number")
dataAsList[0].append("Cohead_name")
dataAsList[0].append("Cohead_id")
dataAsList[0].append("Cohead_email")
dataAsList[0].append("Cohead_number")

for i in range(1, len(dataAsList)):

    # Check for competition name
    competitionName = dataAsList[i][3]

    if competitionName:
        headDetails = getHeadDetails(competitionName)

        if len(headDetails) != 0:
            headName = headDetails[1]
            headId = headDetails[2]
            headMail = getMailFromID(headId)
            headNumber = headDetails[3]

            dataAsList[i].append(headName)
            dataAsList[i].append(headId)
            dataAsList[i].append(headMail)
            dataAsList[i].append(headNumber)

        coHeadDetails = getCoHeadDetails(competitionName)

        if len(coHeadDetails) != 0:
            coHeadName = coHeadDetails[1]
            coHeadId = coHeadDetails[2]
            coHeadMail = getMailFromID(coHeadId)
            coHeadNumber = coHeadDetails[3]

            dataAsList[i].append(coHeadName)
            dataAsList[i].append(coHeadId)
            dataAsList[i].append(coHeadMail)
            dataAsList[i].append(coHeadNumber)

for i in range(len(dataAsList)):
    for j in range(len(dataAsList[i])):
        if str(dataAsList[i][j]).lstrip().rstrip() == "nan":
            dataAsList[i][j] = ""


with open(newParticipantsDataFileName, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(dataAsList)
