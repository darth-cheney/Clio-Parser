from bs4 import BeautifulSoup
import codecs

def del_styling(soup):
	for tag in soup.find_all(True):
		del tag['style']
	for ital in soup.find_all('i'):
		ital.name = 'em'			

def del_spans(soup):
	for item in soup.find_all('span', attrs={'class' : 'MsoFootnoteReference'}):
		item.extract()

def make_citations(soup):
	cite_list = []
	
	#Find all of the paragraphs, find each note, pop it into the cite list
	for paragraph in soup.find_all('p', attrs={'class':'MsoNormal'}):
		for note in paragraph.find_all(attrs={'name':'_ftnref'}):
			cite_list.append(note)		
	
	
	#Iterate through the list of citations and insert <sup> elements and remove the span
	for cite in cite_list:
		sup_tag = soup.new_tag('sup')
		cite.insert(0, sup_tag)
		cite.unwrap()
		
def make_footnotes(soup):
	for span in soup.find_all('span'):
		span.unwrap()
	
	for note in soup.find_all('p', attrs={'class' : 'MsoFootnoteText'}):
		note.name = 'span'
		note['class'] = 'footnote-text'

	for ref_link in soup.find_all('a', attrs={'href' : '#_ftnref'}):
		ref_link.extract()			
			
def main():
	print('Name of file?')
	filename = raw_input()
	try:
		file = open(filename)
	except Exception:
		print 'Cannot open', filename
		raise	
	
	w_filename = raw_input('Name of file to write? ')
	try:
		w_file = codecs.open(w_filename, 'w', 'utf-8-sig')
	except Exception:
		print 'Cannot initialize the new file', w_filename		
		raise
		
	soup = BeautifulSoup(file)
	del_styling(soup)
	del_spans(soup)
	make_citations(soup)
	make_footnotes(soup)
	
	#Print the paragraphs, then the footnotes
	for paragraph in soup.find_all('p', attrs={'class' : 'MsoNormal'}):
		w_file.write(unicode(paragraph))
	for footnote in soup.find_all('span', attrs={'class' : 'footnote-text'}):
		w_file.write(unicode(footnote))	



if __name__ == '__main__':
	main()
