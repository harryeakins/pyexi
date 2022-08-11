from lark import Lark

class Production:
    def __init__(self, lhs, rhs, event_code):
        self.lhs = lhs
        self.rhs = rhs
        self.event_code

element_grammar = {
    "StartTagContent": [
        Production("EE", None, "0.0"),
        Production("AT(*)", "StartTagContent", "0.1"),
        Production("NS", "StartTagContent", "0.2"),
        Production("SC", "Fragment", "0.3"),
        Production(None, "ChildContentItems_0_4", None),

    ],
    "ChildContentItems_0_4": [
        Production("SE(*)", "ElementContent", "0.4"),
        Production("CH", "ElementContent", "0.5"),
        Production("ER", "ElementContent", "0.6"),
        Production("CM", "ElementContent", "0.7.0"),
        Production("PI", "ElementContent", "0.7.1"),
    ],
    "DocEnd": [
        Production("ED", None, "0"),
        Production("CM", "DocEnd", "1.0"),
        Production("PI", "DocEnd", "1.1"),
    ],
}

subgrammar_mappings = {
    "SE(*)": element_grammar,
}

document_grammar = {
    "Document": [
        Production("SD", "DocContent", "0"),
    ],
    "DocContent": [
        Production("SE(*)", "DocEnd", "0"),
        Production("DT", "DocContent", "1.0"),
        Production("CM", "DocContent", "1.1.0"),
        Production("PI", "DocContent", "1.1.1"),
    ],
    "DocEnd": [
        Production("ED", None, "0"),
        Production("CM", "DocEnd", "1.0"),
        Production("PI", "DocEnd", "1.1"),
    ],
}

grammar = r"""
    start: Document

    Document: SD DocContent
    
    DocContent: SE_STAR DocEnd | 
                DT DocContent |
                CM DocContent |
                PI DocContent;
    
    DocEnd: ED |
            CM DocEnd |
            PI DocEnd;

    SE_STAR: "0_1"

"""