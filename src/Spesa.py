class Spesa:
    def __init__(self, nome, prezzo, data, note = "", tagString = ""):
        self.nome = nome.strip() #string
        self.prezzo = prezzo #float
        self.data = data #string
        self.note = note.strip() #string
        self.tag = []
        self.stringToTags(tagString)
    
    def stringToTags(self, tagString):
        tagString = tagString.strip()
        for tag in tagString.split(','):
            tag = tag.strip()
            if tag != "":
                tag = tag.lower()
                self.tag.append(tag)
    
