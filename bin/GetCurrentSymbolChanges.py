import csv


def getCurrentSymbolCUSIP(symbol,fileLoc):
    currentCusipVal =""
    with open(fileLoc,'r') as csvFile:
        csv_reader = csv.DictReader(csvFile)
        for line in csv_reader:
            symbolValue = line['Symbol'].strip()
            if symbolValue == symbol:
                currentCusipVal = line['CUSIP'].strip()
    csvFile.close()
    return currentCusipVal

def getCurrentSymbolISIN(symbol,fileLoc):
    currentISINVal = ""
    with open(fileLoc, 'r') as csvFile:
        csv_reader = csv.DictReader(csvFile)
        for line in csv_reader:
            symbolValue = line['Symbol'].strip()
            if symbolValue == symbol:
                currentISINVal = line['ISIN'].strip()
    csvFile.close()
    return currentISINVal

def getCurrentSymbolDescription(symbol,fileLoc):
    currentDesc = ""
    with open(fileLoc, 'r') as csvFile:
        csv_reader = csv.DictReader(csvFile)
        for line in csv_reader:
            symbolValue = line['Symbol'].strip()
            if symbolValue == symbol:
                currentDesc = line['Company Name'].strip()
                currentDescUpper = str(currentDesc.upper())
    csvFile.close()
    return currentDescUpper