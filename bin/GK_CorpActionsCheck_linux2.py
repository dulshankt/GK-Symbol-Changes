from time import sleep
import os.path
import datetime 
import csv
import shutil
import customLogger
import SeleniumActions
import GetCurrentSymbolChanges
import JiraTicketCreation
import requests
import json
import urllib.request
from urllib import request

#creating a variable for the webhook
slack_webHook_url = 'https://hooks.slack.com/services/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'

#defining logger
logger = customLogger.customLog()
#defining login credentials 
tody = str(datetime.date.today())
todyVals= tody.split("-")
fileName = "{}.txt".format(tody)

yearVal = todyVals[0]
gkChangeCount = 0
today_date = "{}/{}/{}".format(todyVals[1],todyVals[2],todyVals[0])
inputDate = "{}/{}/{}".format(todyVals[1],todyVals[2],todyVals[0])
csvPath="C:\\check GK symbol list\Input\data.csv"
ticketDesc = ''
ticketList = []
attachmentList = []
host = os.environ['host']
jiraName = os.environ['jiraName']
jiraToken = os.environ['jiraToken']
jiraProject = os.environ['jiraProject']
jiraIssue = os.environ['jiraIssue']
jiraTicketAssign = os.environ['jiraAssign']
jiraTicketSummary = "Changing symbol details - {}/{}/{}".format(todyVals[0],todyVals[1],todyVals[2])

#Current Symbol List obtaining methods are in GetCurrentSymbolChanges Module

def downloadSymbolListCsv(csvPath):
    print('Beginning symbol list download with urllib2...')
    jsonUrl = 'http://35.161.168.15:3131/export_symbols?system=parakum'
    resp = request.urlopen(jsonUrl)
    urlInfo = json.load(resp)
    url = urlInfo['details']['url']
    urllib.request.urlretrieve(url, csvPath)
    print("SYMBOL LIST DOWNLOADED!!!!!")


try:
    #get system symbol values
    symbolListFileSelector = input("Consider the symbol list file location as check GK symbol list\Input\data.csv (Y/N) :" ).upper()
    if symbolListFileSelector == 'N':
        logger.info("using data file in different path")
        fileLocVal = input("Enter file location path :")
        csvPath = str(fileLocVal)
    elif symbolListFileSelector == 'Y':
        logger.info("using the recommended data file")
        downloadSymbolListCsv(csvPath)
    else:
        print("Please select from the choices Y/N")
        logger.error("wrong choice - path value!!")
        slack_msg = {'text': 'Error - The user has entered an incorrect argument for file path selection. Program terminated!'}
        requests.post(slack_webHook_url,data=json.dumps(slack_msg))
        exit()
    dateSelector = input("Consider the input date as "+inputDate+" (Y/N) :").upper()
    if dateSelector == 'N':
        logger.info("using custom date value to continue")
        inputDateVal = input("Enter date in mm/dd/yyyy format :")
        inputDate = str(inputDateVal)
    elif dateSelector == 'Y':
        logger.info("using today date")
    else:
        print("Please select from the choices Y/N")
        logger.error("wrong choice - date value!!")
        slack_msg = {'text': 'Error - The user has entered an incorrect argument for date selection. Program terminated!'}
        requests.post(slack_webHook_url,data=json.dumps(slack_msg))
        exit()
    print("Path :"+csvPath)
    logger.info("Path :"+csvPath)
    logger.info("Date :"+inputDate)
    print("Date :"+inputDate)
   
    if os.path.exists(csvPath):
        #fLR = fileLocationRaw.split("\")
        #fileLocationInput = 
        systemSymbols =[]
        #new modifications foc CUSIP to check if the changes have applied properly .. remove if any error occurs 
        systemCUSIPS =[]
        systemISINS = [] 
        systemCompanyDescs = []
        print("correct path")
        logger.info("correct path")
        sleep(5)
        with open(csvPath,'r')as csvFile:
            csv_reader = csv.DictReader(csvFile)
            for line in csv_reader:
                #print(line[1])
                systemSymbols.append(line['Symbol'])
                #new modifications foc CUSIP to check if the changes have applied properly .. remove if any error occurs 
                systemCUSIPS.append(line['CUSIP'])
                systemISINS.append(line['ISIN'])
                systemCompanyDescs.append(line['Company Name'])
        #print(systemSymbols)
        #getting the date as user input
        #inputDate = str(sys.argv[1])
        dateVals = inputDate.split("/")
        if int(dateVals[0]) > 12 or int(dateVals[0]) < 1 or int(dateVals[0])> int(todyVals[1]) or int(dateVals[1]) > 31 or int(dateVals[1]) < 1 or int(dateVals[2]) > int(yearVal) or int(dateVals[2]) < 2010:
            print("Please insert valid date value !!")
            logger.error("The date inserted was wrong, hence the the program stopped")
            slack_msg = {'text': 'Error - The user has entered an incorrect date value. Program terminated!'}
            requests.post(slack_webHook_url,data=json.dumps(slack_msg))
        else:
            gkChangeCount=SeleniumActions.selenium(logger,tody,inputDate,fileName,systemSymbols,GetCurrentSymbolChanges.getCurrentSymbolCUSIP,csvPath,GetCurrentSymbolChanges.getCurrentSymbolISIN,GetCurrentSymbolChanges.getCurrentSymbolDescription,systemCUSIPS,systemISINS,systemCompanyDescs,ticketList,attachmentList,gkChangeCount)


            if gkChangeCount == 0:
                print("No GK Symbol changes for the day so far")
                logger.info("No GK Symbol changes for the day so far")
                slack_msg = {'text': 'INFO - No GK Symbol changes for the day so far!. Program execution successful!'}
                #requests.post(slack_webHook_url,data=json.dumps(slack_msg))
                #jiraTicketID = returnCreatedTicketID(host,jiraName,jiraToken,"Changing symbol details - 2019/09/09")
                #print("JIRA ticket ID :"+jiraTicketID)
            else:
                print("GK Symbol changes are present. Please create a ticket")
                logger.info(" GK Symbol changes are present. Please create a ticket")
                slack_msg = {'text': 'INFO - GK Symbol changes are present and a ticket must be created!. Program execution successful!'}
                requests.post(slack_webHook_url,data=json.dumps(slack_msg))
                #create jira ticket 
                for li in ticketList:
                    ticketDesc = ticketDesc + str(li) + '\n'
                #createJiraTicket(host,jiraName,jiraToken,jiraProject,jiraTicketSummary,ticketDesc,jiraIssue,jiraTicketAssign)
                ifVal = JiraTicketCreation.checkIfTicketExists(host,jiraName,jiraToken,jiraProject,jiraTicketSummary,inputDate,today_date)
                if ifVal:
                    JiraTicketCreation.createJiraTicket(host,jiraName,jiraToken,jiraProject,jiraTicketSummary,ticketDesc,jiraIssue,jiraTicketAssign,attachmentList)
                    jiraTicketID = JiraTicketCreation.returnCreatedTicketID(host,jiraName,jiraToken,jiraProject,jiraTicketSummary)
                    msg = "INFO - Ticket ID is : {}".format(jiraTicketID)
                    print(msg)
                    slack_msg ={'text': msg}
                else:
                    print("Changes a re present! Ticket needs to be updated")
                    JiraTicketCreation.updateTicketIfAvailable(host,jiraName,jiraToken,jiraProject,jiraTicketSummary,ticketDesc)
                    print("Ticket updates were added as a comment")
                print(ifVal)
                
            backupDayVal = "{}-{}-{}".format(dateVals[2],dateVals[0],dateVals[1])
            backupName = "{}.csv".format(backupDayVal)
            backupDataLocation = "C:\\check GK symbol list\Input\\backup\{}".format(backupName)
            print(backupDataLocation)
            with open(backupDataLocation, 'a') as dataCsvBackup:
                shutil.copy(csvPath,backupDataLocation)
                os.remove(csvPath)
            dataCsvBackup.close()
    else:
        print("Please insert correct file Path")
        logger.error("Incorrect file path")
        slack_msg = {'text': 'ERROR - The user has given an incorrect file path /The data.csv file is not available at the specified location. Program terminated!'}
        #requests.post(slack_webHook_url,data=json.dumps(slack_msg))
except Exception as e:
    excValue = "Error :" +str(e) +". Program Terminated!"
    print("Error :" + str(e))
    logger.exception("Error")
   
    slack_msg = {'text': excValue}
    #requests.post(slack_webHook_url,data=json.dumps(slack_msg))
  
#ss = str(r)
#v = driver.find_element_by_xpath("//*[@id='caInfoRow"+ss+"']")
#print(v.text)  
#//*[@id="caInfoRow1"]/td[7]
#executable_path=chrome_driver_path,
#//a[contains(text(),'Search Corporate Actions only')]

