#Boilerplate 
import csv 
import random
import sys
import pprint as pp

#Variable setup
filename=sys.argv[1]
wordDict={}
splitList=[]
iList=[]
bList=[]
cList=[]
correct = 0
a = ''

#Create a dictionary with keys of terms and values of answers
#Create a list of lists of splitlines [Category, NAME\n]
for line in open(filename,'r'):
	if 'Category' not in line:
		wordDict[line.split(';')[0]]=line.split(';')[1].strip('\n')
	else:
		splitList.append(line.split(';'))

#Create a list of categories 
catList=[]
for splitline in splitList:
	catList.append(splitline[1].strip('\n'))

#Helper function that takes a range as an argument and prints lines in that range
def printLineRange(lb,ub):
	for i,line in enumerate(open(filename,'r')):
		if i in range(lb+1,ub):
			print(line.split(';')[0])

#Helper function that prompts the user and generates a response based on whether the user's answer is correct
def wordQuiz(word_selection):
	if word_selection in wordDict.keys():
		answer=input("What is the correct answer? ").lower()
		if answer == wordDict[word_selection]:
			print("Correct!")
			return 1
		else:
			print("Sorry, answer is: ",wordDict[word_selection])
	else:
		print("Sorry, that word isn't stored. Please try again.")
	return 0

#Helper function that prints all the term choices for a category 
#and then calls wordQuiz passing user input as the argument
def printCategoryTerms(cat_selection):	

		#If the category selection is not the last term in the category list
		if cat_selection.upper() in catList[0:len(catList)-1]:
			for i,cat in enumerate(catList):
				if cat_selection.upper() in cat:
					iList.append(i)
					iList.append(i+1)
			for i,fileline in enumerate(open(filename,'r')):
				if catList[iList[0]] in fileline:
					bList.append(i)
				if catList[iList[1]] in fileline:
					bList.append(i)
			printLineRange(bList[0],bList[1])

		#If the category selection is the last term in the category list, 
		#it cannot use the index of the next Category;NAME from the enumerated lines 
		#of the file as an upper bound. 
		#Therefore, the highest index in the enumerated lines of the file is used.
		#More precisely, it uses the length of a list of all the indices minus one.
		elif cat_selection.upper() in catList:
			for i,line in enumerate(open(filename,'r')):
				cList.append(i)
				if cat_selection.upper() in line:
					iList.append(i)
			iList.append(cList[len(cList)-1])
			printLineRange(iList[0],iList[1])

		elif cat_selection.upper() == "SEARCH FOR A WORD":
			wordQuiz(input("Enter word here: "))

		else:
			print("Sorry, that category isn't stored. Please try again.")

		del iList[0:]
		del bList[0:]
		del cList[0:]

mode_selection = input("Which mode would you like: Practice or Test? ")

#PRACTICE MODE
if mode_selection.lower() == 'practice':
	counter = 0
	correct = 0
	print("\nIn practice mode, user can practice as many times as they want.")
	print("If you wish to leave, select category QUIT when choosing a category.\n")
	input("Are you ready? Press enter to begin.")
	print("\nSEARCH FOR WORD")
	for i in catList:
		print(i)
	print("QUIT\n")
	chosen_category=''
	while chosen_category != 'quit':
		chosen_category=input("Which category would you like to select? ")
		if chosen_category != 'quit':
			printCategoryTerms(chosen_category)
			correct += wordQuiz(input("Which word would you like to practice? ").lower())
			counter += 1
	print('Grade Report:', correct, '/', counter)




#TEST MODE
elif mode_selection.lower() == 'test':
	counter = 0
	print("\nTest mode consists of 10 rounds.\n")
	input("Are you ready? Press enter to begin.")

	while counter < 10:
		print("\nSEARCH FOR WORD")
		for i in catList:
			print(i)
		print("\n")	
		printCategoryTerms(input("Which category would you like to select? "))
		correct += wordQuiz(input("Which word would you like to practice? ").lower())
		counter += 1
	print('Grade Report:', correct, '/', counter)
