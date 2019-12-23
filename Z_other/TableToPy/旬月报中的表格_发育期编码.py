from Report.ExcelUtil import SheetUtil

a = SheetUtil(r'C:\Users\Administrator\Desktop\data_test.xlsx')
data = a.get_table_info_from_sheet(sheet_index=1)

table_info = []
for index_02, line in enumerate(data[1:]):
    for index_01, item in enumerate(line[1:]):
        key = '1' + str(index_01+1).rjust(2, '0') + str(index_02).rjust(2, '0')
        value = item.strip('\u7a3b ')
        if item:
            table_info.append([key, value])
        print(value)
    print('*'*100)


a = SheetUtil()
a.set_table(table_info)
a.save_to_book(r'C:\Users\Administrator\Desktop\plant_type.xls', sheet_name='ok')
