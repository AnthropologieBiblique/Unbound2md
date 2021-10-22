import re
import fileinput
import os
import csv

class Bible:
	def __init__(self,name,abbrev):
		self.name = name
		self.abbrev = abbrev
		self.bookNames = {}
		self.createBooknames()
		self.bookList = []
		self.readBibleText()
		self.buildMdBible()
	def createBooknames(self):
		with open('../Source/'+self.abbrev+'/book_names.txt', mode='r') as tsv_file:
			csv_reader = csv.reader(tsv_file, delimiter='\t')
			for row in csv_reader:
				self.bookNames[row[0]] = row[1]
	def addBook(self,book):
		self.bookList.append(book)
	def readBibleText(self):
		with open('../Source/'+self.abbrev+'/'+self.abbrev+'_utf8.txt', mode='r') as tsv_file:
			csv_reader = csv.reader(tsv_file, delimiter='\t')
			bookRef = ''
			chapterRef = ''
			flag = False
			for row in csv_reader:
				if row[0][0] == '#':
					pass
				elif row[0]!=bookRef:
					if flag:
						book.addChapter(chapter)
						self.addBook(book)
					bookRef = row[0]
					book = BibleBook(self.bookNames[bookRef],self.bookNames[bookRef])
					chapterRef = row[1]
					chapter = BibleChapter(chapterRef)
					chapter.addVerse(BibleVerse(row[2],row[3]))
					flag = True
				elif row[1]!=chapterRef:
					book.addChapter(chapter)
					chapterRef = row[1]
					chapter = BibleChapter(chapterRef)
					chapter.addVerse(BibleVerse(row[2],row[3]))
				else :
					chapter.addVerse(BibleVerse(row[2],row[3]))
			book.addChapter(chapter)
			self.addBook(book)

	def buildMdBible(self):
		path = '../Bibles/'+self.abbrev
		print(path)
		try:
			os.mkdir(path)
		except FileExistsError:
			pass
		for book in self.bookList:
			book.buildMdBible(self.abbrev,path)


class BibleBook:
	def __init__(self,name,abbrev):
		self.name = name
		self.abbrev = abbrev
		self.numberChapters = 0
		self.chapterList = []
	def addChapter(self,chapter):
		self.chapterList.append(chapter)
	def buildMdBible(self,bibleAbbrev,path):
			path += '/'+self.name
			try:
				os.mkdir(path)
			except FileExistsError:
				pass
			for chapter in self.chapterList:
				chapter.buildMdBible(bibleAbbrev,self.abbrev,path)


class BibleChapter:
	def __init__(self,number):
		self.number = number
		self.verseList = []
	def addVerse(self,verse):
		self.verseList.append(verse)
	def buildMdBible(self,bibleAbbrev,bookAbbrev,path):
		name = bibleAbbrev +' '+bookAbbrev+' '+self.number
		f = open(path+'/'+name+'.md', 'w')
		f.write('# Chapitre '+self.number+'\n\n')
		for verse in self.verseList:
			f.write('###### '+verse.number+'\n')
			f.write(verse.verseText+'\n')

class BibleVerse:
	def __init__(self,number,verseText):
		self.number = number
		self.verseText = verseText

lsg = Bible("LSG","french_lsg")
vul = Bible("PST","peshitta")
