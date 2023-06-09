from jinja2 import Template, Environment, FileSystemLoader
from bs4 import BeautifulSoup


class Omni_Parser(object):
    def __init__(self, filename):
        print(filename)
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.text_file = open(filename, "r", encoding="utf-8")
        self.xml_as_string = self.text_file.read()
        #lxml renders fine but is non-functional, warning that it is an html parser not xml
        self.soup = BeautifulSoup(self.xml_as_string, features="xml")
        self.info = []
        self.text = []
        self.stitle = ''

    # scrape subsection text from USC
    def getUSCsubsection(self, ref_soup, subsection):
        #print("getUSCsubsection\n")
        for subsection_element in ref_soup.find_all('div'):
            if subsection_element.find('a'):
                if subsection_element.a.has_attr('name'): 
                    if (subsection_element.a['name'] == subsection):
                        return subsection_element

    # scrape subsection text from CFR
    def getCFRsubsection(self, ref_soup, subsection):
        #print("getCFRsubsection\n")
        for subsection_element in ref_soup.find_all('p'):
            if subsection_element.find('span'):
                if subsection_element.span.has_attr('id'): 
                    if (subsection_element.span['id'] == subsection):
                        return subsection_element


    def getExternalURL(self, ref_tag):
        #print("getExternalURL\n")
        ref_tags = ref_tag.split('/')
        doc = ref_tags[2]
        title = ref_tags[3][1:]
        section = ref_tags[4][1:]

        # get URL
        if (doc == 'usc'):
            # url = 'https://www.law.cornell.edu/uscode/text/%s/%s' % (title, section) # cornell link
            url = 'https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title%s-section%s&num=0&edition=prelim' % (title, section)
        elif (doc == 'cfr'):
            url = 'https://www.law.cornell.edu/cfr/text/%s/%s' % (title, section)

        # need to decide whether we just want a url or scraping text
        # if no subsection is listed, just return link
        return url

    def findExternalLinks(self):
        #print("findExternalLinks\n")
        for ref in self.soup.find_all('ref'):
            if ref.has_attr('href'):
                current_href = ref['href'].split('/')
                if (len(current_href) > 4):
                    doc = current_href[2] 
                    if (doc == 'usc' or doc == 'cfr'):
                        a_tag = self.soup.new_tag('a')
                        a_tag['href'] = self.getExternalURL(ref['href'])
                        a_tag['target'] = '_blank'
                        ref.wrap(a_tag)

    def create_Arrays(self):
        #print("createArrays\n")
        referenceItems = self.soup.find_all('referenceItem')
        for item in referenceItems:
            d_l_i = (item.designator, item.label, self.findLinks(item.designator))
            self.info.append(d_l_i)
        return self.info

    def cleanTocLabel(self, this_string):
        #print("cleanTocLabel\n")
        this_string.encode('utf-8')
        this_string = this_string.replace('.', '')
        this_string = this_string.replace(u"\u2014", '')
        this_string = this_string.replace(u"\u201C", '')
        this_string = this_string.replace(u"\u201D", '')
        return this_string

    def addDefinitions(self):
        #print("addDefinitions\n")
        # I'm about to seriously hardcode something for illustration purposes!!
        for section in self.soup.find_all('section', string=True):                            
            section.string = section.string.replace('Administration', '<div class="popup" onclick="popUpText()">Administration<span class="popuptext" id="myPopup"></span></div>')


    def findLinks(self, this_designator):
        #print("findLinks\n")
        label = self.cleanTocLabel(this_designator.text)

        label_split = label.split()
        if (len(label_split) >= 2):
            label_value = label_split[1]
        else:
            label_value = label_split[0]

        for section in self.soup.find_all('section'):
            if section.find('num'):
                if section.num.has_attr('value'):
                    if (section.num['value'] == label_value):
                        if (section.has_attr('identifier')):
                            self.text.append(section)
                            i = section['identifier']
                            i_split = i.split('/')
                            sec = i_split[len(i_split)-1]


                            return sec

    def getShortTitle(self):
        #print("getshortTitle\n")
        shortTitle = self.soup.find_all('short-title')
        #print("shortTitle: ", shortTitle)
        # ?? problem here ??
        if not shortTitle:
            shortTitle = self.soup.find_all('dc:title')
        
        self.stitle = shortTitle[0].text

    def addButtons(self):
        #print("addButtons\n")
    # <button type="button" class="collapsible"></button>
        for num in self.soup.find_all('num'):
            button_tag = self.soup.new_tag('button')
            button_tag['type']='button'
            button_tag['class']='collapsible'
            button_tag.string = ''

            # temp_tag = soup.new_tag('temp')
            # num.insert_before(temp_tag)
            # temp_tag.wrap(button_tag)
            # temp_tag.extract()

            num.insert_before(button_tag)


    def getCrumbs(self, this_identifier):
        #print("getCrumbs\n")
        # d = division
        # t = title
        # st = subtitle
        # pt = part
        # spt = subpart
        # s = section
        crumbs = []

        for i in this_identifier.split('/'):
            this_crumb = ''

            if (i.find('d', 0, 1) == 0):
                this_crumb = 'Division %s' % i[1:]
                crumbs.append(this_crumb)

            elif (i.find('t', 0, 1) == 0):
                this_crumb = 'Title %s' % i[1:]
                crumbs.append(this_crumb)

            elif (i.find('st', 0, 2) == 0):
                this_crumb = 'Subtitle %s' % i[2:]
                crumbs.append(this_crumb)

            elif (i.find('pt', 0, 2) == 0):
                this_crumb = 'Part %s' % i[2:]
                crumbs.append(this_crumb)

            elif (i.find('spt', 0, 3) == 0):
                this_crumb = 'Subpart %s' % i[3:]
                crumbs.append(this_crumb)

            elif (i.find('s', 0, 3) == 0):
                this_crumb = 'Section %s' % i[1:]
                crumbs.append(this_crumb)
                
        return crumbs


    # SOURCE: https://www.codegrepper.com/code-examples/whatever/save+html+to+file+jinja2
    def createHTML(self):
        #print("createHTML\n")
        #print("self.info: ", self.info, "\n")
        #print("self.text: ", self.text, "\n")
        template1 = self.env.get_template('index_template.html')
        output_from_parsed_template1 = template1.render(info=self.info, text=self.text, st=self.stitle)
        #print("output type: ", type(output_from_parsed_template1), "\n")
        with open("static/rendered_html/index.html", "w", encoding="utf-8") as fh:
            fh.write(output_from_parsed_template1)

    def createSectionHTML(self):
        #print("createSectionHTML\n")
        template2 = self.env.get_template('section_template.html')
        index = 0
        j = 0

        for d, l, i in self.info:
            if i != None and index < len(self.text):

                secprev = i
                secnext = i
   
                for k in range(4):
                    if (j > k):
                        if (self.info[j-k-1][2] is not None):
                            secprev = self.info[j-k-1][2]
                            break
      

                for k in range(3):
                    if (j < len(self.info) - k - 1):
                        if (self.info[j+k+1][2] is not None):
                            secnext = self.info[j+k+1][2]
                            break


                output_from_parsed_template2 = template2.render(sec=i, text=self.text[index], crumbs=self.getCrumbs(self.text[index]['identifier']), ps=secprev, ns=secnext, st=self.stitle)

                with open("static/rendered_html/section_" + str(i) + ".html", "w", encoding="utf-8") as fh:
                    fh.write(output_from_parsed_template2)
                    fh.close()
                    
                index += 1

            j += 1
             