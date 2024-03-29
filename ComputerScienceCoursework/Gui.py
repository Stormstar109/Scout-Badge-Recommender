from easygui import *
import sys
from main import recommendation
import json
from csvimporting import csvImporting

# lets to user pick badges using the csv list of badges
def picker():
    try:
        msg = "Please select the badges you have done"
        title = "Badge picker"
        badgeList = list(csvImporting().keys())
        badgeChoice = multchoicebox(msg, title, badgeList)
        if badgeChoice == None:
            mainFunc()
        choiceDict = {}
        for i in range(len(badgeList)):
            choiceDict[badgeList[i]] = 0
        for i in range(len(badgeChoice)):
            choiceDict[badgeList[badgeList.index(badgeChoice[i])]] = 1

    except TypeError:
        sys.exit(0)

    return choiceDict

# the main function for showing the user their recommendations
# it looks large but most of it is just one line which involves 10 variables
def recommendedBadges():
    with open('recommendations.json') as json_file:
        recommendations = list(json.load(json_file))

        if len(recommendations) <= 5:
            msgbox(msg="This application cannot help you as you know what you need to do. \n Go and do it, We believe in you!", title="Yay!")
            mainFunc()

        print(recommendations[0])
        image = "badges\{0}.png".format(recommendations[0])
        choice = buttonbox("We believe that you would like {0}, {1}, {2}, {3}, {4} \n Click the badge you want to find out more about, or click back".format(recommendations[0], recommendations[1], recommendations[2], recommendations[3], recommendations[4]), title="Recommendations", choices=(["Main Menu", recommendations[0], recommendations[1], recommendations[2], recommendations[3], recommendations[4]]), image=image)
        if choice == "Main Menu":
            mainFunc()

        if choice == image:
            badgeFunc(recommendations[0])

        if choice in recommendations:
            badgeFunc(choice)
    return


#A function for creating new recommendations
def newRecommendations():
    badges = picker()                   #goes off to the picker function to let the user pick badges
    recommendations = recommendation(badges)  #outputs a list of lists
    rec1 = []
    for i in range(len(recommendations)):
        tempRec = recommendations[i]
        rec1.append(tempRec[0])

    for i in range(len(list(badges.keys()))):
        if (list(badges.values()))[i] == 1:
            rec1.remove((list(badges.keys()))[i])

        # takes the final list of recommendations and inputs it into a json file
    with open('recommendations.json', 'w') as f:
        json.dump(rec1, f)

    with open('firsttime.json', 'w') as json_file:
        json.dump(False, json_file)

    recommendedBadges()

    return

# a function to remove badges from your pool of owned badges
# very messy code


def removeBadges():

    badgeDict = {}
    rec1 = []
    with open('recommendations.json') as json_file:     # opens the previous recommendations
        recommendations = list(json.load(json_file))

    badgeList = list(csvImporting().keys())      # imports a list of badges

    ownedBadges = [x for x in badgeList if x not in recommendations]     # finds out the badges the user owns

    try:
        choice = multchoicebox(msg="Please enter the badges you wish to remove", title="Remove Badges",
                           choices=ownedBadges)     # the user selects the badges they want gone
        newOwnedBadges = [x for x in ownedBadges if x not in choice] # creates a list of the new owned badges
        for i in range(len(badgeList)):  # converts it to dictionary form for the recommendation engine
            if badgeList[i] in newOwnedBadges:
                badgeDict[badgeList[i]] = 1
            else:
                badgeDict[badgeList[i]] = 0

        recommendations = recommendation(badgeDict)

        for i in range(len(recommendations)):  # creates a list of badges the user has been recommended
            rec1.append(recommendations[i][0])

        for i in range(len(list(badgeDict.keys()))):  # gets rid of done badges
            if (list(badgeDict.values()))[i] == 1:
                rec1.remove((list(badgeDict.keys()))[i])

        with open("recommendations.json", "w") as json_file:  # puts it back into the json file
            json.dump(rec1, json_file)

        recommendedBadges()  # shows the user the badges they want

    except:
        mainFunc()

    return

def addBadges():

    badgeDict = {}
    rec1 = []
    with open('recommendations.json') as json_file:
        recommendations = list(json.load(json_file))

    badgeList = list(csvImporting().keys())

    notOwnedBadges = [x for x in badgeList if x in recommendations]

    try:
        choice = multchoicebox(msg="Please enter the badges you wish to add", title="Add Badges",
                               choices=notOwnedBadges)

        ownedBadges = [x for x in badgeList if x not in recommendations]

        newOwnedBadges = ownedBadges + choice

        for i in range(len(badgeList)):
            if badgeList[i] in newOwnedBadges:
                badgeDict[badgeList[i]] = 1
            else:
                badgeDict[badgeList[i]] = 0

        recommendations = recommendation(badgeDict)

        for i in range(len(recommendations)):
            rec1.append(recommendations[i][0])

        for i in range(len(list(badgeDict.keys()))):
            if (list(badgeDict.values()))[i] == 1:
                rec1.remove((list(badgeDict.keys()))[i])

        with open("recommendations.json", "w") as json_file:
            json.dump(rec1, json_file)

        recommendedBadges()

    except:
        mainFunc()

    return

def allBadgeFunc():
    badgeList = list(csvImporting().keys())
    badgeChoice = choicebox(msg="Choose your badge", title="Badges", choices=badgeList)

    if badgeChoice == None:
        mainFunc()

    else:
        badgeFunc(badgeChoice)


def badgeFunc(choice):  # Allows the user to see the requirements for the badges
    with open('badge.json') as json_file:  # Opens the json file with all the badge requirements in
        badgeRequirements = json.load(json_file)[choice]  # Finds the right json object for this badge

    selection = buttonbox( msg="{0} \nRequirements:\n\n{1}".format(choice,"\n\n".join(badgeRequirements)),
                           choices=["Main Menu", "Badge List", "Recommended Badges", "More like this", "Badge Image"],
                           title=choice)  #  displays the requirements

    if selection == "Main Menu":  # interprets what the user inputs
        mainFunc()

    if selection == "Badge List":
        allBadgeFunc()

    if selection == "Recommended Badges":
        recommendedBadges()

    if selection == "More like this":
        moreLikeThis(choice)

    if selection == "Badge Image":
        badgeFuncImage(choice)


def badgeFuncImage(choice):  # Shows the image to the user
    image = "badges\{0}.png".format(choice)  # Gets the image from the bank of images
    buttonbox(image=image, title=choice, choices=["Back"])
    badgeFunc(choice)


def helpFunc():  # Tells the user everything they need to know about the application
    choice = msgbox(ok_button="Main Menu", msg="Hello and welcome to the Scout Badge Recommendation engine\n"
                                      "This quick guide will take you through everything you need to know about the application\n"
                                      "\n"
                                      "Add New Badges:\n"
                                      "This function allows you to add new badges to your list of badges that you entered"
                                      "when you first started the application\n"
                                      "\n"
                                      "Remove Badges:\n"
                                      "Allows you to remove badges from your list of badges\n"
                                      "\n"
                                      "Badge List:\n"
                                      "Allows you to view a list of all the badges in scouting, clicking on one of these"
                                      "allows you to view the recommendations\n"
                                      "\n"
                                      "Your Recommended Badges:\n"
                                      "Allows you to view your recommended badges which have been specially selected based"
                                      "on the badges you have done\n"
                                      "\n"
                                      "Enter brand new set of badges:\n"
                                      "This function allows you select a completely new set of badges to get recommendations"
                                      "about.")
    if choice == "Main Menu":
        mainFunc()
    else:
        sys.exit()


def moreLikeThis(choice):

    badgeDict = {}
    rec1 = []
    badgeList = list(csvImporting().keys())

    for i in range(len(badgeList)):
        if badgeList[i] == choice:
            badgeDict[badgeList[i]] = 1
        else:
            badgeDict[badgeList[i]] = 0

    recommendations = recommendation(badgeDict)

    for i in range(len(recommendations)):
        rec1.append(recommendations[i][0])

    rec1.remove(choice)

    image = "badges\{0}.png".format(rec1[0])
    selection = buttonbox(
        "Badges like {5} are:  {0}, {1}, {2}, {3}, {4} \n Click the badge you want to find out more about, or click back".format(
            rec1[0], rec1[1], rec1[2], rec1[3], rec1[4], choice),
        title="More Like this", choices=(
        ["Back", "Main Menu", rec1[0], rec1[1], rec1[2], rec1[3], rec1[4]]),
        image=image)

    if selection == "Back":
        badgeFunc(choice)

    if selection == "Main Menu":
        mainFunc()

    if selection == image:
        badgeFunc(rec1[0])

    if selection in rec1:
        badgeFunc(selection)


# the main control function
def mainFunc():
    with open('firsttime.json') as json_file:
        firstTime = json.load(json_file)


    if firstTime == True:
        msgbox("Welcome to the Scout Badge Recommendation engine\n"
               "As this is your first time launching the application, we will take an introductory assessment of what"
               "badges you have done.")
        newRecommendations()



    image = "logo.png"
    choice = buttonbox("Welcome to the Scout Badge Recommendation Engine\nIf you are confused on what to do click the Help button", "Main", choices=["Quit", "Add New Badges", "Remove Badges", "Badge List", "Your Recommended Badges", "Enter brand new set of badges", "Help"], image=image)

    # If statements which control which way you go
    if choice == "Enter brand new set of badges":
        newRecommendations()

    if choice == "Your Recommended Badges":
        recommendedBadges()

    if choice == "Remove Badges":
        removeBadges()

    if choice == "Add New Badges":
        addBadges()

    if choice == "Badge List":
        allBadgeFunc()

    if choice == "Help":
        helpFunc()

    if choice == "logo.png":
        mainFunc()


mainFunc()