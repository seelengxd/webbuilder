#element templates
class Element():
    #use for input 
    def __init__(self, type, attri={}):
        # attri is dictionary of element attributes
        self.type = type
        self.attri = attri
    def getCode(self):
        attris = " ".join(['="'.join(i) + '"' for i in self.attri.items()])
        return f"<{self.type} {attris}>"

class SandwichElement(Element):
    #label, textarea, button
    def __init__(self, type, mid, attri=None):
        super().__init__(type, attri)
        self.mid = mid
    def getCode(self):
        attris = " ".join(['="'.join(i) + '"' for i in self.attri.items()])
        return f"<{self.type} {attris}>{self.mid}</{self.type}>"

class Dropdown():
    def __init__(self, name, options):
        self.name = name
        self.options = options
    def getCode(self):
        res = SandwichElement("label", self.name + ": ", {"for":self.name}).getCode()
        res += f"<select name='{self.name}'>\n"
        for option in self.options:
            res += f"\t<option value='{option}'>{option}</option>\n"
        res += "</select>"
        return res

#load templates (html css) 
with open("part1Templates/formStructure.html") as f:
    temp = f.read()
with open("part1Templates/hardcodedCSS.txt") as f:
    style = f.read()
with open("part1Templates/formjinja.txt") as f:
    jinja = f.read()

buttons = []

#functions to call to return wanted elements of form
def defText(name):
    label = SandwichElement("label", f"{name}: ", {"for":name})
    text = Element("input", {"type":"text", "name":name})
    return label.getCode() + text.getCode()

def defSubmit():
    button = SandwichElement("button", "submit", {"type":"submit"})
    return button.getCode()

def defImg(name):
    label = SandwichElement("label", f"{name}: ", {"for":name})
    input = Element("input", {"type":"file", "name":name})
    return label.getCode() +input.getCode()

def defTextarea(name, placeholder=''):
    attri={'resize':'none', 'height':"150px",'name':name}
    label = SandwichElement("label", f"{name}: ", {"for":name})
    textarea = SandwichElement("textarea", placeholder, attri)
    return label.getCode() + textarea.getCode()

def defDropdown(name, *options):
    dropdown = Dropdown(name, options)
    return dropdown.getCode()

#def defButton(word, href):
#    return f"<button formaction='{href}'>{word}</button>"

def notFormButton(word, href):
    return f"<a href='{href}'><button type='button'>{word}</button></a>"

def buttonWrapper():
    global buttons
    res = "<div style='display:flex; justify-content:center;'>"
    for button in buttons:
        res += "\n\t" + button
    res += "\n</div>"
    buttons = [res]

formurl = "/"

def createForm(file):
    preTabs=3
    commands = {
        "text":defText,
        "submit":defSubmit,
        "img":defImg,
        "textarea":defTextarea,
        "dropdown":defDropdown,
        "button":notFormButton,
        "wrap":buttonWrapper
        }
    global buttons
    #in format of tuple of (dbColName, NameAttri,maxLimitifAny)
    imageCols = []
    otherCols = []
    codes = []
    with open(file) as f:
        #first 3 lines of input
        dbName = f.readline().strip()
        tableName = f.readline().strip()
        formaction = f.readline().strip()
        #making sense of rest of input
        for line in f.read().splitlines():
            query = line.split(",")
            #col name added
            if query[0] in ["text","textarea","dropdown","img"]:
                columnName = query.pop()
                columnName, *limit = columnName.split("^") 
                if query[0] == "img":
                    imageCols.append((columnName, query[1], *limit))
                else:
                    otherCols.append((columnName, query[1], *limit))
            query[-1] = query[-1].split("^")[0]
            #for accidental command caps
            code = commands[query[0].lower()](*query[1:])
            if query[0] in ["submit", "button"]:
                buttons.append(code)
            elif query[0] != "wrap":
                codes.append(code)
    innerForm = "\n".join(codes + buttons)
    innerForm = innerForm.replace("\n","\n"+preTabs*"\t")
    return temp.format(jinja=jinja,style=style, formaction=formaction, form=innerForm)\
           , imageCols, otherCols, dbName, tableName, formaction

def createPython(imageCols, otherCols, dbName, tableName,formaction, to):
    #loading all templates first
    with open("part2Templates/insertTemplate.py") as f:
        insertTemplate = f.read()
    with open("part2Templates/overallTemplate.py") as f:
        overallTemplate = f.read()
    with open("part2Templates/imageTemp.py") as f:
        imageTemp = f.read()
    with open("part2Templates/limitTemp.py") as f:
        limitTemp = f.read()
    createDbStuff = ",\n\t\t\t".join(["{} TEXT".format(i[0]) for i in [*imageCols, *otherCols]])
    #generating parts for insert function code
    imageCode = "\n\t\t".join([imageTemp.format(imageNameAttri=image[1]).replace("\n","\n\t\t") for image in imageCols])
    columnNames = ",".join([i[0] for i in otherCols] + [i[0] for i in imageCols])
    toAddStuff = ",".join([f"data['{i[1]}']" for i in otherCols])
    questionMarks = ",".join(["?"] * (len(imageCols) + len(otherCols)))
    thingsWithLimit = [i for i in imageCols+otherCols if len(i) == 3]
    #for max char specification, (fixed indentation)
    limitCode = "\n".join([limitTemp.format(formName=i[1], limit=i[2]) for i in thingsWithLimit])\
                .replace("\n","\n\t\t")
    insertCode = insertTemplate.format(dbName=dbName, imageCode=imageCode, toAddStuff=toAddStuff, questionMarks=questionMarks,\
                                       to=to, formaction=formaction, tableName=tableName, columnNames=columnNames,limitCode=limitCode,\
                                           createDbStuff=createDbStuff)
    completeCode = overallTemplate.format(form_url=formurl, form_template=to, otherCode=insertCode)
    return completeCode
    
import os
instructions = input("file name with instructions: ")
newFile = input("new file name?: ")
to = "form.html"
os.mkdir(os.getcwd() + f"/{newFile}")
os.mkdir(os.getcwd() + f"/{newFile}/templates")
os.mkdir(os.getcwd() + f"/{newFile}/static")
os.mkdir(os.getcwd() + f"/{newFile}/static/images")
with open(f"{newFile}/templates/{to}", "w") as f:
    form, *everythingElse = createForm(instructions)
    f.write(form)
with open(f"{newFile}/server.py", "w") as f:
    f.write(createPython(*everythingElse, to))
