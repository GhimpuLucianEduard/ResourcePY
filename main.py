import tkinter as tk
import tkinter.filedialog
import subprocess
import os
from lxml import etree
import shutil

xml_namespace = "{http://schemas.microsoft.com/developer/msbuild/2003}"

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

    def find_file_by_name(self, findParam, grepParam):
        findProcoss = subprocess.Popen(["find", self.__resourceDir2.get(), "-name", findParam], stdout=subprocess.PIPE)
        findProcossResult = subprocess.Popen(["grep", grepParam], stdin=findProcoss.stdout, stdout=subprocess.PIPE)

        findProcoss.stdout.close()

        out, err = findProcossResult.communicate()
        result = out.decode("utf-8")
        print(result[:-2])
        # TODO handle not found result
        return result[:-2]

    def find_by_extension(self, extension):
        findProcoss = subprocess.Popen(["find", self.__resourceDir2.get(), "-iname", extension], stdout=subprocess.PIPE)
        out, err = findProcoss.communicate()
        result = out.decode("utf-8")
        print(result[:-2])
        # TODO handle not found result
        return result[:-1]

    def execute_shell(self):

        # subprocess.run(["cp", "-a", self.__resourceDir.get(), iosResourceFile])
        iosResourceFile = self.find_file_by_name("Resources", "iOS/Resources")
        iosCsProjFile = self.find_by_extension("*iOs.csproj")
        print(iosResourceFile, iosCsProjFile)

        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(iosCsProjFile, parser)
        #etree.register_namespace('', "http://schemas.microsoft.com/developer/msbuild/2003")
        root = tree.getroot()

        # find right ItemGroup to add Resources to
        for element in root.findall(f'{xml_namespace}ItemGroup'):
            for child in element.findall(f'{xml_namespace}None'):
                if child.attrib['Include'] == 'Info.plist':
                    tag = element

        # tag = self.get_tag_to_append(iosCsProjFile)

        # <BundleResource Include="Resources\EmptyContact%403x.png" />

        for file in os.listdir(self.__resourceDir.get()):
            # print(file)
            newChild = etree.Element(f'{xml_namespace}BundleResource')
            newChild.set('Include', file)
            tag.append(newChild)
            # shutil.copy(file, iosResourceFile)


        tree.write(iosCsProjFile, pretty_print=True, with_tail=True)








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
