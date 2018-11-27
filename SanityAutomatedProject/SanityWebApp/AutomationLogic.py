from .UserDefinedFunctions import *
from selenium import webdriver
import time
import openpyxl


def automatedTestCases(response):
    # driver = webdriver.Ie('D:\\Softwares\\Python\\IEDriverServer_Win32_3.14.0\\IEDriverServer.exe')
    driver = webdriver.Chrome('C:\\Users\\FUGRO\\Desktop\\Selenium\\chromedriver_win32\\chromedriver.exe')
    openBrowserAndAuthenticate(driver, response)
    isLoaderPresent(driver)
    workbookData = openpyxl.load_workbook("D:\\TestData.xlsx")
    entireWorkbookDataArray = getDataArrayFromExcel(workbookData)
    # print("First Worksheet Data:"+str(entireWorkbookDataArray[0]))
    getProgramFormCodeAndZip(driver, response, entireWorkbookDataArray[0])
    setXpathAndClick(driver, "//button[contains(@class,'btn-get-quote')]")
    # print("Second Worksheet Data:"+str(entireWorkbookDataArray[1]))
    isLoaderPresent(driver)
    for i in range(len(entireWorkbookDataArray[1])):
            # print("elem test:"+str(entireWorkbookDataArray[1][0][0]))
            if entireWorkbookDataArray[1][i][0] == "address":
                print("descp val:"+str(entireWorkbookDataArray[1][i][0])+" response val:"+str(entireWorkbookDataArray[1][i][3]))
                if entireWorkbookDataArray[1][i][3] == response["state"]:
                    print("address is set!!")
                    setAddressForActiveState(driver, entireWorkbookDataArray[1][i][1], entireWorkbookDataArray[1][i][2])
                else:
                    print("address is not set")
                    continue
            if not isElementPresent(driver, entireWorkbookDataArray[1][i][1]):
                continue
            if entireWorkbookDataArray[1][i][3] == 'PaymentSuccess':
                time.sleep(2)
                driver.get_screenshot_as_file("./Screenshots/paymentSuccess.png")
                break
            elif entireWorkbookDataArray[1][i][3] == 'responsiveButton':
                setXpathAndClick(driver, entireWorkbookDataArray[1][i][1])
                isLoaderPresent(driver)
            elif entireWorkbookDataArray[1][i][3] == 'CoverageText':
                checkCovTxtAndPassVal(driver, entireWorkbookDataArray[1][i][1], entireWorkbookDataArray[1][i][2])
            elif entireWorkbookDataArray[1][i][3] == 'active-radio':
                setXpathAndClick(driver, entireWorkbookDataArray[1][i][1])
            elif entireWorkbookDataArray[1][i][3] == 'inActive-radio':
                continue
            elif entireWorkbookDataArray[1][i][3] == 'button' or entireWorkbookDataArray[1][i][3] == 'radio' or entireWorkbookDataArray[1][i][3] == 'checkbox':
                setXpathAndClick(driver, entireWorkbookDataArray[1][i][1])
            elif entireWorkbookDataArray[1][i][3] == 'select':
                if checkDropDownValue(driver, entireWorkbookDataArray[1][i][1]):  # dropDown Already Present
                    continue
                else:
                    setXpathAndPassValueForSelect(driver, entireWorkbookDataArray[1][i][1])
            elif entireWorkbookDataArray[1][i][3] == 'text':
                setXpathAndPassValue(driver, entireWorkbookDataArray[1][i][1], entireWorkbookDataArray[1][i][2])
