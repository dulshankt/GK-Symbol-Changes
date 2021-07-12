from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException #new
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os
import os.path

def selenium(logger,tody,inputDate,fileName,systemSymbols,getCurrentSymbolCUSIP,csvPath,getCurrentSymbolISIN,getCurrentSymbolDescription,systemCUSIPS,systemISINS,systemCompanyDescs,ticketList,attachmentList,gkChangeCount):
    # selenium stuff
    usr = os.environ['user_name']
    pwd = os.environ['password']
    domain = os.environ['domain']
    du = "{}\{}".format(domain, usr)
    # open website
    # chrome_driver_path = '/home/ec2-user/checkGKCA/linuxChromeDriver/chromedriver_linux64/chromedriver'
    chrome_opts = Options()
    # chrome_opts.add_argument("--window-size=1920x1080")
    # chrome_opts.add_argument("--headless")
    # driver = webdriver.Chrome(chrome_options=chrome_opts)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://secure.gkis.net/CAEditor/Account/Logon")
    # driver.find_element_by_name('dmn').send_keys(domain)
    driver.find_element_by_name('username').send_keys(du)
    # driver.find_element_by_name('nm').send_keys(usr)
    driver.find_element_by_name('password').send_keys(pwd)
    driver.find_element_by_xpath("/html/body/div/div/form/table/tbody/tr[3]/td/input").click()

    # navigating to corporate actions

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Search Corporate Actions only')]"))
    )
    driver.find_element_by_xpath("//a[contains(text(),'Search Corporate Actions only')]").click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='searchPanelcontent']/ul[2]/li[1]/span"))
    )
    # print(tody)
    logger.info(tody)
    print(inputDate)
    logger.info(inputDate)
    # print(du)
    # print("clicked")
    # print("found")
    # input values and get the GK list
    driver.find_element_by_id('caSearchRequest_EffectiveDateFrom').send_keys(inputDate)
    driver.find_element_by_id('caSearchRequest_EffectiveDateTo').send_keys(inputDate)
    sleep(1)
    driver.find_element_by_id('caSearchRequest_CaFilteredBy').click()
    sleep(1)
    driver.find_element_by_xpath("//option[contains(text(),'Target and New Security')]").click()
    sleep(2)
    driver.find_element_by_id('SearchButton').click()

    element = WebDriverWait(driver, 200).until(
        # EC.presence_of_element_located((By.XPATH,"//*[@id='CAListContent']/table/tbody/tr/td/nobr/a[2]"))
        EC.presence_of_element_located((By.XPATH, "//*[@id='caInfoRow1']/td[8]"))
    )
    driver.maximize_window()
    sleep(2)
    tableVals = driver.find_element_by_id('CaInfoList')
    print(tableVals)
    # logger.info(tableVals)
    sleep(2)
    driver.execute_script("window.scrollBy(0,250)", "")
    sleep(1)

    # getting to click table values
    # //*[@id="caInfoRow1"]
    print("going to print table rows and columns")
    rows = int(len(driver.find_elements_by_xpath("//*[@id='CaInfoList']/tbody/tr")) / 2)
    cols = int(len(driver.find_elements_by_xpath("//*[@id='caInfoRow1']/td")))
    print(rows)
    # logger.info("No of rows :" +rows)
    print(cols)
    # logger.info("No of columns :" +cols)
    sleep(2)
    # file creation
    # Saving the downloaded system symbols for backup
    fileLocation = "C:\\check GK symbol list\\Output\{}\{}".format(tody, fileName)
    folderLocation = "C:\\check GK symbol list\\Output\{}".format(tody)
    if os.path.exists(folderLocation):
        print("Folder already available")
        logger.info("Folder already exists")
    else:
        os.mkdir(folderLocation)
    with open(fileLocation, 'a') as GKCAList:
        print(inputDate + "\n", file=GKCAList)
        # NOGK bool value addition
        noGKVals = True
        # reading the gk list table
        for r in range(1, rows + 1):
            rowNum = str(r)
            for c in range(1, cols + 1):
                if c == 7:
                    noGKVals = True
                    cc = str(c)
                    symbl = str(driver.find_element_by_xpath("//*[@id='caInfoRow" + rowNum + "']/td[7]").text)
                    caType = str(driver.find_element_by_xpath("//*[@id='caInfoRow" + rowNum + "']/td[3]").text)

                    # print(symbl)
                    # print(caType)
                    sleep(1)
                    element = WebDriverWait(driver, 300).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@id='caInfoRow" + rowNum + "']/td[7]"))
                    )
                    invis = WebDriverWait(driver, 300).until(
                        EC.invisibility_of_element_located((By.CLASS_NAME, 'blockUI blockOverlay')))
                    sleep(1)
                    if (invis):
                        driver.find_element_by_xpath("//*[@id='caInfoRow" + rowNum + "']/td[7]").click()
                        sleep(1)
                    element = WebDriverWait(driver, 300).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@id='CaDetailsTable']/tbody/tr[14]/td[2]"))
                    )
                    sleep(3)

                    oldCusip = str(driver.find_element_by_xpath("//*[@id='CaDetailsTable']/tbody/tr[14]/td[2]").text)
                    oldISIN = str(driver.find_element_by_xpath("//*[@id='CaDetailsTable']/tbody/tr[15]/td[2]").text)
                    oldSymbol = str(driver.find_element_by_xpath("//*[@id='CaDetailsTable']/tbody/tr[15]/td[4]").text)
                    oldDesc = str(driver.find_element_by_xpath("//*[@id='CaDetailsTable']/tbody/tr[16]/td[2]").text)
                    if caType == "Reverse/Forward Split" or caType == "Name/CUSIP/Symbol Change" or caType == "Merger" or caType == "Reincorporation/Change of Dom" or caType == "Listing Change":

                        newCusip = str(
                            driver.find_element_by_xpath("//*[@id='newSecurityDetails']/tbody/tr[4]/td[6]").text)
                        newISIN = str(
                            driver.find_element_by_xpath("//*[@id='newSecurityDetails']/tbody/tr[5]/td[4]").text)
                        newSymbol = str(
                            driver.find_element_by_xpath("//*[@id='newSecurityDetails']/tbody/tr[5]/td[6]").text)
                        newDesc = str(
                            driver.find_element_by_xpath("//*[@id='newSecurityDetails']/tbody/tr[6]/td[2]").text)

                        if symbl in systemSymbols or newSymbol in systemSymbols:
                            jiraSymbolVal = ""
                            jiraCUSIPVal = ""
                            jiraISINVal = ""
                            jiraDescVal = ""
                            jiraSym = ""
                            currentSystemCUSIP = ""
                            currentSystemISIN = ""
                            currentSystemDesc = ""
                            if symbl in systemSymbols:
                                print("Symbol : " + symbl)
                                jiraSym = "\n \n Symbol: {} ({})".format(symbl, caType)
                                currentSystemCUSIP = getCurrentSymbolCUSIP(symbl, csvPath)
                                currentSystemISIN = getCurrentSymbolISIN(symbl, csvPath)
                                currentSystemDesc = getCurrentSymbolDescription(symbl, csvPath)
                            if newSymbol in systemSymbols:
                                print("Symbol : " + newSymbol)
                                jiraSym = "\n \n Symbol: {} ({})".format(newSymbol, caType)
                                currentSystemCUSIP = getCurrentSymbolCUSIP(newSymbol, csvPath)
                                currentSystemISIN = getCurrentSymbolISIN(newSymbol, csvPath)
                                currentSystemDesc = getCurrentSymbolDescription(newSymbol, csvPath)
                            if newSymbol not in systemSymbols and newSymbol != symbl:
                                print("Old Symbol: " + symbl + "  New Symbol: " + newSymbol)
                                jiraSymbolVal = "|| Current Symbol || New Symbol ||\n | {} | {} |".format(symbl,
                                                                                                          newSymbol)
                                noGKVals = False
                            if newCusip not in systemCUSIPS and oldCusip != newCusip:
                                print("Old CUSIP: " + currentSystemCUSIP + "  New CUSIP: " + newCusip)
                                jiraCUSIPVal = "|| Current CUSIP || New CUSIP ||\n | {} | {} |".format(
                                    currentSystemCUSIP, newCusip)
                                noGKVals = False
                            if newISIN not in systemISINS and newISIN != oldISIN:
                                print("Old ISIN: " + currentSystemISIN + "  New ISIN: " + newISIN)
                                jiraISINVal = "|| Current ISIN || New ISIN ||\n | {} | {} |".format(currentSystemISIN,
                                                                                                    newISIN)
                                noGKVals = False
                            if newDesc not in systemCompanyDescs:
                                if currentSystemDesc != newDesc:
                                    print("Old Description: " + currentSystemDesc + " New Description: " + newDesc)
                                    jiraDescVal = "|| Current Description || New Description ||\n | {} | {} |".format(
                                        currentSystemDesc, newDesc)
                                    noGKVals = False
                            if noGKVals == False:

                                # print(statement,file=GKCAList)
                                screenshotListVal = folderLocation + "\\" + newSymbol + ".png"
                                screenshotVal = "!" + newSymbol + ".png!"
                                jiraTicketVals = jiraSym + "\n" + jiraSymbolVal + "\n" + jiraCUSIPVal + "\n" + jiraISINVal + "\n" + jiraDescVal + "\n" + screenshotVal + "\n \n"
                                print(jiraTicketVals, file=GKCAList)
                                # add ticketvalue to list and ss to list
                                ticketList.append(jiraTicketVals)
                                attachmentList.append(screenshotListVal)
                                # new modifications for CUSIP to check if the changes have applied properly .. remove if any error occurs

                                # GetScreenshot

                                driver.save_screenshot(folderLocation + "\\" + newSymbol + ".png")

                                element = WebDriverWait(driver, 300).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]"))
                                )
                                invis = WebDriverWait(driver, 300).until(
                                    EC.invisibility_of_element_located((By.CLASS_NAME, 'blockUI blockOverlay')))
                                sleep(1)
                                if (invis):
                                    driver.find_element_by_xpath(
                                        "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]").click()
                                    sleep(1)

                                gkChangeCount = gkChangeCount + 1
                            else:
                                element = WebDriverWait(driver, 300).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]"))
                                )
                                invis = WebDriverWait(driver, 300).until(
                                    EC.invisibility_of_element_located((By.CLASS_NAME, 'blockUI blockOverlay')))
                                sleep(1)
                                if (invis):
                                    driver.find_element_by_xpath(
                                        "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]").click()
                                    sleep(1)



                        else:
                            element = WebDriverWait(driver, 300).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]"))
                            )
                            invis = WebDriverWait(driver, 300).until(
                                EC.invisibility_of_element_located((By.CLASS_NAME, 'blockUI blockOverlay')))
                            sleep(1)
                            if (invis):
                                driver.find_element_by_xpath(
                                    "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]").click()
                                sleep(1)
                    if caType == "Exchange":

                        newCusip = str(
                            driver.find_element_by_xpath("//*[@id='newSecurityDetails']/tbody/tr[5]/td[6]").text)
                        newISIN = str(
                            driver.find_element_by_xpath("//*[@id='newSecurityDetails']/tbody/tr[6]/td[4]").text)
                        newSymbol = str(
                            driver.find_element_by_xpath("//*[@id='newSecurityDetails']/tbody/tr[6]/td[6]").text)
                        newDesc = str(
                            driver.find_element_by_xpath("//*[@id='newSecurityDetails']/tbody/tr[7]/td[2]").text)

                        if symbl in systemSymbols or newSymbol in systemSymbols:
                            # statement = "Symbol value: {}\n Old CUSIP value: {} New CUSIP value: {}\n Old ISIN value: {} New ISIN value: {}\n Old Symbol Value: {} New Symbol value: {}\n Old Description: {} New Description: {} \n \n ".format(symbl,oldCusip,newCusip,oldISIN,newISIN,oldSymbol,newSymbol,oldDesc,newDesc)
                            # jiraTicketVals ="\n \n *Symbol: {}\n || Current Symbol || New Symbol ||\n | {} | {} |\n || Current CUSIP || New CUSIP ||\n | {} | {} |\n || Current ISIN || New ISIN ||\n | {} | {} |\n || Current Description || New Description ||\n | {} | {} | \n \n".format(symbl,oldSymbol,newSymbol,oldCusip,newCusip,oldISIN,newISIN,oldDesc,newDesc)
                            # print(statement)
                            # print(statement,file=GKCAList)
                            # print(jiraTicketVals, file=GKCAList)
                            # new modifications foc CUSIP to check if the changes have applied properly .. remove if any error occurs
                            jiraSymbolVal = ""
                            jiraCUSIPVal = ""
                            jiraISINVal = ""
                            jiraDescVal = ""
                            jiraSym = ""
                            currentSystemCUSIP = ""
                            currentSystemISIN = ""
                            currentSystemDesc = ""

                            if symbl in systemSymbols:
                                print("Symbol: " + symbl)
                                jiraSym = "\n \n Symbol: {} ({})".format(symbl, caType)
                                currentSystemCUSIP = getCurrentSymbolCUSIP(symbl, csvPath)
                                currentSystemISIN = getCurrentSymbolISIN(symbl, csvPath)
                                currentSystemDesc = getCurrentSymbolDescription(symbl, csvPath)
                            if newSymbol in systemSymbols:
                                print("Symbol: " + newSymbol)
                                jiraSym = "\n \n Symbol: {} ({})".format(newSymbol, caType)
                                currentSystemCUSIP = getCurrentSymbolCUSIP(newSymbol, csvPath)
                                currentSystemISIN = getCurrentSymbolISIN(newSymbol, csvPath)
                                currentSystemDesc = getCurrentSymbolDescription(newSymbol, csvPath)
                            if newSymbol not in systemSymbols and newSymbol != symbl:
                                print("Old Symbol: " + symbl + "  New Symbol: " + newSymbol)
                                jiraSymbolVal = "|| Current Symbol || New Symbol ||\n | {} | {} |".format(symbl,
                                                                                                          newSymbol)
                                noGKVals = False
                            if newCusip not in systemCUSIPS and newCusip != oldCusip:
                                print("Old CUSIP: " + currentSystemCUSIP + "  New CUSIP: " + newCusip)
                                jiraCUSIPVal = "|| Current CUSIP || New CUSIP ||\n | {} | {} |".format(
                                    currentSystemCUSIP, newCusip)
                                noGKVals = False
                            if newISIN not in systemISINS and newISIN != oldISIN:
                                print("Old ISIN: " + currentSystemISIN + "  New ISIN: " + newISIN)
                                jiraISINVal = "|| Current ISIN || New ISIN ||\n | {} | {} |".format(currentSystemISIN,
                                                                                                    newISIN)
                                noGKVals = False
                            if newDesc not in systemCompanyDescs:
                                if currentSystemDesc != newDesc:
                                    print("Old Description: " + currentSystemDesc + " New Description: " + newDesc)
                                    jiraDescVal = "|| Current Description || New Description ||\n | {} | {} |".format(
                                        currentSystemDesc, newDesc)
                                    noGKVals = False
                            if noGKVals == False:

                                screenshotListVal = folderLocation + "\\" + newSymbol + ".png"
                                screenshotVal = "!" + newSymbol + ".png!"
                                jiraTicketVals = jiraSym + "\n" + jiraSymbolVal + "\n" + jiraCUSIPVal + "\n" + jiraISINVal + "\n" + jiraDescVal + "\n" + screenshotVal + "\n \n"
                                print(jiraTicketVals, file=GKCAList)
                                # add ticketvalue to list
                                ticketList.append(jiraTicketVals)
                                attachmentList.append(screenshotListVal)
                                # GetScreenshot
                                driver.save_screenshot(folderLocation + "\\" + newSymbol + ".png")

                                element = WebDriverWait(driver, 300).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]"))
                                )
                                invis = WebDriverWait(driver, 300).until(
                                    EC.invisibility_of_element_located((By.CLASS_NAME, 'blockUI blockOverlay')))
                                sleep(1)
                                if (invis):
                                    driver.find_element_by_xpath(
                                        "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]").click()
                                    sleep(1)

                                gkChangeCount = gkChangeCount + 1

                            else:
                                element = WebDriverWait(driver, 300).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]"))
                                )
                                invis = WebDriverWait(driver, 300).until(
                                    EC.invisibility_of_element_located((By.CLASS_NAME, 'blockUI blockOverlay')))
                                sleep(1)
                                if (invis):
                                    try:
                                        driver.find_element_by_xpath(
                                            "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]").click()
                                        sleep(1)
                                    except ElementClickInterceptedException:
                                        sleep(2)
                                        driver.find_element_by_xpath(
                                            "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]").click()



                        else:
                            element = WebDriverWait(driver, 300).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]"))
                            )
                            invis = WebDriverWait(driver, 300).until(
                                EC.invisibility_of_element_located((By.CLASS_NAME, 'blockUI blockOverlay')))
                            sleep(1)
                            if (invis):
                                try:
                                    driver.find_element_by_xpath(
                                        "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]").click()
                                    sleep(1)
                                except ElementClickInterceptedException:
                                    sleep(2)
                                    driver.find_element_by_xpath(
                                        "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]").click()



                    else:
                        element = WebDriverWait(driver, 300).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]"))
                        )
                        invis = WebDriverWait(driver, 300).until(
                            EC.invisibility_of_element_located((By.CLASS_NAME, 'blockUI blockOverlay')))
                        sleep(1)
                        if (invis):
                            try:
                                driver.find_element_by_xpath(
                                    "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]").click()
                                sleep(1)
                            except ElementClickInterceptedException:
                                sleep(1)
                                driver.find_element_by_xpath(
                                    "//*[@id='CAListContent']/form/table/tbody/tr/td/nobr/a[2]").click()

    GKCAList.close()
    return gkChangeCount

