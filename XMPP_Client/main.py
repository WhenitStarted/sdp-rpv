from time import sleep
import xmpp
import math


# Main program to send telemtery data from MP70 router to the ejabberd server/client
# Currently running on client2 with intent to send data to admin

disableXMPP = False 

# XMPP client credentials, user reciever address, and message
username = 'client2'
passwd = '12345'
to = 'admin@localhost'
msg = "TEST MESSAGE" 

# XMPP INITIALIZATION
if disableXMPP != True:
    client = xmpp.Client('localhost')            
    client.connect(server=('192.168.0.68', 5222)) # connect to ejabberd server using VPN IP 
    
    client.auth(username, passwd)              
    client.sendInitPresence()                  


def main():
    print(msg)                                  

    # Sends Message
    if disableXMPP != True:
        message = xmpp.Message(to, msg)        
        message.setAttr('type', 'chat')         
        client.send(message)                    
                   
    sleep(5) # 5
    

while True: # MAIN
    try:
        if __name__ == "__main__":
            main()
    except KeyboardInterrupt:
        print("\nCTRL+C pressed. Cleaning up...")
        break
        