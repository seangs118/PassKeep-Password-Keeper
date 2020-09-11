from flask import Flask, jsonify, request, send_from_directory, redirect, render_template
import json
import os
import sys
import encrypt
import decrypt
import hashlib
import shutil
import webbrowser
import pyperclip
#from BeautifulSoup import BeautifulSoup

"""
	flask.Flask is flask itself
	flask.jsonify is to make JSON format
	flask.request is to receive data from the user
	flask.send_from_directory is to send HTML file when loading webpage
"""

from flask_cors import CORS #may not need this

app = Flask(__name__) #creating server
CORS(app)
loggedIn = False

def hash_string_256(string):
    """Create a SHA256 hash for a given input string.

    Arguments:
        :string: The string which should be hashed.
    """
    #return hl.sha256(string).hexdigest()
   # print (string)
    return hashlib.sha3_256(string.encode()).hexdigest()


@app.route('/', methods = ['GET']) #decorator, only GET requests
def get_ui():
    loggedIn = False
    if(not(os.path.exists("passwords.txt"))):
        return send_from_directory("ui", 'createPassword.html')
    else:
        return send_from_directory("ui", 'enterPassword.html')

#on button clicked in createPassword.html call:
@app.route('/createPassword', methods = ['POST'])
def createPassword():
    #userPassword = input ("Welcome to your PassKeep! Please create a new password for your usb: ")
    userPassword = request.form['password']
    hash1 = hash_string_256(userPassword)
    
    file = open("passwords.txt", 'w+')
    file.write(hash1)
    file.close()
    return send_from_directory('ui', 'passkeep.html')
	
# on button clicked in enterPassword.html call:
@app.route('/enterPassword', methods = ['POST']) 
def enterPassword():
    loggedIn = False
    while(loggedIn == False):
		#auth = input ("Enter your password: ")
        auth = request.form['password']
        hashAuth = hash_string_256(auth)
        file = open("passwords.txt", 'r+')
        check = file.read()
        if(check == hashAuth):
            loggedIn = True
        else:
            return send_from_directory('ui', 'enterPassword.html')
    return send_from_directory('ui', 'passkeep.html')
    
@app.route('/new', methods = ['POST'])
def new():
    username = request.form['username']
    website = request.form['website']
    length = request.form['length']
    special = request.form['special']
    caps = request.form['caps']
    nums = request.form['nums']

    #print(username, website, length, special, caps, nums)
    encrypt.encrypt(username, website, length, special, caps, nums)
    return send_from_directory('ui','passkeep.html')
    #return redirect(url_for('/passkeep.html'))


@app.route('/passkeep', methods = ['GET'])
def passkeep(): 
    return send_from_directory('ui', 'passkeep.html')
    
   

@app.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    website = request.form['website']
    path = ('passkeep/%s/%s.txt' %(website, username))
    if(os.path.exists(path)):
        userPassword = decrypt.decrypt(website, username)
    
    #return send_from_directory('ui','passkeep.html')
    # copies all the data the user has copied
        pyperclip.copy(userPassword)
        website = 'https://' + website
        what = webbrowser.open_new(website)
        other = "Your Password is copied to your clipboard."
    else:
        other = "no password for this username and website"
    return render_template('print.html', username=username, userPassword = other)

@app.route('/modifyusername', methods = ['POST'])
def modifyusername():
    website = request.form['website']
    username = request.form['username']
    path = ('passKeep/%s/%s.txt' %(website, username))
    usernameNew = request.form['usernameNew']
    newPath = ('passKeep/%s/%s.txt' %(website, usernameNew))
    os.rename(path, newPath)
    return send_from_directory('ui', 'passkeep.html')

@app.route('/modifypassword', methods = ['POST'])
def modifypassword():
    website = request.form['website']
    username = request.form['username']
    
    path = ('passKeep/%s/%s.txt' %(website, username))
    os.remove(path)
    usernameNew = request.form['usernameNew']

    length = request.form['length']
    special = request.form['special']
    caps = request.form['caps']
    nums = request.form['nums']
    encrypt.encrypt(usernameNew, website, length, special, caps, nums)
    return send_from_directory('ui','passkeep.html')


@app.route('/delete', methods = ['POST'])
def delete():     
    website = request.form['website']
    username = request.form['username']
    os.remove('passKeep/%s/%s.txt' %(website, username))
    return send_from_directory('ui','passkeep.html')

    
@app.route('/logout', methods = ['POST'])
def logout(): 
    logoutAction = request.form['logout']
    if (logoutAction == "yes"):
        loggedIn = False
        return send_from_directory('ui','enterPassword.html')
    
@app.route('/reset', methods = ['POST'])
def reset(): 
    sure = request.form['reset']
    auth = request.form['password']
    if(sure == 'yes'):
        file = open("passwords.txt", 'r+')
        check = file.read()
        authHash = hash_string_256(auth)
        if (authHash == check):
            shutil.rmtree('passKeep')
            os.remove('passwords.txt')
            os.mkdir('passKeep')
            #print("Device Wiped, Please restart\n")
            return send_from_directory('ui','createPassword.html')
        else:
            return send_from_directory('ui', 'passKeep.html')
           # print("Incorrect Password\n")
          #  continue    #pop up an incorrect password box and close all tabs
  #  elif (sure == "no"):
       # continue    #close all tabs






# @app.route('/jason', methods = ['GET']) #decorator, only GET requests
# def data_test():
#     return jsonify(username='sgs', email='sgs@gmail.com', id=69420)

# @app.route('/mine', methods = ['POST'])
# def add_transaction():
# 	values = request.get_json() #will be a dictionary holding data
# 	if not values:
# 		response = {
# 			'message': 'No data found.'
# 		}
# 		return jsonify(response), 400 #400 = no data found from client, client error
# 	required_fields = ['recipient', 'amount']
# 	if not all(field in values for field in required_fields): #if values does not contain all the fields
# 		response = {
# 			'message': 'Required data is missing'
# 		}
# 		return jsonify(response), 401

# 	recipient = values['recipient']
# 	amount = values ['amount']
# 	signature = 'Recipient: %s, Values: %s' % (recipient, amount)

# 	# response  = {
# 	# 	'recipient' = recipient,
# 	# 	'amount' = amount
# 	# }

# 	return jsonify(signature), 201


if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 50000) #localhost