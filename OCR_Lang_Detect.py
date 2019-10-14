from tkinter import *
import tkinter as tk
import glob
import os
import ghostscript as gs
import langdetect
import langid
from os import listdir
from os.path import isfile, join
from wand.image import Image as Img
from langdetect import detect
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0
#Initialize the directories before processing
image_files = glob.glob('...input_directory/OCR_File/*')
for f in image_files:
    os.remove(f)
text_files = glob.glob('...input_directory/OCR_Text_File/*')
for t in text_files:
    os.remove(t)
#Menu select Options
dirName = '...input_directory/input_directory'
fileNames = [f for f in listdir(dirName) if isfile(join(dirName, f))]


#-----------------------------------------------------------------------------------
def select():
    sf = "value is %s" % var.get()
    root.title(sf)
    #print(sf)
    root.destroy()
root = tk.Tk()
frame = Frame(root)
frame.pack()
root.geometry("%dx%d+%d+%d" % (530, 180, 300, 250))
root.title("Select Options")
var = tk.StringVar(root)
# initial value
var.set('Please select a file')
option = tk.OptionMenu(root, var, *fileNames)
option.pack(side='left', padx=10, pady=10)
button = tk.Button(root, text="OK", command=select)
button.pack(side='left', padx=20, pady=10)

root.mainloop()
#PDF to Image and then text conversion started
image_counter=0
with Img(filename="...input_directory/%s"% var.get(), resolution=300) as img:
 img.compression_quality = 99
 img.save(filename='...input_directory/OCR_File/sample_scan.jpg')
 list = os.listdir('...input_directory/OCR_File') # dir is your directory path
number_files = len(list)

from PIL import Image
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C:/Program Files (x86)/tessdata"'

filelimit = number_files

print(filelimit)
#Output file to create in a specific directory
outfile = "...input_directory/OCR_Text_File/ocr_out_text.txt"

f = open(outfile, "a",encoding="utf-8")
for i in range(0, filelimit):
    path='...input_directory/OCR_File/'
    filename = path+"sample_scan-"+str(i)+".jpg"

    text = str(((pytesseract.image_to_string(Image.open(filename),lang='eng',config=tessdata_dir_config))))
    #text = text.replace('-\n', '')
    f.write(text)
f.close()

path_to_file = "...input_directory/OCR_Text_File/ocr_out_text.txt"
file_object = open(path_to_file, "r",encoding="utf-8")

names = file_object.read()

def find_between( names, first, last):
    try:
        start = names.index( first ) + len( first )
        end = names.index( last, start )
        return names[start:end]
    except ValueError:
        return ""
#print (find_between ( names, "UBS", "Supplier"))

lang=detect(find_between ( names, "<StringVar1>", "<StringVar2"))
#----------------

print(lang)
tk.messagebox.showinfo("Ocred Document", text)
tk.messagebox.showinfo("Number of pages scanned", "Number of pages in Contract Document : %s" % filelimit)
tk.messagebox.showinfo("Language Detected", "Contract Language is Detected as : %s" % lang)
