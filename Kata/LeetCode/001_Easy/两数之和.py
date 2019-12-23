# -*- coding: utf-8  -*-
# -*- author: jokker -*-

class Solution(object):

    def twoSum(self, nums, target):
        nums_dict = {}
        for i, j in enumerate(nums):
            if j in nums_dict:
                return [i, nums_dict[j]]
            tar = target - j
            nums_dict[tar] = i
        return []


if __name__ == '__main__':

    nums = [2, 7, 11, 15]
    target = 9

    a = Solution()
    b = a.twoSum(nums, target)
    print(b)