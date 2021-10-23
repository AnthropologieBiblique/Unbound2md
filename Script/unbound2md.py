import re
import fileinput
import os
import csv

class Bible:
	def __init__(self,name,unbound_name,abbrev,NRSVA_mapping):
		self.name = name
		self.unbound_name = unbound_name
		self.abbrev = abbrev
		self.NRSVA_mapping = NRSVA_mapping
		self.booksNames = {}
		self.booksAbbrev = {}
		self.booksStandardAbbrev = {}
		self.booksList = []
		self.createBooksNames()
		self.createBooksAbbrev()
		self.createBooksStandardAbbrev()
		self.readBibleText()
		self.buildMdBible()
	def createBooksNames(self):
		with open('../Source/'+self.unbound_name+'/book_names.txt', mode='r') as tsv_file:
			csv_reader = csv.reader(tsv_file, delimiter='\t')
			for row in csv_reader:
				self.booksNames[row[0]] = row[1]
	def createBooksAbbrev(self):
		with open('../Source/'+self.unbound_name+'/book_abbrev.txt', mode='r') as tsv_file:
			csv_reader = csv.reader(tsv_file, delimiter='\t')
			for row in csv_reader:
				self.booksAbbrev[row[0]] = row[1]
	def createBooksStandardAbbrev(self):
		with open('../Source/'+'book_standard_abbrev.txt', mode='r') as tsv_file:
			csv_reader = csv.reader(tsv_file, delimiter='\t')
			for row in csv_reader:
				self.booksStandardAbbrev[row[0]] = row[1]
	def addBook(self,book):
		self.booksList.append(book)
	def readBibleText(self):
		with open('../Source/'+self.unbound_name+'/'+self.unbound_name+'_utf8.txt', mode='r') as tsv_file:
			csv_reader = csv.reader(tsv_file, delimiter='\t')
			bookRef = ''
			chapterRef = ''
			flag = False
			for row in csv_reader:
				if row[0][0] == '':
					pass
				if row[0][0] == '#':
					pass
				elif row[0]!=bookRef:
					if flag:
						book.addChapter(chapter)
						self.addBook(book)
					bookRef = row[0]
					book = BibleBook(self.booksNames[bookRef],self.booksAbbrev[bookRef],self.booksStandardAbbrev[bookRef])
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
		for book in self.booksList:
			book.buildMdBible(self.abbrev,path)


class BibleBook:
	def __init__(self,name,abbrev,standard_abbrev):
		self.name = name
		self.abbrev = abbrev
		self.standard_abbrev = standard_abbrev
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
		f.write('---'+'\n')
		f.write('aliases : '+'\n')
		f.write('tags : '+'\n')
		f.write('---'+'\n\n')
		f.write('# Chapitre '+self.number+'\n\n')
		for verse in self.verseList:
			f.write('###### '+verse.number+'\n')
			f.write(verse.verseText+'\n')

class BibleVerse:
	def __init__(self,number,verseText):
		self.number = number
		self.verseText = verseText

lsg = Bible("Louis Segond","french_lsg","LSG",False)
vul = Bible("Peshitta","peshitta","PST",False)
