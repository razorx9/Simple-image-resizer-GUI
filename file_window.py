from doctest import master
import customtkinter as ctk
from tkinter import filedialog as fd
import os
from PIL import Image
from threading import Thread

ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# image processing class 
class ImageProcessing():

    def __init__(self,foldrName,fileName, option, resizeValue):
        super().__init__()

        self.out_dir = option
        self.checkOutputFolder()

        if option == "Resize":
            self.imageResize(foldrName,fileName, resizeValue)
        elif option == "Resave":
            self.imageResave(foldrName,fileName)
            pass

    def checkOutputFolder(self):
        # check if output folder exists
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)

    def imageResize(self, FolderName, file_name, resizeValue):
        image = Image.open(os.path.join(FolderName, file_name)).convert("RGB")

        x,y = image.size #get opened image size.
        new_dimensions = (int(x*resizeValue),int(y*resizeValue)) #dimension set here
        output = image.resize(new_dimensions, Image.Resampling.BICUBIC) #resize

        output_file_name = os.path.join(self.out_dir, file_name)
        output.save(output_file_name, "JPEG")

    def imageResave(self, FolderName, file_name):
        image = Image.open(os.path.join(FolderName, file_name)).convert("RGB")
        output_file_name = os.path.join(self.out_dir, file_name)
        image.save(output_file_name, "JPEG")

# main class 
class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # window size and title 
        self.geometry("400x260")
        self.title("Image resize")

        # variables
        self.opsSelected = "Resize"
        self.resizeValue = 0.8
        self.folderName = False
        self.UI()

    def UI(self):
        # grid view config 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=250)

        # background frame 
        self.rootFrame = ctk.CTkFrame(master=self, width=250, height=100, corner_radius=15)
        self.rootFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.rootFrame.grid_columnconfigure(0, weight=1)
        self.rootFrame.grid_columnconfigure(1, weight=2)

        # processing label
        self.processLabel = ctk.CTkLabel(master=self.rootFrame, text="Select folder for processing")
        self.processLabel.grid(row=0, column = 0, columnspan = 2, pady=5, padx=2, sticky="nsew")

        # Progressbar
        self.pbar = ctk.CTkProgressBar(master=self.rootFrame)
        self.pbar.grid(row=1, column = 0, columnspan = 2, padx =20, pady=10, sticky="nsew")
        self.pbar.set(0)

        # folder select button 
        self.folderSelectBtn = ctk.CTkButton(master=self.rootFrame, 
                                                height = 10, 
                                                text="Select folder",
                                                command=self.select_folder)
        self.folderSelectBtn.grid(row=2, column = 0, columnspan = 1, padx=20, pady=5, sticky="nsew")

        # folder path label
        self.folderPathLabel = ctk.CTkLabel(master=self.rootFrame, height = 10, text="...path...")
        self.folderPathLabel.grid(row=2, column = 1, columnspan = 1, pady=10, padx=1, sticky="w")
        
        # option select button
        self.opsSelectBtn = ctk.CTkOptionMenu(master=self.rootFrame, 
                                                height = 25,
                                                values=["Resize", "Resave"],
                                                command=self.opsSelect)
        self.opsSelectBtn.grid(row=3, column = 0, padx=20, pady=10, sticky="nsew")

        # size select button
        self.sizeSelectBtn = ctk.CTkComboBox(master=self.rootFrame, 
                                                height = 25, 
                                                values=["0.9", "0.8", "0.5", "0.25"], 
                                                command=self.sizeSelect)
        self.sizeSelectBtn.grid(row=3, column = 1, padx=1, pady=10, sticky="w")
        self.sizeSelectBtn.set("0.8")

        # run button 
        self.runScriptBtn = ctk.CTkButton(master=self.rootFrame, 
                                            height = 50, 
                                            text="Start",
                                            fg_color="#D35B58",
                                            hover_color="#C77C78",
                                            command=self.run_main)
        self.runScriptBtn.grid(row=4, column = 0, columnspan = 2, padx=20, pady=5, sticky="nsew")

        #status bar label
        self.bottomLabel = ctk.CTkLabel(master=self, text_color="#777777" ,height= 0,text="Made by Didil")
        self.bottomLabel.place(relx=0.5, rely=1, anchor=ctk.S)

    # folder select dialog: folderSelectBtn pressed
    def select_folder(self):
        self.folderName = fd.askdirectory(title='Open a file')
        self.folderPathLabel.configure(text = "..."+self.folderName[-15:])

    # opsSelectBtn pressed
    def opsSelect(self, option):
        self.opsSelected = option
        pass

    # sizeSelectBtn pressed
    def sizeSelect(self, size):
        self.resizeValue = float(size)
        pass

    # start thread: runScriptBtn pressed
    def run_main(self):
        if self.folderName:
                self.t1 = Thread(target=self.imageProcess)
                self.t1.start()
                print(self.folderName, self.opsSelected, self.resizeValue)

    # processing thread 
    def imageProcess(self):
        for count, file_name in enumerate(os.listdir(self.folderName)):
            self.setValue(count+1, file_name)
            ImageProcessing(self.folderName, file_name, self.opsSelected, self.resizeValue)
            

    # set pbar and label values
    def setValue(self,count,file_name):
        total = len(os.listdir(self.folderName))
        ratio = total/count
        pbarValue = 1/ratio
        self.processLabel.configure(text = "Processed {0} files out of {1}".format(count,total))
        self.pbar.set(pbarValue)
        self.bottomLabel.configure(text= file_name)


if __name__ == "__main__":
    app = App()
    app.resizable(False,False)
    app.mainloop()