from Report.ExcelUtil import SheetUtil

a = SheetUtil(r'C:\Users\Administrator\Desktop\data_test.xlsx')
data = a.get_table_info_from_sheet(sheet_index=0)

table_info = []
for line in data:
    crop_name = line[0]
    station_names = line[1]
    fyq = line[2:]

    for station_name in station_names.split(u'\u3001'):
        line_info = [crop_name, station_name]
        line_info.extend(fyq)
        table_info.append(line_info)


a = SheetUtil()
a.set_table(table_info)
a.save_to_book(r'C:\Users\Administrator\Desktop\aa.xls', sheet_name='ok')
