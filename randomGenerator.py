import random


def randomGenerate (length, special, caps, nums):    

    chars = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()10'
    specialchars = '!@#$%^&*()'
    numchars = '1234567890'
    capchars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    length = int(length)
    special = int(special)
    caps = int(caps)
    nums = int(nums)
    restlength = length-caps-nums-special
    while(restlength<0):
        length = int(length)
        special = int(special)
        caps = int(caps)
        nums = int(nums)
        restlength = length-caps-nums-special

    password = ''
    choice = random.randint(0,2)
    if (choice==0):
        for c in range(caps):
            password += random.choice(capchars)
        for c in range(special):
            password += random.choice(specialchars)
        for c in range(nums):
            password +=random.choice(numchars)
    if (choice==1):
        for c in range(nums):
            password += random.choice(numchars)
        for c in range(caps):
            password += random.choice(capchars)
        for c in range(special):
            password +=random.choice(specialchars)
    if (choice==2):
        for c in range(special):
            password += random.choice(specialchars)
        for c in range(caps):
            password += random.choice(capchars)
        for c in range(nums):
            password +=random.choice(numchars)
    #print(choice)

    for c in range(restlength):
        password += random.choice(chars)

    #username = input('username?')
   # website = input ('website?')

    #file info

    fo= open("passwords.txt","a+")
    #fo.write("%s %s "  %(website, username))
    #fo.write("\n")


    return password



