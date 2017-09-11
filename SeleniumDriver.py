# AUTHOR: GARRETT BREEDEN
# DESCRIPTION: Automate creating Sales Splits and Sales Clear in JIRA



# TODO: Automatically copy new case created into clipboard (Look into parsing HTML / Screenshotting)
# TODO: https://github.com/kybu/headless-selenium-for-win

from selenium import webdriver
# Allows for keystokes to be passed
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyperclip
import pickle


class SeleniumDriver():
    def __init__(self,):
        profile = webdriver.FirefoxProfile()
        self.driver = webdriver.Firefox(profile)
        self.sessionCookies = None

    def loadPage(self, website, title):
        self.driver.get(website)
        assert title in self.driver.title  # Ensure jira loaded correctly
        print("Loaded {} successfully".format(title))

    def login(self, username, password):

        username_form = self.driver.find_element_by_xpath(
            ".//*[@id='login-form-username']")
        username_form.clear()
        username_form.send_keys(username)

        password_form = self.driver.find_element_by_xpath(
            ".//*[@id='login-form-password']")
        password_form.clear()
        password_form.send_keys(password)

        submit_button = self.driver.find_element_by_xpath(
            ".//*[@id='login-form-submit']")
        submit_button.click()
        self.saveSessionCookies("InitialLogin.pkl")

    def createNewTicket(self):
        title = "Dashboard"
        while((title not in self.driver.title) == True):
            sleep(.25)
            print("sleeping .25 seconds to finish loading page")
        
        
        self.loadPage(
            "https://devops.partech.com/jira/secure/CreateIssue!default.jspa", "Create Issue")
        #bbs_element = self.driver.find_element_by_xpath(".//*[@id='brink-bugs-and-support-(bbs)-84']/a")
        self.saveSessionCookies("CreateIssue.pkl")
        

        project_field_element = self.driver.find_element_by_xpath(
            ".//*[@id='project-field']")
        project_field_element.send_keys("B3SE")
        project_field_element.send_keys(Keys.ENTER)

        issue_type_field_element = self.driver.find_element_by_xpath(
            ".//*[@id='issuetype-field']")
        issue_type_field_element.send_keys("Task")
        issue_type_field_element.send_keys(Keys.ENTER)

        issue_submit_button = self.driver.find_element_by_xpath(
            ".//*[@id='issue-create-submit']")
        issue_submit_button.click()

    def inputDataToCase(self, summary, description):
        sleep(2)  # Ensure page loads entirely
        self.saveSessionCookies("TicketSetup.pkl")
        summary_field = self.driver.find_element_by_xpath(
            ".//*[@id='summary']")
        summary_field.click()
        summary_field.send_keys(summary)

        # Select Text Field to Input RAW Markup
        description_text_field = self.driver.find_element_by_xpath(".//*[@id='aui-uid-1']")
        description_text_field.click()
        
        # Input data into description
        pyperclip.copy(description)
        summary_field.click()
        summary_field.send_keys(Keys.TAB, Keys.COMMAND + "v")

        # Set Priority of Case
        priority_drop_down = self.driver.find_element_by_xpath(".//*[@id='priority-field']")
        priority_drop_down.click()
        priority_drop_down.send_keys("Highest", Keys.TAB)

        # Add state tag
        # tags_drop_down = self.driver.find_element_by_xpath(".//*[@id='labels-multi-select']/span")
        # tags_drop_down.click()

        submit_JIRA_case_button = self.driver.find_element_by_xpath(".//*[@id='issue-create-submit']")
        submit_JIRA_case_button.click()

        self.driver.quit()

    # TODO: Finish Parsing Users Function
    def parseUsers(self, users):
        pass


        # This is a HTML Select tag, use <option value="10413">Minor</option>
        # severity_element = self.driver.find_element_by_xpath(
        #    ".//*[@id='tinymce']/p")

        assigned_to_element = self.driver.find_element_by_xpath(
            ".//*[@id='assignee-field']")  

    # TODO: Enable postAttachment function

    # Let the user control add this until completed
    def postAttachment(self, admin_site, site_id, location_id):
        pass
    
    def saveSessionCookies(self, name):
        pickle.dump(self.driver.get_cookies(), open(name, "wb"))

    def loadSessionCookies(self):
        self.sessionCookies = pickle.load(open("currentSession.pkl", "rb"))
        for cookie in self.sessionCookies:
            self.driver.add_cookie(cookie)

    


# if __name__ == "__main__":
#     firefox = SeleniumDriver()

#     firefox.loadPage("https://devops.partech.com/jira/login.jsp", "JIRA")
#     firefox.login("")
#     firefox.createNewTicket()
#     firefox.inputDataToCase("Sync Error Test",
#                             "123456-1", "Lets make a new case in JIRA to Showcase useage")

    # save new created case
    # .//*[@id='aui-flag-container']/div/div


  
