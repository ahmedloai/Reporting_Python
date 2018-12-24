import Libs
import Utilities
##--------------------------------------------------------------------   
def Report_Stacked(testName, stage, filename):
    print(testName + '_' + stage)
    Libs.plt.gcf().clear()
    
    if Libs.readFromLocal:
        #Read Report File from local
        reportpath = Libs.reportLocal + filename
        dframe = Libs.pd.read_csv(reportpath, sep = ',', header = 0,index_col = [0,1]).tail(12)
    else:
        #Read Report File from Jenkins
        Repurl = Libs.reportURL + filename
        r = Libs.requests.get(Repurl, auth=('NG7CA2E','airbus'))
        reportFile = Libs.io.StringIO(r.content.decode('utf-8'))
        dframe = Libs.pd.read_csv(reportFile, sep = ',', header = 0, index_col = [0,1]).tail(12)
    
        
    if testName == 'BatchArchiver':
        gtitle = 'BatchArchiver on '+stage+ ' At '+ Libs.currenttimeAsTitel
        ax = dframe.plot(y = [0,1], color = ('yellowgreen', 'lightcoral') ,kind ='bar', stacked = True ,fontsize = 14)
    else:
        gtitle = testName + ' on '+stage+ ' At '+ Libs.currenttimeAsTitel
        ax = dframe.plot(y = [0,1,2], color = ('yellowgreen', 'lightcoral','gold') ,kind ='bar', stacked = True ,fontsize = 14)

    #Build the graph
    ax.legend(bbox_to_anchor=(1, 0.5))
    ax.set_ylabel("Percentage (%)", fontsize = 14)
    ax.set_xlabel("\nTimestamp/Run", fontsize = 14)
    ax.set_title(gtitle, fontsize=14, fontweight="bold")
    #Save the graph
    temp = Libs.reportsPath + testName + '_' + stage + '_StackedChart' + Libs.currenttime.strftime('%d-%m-%y') +'.pdf'
    Libs.plt.savefig(temp,bbox_inches = 'tight')  
##--------------------------------------------------------------------   
def BatchArchiver_PieChart(stage, filename):
    print('BatchArchiver')
    Libs.plt.gcf().clear()
    gtitle = 'BatchArchiver on '+stage+ ' At '+ Libs.currenttimeAsTitel
    
    if Libs.readFromLocal:
        #Read Report File from local
        reportpath = Libs.reportLocal + filename
        dframe = Libs.pd.read_csv(reportpath, sep = ',', header = 0).tail(12)
    else:
        #Read Report File from Jenkins
        Repurl = Libs.reportURL + filename
        r = Libs.requests.get(Repurl, auth=('NG7CA2E','airbus'))
        reportFile = Libs.io.StringIO(r.content.decode('utf-8'))
        dframe = Libs.pd.read_csv(reportFile, sep = ',', header = 0).tail(12)
    
    fig, axes= Libs.plt.subplots(4, 3, figsize=(12,12))
    
    labels = 'Success', 'Failed'
    colors = ['yellowgreen','lightcoral']
    explode = (0.1, 0)  # explode 1st slice
    
    for i, ax in enumerate(axes.flatten()):
        if i<len(dframe):
            sizes=[]
            sizes.append(dframe.iloc[i,2])
            sizes.append(dframe.iloc[i,3])
            # Plot
            ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                     autopct='%1.1f%%', shadow=True, startangle=140)
            ax.axis('equal')
            ax.set_title(dframe.iloc[i,0] + ' Run No. ' + str(dframe.iloc[i,1]), fontsize = 14)
        else:
            break
    
    fig.suptitle(gtitle, fontsize=14, fontweight="bold")
    temp = Libs.reportsPath + 'BatchArchiver_' + stage + '_PieChart' + Libs.currenttime.strftime('%d-%m-%y') +'.pdf'
    Utilities.ClearEmptyGraph(fig, axes, len(dframe))
    fig.savefig(temp, bbox_inches = 'tight')   
##------------------------------------------------------------------------------------
def SeleniumReport_PieChart(customer, stage, filename):
    print(customer+'_'+stage)
    Libs.plt.gcf().clear()
    gtitle = customer + ' on '+ stage + ' At '+ Libs.currenttimeAsTitel

    if Libs.readFromLocal:
        #Read Report File from local
        reportpath = Libs.reportLocal + filename
        dframe = Libs.pd.read_csv(reportpath, sep = ',', header = 0).tail(12)
    else:
        #Read Report File from Jenkins
        Repurl = Libs.reportURL + filename
        r = Libs.requests.get(Repurl, auth=('NG7CA2E','airbus'))
        reportFile = Libs.io.StringIO(r.content.decode('utf-8'))
        dframe = Libs.pd.read_csv(reportFile, sep = ',', header = 0).tail(12)
    
    fig, axes= Libs.plt.subplots(4, 3, figsize=(12,12))
    
    for i, ax in enumerate(axes.flatten()):
        if i<len(dframe):
            sizes = []
            colors = []
            labels = []
            explode = []
            if dframe.iloc[i,2] > 0:
                sizes.append(dframe.iloc[i,2])
                colors.append('yellowgreen')
                labels.append('Success')
                explode.append(0.1)
            if dframe.iloc[i,3] > 0:
                sizes.append(dframe.iloc[i,3])
                colors.append('lightcoral')
                labels.append('Failed')
                explode.append(0)
            if dframe.iloc[i,4] > 0:
                sizes.append(dframe.iloc[i,4])
                colors.append('gold')
                labels.append('Skipped')
                explode.append(0)
                
            # Plot
            ax.pie(sizes, explode = tuple(explode), labels =tuple(labels), colors = colors,
                     autopct ='%1.1f%%', shadow =True, startangle = 140)
            ax.axis('equal')
            ax.set_title(dframe.iloc[i,0] + ' Run No. ' + str(dframe.iloc[i,1]), fontsize = 14)
        else:
            break
    
    fig.suptitle(gtitle, fontsize=14, fontweight="bold")
    temp = Libs.reportsPath + customer + '_' + stage + '_PieChart' + Libs.currenttime.strftime('%d-%m-%y') +'.pdf'
    Utilities.ClearEmptyGraph(fig, axes, len(dframe))
    fig.savefig(temp, bbox_inches = 'tight')   
##------------------------------------------------------------------------------------
def LoadTest_Reporting_Sequential():
    Repurl='http://de0-vsiaas-1481.eu-v.airbus-v.corp:8080/view/Reports/job/Report_LoadTest/lastSuccessfulBuild/artifact/LoadTest-Report.xlsx'
    r = Libs.requests.get(Repurl, auth=('NG7CA2E','airbus'))
    workbooksheets = Libs.xlrd.open_workbook(file_contents= r._content)
    row = []
    rawdata = []
    
    for sheet in workbooksheets.sheets():
        if "para" in sheet.name:
            continue
        #build the dataframe
        for r in range(1,sheet.nrows):
            row.clear()
            for c in range(0,sheet.ncols):
                row.append(sheet.cell_value(r,c))
            rawdata.append(tuple(row))
        dframe = Libs.pd.DataFrame.from_records(rawdata, columns=['TimeStamp','FileSize(MB)','Time(Sec)']).tail(10)
        #print (dframe)
    
        fig, axes= Libs.plt.subplots(1, 2, figsize=(12,6))
        for i, ax in enumerate(axes.flatten()):
            if i==0:
                ax.bar(x=dframe['TimeStamp'], height=dframe['FileSize(MB)'], color= 'darkseagreen')
                ax.set_ylabel("Size (MB)", fontsize = 14) 
                ax.set_title('File Size (MB)', fontsize=14, fontweight="bold")
            if i==1:
                ax.bar(x=dframe['TimeStamp'], height=dframe['Time(Sec)'], color= 'grey')
                ax.set_ylabel("Time (Sec)", fontsize = 14)        
                ax.set_title('Duration (Sec)', fontsize=14, fontweight="bold")
        
            ax.set_xlabel("\nTimestamp", fontsize = 14)
            for tricks in ax.get_xticklabels():
            #temp = Libs.datetime.datetime.strptime(str(tricks),'%I:%M%p on %B %d, %Y')
                tricks.set_rotation(90)
        gtitle = sheet.name.upper() + ' At '+ currenttime.strftime("%Y-%m-%d %H:%M")
        fig.suptitle(gtitle, fontsize=14, fontweight="bold")
        temp = reportPath + sheet.name.upper() +'_' + currenttime.strftime('%d-%m-%y') +'.pdf'
        fig.savefig(temp, bbox_inches = 'tight')
##------------------------------------------------------------------------------------
def LoadTest_Reporting_Parallel():
    Repurl='http://de0-vsiaas-1481.eu-v.airbus-v.corp:8080/view/Reports/job/Report_LoadTest/lastSuccessfulBuild/artifact/LoadTest-Report.xlsx'
    r = Libs.requests.get(Repurl, auth=('NG7CA2E','airbus'))
    workbooksheets = Libs.xlrd.open_workbook(file_contents= r._content)
    row = []
    rawdata = []
    
    for sheet in workbooksheets.sheets():
        if "sequ" in sheet.name:
            continue
        #build the dataframe
        for r in range(1,sheet.nrows):
            row.clear()
            for c in range(0,sheet.ncols):
                row.append(sheet.cell_value(r,c))
            rawdata.append(tuple(row))
        dframe = Libs.pd.DataFrame.from_records(rawdata, columns=['TimeStamp','FileSize(MB)','Time(Sec)','Requests', 'Category']).tail(10)
        print (dframe)
        
        fig, axes= Libs.plt.subplots(1, 2, figsize=(12,6))
        for i, ax in enumerate(axes.flatten()):
            if i==0:
                ax.bar(x=dframe['TimeStamp'], height=dframe['FileSize(MB)'], color= 'darkseagreen')
                ax.set_ylabel("Size (MB)", fontsize = 14) 
                ax.set_title('File Size (MB)', fontsize=14, fontweight="bold")
            if i==1:
                ax.bar(x=dframe['TimeStamp'], height=dframe['Requests'], color= 'grey')
                ax.set_ylabel("Requests", fontsize = 14)        
                ax.set_title('No of Parallel Requests', fontsize=14, fontweight="bold")
        
            ax.set_xlabel("\nTimestamp", fontsize = 14)
            for tricks in ax.get_xticklabels():
            #temp = Libs.datetime.datetime.strptime(str(tricks),'%I:%M%p on %B %d, %Y')
                tricks.set_rotation(90)
        gtitle = sheet.name.upper() + ' At '+ currenttime.strftime("%Y-%m-%d %H:%M")
        fig.suptitle(gtitle, fontsize=14, fontweight="bold")
        temp = reportPath + sheet.name.upper() +'_' + currenttime.strftime('%d-%m-%y') +'.pdf'
        fig.savefig(temp, bbox_inches = 'tight')
                
def BatchArchiver_DataSize(stage, filename):
    print('BatchArchiver')
    Libs.plt.gcf().clear()
    gtitle = 'BatchArchiver on '+stage+ ' At '+ Libs.currenttimeAsTitel
    
    sizeslist=["10MB","100MB","250MB","1000MB","2000MB"]
    
    if Libs.readFromLocal:
        #Read Report File from local
        reportpath = Libs.reportLocal + filename
        dframe = Libs.pd.read_csv(reportpath, sep = ',', header = 0).tail(12)   
    else:
        #Read Report File from Jenkins
        Repurl = Libs.reportURL + filename
        r = Libs.requests.get(Repurl, auth=('NG7CA2E','airbus'))
        reportFile = Libs.io.StringIO(r.content.decode('utf-8'))
        dframe = Libs.pd.read_csv(reportFile, sep = ',', header = 0).tail(12)
   
    fig, axes= Libs.plt.subplots(4, 3, figsize=(17,15))
    
    for i, ax in enumerate(axes.flatten()):
        if i<len(dframe):
            act=[]
            act.append(dframe.iloc[i,2])
            act.append(dframe.iloc[i,3])
            act.append(dframe.iloc[i,4])
            act.append(dframe.iloc[i,5])
            act.append(dframe.iloc[i,6])
            # Plot
            ax.scatter(sizeslist, act, label='ddd')
            ax.set_title(dframe.iloc[i,0] + ' Run No. ' + str(dframe.iloc[i,1]), fontsize = 14)
        else:
            break
    
    fig.suptitle(gtitle, fontsize=14, fontweight="bold")
    temp = Libs.reportsPath + 'BatchArchiver_' + stage + '_DataSize' + Libs.currenttime.strftime('%d-%m-%y') +'.pdf'
    Utilities.ClearEmptyGraph(fig, axes, len(dframe))
    fig.savefig(temp, bbox_inches = 'tight')
    fig.get_frameon()
    
#####################################################################   
#####################################################################   
#####################################################################   
#####################################################################   
def Build_StackedCharts():
    for customer in Libs.customers:
        for stage in Libs.stages:
            rawdata = customer+'_'+stage+'.csv'
            Report_Stacked(customer,stage,rawdata)        
    
    Report_Stacked('BatchArchiver','INT','BA_INT.csv')
    Report_Stacked('BatchArchiver','VAL','BA_VAL.csv')
    
def Build_PieCharts():
    BatchArchiver_PieChart('INT','BA_INT.csv')
    BatchArchiver_PieChart('VAL','BA_VAL.csv')

    for customer in Libs.customers:
        for stage in Libs.stages:
            rawdata = customer+'_'+stage+'.csv'
            SeleniumReport_PieChart(customer,stage,rawdata)