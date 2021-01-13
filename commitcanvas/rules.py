# pylint: disable = import-error
import re
import fixes
class Rules:
    
    title = None
    arg = None
    error_message = None
    target = None

class Errors:
    def __init__(self, message, content = ""):
        self.message = message
        self.content = content

    def __str__(self):
        return f" \u2717 {self.message}. {self.content}"

# separate different parts of the commit message into different classes to use them as target later
class Commit:
    commit = "feat: Huffman-code serialization, and do a lot of refactoring. Highlights include:\n* Much more efficient StringStore\n* Vocab maintains a by-orth mapping of Lexemes\n* Avoid manually slicing Py_UNICODE buffers,simplifying tokenizer and vocab C APIs\n* Remove various bits of dead code\n* Work on removing GIL around parser\n* Work on bridge to Theano"

print(Commit.commit,"\n\n")
class Header(Commit):
    header = Commit.commit.split('\n', 1)[0]

class Header_type(Commit):
    if ":" in Header.header:
        header_type = Header.header.split(":")[0]
    else:
        header_type = None
    
class Subject(Commit):
    if ":" in Header.header:
        line = Header.header.split(":")[1]
        if line.startswith(" "):
            subject = line.split(" ",1)[1]
        else:
            subject = line
    else:
        subject = Header.header

class Body(Commit):
    splitted = Commit.commit.splitlines()
    if len(splitted) > 1:
        body = Commit.commit.split('\n', 1)[-1]
    else:
        body = None

# Define the rules
class Max_length(Rules):
    error_msg = "Maximum {} characters allowed. Found {} characters."
    def check(self):
        target = self.target
        if target:
            if len(target) > self.arg:
                return Errors(self.title, self.error_msg.format(self.arg,len(target),target))

class Max_lines(Rules):
    error_msg = "Maximum {} lines allowed. Found {} lines. Try raphrasing, these are suggested sentences with highest scores:\n{}"
    def check(self):
        target = self.target
        if target:
            if len(target.splitlines()) > 5:
                rank = fixes.Sentence_rank()
                ranked_sentences = rank.sentence_rank(target)
                return Errors(self.title, self.error_msg.format(5,len(target.splitlines()),ranked_sentences))

class Min_length(Rules):
    error_msg = "At least {} characters required. Found {} characters in \"{}\""
    def check(self):
        target = self.target
        if target:
            if len(target) < self.arg:
                return Errors(self.title, self.error_msg.format(self.arg,len(target),target))

class Capitalize(Rules):
    error_msg = "\"{}\" starts with lower case letter"
    def check(self,target=None):
        target = self.target
        if target:
            if not target[0].isupper():
                return Errors(self.title, self.error_msg.format(target))

class LowerCase(Rules):
    error_msg = "\"{}\" starts with upper case letter"
    def check(self,target=None):
        target = self.target
        if target:
            if not target[0].islower():
                return Errors(self.title, self.error_msg.format(target))

class Invalid_character(Rules):
    error_msg = "\"{}\" found at the end of \"{}\""
    def check(self):
        target = self.target
        invalid_characters = [".",":"]
        if target:
            for char in invalid_characters:
                if target.endswith(char):
                    return Errors(self.title, self.error_msg.format(char,target))

class Required(Rules):
    
    def check(self):
        target = self.target
        if not target:
            return Errors(self.title)

class Blank_line(Rules):
    error_msg = "No blank line found before \"{}\""
    def check(self):
        target = self.target
        if target:
            splitted = target.splitlines()      
            if splitted[0]:
                return Errors(self.title, self.error_msg.format(splitted[0]))

class Validate_Type(Rules):
    error_msg = "Found \"{}\" in \"{}\"."
    def check(self):
        target = self.target
        if target:
            types = ["feat","style","test","refactor","fix","perf","docs","chore","ci","build"]
            if target.lower() not in types:
                return Errors(self.title, self.error_msg.format(target,Header.header))

# Apply rules to targets such as subject,body,type
class subject_max_length(Max_length,Subject):
    title = "Subject maximum length exceeded"
    arg = 50
    target = Subject.subject

class subject_min_length(Min_length,Subject):
    title = "Subject line is less than minimum length"
    arg = 10
    target = Subject.subject

class subject_capitalize(Capitalize,Subject):
    title = "Capitalize commit message subject"
    target = Subject.subject

class subject_invalid_character(Invalid_character,Subject):
    title = "Invalid character in subject line"
    target = Subject.subject

class subject_required(Required,Subject):
    title = "Subject required in header"
    target = Subject.subject

class body_blank_line(Blank_line,Body):
    title = "Blank line required"
    target = Body.body

class body_max_lines(Max_lines,Body):
    title = "Body maximum lines exceeded"
    target = Body.body

class invalid_type(Validate_Type,Header_type):
    title = "Type should be one of: feat,style,test,refactor,fix,perf,docs,chore,ci,build"
    target = Header_type.header_type

class type_lowercase(LowerCase,Header_type):
    title = "Type should be lower case"
    target = Header_type.header_type

class type_require(Required,Header_type):
    title = "Commit message type required"
    target = Header_type.header_type





