#base_pair comparison
#12/16/2019 v3.2 => need to add mismatch checking algorithm
#Used dictionary instead of arrays as data structure to improve speed
#Implemented GUI

from itertools import filterfalse
from tkinter import *
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk
from pathlib import Path, PurePath
from datetime import datetime

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window()
        self.init_background()
        self.init_frame()

    def init_window(self):
        # changing the title of our master widget      
        self.master.title("bp_seq_comp_app")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

    def init_background(self):
        self.image = Image.open(Path("DNA_background.jpg"))
        self.img_copy= self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)


    def init_frame(self):
        start_frame = Frame(self, bg="#DCDCDC")
        start_frame.place(relwidth= .7, relheight=.7, relx=.5, rely=.5, anchor=CENTER)

        frame_title = Label(start_frame, text="BP Sequence Matching App", font=("Helvetica", 24), bg="#DCDCDC")
        frame_title.pack(pady=(25, 10))

        frame_heading = Label(start_frame, 
            text= "Directions: PLEASE enter full file name with extension,\n e.g. input_fil.txt, for both the input and output files.\n File MUST be in Input folder, unless file path is used.", pady=10, bg="#DCDCDC")
        frame_heading.pack()

        self.ifpLen_e = Entry(start_frame)
        self.ifpLen_e.pack()
        self.ifpLen_e.insert(0, "Input File Path/Name")

        self.bpLen_e = Entry(start_frame)
        self.bpLen_e.pack()
        self.bpLen_e.insert(0, "Enter bp length")  

        self.sdfLen_e = Entry(start_frame)
        self.sdfLen_e.pack()
        self.sdfLen_e.insert(0, "Start point difference in bp")    

        self.minMLen_e = Entry(start_frame)
        self.minMLen_e.pack()
        self.minMLen_e.insert(0, "Minimum matches required")  

        self.run_button = Button(start_frame, text="Run", activeforeground="#4d4dff", command=self.run_program)
        self.run_button.pack(pady=10)

    def _resize_image(self,event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)

    def run_program(self):
        passer = False
        if (Path(self.ifpLen_e.get()).is_file()):
            text_fl = self.ifpLen_e.get()
            passer = True
        else:
            try:
                text_fl = str(Path.cwd()) + '/Input/' + self.ifpLen_e.get()
                f = open(text_fl)
                f.close()
                passer = True
            except IOError:
                passer = False
                messagebox.showerror("Error", "Input file path/name or location is wrong")
            except:
                passer = False
                messagebox.showerror("Error", "Unexpected Error")

        try:
            bp_length = int(self.bpLen_e.get())
            passer = True
        except ValueError:
            passer = False
            messagebox.showerror("Error", "'"+self.bpLen_e.get()+"'" + " is not an integer")
        except:
            passer = False
            messagebox.showerror("Error", "Unexpected Error")

        try:
            sp_diff = int(self.sdfLen_e.get())
            passer = True
        except ValueError:
            passer = False
            messagebox.showerror("Error", "'"+self.sdfLen_e.get()+"'" + " is not an integer")
        except:
            passer = False
            messagebox.showerror("Error", "Unexpected Error")

        try:
            min_match = int(self.minMLen_e.get())
            passer = True
        except ValueError:
            passer = False
            messagebox.showerror("Error", "'"+self.minMLen_e.get()+"'" + " is not an integer")
        except:
            passer = False
            messagebox.showerror("Error", "Unexpected Error")

        if passer == True:
            seq_array = read_into(text_fl)
            file_path = str(Path.cwd()) + '/Output/' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '_' + self.bpLen_e.get() + 'bp_' + self.sdfLen_e.get() + 'sdf_' + self.minMLen_e.get() + 'min.txt'
            fp = open(file_path, 'w+') 
            fp.write(file_path + '\n\n')
            fp.write('bp_length: %d; starting point difference: %d; minimum matches accounted: %d' % (bp_length, sp_diff, min_match))
            fp.write('\n\n')
            for seq in seq_array:
                bp_seqList = read_parse(seq, bp_length, sp_diff)
                bpSeq_matchList = bpSeq_comp (min_match, bp_seqList)
                write_file(fp, bpSeq_matchList, seq)

            fp.close()
            messagebox.showinfo("It Worked!", "SUCCESS!!! \n Output file: " + file_path + ". \n Press OK to continue testing.")


#Python script begins
def read_into (text_fl):
    seq_array_temp = []
    with open(text_fl,"r") as fp:
        for cnt, line in enumerate(fp):
            if line == '\n':
                continue
            seq_array_temp.append(line)
    it = iter(seq_array_temp)
    seq_array = list(zip (it, it))
    return seq_array


def read_parse (seq, bp_length, sp_diff):
    bp_seqList = {}
    seq_string = seq[1]
    for i in range( len(seq_string) - (bp_length-1) ):
        if seq_string[i:i+bp_length] in bp_seqList:
            temp = bp_seqList.get(seq_string[i:i+bp_length])
            if i - temp[-1] >= sp_diff:
                temp.append(i)
            bp_seqList[seq_string[i:i+bp_length]] = temp
        else:
            temp = [i]
            bp_seqList[seq_string[i:i+bp_length]] = temp
    return bp_seqList

def bpSeq_comp (min_match, bp_seqList):
    bpSeq_matchList = []
    for key, val in bp_seqList.items():
        if len(val) >= min_match:
            temp = (key, val)
            bpSeq_matchList.append(temp)
    return bpSeq_matchList

def write_file (fp, bpSeq_matchList, seq):
    fp.write(seq[0])
    fp.write('Total matched sequences: %d' % len(bpSeq_matchList) + '\n\n')
    for elm in bpSeq_matchList:
        fp.write('%s : %d matches; Starting positions: ' % (elm[0], len(elm[1])))
        fp.write(' '.join(map(str,elm[1])))
        fp.write('\n')
    fp.write('\n\n')

def main():
    root = Tk()
    root.geometry("600x500")
    app = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()
