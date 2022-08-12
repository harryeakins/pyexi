from collections import defaultdict
from itertools import product
from math import log2, ceil
import xml.sax as sax

class Production:
    def __init__(self, rhs, *args):
        self.rhs = rhs
        self.event_code = args

    def set_bit_lengths(self, *args):
        assert len(args) >= len(self.event_code)
        self.bit_lengths = args[:len(self.event_code)]

    def get_bits(self):
        result = []
        for code, bits in zip(self.event_code, self.bit_lengths):
            if bits > 0:
                result.append(format(code, f"0{bits}b"))
            else:
                result.append("")
        return result

class Grammar:
    def __init__(self, initial_state, dict):
        self.initial_state = initial_state
        self.dict = dict
        self._update_bitlengths()

    def _update_bitlengths(self):
        for lhs in self.dict:
            max_values = defaultdict(int)
            for event in self.dict[lhs]:
                production = self.dict[lhs][event]
                for i, code in enumerate(production.event_code):
                    max_values[i] = max(max_values[i], code)
            
            bit_lengths = [ceil(log2(max_values[i]+1)) for i in range(len(max_values))]

            for event in self.dict[lhs]:
                production = self.dict[lhs][event]
                production.set_bit_lengths(*bit_lengths)


element_grammar = Grammar("StartTagContent", {
    "StartTagContent": {
        "EE": Production(None, 0, 0),
        "AT(*)": Production("StartTagContent", 0, 1),
        "NS": Production("StartTagContent", 0, 2),
        "SC": Production("Fragment", 0, 3),
        "SE(*)": Production("ElementContent", 0, 4),
        "CH": Production("ElementContent", 0, 5),
        "ER": Production("ElementContent", 0, 6),
        "CM": Production("ElementContent", 0, 7, 0),
        "PI": Production("ElementContent", 0, 7, 1),
    },
    "ElementContent": {
        "EE": Production(None, 0),
        "SE(*)": Production("ElementContent", 1, 0),
        "CH": Production("ElementContent", 1, 1),
        "ER": Production("ElementContent", 1, 2),
        "CM": Production("ElementContent", 1, 3, 0),
        "PI": Production("ElementContent", 1, 3, 1),
    },
})

document_grammar = Grammar("Document", {
    "Document": {
        "SD": Production("DocContent", 0),
    },
    "DocContent": {
        "SE(*)": Production("DocEnd", 0),
        "DT": Production("DocContent", 1, 0),
        "CM": Production("DocContent", 1, 1, 0),
        "PI": Production("DocContent", 1, 1, 1),
    },
    "DocEnd": {
        "ED": Production(None, 0),
        "CM": Production("DocEnd", 1, 0),
        "PI": Production("DocEnd", 1, 1),
    },
})

subgrammar_mappings = {
    "Document": document_grammar,
    "SE(*)": element_grammar,
}

class ExiHandler(sax.handler.ContentHandler):
    def __init__(self):
        self.stateStack = ["Document"]
        self.grammarStack = [document_grammar]
        self.events = []
        self.output = []

    def startDocument(self):
        self._process_event("SD")

    def startElement(self, name, attrs):
        self._process_event("SE(*)")
        for attr in attrs.items():
            self._process_event("AT(*)")

    def endElement(self, name):
        self._process_event("EE")

    def endDocument(self):
        self._process_event("ED")

    def _process_event(self, event):
        grammar = self.grammarStack[-1]
        state = self.stateStack.pop()
        production = grammar.dict[state][event]

        self.events.append(event)
        self.output.append(production.get_bits())

        if production.rhs is not None:
            self.stateStack.append(production.rhs)
        else:
            self.grammarStack.pop()

        if event in subgrammar_mappings:
            subgrammar = subgrammar_mappings[event]
            self.grammarStack.append(subgrammar)
            self.stateStack.append(subgrammar.initial_state)

    def characters(self, content):
        if content.strip() != "":
            print("CONTENT:", repr(content))
