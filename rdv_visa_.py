import time # for sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import email
import smtplib

msg = email.message_from_string('The RdV is available now!!!!')
msg['From'] = "sender email adresse"
msg['To'] = "destination email adresse"
msg['Subject'] = "RdV prefecture"

while True:
    # New instance for Chrome
    browser = webdriver.Chrome(ChromeDriverManager().install())
    # Open the webpage
    try:
        browser.get('Prefecture RdV link')
        
        # Save the window opener (current window, do not mistaken with tab... not the same)
        main_window = browser.current_window_handle
        # Accept cookies
        #browser.find_element_by_xpath("//a[@onclick='javascript:accepter()']").click()
        ################################################## Fill all the first form
        # Click in checkbox "Veuillez cocher la case pour..."
        browser.find_element_by_xpath("//input[@type='checkbox']").click()
        # Click in the submit button
        browser.find_element_by_xpath("//input[@name='nextButton']").click()
        ##################################################

        ################################################## Fill all the second form
        # Click in the radio button "Prendre un rendez-vous pour un renouvellement de titre..."
        #browser.find_element_by_xpath("//input[@id='nextButton']").click()
        # Click in the submit button
        #browser.find_element_by_xpath("//input[@type='submit']").click()
        #browser.find_element_by_xpath("//input[@name='nextButton']").click()
        ##################################################

        # Text to find when there is an error
        text = "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous. Veuillez recommencer ultérieurement."

        #if ((text in browser.page_source) or ("502" in browser.page_source) or ("503" in browser.page_source) or ("504" in browser.page_source)):
        if ((text in browser.page_source)):
            # Print in console that we didn't have the rd
            print("Pas de chance pour trouver un rendez-vous ='(")
            # Close the browser
            browser.quit()
            # Retry in some seconds
            time.sleep(300)
        else:
            # Open tab and trigger the alarm
            # browser.execute_script("window.open('http://soundbible.com/mp3/analog-watch-alarm_daniel-simion.mp3', '_blank')")
            s = smtplib.SMTP("smtp-mail.outlook.com",587)
            s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
            s.starttls() #Puts connection to SMTP server in TLS mode
            s.ehlo()
            s.login('user name or email adresse of sender', 'password of sendder')

            s.sendmail("sender email addresse", "destination email adresse", msg.as_string())

            s.quit()
            print('Mail Sent') 
            break
    except:
        browser.quit()
        time.sleep(300)

    