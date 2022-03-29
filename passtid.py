from selenium import webdriver
from time import sleep
import argparse

DESIRED_LOCATIONS = ['Sthlm City', 'Solna', 'Globen', 'Norrtälje']
DESIRED_MONTHS = ['mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep']

class PassBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def clear_cookies(self):
        self.driver.delete_all_cookies()

    def init(self, url):
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                                   "source": """
                                   Object.defineProperty(navigator, 'webdriver', {
                                       get: () => undefined
                                    })
                                """})
        self.driver.get(url)
        book_btn = self.driver.find_element_by_xpath('//*[@id="Main"]/div[2]/div[1]/div/form/div[2]/input')
        book_btn.click()
        info_checkbox = self.driver.find_element_by_xpath('//*[@id="AcceptInformationStorage"]')
        info_checkbox.click()
        next_step_btn = self.driver.find_element_by_xpath('//*[@id="Main"]/form/div[2]/input')
        next_step_btn.click()
        swede_checkbox = self.driver.find_element_by_xpath('//*[@id="ServiceCategoryCustomers_0__ServiceCategoryId"]')
        swede_checkbox.click()
        next_step_btn = self.driver.find_element_by_xpath('//*[@id="Main"]/form/div[2]/input')
        next_step_btn.click()

    def search(self, locations, months, user_data):
        while True:
            # sleep(0.05)
            print('Starting search...')
            try:
                warning = self.driver.find_element_by_xpath('//*[@id="Main"]/div[2]/ul/li')
                print(warning.text)
                print('Blocked due to too many searches, restarting...')
                return False
            except:
                success = self._find_slot(locations, months, user_data)
                if success:
                    return True

    def _find_slot(self, desired_locations, desired_months, user_data):
        print('Starting search...')
        try:
            warning = self.driver.find_element_by_xpath('//*[@id="Main"]/div[2]/ul/li')
            print(warning.text)
            print('Blocked due to too many searches, restarting...')
            return False
        except:
            ...
        first_available_btn = self.driver.find_element_by_xpath('//*[@id="Main"]/form[1]/div/div[6]/div/input[2]')
        first_available_btn.click()
        tables = self.driver.find_elements_by_class_name('timetable')
        for table in tables:
            location = table.find_element_by_id('sectionName').text.strip().replace('\n', ' ')
            date = table.find_element_by_id('dateText').text
            if location in desired_locations and acceptable_date(date, desired_months):
                time_slots = table.find_elements_by_class_name('timetable-cells')
                if time_slots:
                    return self._reserve_slot(time_slots[-1], user_data)

    def _reserve_slot(self, time_slot, user_data):
        time_slot.click()
        next_btn = self.driver.find_element_by_xpath('//*[@id="booking-next"]')
        next_btn.click()
        # To check if we reached the next page or not
        enter_name_header = self.driver.find_element_by_xpath('//*[@id="Main"]/div/h1')
        print('Current page header:', enter_name_header.text)
        if enter_name_header.text == 'Välj tid':
            print('Wasn\'t fast enough, returning to search...')
            return
        else:
            return self._book_slot(user_data)

    def _book_slot(self, user_data):
        first_name_box = self.driver.find_element_by_xpath('//*[@id="Customers_0__BookingFieldValues_0__Value"]')
        first_name_box.send_keys(user_data['first_name'])
        last_name_box = self.driver.find_element_by_xpath('//*[@id="Customers_0__BookingFieldValues_1__Value"]')
        last_name_box.send_keys(user_data['last_name'])
        passport_checkbox = self.driver.find_element_by_xpath('//*[@id="Customers_0__Services_0__IsSelected"]')
        passport_checkbox.click()
        next_btn = self.driver.find_element_by_xpath('//*[@id="Main"]/form/div[2]/input')
        next_btn.click()
        next_btn = self.driver.find_element_by_xpath('//*[@id="Main"]/form/div/input')
        next_btn.click()
        email_box_1 = self.driver.find_element_by_xpath('//*[@id="EmailAddress"]')
        email_box_1.send_keys(user_data['email'])
        email_box_2 = self.driver.find_element_by_xpath('//*[@id="ConfirmEmailAddress"]')
        email_box_2.send_keys(user_data['email'])
        phone_box_1 = self.driver.find_element_by_xpath('//*[@id="PhoneNumber"]')
        phone_box_1.send_keys(user_data['phone'])
        phone_box_2 = self.driver.find_element_by_xpath('//*[@id="ConfirmPhoneNumber"]')
        phone_box_2.send_keys(user_data['phone'])
        email_confirmation = self.driver.find_element_by_xpath('//*[@id="SelectedContacts_0__IsSelected"]')
        email_confirmation.click()
        sms_confirmation = self.driver.find_element_by_xpath('//*[@id="SelectedContacts_1__IsSelected"]')
        sms_confirmation.click()
        email_reminder = self.driver.find_element_by_xpath('//*[@id="SelectedContacts_2__IsSelected"]')
        email_reminder.click()
        sms_reminder = self.driver.find_element_by_xpath('//*[@id="SelectedContacts_3__IsSelected"]')
        sms_reminder.click()
        next_btn = self.driver.find_element_by_xpath('//*[@id="Main"]/form/div[2]/input')
        next_btn.click()
        booking_summary = self.driver.find_element_by_xpath('//*[@id="Main"]/form/div[2]')
        print(booking_summary.text)
        confirm_btn = self.driver.find_element_by_xpath('//*[@id="Main"]/form/div[1]/input')
        confirm_btn.click()
        return True

def acceptable_date(date, desired_months):
    month = date.split()[1]
    if month in desired_months:
        return True
    else:
        return False

def run(url, locations, months, user_data):
    bot = PassBot()
    while True:
        try:
            bot.clear_cookies()
            bot.init(url)
            success = bot.search(locations, months, user_data)
            if success:
                print('Timeslot booked succesfully!')
                return
            # sleep(0.05)
        except Exception as e:
            print('An exception occured in main loop:', e)

def main():
    parser = argparse.ArgumentParser(description='Passport timeslot scanner arguments.')
    parser.add_argument('--url', type=str, 
        help='The starting URL based on area, for example: https://bokapass.nemoq.se/Booking/Booking/Index/Stockholm',
        default='https://bokapass.nemoq.se/Booking/Booking/Index/Stockholm')
    parser.add_argument('--locations', type=str, 
        help='The locations you are interested in (comma separated), for example: --locations="Sthlm City,Globen,Norrtälje"',
        default='Sthlm City,Globen,Solna,Norrtälje')
    parser.add_argument('--months', type=str,
        help='The months that you are interested in (comma separated, three letter format), \
        for example: --months=mar,apr,maj,jun,jul,dec',
        default='mar,apr,maj,jun')
    parser.add_argument('--name', type=str,
        help='Your full name, for example: --name=Kalle Anka',
        required=True)
    parser.add_argument('--email', type=str,
        help='Your email address, for example: --email=cool@example.com',
        required=True)
    parser.add_argument('--phone', type=str,
        help='Your phone number, for example: --phone=1234',
        required=True)
    args = parser.parse_args()
    locations = args.locations.split(',')
    months = args.months.split(',')
    user_data = {
        "first_name" : args.name.split()[0],
        "last_name" : args.name.split()[1],
        "phone" : args.phone,
        "email" : args.email
    }
    run(args.url, locations, months, user_data)

if __name__ == '__main__':
    main()