# -*- coding: utf-8  -*-
# -*- author: jokker -*-

class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """

        if numRows == 1:
            return s

        def addElementToDict(nowDict, element, line):
            if line in nowDict:
                nowDict[line].append(element)
            else:
                nowDict[line] = []
                nowDict[line].append(element)

        resultDict = {}

        for index, each in enumerate(s):

            _, nowIndex = divmod(index, 2 * numRows - 2)

            if nowIndex < numRows:
                addElementToDict(resultDict, each, nowIndex + 1)
            else:
                addElementToDict(resultDict, each, 2 * numRows - 1 - nowIndex)

        result = ""
        for i in range(1, numRows + 1):
            if i in resultDict:
                result += "".join(resultDict[i])

        return result

if __name__ == '__main__':

    pass