import re
import pyperclip
def regex(toClip):
    emailRegex = re.compile(r"""
    [A-Za-z0-9]+  #This is the username
    @ #This is the "@" sign 
    [A-Za-z0-9]+ #This is the domain
    \.[A-Za-z0-9\.]{2,6} #This is the top level domain
    """, re.VERBOSE)

    phoneRegex = re.compile(r"""
    (\+\d{1,3}\s)? #This is the optional country code
    (\d{4,5})      #This is the area code
    (\s)?            #This is an optional space
    (\d{6})        #This is the phone number
    """, re.VERBOSE)

    emailList = emailRegex.findall(pyperclip.paste())
    rawPhoneList = phoneRegex.findall(pyperclip.paste())
    phoneList = []

    for tuple in rawPhoneList:
        newEntry = ""
        for item in tuple:
            newEntry += item
        phoneList.append(newEntry)

    if toClip == True:
        toCopy = ""
        newList = emailList + phoneList
        for item in newList:
            toCopy += "\n" + item
        pyperclip.copy(toCopy)
    return emailList + phoneList 