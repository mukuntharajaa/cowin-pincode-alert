# cowin-pincode-alert
A daemon which can monitor vaccine availability for a particular pincode and push notifications to telegram


There are many libraries and telegram bots available. But somehow When I set up alert for interior pincodes, almost all of them failed and did not send me any notification.

So I decided to write up my own daemon which can push notification, if vaccine is available for a particular pincode.

What-this-does:
- Runs as a daemon monitoring for a pincode ( every 1 minute )
- If there is any availability, it sends notification to telegram
- From second run onwards, it compares the data with previous run and send notification only if there is any positive-change in the availability
  ( i.e., a centre may get added, number of doses may increase/decrease, but still non-zero)
  
Pre-requisite:
- You can run this daemon in a computer/cloud ( azure etc ) 24x7
- A telegram account

Steps to run this daemon:
1) Change "pin_code" variable in main.py to your desired pincode
2) pip install --user telegram-send and pip install --user cowin-vaccine-api
3) Run "telegram --configure" and follow on-screen instructions to setup a bot for yourself(where you will receive notification)
4) Modify cowin-alert.service ExecStart path where main.py is stored in your computer
5) Copy cowin-alert.service to ~/.config/systemd/user
6) Start with "systemctl --user start cowin-alert" and check with "systemctl --user status cowin-alert.service"

Thats all, if everything goes well, you should see notification in your mobile, whenever its available.

TODO:
[] - Add filtering options ( eg: age_limit, vaccin preference , timeout )
[] - Delete stale entries from cache
[] - Explore multiple pincodes 
