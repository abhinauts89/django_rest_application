import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, TimeoutException


def openBrowserAndAuthenticate(driver, response):
    driver.get(response["environment"])
    driver.maximize_window()
    driver.execute_script("window.focus();")  # added since was unable to switch to newly opened tab
    driver.implicitly_wait(120)
    driver.find_element_by_id("username").send_keys(response["username"])
    driver.find_element_by_name("password").send_keys(response["password"])
    driver.find_element_by_id("kc-login").click()


def getDataArrayFromExcel(workbookData):
    print("Print all sheets in workbook:"+str(workbookData.sheetnames))
    allSheetsDataArray = []
    for i in range(len(workbookData.sheetnames)):
        # print("individual sheet name:"+str(workbookData.sheetnames[i]))
        allSheetsDataArray.append(passSheetDataToArray(workbookData[workbookData.sheetnames[i]]))
    # print("entire worksheet Data Array:"+str(allSheetsDataArray))

    return allSheetsDataArray


def passSheetDataToArray(activeSheet):
    rows = activeSheet.max_row
    columns = activeSheet.max_column
    print("max rows is "+str(rows)+" max columns is "+str(columns)+" in "+str(activeSheet))
    individualSheetData = [[0 for x in range(1, columns + 1)] for y in range(1, rows)]  # we don't want first row
    # print("individualSheetArray:"+str(individualSheetData))
    for i in range(2, rows + 1):  # range starting from 2 since we don't want first row
        for j in range(1, columns + 1):
            individualSheetData[i-2][j-1] = getCellValueFromExcel(activeSheet, i, j)
    return individualSheetData


def getCellValueFromExcel(activeSheet, row, col):
    cellValue = activeSheet.cell(row, col).value
    # print("cellValue of row "+str(row)+" and column "+str(col)+" is "+str(cellValue))
    return cellValue


def getProgramFormCodeAndZip(driver, response, sheetData):
    for i in range(len(sheetData)):
        # print("description val "+str(sheetData[i][0])+" and value in response "+str(sheetData[i][3]))
        programCodeVariable = sheetData[i][0] == "programCode" and sheetData[i][3] == response["programCode"]
        formCodeVariable = sheetData[i][0] == "formCode" and sheetData[i][3] == response["formCode"]
        zipCodeVariable = sheetData[i][0] == "zipCode" and sheetData[i][3] == response["state"]
        # print("programCodeVariable:"+str(programCodeVariable)+" and formCodeVariable:"+str(formCodeVariable))
        if programCodeVariable or formCodeVariable:
            setXpathAndClick(driver, sheetData[i][1])
        if zipCodeVariable:
            setXpathAndPassValue(driver, sheetData[i][1], sheetData[i][2])


def setXpathAndPassValue(driver, xPathValue, valueToBeAssigned):
    print("xPathValue is :"+str(xPathValue))
    print("valueToBeAssigned is "+str(valueToBeAssigned))
    print("is "+xPathValue+" enabled::"+str(driver.find_element_by_xpath(xPathValue).is_enabled()))
    print("val present in txt::" + str(driver.find_element_by_xpath(xPathValue).get_attribute("value")))
    element = driver.find_element_by_xpath(xPathValue)
    if valueToBeAssigned is None:
        return
    if element.get_attribute("value") == "" and element.is_enabled():
        element.send_keys(valueToBeAssigned)
        print("ele::"+str(element))
        driver.execute_script("arguments[0].blur();", element)
        time.sleep(1)


def setAddressForActiveState(driver, xPath, valToAssign):
    xPathList = str(xPath).split("\n")
    valToAssignList = str(valToAssign).split("\n")
    for i in range(len(xPathList)):
        print("individual xPath of list is::"+str(xPathList[i]))
        print("individual value of list is::" + str(valToAssignList[i]))
        element = driver.find_element_by_xpath(xPathList[i])
        element.send_keys(valToAssignList[i])


def checkCovTxtAndPassVal(driver,xPathValue, valueToBeAssigned):
    print("xPathValue is :" + str(xPathValue))
    print("valueToBeAssigned is " + str(valueToBeAssigned))
    print("val present in txt::" + str(driver.find_element_by_xpath(xPathValue).get_attribute("value")))
    print(type(valueToBeAssigned))
    isTextValueLess=str(driver.find_element_by_xpath(xPathValue).get_attribute("value")).replace(",","")
    print(isTextValueLess)
    if driver.find_element_by_xpath(xPathValue).get_attribute("value") == "" and driver.find_element_by_xpath(xPathValue).is_enabled():
        element=driver.find_element_by_xpath(xPathValue)
        element.send_keys(valueToBeAssigned)
        print("ele::"+str(element))
        driver.execute_script("arguments[0].blur();",element)
        time.sleep(1)
    elif int(isTextValueLess)<valueToBeAssigned and driver.find_element_by_xpath(xPathValue).is_enabled():
        element = driver.find_element_by_xpath(xPathValue)
        txtLength=len(element.get_attribute("value"))
        # element.send_keys(Keys.CONTROL+"a")
        element.send_keys(txtLength*Keys.BACKSPACE)
        element.send_keys(valueToBeAssigned)
        driver.execute_script("arguments[0].blur();", element)
        time.sleep(1)
    return


def checkDropDownValue(driver,xPathValue):
    dropVal=Select(driver.find_element_by_xpath(xPathValue))
    print("first selected option: "+str(dropVal.first_selected_option.text))
    dropDownList=['-Select-','Month','Year']
    isDropDownElementSelect=False
    # if dropVal.first_selected_option.text == ('-Select-' or 'Month' or 'Year'):
    #     print("Drop Down value is select")
    #     return False
    # else:
    #     print("Element already present in drop")
    #     return True
    for dropDownListVal in dropDownList:
        print("List element::"+str(dropDownListVal))
        if dropDownListVal==dropVal.first_selected_option.text:
            isDropDownElementSelect=True
            break

    if isDropDownElementSelect:
        print("Drop Down value is select")
        return False
    else:
        print("Element already present in drop")
        return True

# def setXpathAndPassValueForSelect(xPathValue, valueToBeAssigned):
#     obj = Select(driver.find_element_by_xpath(xPathValue))
#     print("first selected option: "+str(obj.first_selected_option.text))
#     if obj.first_selected_option.text != '-Select-':
#         return
#     else:
#         obj.select_by_visible_text(valueToBeAssigned)
#     return


def setXpathAndPassValueForSelect(driver,xPathValue):
    obj = driver.find_element_by_xpath(xPathValue)
    obj.send_keys(Keys.DOWN)


def isLoaderPresent(driver):
    try:
        print("loader displayed::"+str(driver.find_element_by_class_name("overlay").is_displayed()))
        if not driver.find_element_by_class_name("overlay").is_displayed():
            print("Loader not present!!!")
            time.sleep(2)
            return
        else:
            print("In Recursive loop since loader present!!!")
            time.sleep(10)
            isLoaderPresent(driver)
    except NoSuchElementException:
        print("No Element found Exception for Overlay!!!")
        return


def isElementPresent(driver, xpath):
    try:
            driver.implicitly_wait(4)
            driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        print("element "+str(xpath)+" not found!!!")
        return False
    return True


def setXpathAndClick(driver, xPathValue):
        element = driver.find_element_by_xpath(xPathValue)
        print("clicked button::" + str(element.text or element.get_attribute("value")))
        driver.execute_script("arguments[0].click()", element)
        # takes two parameter second is elements and first is arg


