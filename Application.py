from tkinter import *
from tkinter import filedialog, messagebox
import Cipher as cp
import OutputFormatter as fmt

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.bind_class("Text", "<Control-a>", self.selectall)
        self.master.bind_class("Text", "<Control-v>", self.pasteall)
        self.filepath = None

		# Input
        inputFrame = Frame()
        Label(inputFrame, text="Original Text", font=("Helvetica", 16)).grid(row=0)
        Button(inputFrame, text='Load File', command=self.askopenfile).grid(row=1)
        inputFrame.grid(row=0)
        self.eInput = Text(master, height=4, width=90, font=("Consolas", 12))
        self.eInput.grid(row=1, column=0, padx=10, pady=(0,25))

		# Key
        Label(master, text="Key", font=("Helvetica", 16)).grid(row=2, column=0)
        self.eKey = Text(master, height=1, width=90, font=("Consolas", 12))
        self.eKey.grid(row=3, column=0, padx=10, pady=(0,25))

		# Opsi
        actionFrame = Frame()
        Label(master, text="Cipher Select", font=("Helvetica", 16)).grid(row=4)
        self.cipherOption = CipherOptions(master=actionFrame)
        self.cipherOption.grid(row=4, pady=(0,25))
        Label(actionFrame, text="Output Format", font=("Helvetica", 16)).grid(row=5)
        self.outputChoice = OutputChoices(master=actionFrame)
        self.outputChoice.grid(row=6, pady=(0,25))
        selectionFrame = Frame(master=actionFrame)
        Button(selectionFrame, text='Encrypt', command=self.encrypt).grid(row=2, column=0, padx=5, pady=4)
        Button(selectionFrame, text='Decrypt', command=self.decrypt).grid(row=2, column=1, padx=5, pady=4)
        selectionFrame.grid(row=7)
        actionFrame.grid(row=8, column=0, columnspan=2, pady=(0,25))

		# Output
        outputFrame = Frame()
        Label(outputFrame, text="Processed Text", font=("Helvetica", 16)).grid(column=0)
        outputFrame.grid(row=9)
        self.eOutput = Text(master, height=4, width=90, font=("Consolas", 12))
        self.eOutput.grid(row=10, padx=10)
        saveFrame = Frame()
        Button(saveFrame, text='Save File', command=self.savefile).grid(column=1)
        saveFrame.grid(row=11)

    def selectall(self, event):
        event.widget.tag_add("sel", "1.0", "end-1c")

    def pasteall(self, event):
        event.widget.delete("1.0", END)
        text = self.master.selection_get(selection='CLIPBOARD')
        event.widget.insert(END, text)

    def askopenfile(self):
        if (type(self.cipherOption.getCipher()) is cp.VigenereExtended):
            filepath = filedialog.askopenfilename()
            if filepath != None:
                self.filepath = filepath
                self.eInput.delete(1.0, END)
                self.eInput.insert(END, filepath)
            else:
                print("Something wrong")
        else:
            try:
                file = filedialog.askopenfile(parent=gui, mode='r', title='Open File')
                data = file.read()
                file.close()
                self.eInput.delete(1.0, END)
                self.eInput.insert(END, data)
            except:
                messagebox.showerror("Error", "Pastikan file teks bukan untuk Extended Vigenere Cipher")

    def savefile(self):
        if (type(self.cipherOption.getCipher()) is cp.VigenereExtended):
            messagebox.showwarning("Warning", "Tidak bisa menyimpan file untuk Extenede Vigenere Cipher")
        elif (len(self.eOutput.get("1.0", "end-1c")) == 0):
            messagebox.showwarning("Warning", "Output masih kosong!")
        else:
            filename =  filedialog.asksaveasfilename(title = "Save As",filetypes = (("Text Files","*.txt"),("All Files","*.*")))
            f = open(filename,"w")
            f.write(self.eOutput.get("1.0", "end-1c"))
            f.close()

    def validate(self):
        if (len(self.eInput.get("1.0", "end-1c")) == 0):
            messagebox.showwarning("Warning", "Input tidak boleh kosong!")
            return False
        elif (len(self.eKey.get("1.0", "end-1c")) == 0):
            messagebox.showwarning("Warning", "Key tidak boleh kosong!")
            return False
        elif (type(self.cipherOption.getCipher()) is cp.VigenereExtended and self.filepath == None):
            messagebox.showwarning("Warning", "File masih kosong atau hanya bisa enkripsi/dekripsi file to file untuk Extended Vigenere Cipher")
            return False
        else:
            return True

    def encrypt(self):
        if (not self.validate()):
            return
        cipher = self.cipherOption.getCipher()
        cipher.changeKey(self.eKey.get("1.0", "end-1c"))
        plainText = self.eInput.get("1.0", "end-1c")
        if (type(cipher) is cp.VigenereExtended):
            plainText = open(self.filepath, "rb").read()
            outputPath = "/".join(self.filepath.split('/')
                                  [:-1])+"/enc_"+self.filepath.split('/')[-1]
            data = cipher.encrypt(plainText)
            safeData(outputPath, data)
            self.eOutput.delete(1.0, END)
            self.eOutput.insert(END, "File succesfully encrypted!")
            self.filepath = None
        else:
            cipherText = cipher.encrypt(plainText)
            text = cipherText
            if (type(cipher) is cp.Playfair):
                pass
            else:
                text = self.outputChoice.getFormatter().format(plainText, cipherText)
            self.eOutput.delete(1.0, END)
            self.eOutput.insert(END, text)

    def decrypt(self):
        self.validate()
        cipher = self.cipherOption.getCipher()
        cipher.changeKey(self.eKey.get("1.0", "end-1c"))
        originalText = self.eInput.get("1.0", "end-1c")
        if (type(cipher) is cp.VigenereExtended):
            originalText = open(self.filepath, "rb").read()
            outputPath = "/".join(self.filepath.split('/')
                                  [:-1])+"/dec_"+self.filepath.split('/')[-1]
            data = cipher.decrypt(originalText)
            safeData(outputPath, data)
            self.eOutput.delete(1.0, END)
            self.eOutput.insert(END, "File succesfully decrypted!")
            self.filepath = None
        else:
            processed = cipher.decrypt(originalText)
            text = processed
            if (type(cipher) is cp.Playfair):
                pass
            elif (type(cipher) is cp.VigenereExtended):
                pass
            else:
                text = fmt.Original().format(originalText, processed)
            self.eOutput.delete(1.0, END)
            self.eOutput.insert(END, text)

class CipherOptions(Frame):
    ciphers = [
        ("Vigenere Cipher Standard", 1),
        ("Full Vigenere Cipher", 2),
        ("Auto-key Vigenere Cipher", 3),
        ("Extended Vigenere Cipher", 4),
        ("Playfair Cipher", 5),
        ("Super Enkripsi", 6),
        ("Affine Cipher", 7),
        ("Hill Cipher", 8),
        # ("Enigma Cipher", 9),
    ]

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.v = IntVar()
        self.v.set(1)
        # Label(self, text="Cipher Select", font=("Helvetica", 16)).grid(row=0, column=2)

        for i, v in enumerate(self.ciphers[:len(self.ciphers)//2]):
            cipher, val = v
            Radiobutton(self, text=cipher, variable=self.v, value=val, padx=10).grid(row=1, column=i, sticky=W)

        for i, v in enumerate(self.ciphers[len(self.ciphers)//2:]):
            cipher, val = v
            Radiobutton(self, text=cipher, variable=self.v, value=val, padx=10).grid(row=2, column=i, sticky=W)

    def getCipher(self):
        if (self.v.get() == 1):
            return cp.VigenereStandard()
        elif (self.v.get() == 2):
            return cp.VigenereFull(matrixName="test")
        elif (self.v.get() == 3):
            return cp.VigenereAutoKey()
        elif (self.v.get() == 4):
            return cp.VigenereExtended()
        elif (self.v.get() == 5):
            return cp.Playfair()
        elif (self.v.get() == 6):
            return cp.SuperEncryption()
        elif (self.v.get() == 7):
            return cp.Affine()
        elif (self.v.get() == 8):
            return cp.Hill()
        '''
        elif (self.v.get() == 9):
            return cp.Enigma()
        '''

class OutputChoices(Frame):
    formats = [
        # ("Original", 0),
        ("Tanpa Spasi", 1),
        ("Kelompok 5 Huruf", 2),
    ]

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.v = IntVar()
        self.v.set(1)
        # Label(self, text="Output Format", font=("Helvetica", 16)).grid(row=0, column=1)

        for i, v in enumerate(self.formats):
            fmt, val = v
            Radiobutton(self, text=fmt, variable=self.v, value=val, width=18).grid(row=1, column=i, sticky=W)

    def getFormatter(self):
        '''
        if (self.v.get() == 0):
            return fmt.Original()
        '''
        if (self.v.get() == 1):
            return fmt.NoSpaces()
        elif (self.v.get() == 2):
            return fmt.GroupOfWords()

def safeData(path, data):
    binary_file = open(path, "wb")
    binary_file.write(data)
    binary_file.close()

if __name__ == "__main__":
    gui = Tk()
    gui.title("Tucil 1 IF4020 Kriptografi - Program Cipher")
    app = Application(master=gui)
    app.mainloop()
