# -*- coding: utf-8  -*-
# -*- author: jokker -*-

class Solution:

    def isMatch(self, s: str, p: str) -> bool:

        # print('-'*50)


        # 找到 * 之前的字符，连接为一组对比，

        # 一个个对比，如果 遍历所有的模式如果都不能正确，认为就是错误的

        length_p = len(p)
        length_s = len(s)
        j = 1
        i = 0

        # 为空
        if not s  or not p:
            return False

        # 第一个字符
        if s[0] != p[0] and p[0] != '.':

            if length_p <2:
                return False
            elif p[1] != '*':
                return False
            else:
                j += 2
                i -= 1

        # 后面的字符

        now_j = j

        while i < len(s)-1:

            i = i + 1

            print(i)

            print(s[i])
            print(p[j - 1:j + 1])
            print(s[i:])
            print(p[j:])
            print('-' * 50)

            if j >= length_p or i >= length_s:
                return False

            now_j = j

            if s[i] != p[j]:
                if p[j] == '.':
                    if p[j-1] == '*':
                        if j+1 < length_p and p[j+1] == s[i]:
                            now_j += 1
                            j = j + 2
                    else:
                        j += 1
                elif p[j] == '*':
                    if p[j-1] == '.':
                        continue
                    elif p[j-1] == s[i]:
                        j += 1
                elif j+1 < length_p:
                    if p[j+1] == '*':
                        now_j += 1
                        j += 2
                        i -= 1
                    else:
                        return False
                else:
                    return False
            else:
                j += 1

        # print(j, len(p))

        if now_j == length_p-1:
            return True
        else:
            return False




if __name__ == '__main__':

    # FIXME  这个难度真的有点大，我的思路应该错了

    a = Solution()
    # print(a.isMatch('mississippiabcr8', 'mis*is*ip*.r8'))
    # print(a.isMatch('aab', 'c*a*b'))
    print(a.isMatch('aab', 'c*a*b*'))
    # print(a.isMatch('aa', 'a*'))
    # print(a.isMatch('mississippiabcr8', '.*'))