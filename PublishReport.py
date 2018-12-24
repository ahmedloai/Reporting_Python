import Reports

print('Generating Reports on '+ Reports.Libs.currenttimeAsTitel)

Reports.Utilities.ClearPreviousReport(Reports.Libs.reportsPath)

Reports.Build_PieCharts() # For all target Reports show Success and Failure %
Reports.Build_StackedCharts()  # For all target Reports show Success and Failure %

#More Details on data sizes 
#Reports.LoadTest_Reporting_Parallel()
#Reports.LoadTest_Reporting_Sequential()

Reports.BatchArchiver_DataSize('INT','BA_INT_DATASIZE.csv')
Reports.BatchArchiver_DataSize('VAL','BA_VAL_DATASIZE.csv')

for customer in Reports.Libs.customers:
    Reports.Utilities.MergePDF(customer,Reports.Libs.reportsPath)

for tec in Reports.Libs.components:
    Reports.Utilities.MergePDF(tec,Reports.Libs.reportsPath)