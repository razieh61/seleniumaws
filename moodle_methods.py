import datetime

from selenium import webdriver # import selenium to the file
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import moodle_locators as locators
from selenium.webdriver.support.ui import Select # --- add this import for drop down list
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys

# create a Chrome driver instance, specify path to chromedriver file, it launches the browser
# this gives a DeprecationWarning
# driver = webdriver.Chrome('/Users/razimkh/PycharmProjects/python_cctb2/chromedriver')
# or driver = webdriver.Chrome('../chromedriver')

s = Service(executable_path='../chromedriver')
driver = webdriver.Chrome(service=s)

# Moodle Test Automation Plan
# launch Moodle App website - validate we are on the home page
# navigate to login page - validate we are on the login page
# login with admin account - validate we are on the Dashboard page
# navigate to Add New User page - Site Administration > Users > Add New User - validate we are on the Add new user page
# populate the new user from fields using Faker library fake random data
# submit a new user form
# validate new user added:
# search for a new user using email - validate new is found
# logout of admin account
# or
# login as a new user - validate a new user can login
# logout of admin account
# login with admin account
# search for a new user using email address
# delete new user

def setUp():
    print(f'Launch {locators.app} App')
    print(f'--------------------***---------------------')
    # make browser full screen
    driver.maximize_window()

    # give browser up to 30 seconds to respond
    driver.implicitly_wait(30)

    # navigate to Moodle App website
    driver.get(locators.moodle_url)

    # check that moodle URL and the home page title are as expected
    if driver.current_url == locators.moodle_url and driver.title == locators.moodle_home_page_title:
        print(f'Yey! {locators.app} App website launched successfully :)')
        print(f'{locators.app} Homepage URL: {driver.current_url}, Homepage title: {driver.title}')
        sleep(0.25)
    else:
        print(f'{locators.app} did not launch. check your code or application')
        print(f'Current URL: {driver.current_url}, Page title: {driver.title}')
        tearDown()


def tearDown():
    if driver is not None:
        print(f'-------------------***--------------------')
        print(f'The test is completed at: {datetime.datetime.now()}')
        sleep(0.5)
        driver.close()
        driver.quit()  # kill the instance


def log_in(username, password):
    print(f'-------------------***--------------------')
    if driver.current_url == locators.moodle_url: # check we are on the home page
        driver.find_element(By.LINK_TEXT,'Log in').click()
        if driver.current_url == locators.moodle_login_page_url and \
                driver.title == locators.moodle_login_page_title:
            print(f'{locators.app} App Login page is displayed! Continue to log in.')
            sleep(0.25)
            driver.find_element(By.ID, 'username').send_keys(username)
            sleep(0.25)
            driver.find_element(By.ID, 'password').send_keys(password)
            sleep(0.25)
            driver.find_element(By.ID, 'loginbtn').click() # method 1 using ID
            # locators XPATH practice ----------------
            #driver.find_element(By.XPATH, '//button[contains(., "Log in")]').click() # mehtod 2 - using XPATH
            #driver.find_element(By.XPATH, '//button[contains(text(), "Log in")]').click() # mehtod 3 - using XPATH
            #driver.find_element(By.XPATH, '//button[contains(@id, "loginbtn")]').click() # mehtod 4 - using XPATH + ID
            #driver.find_element(By.XPATH, '//button[@id="loginbtn"]').click() # mehtod 5 using XPATH + id
            #driver.find_element(By.XPATH, '//*[@id="loginbtn"]').click() # method 6 using XPATH + id
            #driver.find_element(By.CSS_SELECTOR, 'button#loginbtn').click() # method 7 using CSS_SELECTOR
            #driver.find_element(By.CSS_SELECTOR, 'button[id="loginbtn"]').click() # method 8 using CSS_SELECTOR

            #breakpoint()
            # ------------------------------
            # validate login successfull - Dashboard page is displayed
            if driver.current_url == locators.moodle_dashboard_url and driver.title == locators.moodle_dashboard_title:
                assert driver.current_url == locators.moodle_dashboard_url
                # if condition returns True, then nothing happens, if condition returns False, AssertionError is raised
                assert driver.title == locators.moodle_dashboard_title
                print(f'--- login is successful. {locators.app} Dashboard is displayed - Page title: {driver.title}')
            else:
                print(f'Dashboard is not displayed. check your code or website and try again')


def log_out():
    print(f'-------------------***--------------------')
    driver.find_element(By.CLASS_NAME, 'userpicture').click()
    sleep(0.25)
    driver.find_element(By.XPATH, '//span[contains(.,"Log out")]').click()
    sleep(0.25)
    if driver.current_url == locators.moodle_url:
        print(f'--- Logout successful! {datetime.datetime.now()}')


def create_new_user():
    print(f'-------------------***--------------------')
    # navigate to 'Add a new user' form
    # find burger button if site administrator was not appear
    if not driver.find_element(By.XPATH, '//span[contains(.,"Site administration")]').is_displayed():
        try:
            driver.find_element(By.CSS_SELECTOR, '.fa-bars').click()
            sleep(0.25)
            driver.find_element(By.XPATH, '//span[contains(., "Site administration")]').click()
        except Exception:
            print(Exception)
    else:
        driver.find_element(By.XPATH, '//span[contains(., "Site administration")]').click()
    sleep(0.25)
    assert  driver.find_element(By.LINK_TEXT, 'Users').is_displayed()
    linkcheck = driver.find_element(By.LINK_TEXT, 'Users').is_displayed()
    print(f'--- User Link is displayed: {linkcheck}')
    driver.find_element(By.LINK_TEXT, 'Users').click()
    sleep(0.25)
    driver.find_element(By.LINK_TEXT, 'Add a new user').click()
    sleep(0.25)
    # vaidate we are on 'Add a new user' page
    assert  driver.find_element(By.LINK_TEXT, 'Add a new user').is_displayed()
    assert driver.title == locators.moodle_add_new_user_path_title
    print(f'--- Navigate to Add a new user page - Page Title: {driver.title}')
    sleep(0.25)
    driver.find_element(By.ID, 'id_username').send_keys(locators.new_username)
    sleep(0.25)
    driver.find_element(By.LINK_TEXT, 'Click to enter text').click()
    sleep(0.25)
    driver.find_element(By.ID, 'id_newpassword').send_keys(locators.new_password)
    sleep(0.25)
    driver.find_element(By.ID, 'id_firstname').send_keys(locators.first_name)
    sleep(0.25)
    driver.find_element(By.ID, 'id_lastname').send_keys(locators.last_name)
    sleep(0.25)
    driver.find_element(By.ID, 'id_email').send_keys(locators.email)
    sleep(0.25)
    Select(driver.find_element(By.ID, 'id_maildisplay')).select_by_visible_text('Allow everyone to see my email address')
    sleep(0.25)
    driver.find_element(By.ID, 'id_moodlenetprofile').send_keys(locators.moodle_net_profile)
    sleep(0.25)
    driver.find_element(By.ID, 'id_city').send_keys(locators.city)
    sleep(0.25)
    Select(driver.find_element(By.ID, 'id_country')).select_by_visible_text(locators.country)
    sleep(0.25)
    Select(driver.find_element(By.ID, 'id_timezone')).select_by_value('America/Vancouver')
    sleep(0.25)
    driver.find_element(By.ID, 'id_description_editoreditable').clear()
    driver.find_element(By.ID, 'id_description_editoreditable').send_keys(locators.description)
    sleep(0.5)

    # upload picture
    driver.find_element(By.CLASS_NAME, 'dndupload-arrow').click()
    img_path = ['System', 'Technology', 'Software Testing', 'Software Manual Testing', 'Course image', 'Mannual-Testing.jpg']
    for p in img_path:
        driver.find_element(By.LINK_TEXT, p).click()
        sleep(0.25)

    # select a radio button
    # Method 1 - click the radio button
    driver.find_element(By.XPATH, '//input[@value="4"]').click()
    # method 2 - click the label attached to radio button
    #driver.find_element(By.XPATH, '//label[contains(., "Create an alias/shortcut to the file"').click()
    sleep(0.25)
    driver.find_element(By.XPATH, '//button[contains(text(), "Select this file")]').click()
    sleep(0.25)
    driver.find_element(By.ID, 'id_imagealt').send_keys(locators.pic_desc)
    sleep(0.25)

    # populate Additional names section
    driver.find_element(By.LINK_TEXT, 'Additional names').click() # click to expand the section
    sleep(0.25)
    driver.find_element(By.ID, 'id_firstnamephonetic').send_keys(locators.first_name)
    sleep(0.25)
    driver.find_element(By.ID, 'id_lastnamephonetic').send_keys(locators.last_name)
    sleep(0.25)
    driver.find_element(By.ID, 'id_middlename').send_keys(locators.first_name)
    sleep(0.25)
    driver.find_element(By.ID, 'id_alternatename').send_keys(locators.first_name)
    sleep(0.25)

    # populate list of interests
    driver.find_element(By.LINK_TEXT, 'Interests').click()
    sleep(0.25)

    # add multiple interests using loop

    for tag in locators.list_of_interests:
        driver.find_element(By.XPATH, '//input[contains(@id, "form_autocomplete_input")]').send_keys(tag + '\n')
        #driver.find_element(By.XPATH, '//input[contains(@id, "form_autocomplete_input")]').send_keys(tag + ',')
        #driver.find_element(By.XPATH, '//input[contains(@id, "form_autocomplete_input")]').send_keys(Keys.ENTER)
        sleep(0.25)
    # for i in range(3):
    #     driver.find_element(By.XPATH, '//input[contains(@id, "form_autocomplete_input")]').send_keys(locators.fake.job() + '\n')

    #populate optional fields
    #driver.find_element(By.LINK_TEXT, 'Optional').click()
    driver.find_element(By.XPATH, '//a[text()="Optional"]').click()

    for i in range(len(locators.lst_opt)):
        fld, fid, val = locators.lst_opt[i], locators.lst_ids[i], locators.lst_val[i]
        #print(f'Populate optional field: {fld}')
        driver.find_element(By.ID, fid).send_keys(val)
        sleep(0.25)
######################################
    # press submit button to complete registration
    driver.find_element(By.ID, 'id_submitbutton').click()
    sleep(0.25)
    print(f'--- New user {locators.new_username}/{locators.new_password}/{locators.email} is added')


def search_user():
    print(f'---------------***----------------')
    print('--------------- Search User ---------------')
    if locators.moodle_users_main_page_url in driver.current_url and driver.title == locators.moodle_users_main_page_title:
        assert driver.find_element(By.LINK_TEXT, 'Browse list of users').is_displayed()
        print('---- Browse list of users page is displayed')
        if driver.find_element(By.ID, 'fgroup_id_email_grp_label').is_displayed() and \
                driver.find_element(By.NAME, 'email').is_displayed():
            sleep(0.25)
            print(f'--- Search for user by email {locators.email}')
            driver.find_element(By.CSS_SELECTOR, 'input#id_email').send_keys(locators.email)
            sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, 'input#id_addfilter').click()
            driver.implicitly_wait(5)
            try:
                # check for more related td values
                assert driver.find_element(By.XPATH, f'//td[contains(., "{locators.full_name}")]/../td[contains(., "{locators.email}")]').is_displayed()
                # capture user Moodle System ID
                href = driver.find_element(By.LINK_TEXT, locators.full_name).get_attribute("href")
                locators.sysid = href[href.find('=') + 1 : href.rfind('&')]
                print(f'--- User {locators.full_name} / {locators.email} / System id: {locators.sysid} is found! ----')
            except NoSuchElementException as nse:
                print(f'{locators.email} does not exist')
            # if usercheck:
            #     print(f'--- User {locators.full_name} / {locators.email} / System id: {locators.sysid} is found! ----')
            #
            # else:
            #     print(f'--- User {locators.full_name} / {locators.email} was not found!')


def check_new_user_can_login():
    print(f'-------------------***--------------------')
    if driver.current_url == locators.moodle_dashboard_url:
        if driver.find_element(By.XPATH, f'//span[contains(., "{locators.full_name}")]').is_displayed():
            print(f'--- User with the name {locators.full_name} login is confirmed ---')


def delete_user():
    print(f'-------------------***--------------------')
    print('--------------- Delete User Function ---------------')
    # navigate to Site Administration
    driver.find_element(By.XPATH, '//span[contains(., "Site administration")]').click()
    sleep(0.25)
    assert  driver.find_element(By.LINK_TEXT, 'Users').is_displayed()
    driver.find_element(By.LINK_TEXT, 'Users').click()
    sleep(0.25)
    driver.find_element(By.LINK_TEXT, 'Browse list of users').click()
    sleep(0.25)
    # search for user
    print('---------------  but first check if the user is found ---------------')
    search_user()
    # delete user
    print('---------------  Now we are going to Delete User ---------------')
    assert driver.find_element(By.XPATH, f'//td[contains(., "{locators.full_name}")]/../td/a[contains(@href, "delete={locators.sysid}")]').is_displayed()
    driver.find_element(By.XPATH, f'//td[contains(., "{locators.email}")]/../td/a[contains(@href, "delete={locators.sysid}")]').click()
    sleep(0.25)
    driver.find_element(By.XPATH, '//button[text()="Delete"]').click()
    sleep(0.25)
    print(f'--- User {locators.email}, System ID: {locators.sysid} is deleted at: {datetime.datetime.now()}')
    print('--------------- check if the user has been deleted successfully ---------------')
    # confirm delete
    search_user()
    #href="http://52.39.5.126/admin/user.php?sort=name&amp;dir=ASC&amp;perpage=30&amp;page=0&amp;delete=1461&amp;sesskey=0dvCQNwUvM" id="yui_3_17_2_1_1646165230582_558"
    #print(deletecheck)
    # if deletecheck:
    #     driver.find_element(By.XPATH,f'//td[contains(., "{locators.email}")]/../td/a[contains(@href, "delete={locators.sysid}")]').click()
    #     driver.find_element(By.XPATH, '//button[text()="Delete"]').click()
    #     sleep(0.25)
    #     print(f'--- User {locators.email}, System ID: {locators.sysid} is deleted at: {datetime.datetime.now()}')
    # else:
    #     print(f'User is not found! ')



# setUp()
# log_in(locators.admin_username, locators.admin_password)
# create_new_user()
# search_user()
# log_out()
# log_in(locators.new_username, locators.new_password)
# check_new_user_can_login()
# log_out()
# log_in(locators.admin_username, locators.admin_password)
# delete_user()
# log_out()
# tearDown()

