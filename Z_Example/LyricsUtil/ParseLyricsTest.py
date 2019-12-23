# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""歌词解析，格式很简单，可以写一个脚本进行解析"""

from ReadData.LyricsUtil import LyricsUtil

lrcPath = r'D:\Code\Util_Util\Z_Example\LyricsUtil\data\test_002.lrc'

a = LyricsUtil.get_lyrics_info(lrcPath, 'GBK')

for each in a.items():
    print(each)

