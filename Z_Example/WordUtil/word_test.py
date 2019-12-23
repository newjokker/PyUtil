# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from Report.WordUtil import WordUtilOld

# 替换字典
template_path = r'D:\Code\Util_Util\Z_Example\WordUtil\word\muban_tem.jpg'
replace_pic_path = r'D:\Code\Util_Util\Z_Example\WordUtil\word\muban_pos.jpg'

word_info = {
    'pics': {template_path: replace_pic_path},
    'words': {'NAME': 'Jokker', 'phone': '18761609908', 'ABC': 'abcbca',
              'a': 'aaaa', 'b': 'bbbbb', 'c':'cccc'},
    # 表格是自增模式还是替换模式，是替换模式的话可以放在 data 关键字中的
    'tables': [{'mode': 'add_row', 'num': 0, 'value': [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
               {'mode': 'replace', 'num': 1, 'value': {'MM': '123'}}]}
# ------------------------------------------------------------------------------------------------------------------
DocTemplate = r'D:\Code\Util_Util\Z_Example\WordUtil\word\hehe.docx'
word_path = r'C:\Users\Administrator\Desktop\New_frm_wprd.docx'
# ------------------------------------------------------------------------------------------------------------------
a = WordUtilOld(DocTemplate, word_info, word_path)
a.do_process()


