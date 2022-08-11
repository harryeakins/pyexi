from xml import sax

class ExiSchemaHandler(sax.handler.ContentHandler):
    def __init__(self):
        self.elementStack = []
        self.tagStack = []

    def startElement(self, name, attrs):
        self.tagStack.append(name)
        if name == "xs:element":
            self.elementStack.append(attrs["name"])
        
        print(f"BEGIN: <{name}>, {attrs.keys()}")

    def endElement(self, name):
        print(f"END: </{name}>")

    def characters(self, content):
        if content.strip() != "":
            print("CONTENT:", repr(content))

class ExiEncoder(object):
    def __init__(self):
        pass

