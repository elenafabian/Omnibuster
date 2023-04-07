import sys
import xml.dom.minidom
import os

class OmniparseDOM:
    def __init__(self, srcFilePath, destFilePath):
        self.filePath = destFilePath
        # file: the destination for this Omnibuster rendering
        self.file = open(destFilePath, "w", encoding="utf-8")
        # orig: the xml string from congress.gov
        self.orig = xml.dom.minidom.parse(srcFilePath)

    def header_html(self):
        # page header: title and bill information
        title_tags = self.orig.getElementsByTagName("dc:title")
        title_full = title_tags[0].firstChild.data.split(':', 1)
        date = self.orig.getElementsByTagName("dc:date")[0].firstChild
        if (not date):
            date = ""
        else:
            date = date.data
        publisher = self.orig.getElementsByTagName("dc:publisher")[0].firstChild.data
        html = ("<header class=\"headerRibbon sticky\" id=\"myHeader\">\n" +
		        "<div class=\"headerTxt\">\n" +
			    "<div id=\"BillInfo\" class=\"billInfo\">\n" +
				"<h3>" + title_full[0] + "</h3>\n" +
                # TODO: need to pull the correct date
				"<h3>" + date + "</h3>\n" +
                # TODO: need to pull house of rep or senate?
				"<h3>" + publisher + "</h3>\n" +
			    "</div>\n" +
  			    "<h2 id=\"BillTitle\" class=\"billTitle\">" + title_full[1] + "</h2>\n" +
		        "</div>\n" +
	            "</header>\n")
        self.file.write(html)

    def bill_nav_html(self):
        # table of contents navbar
        html = ("<nav id=\"mySidenav\" class=\"sidenav\">\n" +
                "<div id=\"openbtn\" style=\"font-size:30px;cursor:pointer\" onclick=\"openNav()\" class=\"openbtn\">&#9776;</div>\n" +
                "<div id=\"myNavContainer\" class=\"navContainer\">\n" +
	            "<div class=\"TOC\">Table of Contents</div>\n" +
	            "<a href=\"javascript:void(0)\" class=\"closebtn\" onclick=\"closeNav()\">&times;</a>\n" +	
	            "<br>\n")
        sectionTitle_tags = []
        # body name for bill docs
        legis_body = self.orig.getElementsByTagName("legis-body")[0]
        for k in legis_body.childNodes:
            if isinstance(k, xml.dom.minidom.Element):
                if k.tagName == "section":
                    sectionTitle_tags.append(k)
                elif k.tagName == "division":
                    sectionTitle_tags.append(k)
                elif k.tagName == "title":
                    sectionTitle_tags.append(k)
                elif k.tagName == "amendment":
                    for l in k.childNodes:
                        if isinstance(l, xml.dom.minidom.Element):
                            if l.tagName == "amendment-block":
                                for m in l.childNodes:
                                    if isinstance(m, xml.dom.minidom.Element):
                                        if m.tagName == "section":
                                            sectionTitle_tags.append(m)
                                        elif m.tagName == "division":
                                            sectionTitle_tags.append(m)
                                        elif m.tagName == "title":
                                            sectionTitle_tags.append(m)
        
        for i in sectionTitle_tags:
            sectionHeader = i.getElementsByTagName("header")
            # for sections with no header (undesignated section?) just skip
            if (not i.getElementsByTagName("header")):
                continue
            enum = i.getElementsByTagName("enum")
            if (enum):

                tocID = i.getAttribute("id")
                html += "\t\t<a href=\"#toctag" + str(tocID) + "\">\n"
                html += self.doc_html_helper(enum[0])
                html += self.doc_html_helper(sectionHeader[0])
                html += "</a>\n"

        html += "\t</div>\n</nav>\n"
        self.file.write(html)

    def amend_nav_html(self):
        html = ("<nav id=\"mySidenav\" class=\"sidenav\">\n" +
                "<div id=\"openbtn\" style=\"font-size:30px;cursor:pointer\" onclick=\"openNav()\" class=\"openbtn\">&#9776;</div>\n" +
                "<div id=\"myNavContainer\" class=\"navContainer\">\n" +
	            "<div class=\"TOC\">Table of Contents</div>\n" +
	            "<a href=\"javascript:void(0)\" class=\"closebtn\" onclick=\"closeNav()\">&times;</a>\n" +	
	            "<br>\n")
        sectionTitle_tags = []
        # body name for amendment docs
        eng_amend_body = self.orig.getElementsByTagName("engrossed-amendment-body")[0]
        for k in eng_amend_body.childNodes:
            if isinstance(k, xml.dom.minidom.Element):
                if k.tagName == "section":
                    sectionTitle_tags.append(k)
                elif k.tagName == "division":
                    sectionTitle_tags.append(k)
                elif k.tagName == "title":
                    sectionTitle_tags.append(k)
                if k.tagName == "amendment":
                    for l in k.childNodes:
                        if isinstance(l, xml.dom.minidom.Element):
                            if l.tagName == "amendment-block":
                                for m in l.childNodes:
                                    if isinstance(m, xml.dom.minidom.Element):
                                        if m.tagName == "section":
                                            sectionTitle_tags.append(m)
                                        elif m.tagName == "division":
                                            sectionTitle_tags.append(m)
                                        elif m.tagName == "title":
                                            sectionTitle_tags.append(m)
        
        for i in sectionTitle_tags:
            sectionHeader = i.getElementsByTagName("header")
            # for sections with no header (undesignated section?) just skip
            if (not i.getElementsByTagName("header")):
                continue
            enum = i.getElementsByTagName("enum")
            if (enum):

                tocID = i.getAttribute("id")
                html += "\t\t<a href=\"#toctag" + str(tocID) + "\">\n"
                html += self.doc_html_helper(enum[0])
                html += self.doc_html_helper(sectionHeader[0])
                html += "</a>\n"

        html += "\t</div>\n</nav>\n"
        self.file.write(html)

    def parse_section(self, k):
        # start section with line break
        html = "<br>\n"
        # open section div
        html += "<div class= \"sec2 " + k.tagName + "\">\n"
        # deal with enum and header separately, then do rest of child nodes
        if(len(k.childNodes) >= 2 and 
            isinstance(k.childNodes[0], xml.dom.minidom.Element) and
            isinstance(k.childNodes[1], xml.dom.minidom.Element) and
            k.childNodes[0].tagName == "enum" and 
            k.childNodes[1].tagName == "header"):
            # enum/header container
            tocID = k.getAttribute("id")
            html += "<div class=\"enum_header sec1\" id=\"toctag" + str(tocID) + "\">\n"
            # enum
            html += self.doc_html_helper(k.childNodes[0])
            # header
            html += self.doc_html_helper(k.childNodes[1])
            # close container
            html += "</div>\n"
            # button for collapsible section
            html += "<button class=\"collapsible active\" style=\"font-size: 24px;\"></button>\n"
            k.childNodes.pop(0)
            k.childNodes.pop(0)
            # open div for content of section
            html += "<div id=\"content\" class=\"content\" style=\"display: block;\">\n"
            # recurse on rest of child nodes
            html += self.doc_html_helper(k)
            # close div for content of section
            html += "</div>\n"
        else:
            #print("error: unrecognized section header")
            html += self.doc_html_helper(k)
        # close div for section
        html += "</div>\n"
        html += "<br>\n"
        return html
    
    def parse_division(self, k):
        # start division with line break
        html = "<br>\n"
        # open division div
        html += "<div class= \"sec2 " + k.tagName + "\">\n"
        # deal with enum and header separately, then do rest of child nodes
        if(len(k.childNodes) >= 2 and 
            isinstance(k.childNodes[0], xml.dom.minidom.Element) and
            isinstance(k.childNodes[1], xml.dom.minidom.Element) and
            k.childNodes[0].tagName == "enum" and 
            k.childNodes[1].tagName == "header"):
            # enum/header container
            tocID = k.getAttribute("id")
            html += "<div class=\"enum_header sec1\" id=\"toctag" + str(tocID) + "\">\n"
            # enum
            html += "DIVISION "
            html += self.doc_html_helper(k.childNodes[0])
            # header
            html += self.doc_html_helper(k.childNodes[1])
            # close container
            html += "</div>\n"
            # button for collapsible section
            html += "<button class=\"collapsible active\" style=\"font-size: 24px;\"></button>\n"
            k.childNodes.pop(0)
            k.childNodes.pop(0)
            # open div for content of section
            html += "<div id=\"content\" class=\"content\" style=\"display: block;\">\n"
            # recurse on rest of child nodes
            html += self.doc_html_helper(k)
            # close div for content of section
            html += "</div>\n"
        else:
            #print("error: unrecognized division header")
            html += self.doc_html_helper(k)
        # close div for section
        html += "</div>\n"
        html += "<br>\n"
        return html
    
    def parse_title(self, k):
        # start section with line break
        html = "<br>\n"
        # open section div
        html += "<div class= \"sec2 " + k.tagName + "\">\n"
        # deal with enum and header separately, then do rest of child nodes
        if(len(k.childNodes) >= 2 and 
            isinstance(k.childNodes[0], xml.dom.minidom.Element) and
            isinstance(k.childNodes[1], xml.dom.minidom.Element) and
            k.childNodes[0].tagName == "enum" and 
            (k.childNodes[1].tagName == "header" or k.childNodes[1].tagName == "appropriations-major")):
            # enum/header container
            tocID = k.getAttribute("id")
            html += "<div class=\"enum_header sec1\" id=\"toctag" + str(tocID) + "\">\n"
            # enum
            html += self.doc_html_helper(k.childNodes[0])
            # header
            html += self.doc_html_helper(k.childNodes[1])
            # close container
            html += "</div>\n"
            # button for collapsible section
            html += "<button class=\"collapsible active\" style=\"font-size: 24px;\"></button>\n"
            k.childNodes.pop(0)
            k.childNodes.pop(0)
            # open div for content of section
            html += "<div id=\"content\" class=\"content\" style=\"display: block;\">\n"
            # recurse on rest of child nodes
            html += self.doc_html_helper(k)
            # close div for content of section
            html += "</div>\n"
        else:
            #print("error: unrecognized section header")
            html += self.doc_html_helper(k)
        # close div for section
        html += "</div>\n"
        html += "<br>\n"
        return html

    def parse_subsection(self, k):
        html = ""
        # open subsection div
        html += "<div class=\"sec2 " + k.tagName + "\">\n"
        # parse body of subsection
        if (len(k.childNodes) >= 2 and 
            isinstance(k.childNodes[0], xml.dom.minidom.Element) and
            isinstance(k.childNodes[1], xml.dom.minidom.Element) and
            k.childNodes[0].tagName == "enum" and 
            k.childNodes[1].tagName == "header"):
            # enum/header container
            enum = self.doc_html_helper(k.childNodes[0])
            html += "<div id=\"enum_header\" class=\"sec2\" name=\"" + enum + ">\n"
            # enum
            html += enum
            # header
            html += self.doc_html_helper(k.childNodes[1])
            # close enum/header container
            html += "</div>\n"
            # pop enum and header
            k.childNodes.pop(0)
            k.childNodes.pop(0)
            # parse rest of body
            while (k.childNodes):
                # standard text content
                if (isinstance(k.childNodes[0], xml.dom.minidom.Text)):
                    html += self.doc_html_helper(k.childNodes[0])
                # if we find a paragraph, break and put into collapsible container
                elif (k.childNodes[0].tagName == "paragraph"):
                    break
                # standard container content
                else:
                    html += "<span class=\"sec2 " + k.childNodes[0].tagName + "\">\n"
                    html += self.doc_html_helper(k.childNodes[0])
                    html += "</span>\n"
                # pop current body element
                k.childNodes.pop(0)
            # parse paragraphs
            if (k.childNodes):
                # button for collapsible container
                html += "<br><button class=\"collapsible active\" style=\"font-size: 24px;\"></button>\n"
                # open div for content of subsection
                html += "<div id=\"content\" class=\"content\" style=\"display: block;\">\n"
                # recurse on rest of child nodes
                html += self.doc_html_helper(k)
                # close div for content of subsection
                html += "</div>\n" 
        # no standard subsection header, just parse the contents
        else:
            #print("error: unrecognized subsection header")
            html += self.doc_html_helper(k)
        # close subsection div
        html += "\n</div>\n<br>\n"
        return html

    def parse_paragraph(self, k):
        html = ""
        # open paragraph div
        html += "<div class=\"sec2 " + k.tagName + "\">\n"
        # parse body of paragraph
        if (k.childNodes[0].tagName == "enum"):
            # enum header
            html += "<span class=\"" + k.childNodes[0].tagName + "\">\n"
            html += self.doc_html_helper(k.childNodes[0])
            html += "</span>\n"
            # pop element
            k.childNodes.pop(0)
            # parse rest of body
            while (k.childNodes):
                # standard text content
                if (isinstance(k.childNodes[0], xml.dom.minidom.Text)):
                    html += self.doc_html_helper(k.childNodes[0])
                # if we find a subparagraph, break and put into collapsible container
                elif (k.childNodes[0].tagName == "subparagraph"):
                    break
                # standard container content
                else:
                    html += "<span class=\"sec2 " + k.childNodes[0].tagName + "\">\n"
                    html += self.doc_html_helper(k.childNodes[0])
                    html += "</span>\n"
                # pop element
                k.childNodes.pop(0)
            # parse subparagraphs
            if (k.childNodes):
                # button for collapsible section
                html += "<br><button class=\"collapsible active\" style=\"font-size: 24px;\"></button>\n"
                # open div for content of section
                html += "<div id=\"content\" class=\"content\" style=\"display: block;\">\n"
                # recurse on rest of child nodes
                html += self.doc_html_helper(k)
                # close div for content of section
                html += "</div>\n" 
        # no standard section header, just parse the contents
        else:
            #print("error: unrecognized paragraph header")
            html += self.doc_html_helper(k)
        # close paragraph div
        html += "\n</div>\n<br>\n"
        return html

    def parse_subparagraph(self, k):
        html = ""
        html += "<div class=\"sec2 " + k.tagName + "\">\n"
        for child in k.childNodes:
            html += "<br>\n"
            html += self.doc_html_helper(child)
        html += "\n</div>\n<br>\n"
        return html

    def doc_html_helper(self, node):
        html = ""
        for k in node.childNodes:

            if isinstance(k, xml.dom.minidom.Text):
                
                if k.parentNode.tagName == "quote":
                    html += "\""
                    html += k.data
                    html += "\""
                elif k.parentNode.tagName == "term":
                    html += "<a class=\"term\">"
                    html += k.data
                    html += "</a>\n"
                elif k.parentNode.tagName == "enum":
                    html += "<span class=\"enum\">"
                    html += k.data
                    if (k.data[len(k) - 1] != "." and k.data[len(k) - 1] != ")"):
                        html += "."
                    html += "</span>\n"
                elif k.parentNode.tagName == "header":
                    html += "<span class=\"term\">"
                    html += k.data
                    html += "</span>\n"
                elif k.parentNode.tagName == "toc":
                    html += "<span class=\"term\">"
                    html += k.data
                    html += "</span>\n<br>\n"
                else:
                    html += k.data

            elif isinstance(k, xml.dom.minidom.Element):
                if (k.tagName == "subsection"):
                    html += self.parse_subsection(k) 
                elif (k.tagName == "appropriations-major"):
                    html += self.parse_subsection(k.firstChild) 
                # MAYBE: use subsection for appropriations-intermediate tag????
                elif (k.tagName == "appropriations-intermediate"):
                    html += self.parse_subsection(k) 
                elif (k.tagName == "paragraph"):
                    html += self.parse_paragraph(k)
                # MAYBE: use paragraph for appropriations-small tag????
                elif (k.tagName == "appropriations-small"):
                    html += self.parse_paragraph(k)
                elif (k.tagName == "subparagraph"):
                    html += self.parse_subparagraph(k)
                # TEXT CONTAINER ELEMENT
                elif (k.tagName == "text"):
                    html += "<span class=\"sec2 " + k.tagName + "\">\n"
                    html += self.doc_html_helper(k)
                    html += "\n</span>\n<br>\n"
                elif (k.tagName == "quote"):
                    contents = self.doc_html_helper(k)
                    if (contents[0] == "\""):
                        html += contents
                    else:
                        html += "\""
                        html += contents
                        html += "\""
                elif (k.tagName == "section"):
                    html += self.parse_section(k)
                elif(k.tagName == "division"):
                    html+= self.parse_division(k)
                elif(k.tagName == "title"):
                    html+= self.parse_title(k)
                elif (k.tagName == "toc-entry"):
                    html += self.doc_html_helper(k)
                    html += "<br>\n"
                else:
                    html += self.doc_html_helper(k)
            else:
                print("error: unrecognized element")

        return html
    
    def bill_doc_html(self):
        # main body of page
        legis_body = self.orig.getElementsByTagName("legis-body")[0]

        # main content header
        self.file.write("<div id=\"main\" class=\"main\">\n")
        
        html = ""   
        html += ("<button class=\"highlightBtn material-symbols-outlined\" id=\"highlightBtn\"" + 
                 "onclick=\"highlightSelection()\">format_ink_highlighter</button>\n")
        html += self.doc_html_helper(legis_body)
        
        self.file.write(html)
        # close main content header
        self.file.write("</div>\n")

    def amend_doc_html(self):
        # main body of page
        eng_amend_body = self.orig.getElementsByTagName("engrossed-amendment-body")[0]
        # main content header
        self.file.write("<div id=\"main\" class=\"main\">\n")
        
        html = ""
        
        html += self.doc_html_helper(eng_amend_body)

        self.file.write(html)
        # close main content header
        self.file.write("</div>\n")

    def comm_pane_html(self):
        commFilePath = self.filePath[:-5] + "_comm.txt"
        html = "<div id=\"commPane\" class=\"commPane\">\n<form id=\"formComm\" action=\"/comment\" method=\"post\">\n"
        html += "<textarea name=\"commSrc\" style=\"display:none;\">" + self.filePath + "</textarea>"
        html += "<textarea name=\"commDst\" style=\"display:none;\">" + commFilePath + "</textarea>"
        html += "<textarea id=\"rawComm\" name=\"rawComm\">Add comment...</textarea>\n"
        html += "<button class=\"saveBtn\" id=\"save\" type=\"submit\">save</button>\n"
        html += "</form>\n"
        if (os.path.isfile(commFilePath)):
            c = open(commFilePath, 'r', encoding="utf-8")
            comments = c.read()
            html += comments
            c.close()
        html += "</div>\n"
        self.file.write(html)

    def doc_viewer_html(self):
        self.file.write("<div class=\"viewer\">")

        if (self.orig.doctype.name == 'bill'):
            self.bill_nav_html()
            self.bill_doc_html()
        elif (self.orig.doctype.name == 'amendment-doc'):
            self.amend_nav_html()
            self.amend_doc_html()
        self.comm_pane_html()

        self.file.write("</div>")

    def start_html(self):
        self.file.write("<!DOCTYPE HTML>\n" +
                        "<html>\n" +
                        "<head>\n" +
                        "<title>Omnibuster Bill Render</title>\n" +
                        "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0\"/>\n" +
                        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n" +
                        "<link rel=\"stylesheet\" href=\"HR_Temp_Style2.css\">\n" +
                        "</head>\n"
                        )
    
    def finish_html(self):
        # ending document: link to script sheet and close body
        self.file.write("<script src=\"HR_Temp_Script.js\"></script>\n" +
                        "</html>")

    def start_parse(self):
        ''' 
        ---- This section will take the original xml string and make it a pretty file, but is not needed for functionality ----
        file = open("temp.xml", "w", encoding="utf-8")
        file.write(self.orig.toprettyxml())
        file.close()
        '''

        self.start_html();

        self.header_html()
        
        self.doc_viewer_html()
        
        self.finish_html()

        self.file.close()
