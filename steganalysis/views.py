from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from steganalysis.functions.functions import handle_uploaded_file  
from steganalysis.forms import StudentForm 

from PIL import Image
import PIL.Image
from numpy import array
import os
import binascii

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import pefile
import os
import math
import pickle
import joblib
import sys
import argparse

import winsound
import codecs

from tkinter import *
import tkinter
from tkinter import messagebox

def index(request):  
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES)  
        if student.is_valid():
            global k  
            k=handle_uploaded_file(request.FILES['file'])
            print(k)  
            return render(request,"index1.html") 
    else:  
        student = StudentForm()  
        return render(request,"index.html",{'form':student})
def extract1(request):
    print(k)


    def find_filename(data):
        filename = ''
        next_stop = 0
        for each in range(0, len(data[3:]), 1):
            if each<=len(data[3:])-4:
                if data[each]=='00000000' and data[each+1]=='00000000' and data[each+2]=='00000000' and data[each+3]=='00000000':
                    position = each
                    break
        name_data = data[3:position]
        filename = ''.join([chr(int(x, 2)) for x in name_data])
        next_stop = position + 4
        return next_stop, filename


    img_loc = ''
    os.system('cls')
    print(os.getcwd())
    img_loc = "steganalysis\\upload\\"+k
    if img_loc.find("\\")!=-1:
        img_loc.replace("\\", "//")
    print(img_loc)
    if os.path.isfile(img_loc)==False:
        print("File not found: ")
        input("Press enter to continue: ")
        return render(request,"home.html")
    print("   --Decoding the image......")
    try:
        #img2 = Image.open(img_loc)
        img2=PIL.Image.open(img_loc)
    except Exception as e:
        print("Not able to import image: " + str(e))
        input("Press enter to continue: ")
    decodeArray = array(img2)    #saving the image as an array so that operation can be performed
    x = 0
    data = ''
    store = []
    for n in range(0, 24, 1):   # checking for the head binary for verification.
        if decodeArray[0][n][0]%2==1:
            x += 1
    if x==24:  #if header verified then read the whole image
        for x in range(0, len(decodeArray), 1):   #algorith to extract the odd or even to 0 or 1 respectively.
            for y in range(0, len(decodeArray[x]), 1):
                if decodeArray[x][y][0]%2==0:
                    data = data + '1'
                elif decodeArray[x][y][0]%2==1:
                    data = data + '0'
                if len(data)==8:
                    store.append(data)
                    data = ''   #BELOW CODE: verify that the tail has been reached.
                if len(store)>=10 and store[-1]=='11001100' and store[-2]=='10101010' and store[-3]=='11001100' and store[-4]=='10101010' and store[-5]=='11001100' and store[-6]=='10101010' and store[-7]=='11001100' and store[-8]=='10101010' and store[-9]=='11001100' and store[-10]=='10101010':
                    break
            if len(store)>=10 and store[-1]=='11001100' and store[-2]=='10101010' and store[-3]=='11001100' and store[-4]=='10101010' and store[-5]=='11001100' and store[-6]=='10101010' and store[-7]=='11001100' and store[-8]=='10101010' and store[-9]=='11001100' and store[-10]=='10101010':
                    break
    else:
        print("   --Sorry the file do not contain any file, or the image may be tempered.")
        return render(request,"nofile.html")
    global encoded
    encoded = ''.encode()   #engine to convert the binary 1 and 0 to hex bytes that can be written to a file.
    next_stop, filename = find_filename(store)
    print("   --File detected: " + filename)
    print("   --Trying to restore...........")
    for each in store[next_stop:-10]: 
        each = hex(int(each, 2))
        if each.find('0x')!=-1 and len(each)==4:
            encoded = encoded + binascii.unhexlify(each.replace('0x', ''))
        elif len(each)==3:
            encoded = encoded + binascii.unhexlify(each.replace('0x', '0'))
        else:
            encoded = encoded + each.encode()
    print("   --Restore successful........")
    print("   --Saving the file: " + filename)
    try:
        with open(img_loc.replace(os.path.basename(img_loc), filename), 'wb') as filesave:
            filesave.write(encoded)
            filesave.close()
    except Exception as e:
        print("   --Oops the file extraction was successful, but was not able to save the file.")
        print("   --It seems that the directory of the PNG image is a read only, try moving the PNG file and try again.")
        input("Press enter to continue:")
    print("   --File saved at: " + img_loc.replace(os.path.basename(img_loc), filename))
    """return(img_loc.replace(os.path.basename(img_loc), filename))"""
    print(filesave)
    print(filename)
    global fipath
    fipath=img_loc.replace(os.path.basename(img_loc), filename)
    print(fipath)

    data=pd.read_csv("steganalysis/legit.csv",sep='|')
    na=pd.concat([data.isnull().sum()],axis=1,keys=["Train"])
    na[na.sum(axis=1)>0]
    data["MajorLinkerVersion"]=data["MajorLinkerVersion"].fillna(data["MajorLinkerVersion"].mode()[0])
    data.drop(['Name'],axis=1,inplace=True)
    data.drop(['md5'],axis=1,inplace=True)
    Y=data['legitimate'].values
    Y=Y.astype('int')
    X=data.drop(labels=['legitimate'],axis=1)
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=20)
    model=RandomForestClassifier(n_estimators=64,random_state=30)
    model.fit(X_train,Y_train)
    prediction_test=model.predict(X_test)
    prediction_test
    print("Acc:",metrics.accuracy_score(Y_test,prediction_test))


    def get_entropy(data):
        if len(data) == 0:
            return 0.0
        occurences = array.array('L', [0]*256)
        for x in data:
            occurences[x if isinstance(x, int) else ord(x)] += 1
        entropy = 0
        for x in occurences:
            if x:
                p_x =float(x) / len(data)
                entropy -=p_x*math.log(p_x, 2)
        return entropy


    def get_resources(pe):
        """Extract resources :
        [entropy, size]"""
        resources =[]
        if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
            try:
                for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                    if hasattr(resource_type, 'directory'):
                        for resource_id in resource_type.directory.entries:
                            if hasattr(resource_id, 'directory'):
                                for resource_lang in resource_id.directory.entries:
                                    data =pe.get_data(resource_lang.data.struct.OffsetToData, resource_lang.data.struct.Size)
                                    size = resource_lang.data.struct.Size
                                    entropy =get_entropy(data)

                                    resources.append([entropy, size])
            except:
                return resources
        return resources



    def get_version_info(pe):
        """Return version infos"""
        res ={}
        for fileinfo in pe.FileInfo:
            if fileinfo.Key =='StringFileInfo':
                for st in fileinfo.StringTable:
                    for entry in st.entries.items():
                        res[entry[0]] = entry[1]
            if fileinfo.Key =='VarFileInfo':
                for var in fileinfo.Var:
                    res[var.entry.items()[0][0]] =var.entry.items()[0][1]
        if hasattr(pe, 'VS_FIXEDFILEINFO'):
            res['flags'] =pe.VS_FIXEDFILEINFO.FileFlags
            res['os'] =pe.VS_FIXEDFILEINFO.FileOS
            res['type'] =pe.VS_FIXEDFILEINFO.FileType
            res['file_version'] =pe.VS_FIXEDFILEINFO.FileVersionLS
            res['product_version'] =pe.VS_FIXEDFILEINFO.ProductVersionLS
            res['signature'] =pe.VS_FIXEDFILEINFO.Signature
            res['struct_version'] =pe.VS_FIXEDFILEINFO.StrucVersion
        return res


    def extract_infos(fpath):
        res = {}
        pe = pefile.PE(fpath)
        print(pe)
        res['Machine'] = pe.FILE_HEADER.Machine
        res['SizeOfOptionalHeader'] =pe.FILE_HEADER.SizeOfOptionalHeader
        res['Characteristics'] =pe.FILE_HEADER.Characteristics
        res['MajorLinkerVersion'] =pe.OPTIONAL_HEADER.MajorLinkerVersion
        res['MinorLinkerVersion'] =pe.OPTIONAL_HEADER.MinorLinkerVersion
        res['SizeOfCode'] =pe.OPTIONAL_HEADER.SizeOfCode
        res['SizeOfInitializedData'] =pe.OPTIONAL_HEADER.SizeOfInitializedData
        res['SizeOfUninitializedData'] =pe.OPTIONAL_HEADER.SizeOfUninitializedData
        res['AddressOfEntryPoint'] =pe.OPTIONAL_HEADER.AddressOfEntryPoint
        res['BaseOfCode'] =pe.OPTIONAL_HEADER.BaseOfCode
        try:
            res['BaseOfData'] = pe.OPTIONAL_HEADER.BaseOfData
        except AttributeError:
            res['BaseOfData'] = 0
        res['ImageBase'] = pe.OPTIONAL_HEADER.ImageBase
        res['SectionAlignment'] = pe.OPTIONAL_HEADER.SectionAlignment
        res['FileAlignment'] = pe.OPTIONAL_HEADER.FileAlignment
        res['MajorOperatingSystemVersion'] = pe.OPTIONAL_HEADER.MajorOperatingSystemVersion
        res['MinorOperatingSystemVersion'] = pe.OPTIONAL_HEADER.MinorOperatingSystemVersion
        res['MajorImageVersion'] = pe.OPTIONAL_HEADER.MajorImageVersion
        res['MinorImageVersion'] = pe.OPTIONAL_HEADER.MinorImageVersion
        res['MajorSubsystemVersion'] = pe.OPTIONAL_HEADER.MajorSubsystemVersion
        res['MinorSubsystemVersion'] = pe.OPTIONAL_HEADER.MinorSubsystemVersion
        res['SizeOfImage'] = pe.OPTIONAL_HEADER.SizeOfImage
        res['SizeOfHeaders'] = pe.OPTIONAL_HEADER.SizeOfHeaders
        res['CheckSum'] = pe.OPTIONAL_HEADER.CheckSum
        res['Subsystem'] = pe.OPTIONAL_HEADER.Subsystem
        res['DllCharacteristics'] = pe.OPTIONAL_HEADER.DllCharacteristics
        res['SizeOfStackReserve'] = pe.OPTIONAL_HEADER.SizeOfStackReserve
        res['SizeOfStackCommit'] = pe.OPTIONAL_HEADER.SizeOfStackCommit
        res['SizeOfHeapReserve'] = pe.OPTIONAL_HEADER.SizeOfHeapReserve
        res['SizeOfHeapCommit'] = pe.OPTIONAL_HEADER.SizeOfHeapCommit
        res['LoaderFlags'] = pe.OPTIONAL_HEADER.LoaderFlags
        res['NumberOfRvaAndSizes'] = pe.OPTIONAL_HEADER.NumberOfRvaAndSizes
        # Sections
        res['SectionsNb'] = len(pe.sections)
        entropy = list(map(lambda x:x.get_entropy(), pe.sections))
        res['SectionsMeanEntropy'] = sum(entropy)/float(len(entropy))
        res['SectionsMinEntropy'] = min(entropy)
        res['SectionsMaxEntropy'] = max(entropy)
        raw_sizes = list(map(lambda x:x.SizeOfRawData, pe.sections))
        res['SectionsMeanRawsize'] = sum(raw_sizes)/float(len(raw_sizes))
        res['SectionsMinRawsize'] = min(raw_sizes)
        res['SectionsMaxRawsize'] = max(raw_sizes)
        virtual_sizes = list(map(lambda x:x.Misc_VirtualSize, pe.sections))
        res['SectionsMeanVirtualsize'] = sum(virtual_sizes)/float(len(virtual_sizes))
        res['SectionsMinVirtualsize'] = min(virtual_sizes)
        res['SectionMaxVirtualsize'] = max(virtual_sizes)

        #Imports
        try:
            res['ImportsNbDLL'] = len(pe.DIRECTORY_ENTRY_IMPORT)
            imports = sum([x.imports for x in pe.DIRECTORY_ENTRY_IMPORT], [])
            res['ImportsNb'] = len(imports)
            res['ImportsNbOrdinal'] = len(list(filter(lambda x:x.name is None, imports)))
        except AttributeError:
            res['ImportsNbDLL'] = 0
            res['ImportsNb'] = 0
            res['ImportsNbOrdinal'] = 0

        #Exports
        try:
            res['ExportNb'] = len(pe.DIRECTORY_ENTRY_EXPORT.symbols)
        except AttributeError:
            # No export
            res['ExportNb'] = 0
        #Resources
        resources= get_resources(pe)
        res['ResourcesNb'] = len(resources)
        if len(resources)> 0:
            entropy = list(map(lambda x:x[0], resources))
            res['ResourcesMeanEntropy'] = sum(entropy)/float(len(entropy))
            res['ResourcesMinEntropy'] = min(entropy)
            res['ResourcesMaxEntropy'] = max(entropy)
            sizes = list(map(lambda x:x[1], resources))
            res['ResourcesMeanSize'] = sum(sizes)/float(len(sizes))
            res['ResourcesMinSize'] = min(sizes)
            res['ResourcesMaxSize'] = max(sizes)
        else:
            res['ResourcesNb'] = 0
            res['ResourcesMeanEntropy'] = 0
            res['ResourcesMinEntropy'] = 0
            res['ResourcesMaxEntropy'] = 0
            res['ResourcesMeanSize'] = 0
            res['ResourcesMinSize'] = 0
            res['ResourcesMaxSize'] = 0

        # Load configuration size
        try:
            res['LoadConfigurationSize'] = pe.DIRECTORY_ENTRY_LOAD_CONFIG.struct.Size
        except AttributeError:
            res['LoadConfigurationSize'] = 0


        # Version configuration size
        try:
            version_infos = get_version_info(pe)
            res['VersionInformationSize'] = len(version_infos.keys())
        except AttributeError:
            res['VersionInformationSize'] = 0
        return res

    print(fipath)
    l=[]
    for i in extract_infos(fipath).values():
        l.append(i)
    print(l)
    l1=[]
    l1.append(l)
    pred=model.predict(l1)
    print(pred)
    if pred[0]==0:
        feq=4500 #amount of sound
        dur=5000#in milliseconds 1000ms=1sec
        winsound.Beep(feq, dur)
        root=tkinter.Tk()
        root.withdraw()
        for i in range(10):
            messagebox.showwarning("warning","malicious file please delete the image")
        return render(request,"home1.html",{'data':'malicious file'})
    if pred[0]==1:
        root=tkinter.Tk()
        root.withdraw()
        for i in range(10):
            messagebox.showwarning("safe","safe to use the image")
        return render(request,"home1.html",{'data':'legitimate file'})
