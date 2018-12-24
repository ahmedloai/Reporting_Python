import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import datetime
import xlrd 
import os
import io 
import requests
from requests.auth import HTTPBasicAuth
from PyPDF2 import PdfFileMerger,PdfFileReader,PdfFileWriter

#Paramerters
currenttime = datetime.datetime.now()
currenttimeAsTitel = currenttime.strftime("%I:%M%p on %B %d, %Y")
reportURL = 'http://de0-vsiaas-1481.eu-v.airbus-v.corp:8080/view/Reports/job/Report_Build_RawData/ws/Reports/'
reportLocal = "./Reports_LocalPath/"
reportsPath= "./ResultsAsPDF/"
readFromLocal= True
customers = ['SIAS','SB Reports','Smoke Test','TechData', 'ALS']
components = ['BatchArchiver','LoadTest']
stages = ['INT','VAL']