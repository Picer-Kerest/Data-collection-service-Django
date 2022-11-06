import schedule

def sending():
   with open('D:\Django\Oleg Novikov Data Collection Service\scraping_service-project\send_emails.py', 'r',
             encoding='utf-8') as f:
       exec(f.read())

   schedule.every(1).minutes.do(sending)

   while True:
       schedule.run_pending()
       # time.sleep(1)

sending()