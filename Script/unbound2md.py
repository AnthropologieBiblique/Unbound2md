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
		self.booksStandardNames = {}
		self.booksStandardAbbrev = {}
		self.booksEnglishNames = {}
		self.booksList = []
		self.createBooksNames()
		self.createBooksAbbrev()
		self.createBooksStandardNames()
		self.createBooksStandardAbbrev()
		self.createBooksEnglishNames()
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
	def createBooksStandardNames(self):
		with open('../Source/'+'book_standard_names.txt', mode='r') as tsv_file:
			csv_reader = csv.reader(tsv_file, delimiter='\t')
			for row in csv_reader:
				self.booksStandardNames[row[0]] = row[1]
	def createBooksStandardAbbrev(self):
		with open('../Source/'+'book_standard_abbrev.txt', mode='r') as tsv_file:
			csv_reader = csv.reader(tsv_file, delimiter='\t')
			for row in csv_reader:
				self.booksStandardAbbrev[row[0]] = row[1]
	def createBooksEnglishNames(self):
		with open('../Source/'+'book_english_names.txt', mode='r') as tsv_file:
			csv_reader = csv.reader(tsv_file, delimiter='\t')
			for row in csv_reader:
				self.booksEnglishNames[row[0]] = row[1]
	def addBook(self,book):
		self.booksList.append(book)
	def readBibleText(self):
		with open('../Source/'+self.unbound_name+'/'+self.unbound_name+'_utf8_mapped_to_NRSVA.txt', mode='r') as tsv_file:
			csv_reader = csv.reader(tsv_file, delimiter='\t')
			bookRef = ''
			chapterRef = ''
			flag = False
			for row in csv_reader:
				if row[0][0] == '#':
					pass
				elif row[8] == '':
					pass
				elif row[3]!=bookRef:
					if flag:
						book.addChapter(chapter)
						self.addBook(book)
					bookRef = row[3]
					bookStandardRef = row[0]
					book = BibleBook(self.booksNames[bookRef],
						self.booksAbbrev[bookRef],
						self.booksStandardNames[bookStandardRef],
						self.booksStandardAbbrev[bookStandardRef],
						self.booksEnglishNames[bookStandardRef])
					chapterRef = row[4]
					chapterStandardRef = row[1]
					chapter = BibleChapter(chapterRef,chapterStandardRef)
					chapter.addVerse(BibleVerse(row[5],row[6],row[8]))
					flag = True
				elif row[4]!=chapterRef:
					book.addChapter(chapter)
					chapterRef = row[4]
					chapterStandardRef = row[1]
					chapter = BibleChapter(chapterRef,chapterStandardRef)
					chapter.addVerse(BibleVerse(row[5],row[6],row[8]))
				else :
					chapter.addVerse(BibleVerse(row[5],row[6],row[8]))
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
	def __init__(self,name,abbrev,standardName,standardAbbrev,englishName):
		self.name = name
		self.abbrev = abbrev
		self.standardName = standardName
		self.standardAbbrev = standardAbbrev
		self.englishName = englishName
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
				chapter.buildMdBible(bibleAbbrev,self.name,self.abbrev,self.standardName,self.standardAbbrev,self.englishName,path)


class BibleChapter:
	def __init__(self,number,standard_number):
		self.number = number
		self.standard_number = standard_number
		self.verseList = []
	def addVerse(self,verse):
		self.verseList.append(verse)
	def buildMdBible(self,bibleAbbrev,bookName,bookAbbrev,bookStandardName,bookStandardAbbrev,bookEnglishName,path):
		name = bibleAbbrev +' '+bookAbbrev+' '+self.number
		f = open(path+'/'+name+'.md', 'w')
		f.write('---'+'\n')
		f.write('aliases : '+'\n')
		f.write('- '+bookName+' '+self.number+'\n')
		f.write('- '+bookStandardName+' '+self.standard_number+'\n')
		f.write('- '+bookStandardAbbrev+' '+self.standard_number+'\n')
		if bookStandardName != bookEnglishName:
			f.write('- '+bookEnglishName+' '+self.standard_number+'\n')
		f.write('tags : '+'Bible/'+bookStandardAbbrev.replace(" ", "")+'/'+self.standard_number.replace(" ", "")+'\n')
		f.write('---'+'\n\n')
		f.write('# '+bookName+' '+self.number+'\n\n')
		for verse in self.verseList:
			f.write('###### '+verse.number+verse.sub_number+'\n')
			f.write(verse.verseText+'\n')

class BibleVerse:
	def __init__(self,number,sub_number,verseText):
		self.number = number
		self.sub_number = sub_number
		self.verseText = verseText

#lsg = Bible("Louis Segond","french_lsg","LSG",False)
#vul = Bible("Peshitta","peshitta","PST",False)

vul = Bible("Vulgata Clementina","latin_vulgata_clementina","VG",True)
novVul = Bible("Nova Vulgata","latin_nova_vulgata","NVG",True)
hebrew = Bible("Hebrew BHS accents","hebrew_bhs_vowels","BHS",True)
lxx = Bible("Septante accentuée","lxx_a_accents","LXX",True)
