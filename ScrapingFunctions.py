# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 23:46:20 2023

"""

from bs4 import BeautifulSoup 
import requests
from csv import writer
import pandas as pd

def scrapeProducts(category,filename,sortingValue):
    url = f"https://www.morele.net{category}"
    requestedHTML = requests.get(url)
    workingDocument = BeautifulSoup(requestedHTML.text, "html.parser")
    filename =  filename + ".xlsx"

    numberOfPages = int(workingDocument.find(class_="pagination-btn-nolink-anchor").string)

            
    with open(filename,"a", encoding="utf-8",newline="") as f:
        writeData = writer(f, delimiter=";")
        header = ["Nazwa","Cena",'Link']
        writeData.writerow(header)

        for page in range(1,numberOfPages+1):
            url = f"https://www.morele.net{category},,,,,,,,0,,,,/{page}/"
            requestedHTML = requests.get(url)
            workingDocument = BeautifulSoup(requestedHTML.text, "html.parser")
                
            listedProducts = workingDocument.find_all(class_="cat-product-inside")
            for product in listedProducts:    
                productTitle = product.find('a',class_="productLink")
                
                productPrice = product.find('div',class_="price-new")
                priceToFloat = float(str(str(productPrice.text).split('\n')[1]).replace("zł","").replace("od","").replace(" ","").replace(",","."))
                
                productLink = "https://www.morele.net"+productTitle['href']
                productLink = f'=HIPERŁĄCZE("{productLink}")'
                
                info = [productTitle['title'],priceToFloat,productLink]          
                writeData.writerow(info)
    
    sortedCsvFile = pd.read_csv(filename, sep=";",engine="python")
    # sortowanie
    if sortingValue == 0:
        pass
    if sortingValue == 1:
        sortedCsvFile.sort_values(['Nazwa'], inplace=True) 
    if sortingValue == 2:
        sortedCsvFile.sort_values(['Cena'], inplace=True)
    sortedCsvFile.to_excel(filename,index =False)
    


def scrapeCategories():
    url = "https://www.morele.net/podzespoly-komputerowe/podzespoly-komputerowe/"
    requestedCategoriesHTML= requests.get(url)
    workingDocumentCategories = BeautifulSoup(requestedCategoriesHTML.text, "html.parser")

    listOfCategories = []
    listofCategoryLinks = []
    dictionaryOfCategories = {}
    listedCategories = workingDocumentCategories.find_all('div',class_="text-box")
    for category in listedCategories:
        categoryName = category.find('span')
        fixedCategoryName = categoryName.text.lstrip(" ")
        listOfCategories.append(fixedCategoryName)

    listOfCategories.pop(len(listOfCategories)-1)


    listedCategoriesLinks = workingDocumentCategories.find_all('a',class_="col-xs-12 col-md-6 col-lg-4 col-xl-3")
    for category in listedCategoriesLinks:
        categoryLink =  category['href']
        listofCategoryLinks.append(categoryLink)\

    dictionaryOfCategories = dict(map(lambda i,j: (i,j),listOfCategories,listofCategoryLinks))
    del dictionaryOfCategories['Dyski SSD (z demontażu)']
    del dictionaryOfCategories['Tunery TV, FM, karty video']
    del dictionaryOfCategories['Karty dźwiękowe']
    
    return dictionaryOfCategories
        
















