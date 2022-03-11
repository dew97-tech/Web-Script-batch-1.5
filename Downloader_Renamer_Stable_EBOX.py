from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
from requests import get
import os
import re
import time

# -------Enter Your Desired FTP Domain Address-------

try:
    domain = 'http://fs.ebox.live/'
    main_link = str(input('Enter URL: '))
    page = requests.get(main_link)
    filetype = '.' + input('Enter File Extension Excluding DOT : ')
    soup = BeautifulSoup(page.text, 'html.parser')

    # ------The Download Will Begin----------
    # ------The Downloaded Files Will Be In Same Directory Where Py File Is-------

    exception_occured = False
    chunk_size = 1024
    for link in soup.find_all('a'):
        url = link.get('href')
        if(url[-4:] == filetype):
            ##THIS VERSION IS ONLY FOR EBOX FTP SERVER
            file_name = url.split('/')[-1]
            url = main_link+file_name
            r = requests.get(url, stream=True)
            total_size = int(r.headers['content-length'])
            print(url)
            try:
                with open(file_name, 'wb') as file:
                    for data in tqdm(iterable=r.iter_content(chunk_size=chunk_size), total=total_size/chunk_size, unit='KB'):
                        file.write(data)

            except KeyboardInterrupt as e:
                print("Dear User You Have Pressed Ctrl + C")
                exception_occured = True
                break

                if(file.closed != True):
                    file.close
                    exception_occured = True
                    print("File Closed")

            except Exception as e:
                exception_occured = True
                print("Write Failed")
    if(not exception_occured):
        print("All Files Have Been Downloaded Successfully")
    # ------All Files Would Have Been Downloaded By Now-----------

    # ------Taking Input For File Extention------

    extention = input("Enter Desired File Extention : ")
    currentDir = os.getcwd()
    print("", end='\n')
    print("The Following Files Will Be In : " + extention)
    print("", end='\n')
    time.sleep(0.5)
    print("The Following Files Will Be Renamed To This File FORMAT")
    print("", end='\n')
    time.sleep(2.0)

    # -------Getting File Information Before Renaming-------
    series_name_list = []
    for files in os.listdir(currentDir):
        series_name = files
        match_found = re.search(r'\w\d\d\w\d\d', series_name)
        if(match_found != None):
            series_name = series_name.replace('.', ' ')
            match_index_start, match_index_stop = match_found.span()
            series_name = series_name[:match_index_stop]
            series_name = series_name+"."+extention
            series_name_list.append(series_name)
            print(series_name)
            time.sleep(0.5)

    print("", end='\n')
    print("Do You Want To Continue : Y/N")
    input_value = input("Enter Your Choice : ")
    input_value = input_value.lower()
    iterator = 0

    # --------Renaming Procedure Of The Files--------
    if(input_value == 'y'):
        for files in os.listdir(currentDir):
            series_name = files
            match_found = re.search(r'\w\d\d\w\d\d', series_name)
            if(match_found != None):
                try:
                    os.rename(series_name, series_name_list[iterator])
                    iterator = iterator+1

                except Exception as e:
                    print("File Rename Failed"+series_name)

    print("The Files Have Been Renamed Succesfully")

except KeyboardInterrupt as e:
    print("Dear User You Have Pressed Ctrl + C")
