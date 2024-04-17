import xmpp

username = 'client2'
passwd = '12345'
to='admin@localhost'
msg='hello :)'


client = xmpp.Client('localhost')
client.connect(server=('192.168.0.68',5222))

client.auth(username, passwd)
client.sendInitPresence()
message = xmpp.Message(to, msg)
message.setAttr('type', 'chat')
client.send(message)
