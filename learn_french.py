#Boilerplate 
import csv 
import random
import sys
import pprint as pp

#Variable setup
filename=sys.argv[1]
wordDict={}
splitList=[]
catRank=[]
fileLoc=[]
numFileList=[]
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
def printCategoryTerms(cat_selection):	

		#If the category selection is not the last term in the category list
		if cat_selection.upper() in catList[0:len(catList)-1]:
			for i,cat in enumerate(catList):
				#Append the indexes for the ith and (i+1)th category
				if cat_selection.upper() in cat:
					catRank.append(i)
					catRank.append(i+1)
			for i,fileline in enumerate(open(filename,'r')):
				#Search for ith and (i+1)th category in file and append their locations
				if catList[catRank[0]] in fileline:
					fileLoc.append(i)
				if catList[catRank[1]] in fileline:
					fileLoc.append(i)
			#Pass the locations as an argument to printLineRange
			printLineRange(fileLoc[0],fileLoc[1])

		#Special case: if the category selection is the last term in the category list, 
		#it cannot use the index of the next Category;NAME from the enumerated lines 
		#of the file as an upper bound. 
		#Therefore, the highest index in the enumerated lines of the file is used.
		#More precisely, it uses the length of a list of all the indices minus one.
		elif cat_selection.upper() in catList:
			#The first term of catRank should be the lb, which is the location of the last category.
			#The ub is the last line in the file.
			for i,line in enumerate(open(filename,'r')):
				numFileList.append(i)
				if cat_selection.upper() in line:
					catRank.append(i)
			catRank.append(numFileList[len(numFileList)-1])
			printLineRange(catRank[0],catRank[1])

		else:
			print("Sorry, that category isn't stored. Please try again.")
			return "Problem"

		#Clear the cache
		del catRank[0:]
		del fileLoc[0:]
		del numFileList[0:]

def gamePlayer(numRounds):
	counter = 0
	correct = 0
	print("\nSEARCH FOR A WORD")
	for i in catList:
		print(i)
	print("QUIT\n")
	chosen_category=''
	while chosen_category != 'quit' and counter < numRounds:
		chosen_category=input("Which category would you like to select? ")
		if chosen_category != 'quit':
			#"SEARCH FOR A WORD" is a special case. 
			if chosen_category.upper() == "SEARCH FOR A WORD":
				word_to_search=input("Enter word here: ")
				if word_to_search in wordDict.keys():
					correct += wordQuiz(word_to_search)
					counter += 1
				else:
					print("Sorry, that word isn't stored. Please try again.")
			else: 
				#printCategoryTerms(chosen_category) will run smoothly if chosen_category is in catList.
				if printCategoryTerms(chosen_category) != "Problem":
					#Since input is a function, we need to assign it
					#to a variable otherwise we cannot store its value.				#value.
					word_selection=input("Which word would you like to practice? ")
					correct += wordQuiz(word_selection.lower())
					if word_selection in wordDict.keys():
						counter += 1
	print('Grade Report:', correct, '/', counter)

mode_selection = input("Which mode would you like: Practice or Test? ")

if mode_selection.lower() == 'practice':
	print("\nIn practice mode, user can practice up to 100 times.")
	print("If you wish to leave, select category QUIT when choosing a category.\n")
	input("Are you ready? Press enter to begin.")
	gamePlayer(100)
	
elif mode_selection.lower() == 'test':
	counter = 0
	print("\nTest mode consists of 10 rounds.\n")
	input("Are you ready? Press enter to begin.")
	gamePlayer(10)
