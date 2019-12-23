# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
我之前的错误一直出在如何遍历可能的三个数的组合上，我试图左右指针指向头尾慢慢向中间移动，这个是错误的

给定一个包括 n 个整数的数组 nums 和 一个目标值 target。找出 nums 中的三个整数，使得它们的和与 target 最接近。返回这三个数的和。假定每组输入只存在唯一答案。

例如，给定数组 nums = [-1，2，1，-4], 和 target = 1.

与 target 最接近的三个数的和为 2. (-1 + 2 + 1 = 2).

"""

class Solution:
    def threeSumClosest(self, nums, target):


        """是错的，看看是哪里错了"""


        # 排序
        nums.sort()

        res = float('inf')

        length = len(nums)
        for i in range(length):

            if i > 0 and nums[i] == nums[i - 1]:
                continue

            L, R = i+1, length-1

            while L < R:
                res_temp = nums[L] + nums[R] + nums[i]

                if abs(res - target) > abs(res_temp - target):
                    res = res_temp

                if res > target:
                    R -= 1
                elif res == target:
                    return target
                else:
                    L += 1
        return res


if __name__ == '__main__':

    a = Solution()
    print(a.threeSumClosest([8,9,-1,1,2,3,4], 19))
