# IOT-SD3-2023-GOWR-IT
This is Collage IOT Projekt
It is an foundation for an smart flower pot. 
## Getting Data by the PI an snsoers.
The PI Folder:
That is the part on that need to insatall on the PI, I had use the PI ZERO 2 W With Sensors. Think on geting the .evn hand shake from the server it get the sassay in fromation how to conect, the conation token and the induwidual database login detiles and the RRS Feed detils.
## Prosseningdata
The Server Folder:
The Server menage the viewing the Webpage an checking te in coming data for the PI 
The sever if it run can creat an new int off an PI this text need to be copied to conect the pi with the server and Databank
## Storing data 
The Databank need to get setup over the setup.py from the server. For the init it need to fill out in the .evn the address, user name and password and the full exis on one tabel and the name of the tabel. 

## Security comunitcation 
I use sing in with Googel, I only use this to get an email adress so is not relveant for an static conation plece take an look if woud like to chage it in the scrutiyservers.py if you would like to make some changes. 
The PI and the databank now echt key this get ervy time new generaten be the fist contakt. The pi will tan comunicate only with the database and the RRS Feed with the server else the privat RRS feed to the Phone them selfe. The Phone gaet an token that can degript the message of the PI and the Server.
The PubNub communication is split into two different connections to ensure that the connection is safe and not understandable for outsiders. Also, the access manager is in use, which makes the whole communication more secure, so no threat can see what messages are being sent.

## Known Problems
Features: Excel export of the data, sharing the graphics, showing links
Security: Missing use of session tokens. The problem is, if you know someone is logged in and you have all the secret data of them, like the Google ID email and name of the account, and set them in the format of the system, the tokens can be used to bypass the security as that person. This is a fundamental fault, but it overcomes my knowledge of security programming. Even with a temporary session token, I still don't know enough about it to really make it kind of save.
Google login is not stable in Opera and Edge. In Chrome and Firefox, the login is stable. Could be something related to how the browser handles cookies.
CSS is not complete; there are still some definitions missing, so it is not unified across web browsers.
