import Libs

def BackupOldReports(source, destination):
    print('Backup of Old Reports')

def ClearPreviousReport(reportsPath):
    print('Clearing previous Reports from ' + reportsPath)
    files = [f for f in Libs.os.listdir(reportsPath)]
    for f in files:
        Libs.os.remove(Libs.reportsPath + f)    
        
def ClearEmptyGraph(fig, axes, count):
    if count >= 12:
        return
    else:
     for X in range(0,4):
        for Y in range(0,3):
            if not axes[X][Y].has_data():
               axes[X][Y].set_visible(False)
    

def MergePDF(customer, wdir):
    files=[f for f in Libs.os.listdir(wdir) if customer in f and 'pdf' in f]
    if len(files) == 0:
        return
    merger =  Libs.PdfFileMerger()
    
    for f in files:
        merger.append(Libs.PdfFileReader(Libs.reportsPath + f), 'rb')
        Libs.os.remove(Libs.reportsPath + f)    
    
    merger.write(Libs.reportsPath + customer + '_' + Libs.currenttime.strftime('%d-%m-%y') + '.pdf')

    