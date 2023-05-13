# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 17:57:49 2023

"""

import customtkinter as ctk
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

from ScrapingFunctions import scrapeProducts,scrapeCategories
    

root = ctk.CTk()
root.geometry("500x400")
root.title("morele.net Scraper")

scrapedCategories = scrapeCategories()

optionmenu_default = ctk.StringVar(value="Kategoria")
selectedFileName = ctk.StringVar(value="")
selectedSortingStyle= ctk.IntVar(value=0)
def selected_category_callback(selected):
    global selectedCategory
    selectedCategory = scrapedCategories[f"{selected}"]
   
def scrapeFromSelectedCategory():       
        root.scrapingProgressBar.start()
        root.statusLabel.configure(text="Status: In progress")
        scrapeProducts(selectedCategory, root.entryFileName.get(),tellCheckBoxesValue(selectedSortingStyle.get()))
        root.statusLabel.configure(text="Status: Completed")
        root.scrapingProgressBar.stop()
        root.scrapingProgressBar.set(1)
    
def tellCheckBoxesValue(radioButton):
    if radioButton == 1:
        return 2
    if radioButton == 2:
        return 1
    return 0

def checkEntryValue(*args):
    entryField = root.entryFileName.get()
    entryOption = root.rightsideFrameCategoriesOptions.get()    
    if  (entryField =="" or entryOption == "Kategoria"):
        root.scrapeDataButton.configure(state="disabled")
    else:
        root.scrapeDataButton.configure(state="normal")
        
        
selectedFileName.trace("w",checkEntryValue)
optionmenu_default.trace("w",checkEntryValue)
    
    

frame = ctk.CTkFrame(master=root)
root.grid_rowconfigure((0,1,2,3), weight=1)
root.grid_columnconfigure((0,1,2), weight=1)

root.leftsideFrame = ctk.CTkFrame(root, corner_radius=10)
root.leftsideFrame.grid(row=0, column=0, rowspan=2, sticky="ns",padx=20,pady=20)
root.leftsideFrame.grid_rowconfigure(2, weight=1)

root.leftsideFrameBottom = ctk.CTkFrame(root, corner_radius=10)
root.leftsideFrameBottom.grid(row=2, column=0, rowspan=2, sticky="n",padx=20,pady=20)
root.leftsideFrameBottom.grid_rowconfigure(2, weight=1)

root.rightsideFrame = ctk.CTkFrame(root, width=140, corner_radius=10)
root.rightsideFrame.grid(row=0, column=1, rowspan=3, sticky="nsew",padx=10,pady=20)
root.rightsideFrame.grid_rowconfigure(3, weight=10)

root.rightsideFrameBottom = ctk.CTkFrame(root.rightsideFrame, width=140, corner_radius=10)
root.rightsideFrameBottom.grid(row=3, column=0, rowspan=1,columnspan=2, sticky="nsew",padx=10,pady=20)



root.label = ctk.CTkLabel(root.leftsideFrame, text="File name", font=ctk.CTkFont(size=20, weight="bold"))
root.label.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

root.entryFileName = ctk.CTkEntry(root.leftsideFrame, placeholder_text="Wpisz nazwę pliku", width=170, textvariable=selectedFileName)
root.entryFileName.grid(row=1, column=0, padx=20, pady=20, sticky="ns")



root.scrapeDataButton = ctk.CTkButton(root.leftsideFrameBottom, text="Scrape data",command=lambda: threading.Thread(target=scrapeFromSelectedCategory).start(), state="disabled")
root.scrapeDataButton.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

root.scrapingProgressBar = ctk.CTkProgressBar(root.leftsideFrameBottom, width = 200, mode="determinate",indeterminate_speed=1, determinate_speed=1)
root.scrapingProgressBar.grid(row=1,column=0, padx=20, pady=10, sticky="nsew")

root.scrapingProgressBar.set(0)

root.statusLabel = ctk.CTkLabel(root.leftsideFrameBottom, text="Status: Idle", font=ctk.CTkFont(size=15, weight="bold"))
root.statusLabel.grid(row=2,column=0, padx=20, pady=10, sticky="nsew")




root.rightsideFrameLabel = ctk.CTkLabel(root.rightsideFrame, text="Select category", font=ctk.CTkFont(size=20, weight="bold"))
root.rightsideFrameLabel.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

root.rightsideFrameCategoriesOptions = ctk.CTkOptionMenu(root.rightsideFrame, values = list(scrapedCategories.keys()),command=selected_category_callback, variable=optionmenu_default)
root.rightsideFrameCategoriesOptions.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="nsew")

root.labelSorting = ctk.CTkLabel(root.rightsideFrameBottom, text="Sort data:",font=ctk.CTkFont(size=17, weight="bold"))
root.labelSorting.grid(row=0, column=0,padx=20, pady=20, columnspan=3, sticky="e")

root.checkboxProductPrice= ctk.CTkRadioButton(root.rightsideFrameBottom, text="Cena", value=1, variable=selectedSortingStyle)
root.checkboxProductPrice.grid(row=1, column=0,padx=20, pady=0, sticky="e")

root.checkboxProductName= ctk.CTkRadioButton(root.rightsideFrameBottom, text="Nazwa", value=2, variable=selectedSortingStyle)
root.checkboxProductName.grid(row=2, column=0,padx=20, pady=(20,0), sticky="e")



root.mainloop()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



