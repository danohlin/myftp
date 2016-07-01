# myftp
##Simple FTP client

Name: Dan Ohlin  
Operating system: Windows  
Programing language: Python 2.7  
Compiling instructions: N/A  


Running instructions:  
Start program from command line using: python myftp.py <ftpserver>  
example: python myftp.py inet.cs.fiu.edu  

User will then be prompted for user name and password.  

Upon successful login, user can enter the following commands (as delineated in the assignment):  
cd remote-path  
get remote-file  
put local-file  
delete remote-file  
quit  

User can also enter:  
ls (to list files and folders in the current directory on the server)  
pwd (to list the current working directory on the server)  
