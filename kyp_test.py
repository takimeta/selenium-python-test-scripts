import json 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select

def init_driver():
    
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    # driver = webdriver.Safari()
    # driver = webdriver.Edge()
    driver.wait = WebDriverWait(driver, 0.70)
    return driver

if __name__ == "__main__":
    driver = init_driver()
    wait = WebDriverWait(driver, 10)
    driver.get("http://kyprolis-hcp-dev-2019.bluemod.us/administration-and-dose-modifications")
    jsonData = json.load(open('kyp_dosing_calc.json'))
    printKRdBtn = driver.find_element_by_id('regimen-krd')
    printKdTwiceBtn = driver.find_element_by_id('regimen-kd-twice')
    printKdOnceWkBtn = driver.find_element_by_id('regimen-kd-once')

    driver.execute_script("window.scrollTo(0, 600);")

    for index, object in enumerate(jsonData):
        
        # wait for click regimen element to appear in DOM, then click
        try:
            driver.wait.until(EC.element_to_be_clickable((By.ID, object.get('step1ClickRegimen')))).click()
            print('I can click the Step 1 Regimen button.')
            
            # Test to see if hidden buttons can be clicked
            # Hidden Kd Twice Weekly
            try:
                driver.wait.until(EC.element_to_be_clickable((By.ID, printKdTwiceBtn))).click()
                print('ERROR: Kd Twice Weekly button was clicked by accident!')
            except:
                print('Kd Twice Weekly Button is successfully hidden.')

            # Hidden Once Weekly
            try:
                driver.wait.until(EC.element_to_be_clickable((By.ID, printKdOnceWkBtn))).click()
                print('ERROR: Kd Once Weekly button was clicked by accident!')
            except:
                print('The Kd Once Weekly Button is successfully hidden.')

            # Hidden Krd
            try:
                driver.wait.until(EC.element_to_be_clickable((By.ID, printKRdBtn))).click()
                print('ERROR: KRd button was clicked by accident!')
            except:
                print('The KRd Button is successfully hidden.')
            print("I'm able to click the appropriate Step 1 button.")
        except WebDriverException:
            print("ERROR: I can't click the Step 1 button!")

        # wait for Select BSA drop down to appear then click each selection
        select = Select(wait.until(EC.element_to_be_clickable((By.ID, "MySelect"))))
        try:
            select.select_by_value(object.get('step2SelectBSA'))
            print("I've successfully clicked the BSA Drop Down.")
        except WebDriverException:
            print("ERROR: I can't click the BSA Select drop down!")

        # compare primingDose JSON to page element
        if object.get('primingDoseResult') == int(wait.until(EC.element_to_be_clickable((By.ID, 'priming-dose'))).text):
            print("The Priming Dose on the JSON matches the result on the page.")
        else:
            print("ERROR: The Priming Dose on the JSON does not match the Priming Dose result on the page!")

        # compare theraDose JSON to page element
        if object.get('theraDoseResult') == int(wait.until(EC.element_to_be_clickable((By.ID, 'therapeutic-dose'))).text):
            print("The Therapeutic Dose on the JSON mathes the result from the web page.")
        else:
            print("ERROR: The Therapeutic Dose on the JSON does not match the result on the page!")
        
        # Step 3 text link check
        if object.get('step3Textlink') == (driver.wait.until(EC.element_to_be_clickable((By.ID, 'dosing-link'))).text):
            print('I can see the text link copy in the JSON matches the copy on the page.')
        else:
            print("ERROR: I can't see the text link copy as it appears in the DOM!")

        # Step 3 text link URL check
        if object.get('step3URLCheck') == (driver.wait.until(EC.element_to_be_clickable((By.ID, 'dosing-link'))).get_attribute('href')):
            print("The URL for Step 3's text link matches the one listed in the JSON.")
        else:
            print("ERROR: The URL on the page doesn't match what's listed in the JSON!")

        reset = driver.wait.until(EC.element_to_be_clickable((By.ID, 'reset-button')))
        reset.click()
    driver.quit()
    