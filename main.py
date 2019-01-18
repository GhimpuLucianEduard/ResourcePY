import tkinter as tk
import tkinter.filedialog
import subprocess
import sh


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.__resourceDir = tk.StringVar()
        self.__resourceDir2 = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        textInfo = tk.Label(self, text="Resource directory:")
        textInfo.pack()

        resourceDirLabel = tk.Label(self, textvariable=self.__resourceDir)
        resourceDirLabel.pack()

        self.browseBtn = tk.Button(self, text="Browse", fg="red", command=self.browse_button)
        self.browseBtn.pack()

        textInfo2 = tk.Label(self, text="Target directory:")
        textInfo2.pack()

        resourceDirLabel2 = tk.Label(self, textvariable=self.__resourceDir2)
        resourceDirLabel2.pack()

        self.browseBtn2 = tk.Button(self, text="Browse2", fg="red", command=self.browse_button2)
        self.browseBtn2.pack()

        self.shellExecutor = tk.Button(self, text="Copy resources to target", fg="red", command=self.execute_shell)
        self.shellExecutor.pack()

    def browse_button(self):
        filename = tk.filedialog.askdirectory()
        self.__resourceDir.set(filename)


    def browse_button2(self):
        filename = tk.filedialog.askdirectory()
        self.__resourceDir2.set(filename)


    def execute_shell(self):

        # subprocess.run(["cp", "-a", self.__resourceDir.get(), self.__resourceDir2.get()])

        process = subprocess.Popen(["find", self.__resourceDir2.get(), "-name", "Resources"], stdout=subprocess.PIPE)
        process2 = subprocess.Popen(["grep", "iOS/Resources"], stdin=process.stdout, stdout=subprocess.PIPE)

        process.stdout.close()

        out, err = process2.communicate()
        outtest = out.decode("utf-8")
        print(outtest[:-2])





root = tk.Tk()

width = 500  # width for the Tk root
height = 300  # height for the Tk root

# get screen width and height
screenWidth = root.winfo_screenwidth()  # width of the screen
screenHeight = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (screenWidth / 2) - (width / 2)
y = (screenHeight / 2) - (height / 2)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (width, height, x, y))

app = Application(master=root)
app.mainloop()
