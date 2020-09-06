class OutputFormatter:
    def __init__(self): pass

# Output Biasa/ngikutin Input
class Original(OutputFormatter):
    def format(self, originalText, processedText):
        text = list(originalText)
        cpr = list(processedText)
        text = [cpr.pop(0) if c.isalpha() else c for c in text]
        return "".join(text)

# Output Tanpa Spasi
class NoSpaces(OutputFormatter):
    def format(self, originalText, processedText):
        text = list(originalText)
        cpr = list(processedText)
        text = [cpr.pop(0) if c.isalpha() else c for c in text]
        text = "".join(text)
        return text.replace(' ', '')

# Output Kelompok 5 Huruf
class GroupOfWords(OutputFormatter):
    def format(self, originalText, processedText):
        N = 5
        return " ".join([processedText[i:i+N] for i in range(0, len(processedText), N)])
