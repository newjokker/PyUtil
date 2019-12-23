# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
给定两个大小为 m 和 n 的有序数组 nums1 和 nums2。

请你找出这两个有序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。

你可以假设 nums1 和 nums2 不会同时为空。

示例 1:

nums1 = [1, 3]
nums2 = [2]

则中位数是 2.0
示例 2:

nums1 = [1, 2]
nums2 = [3, 4]

则中位数是 (2 + 3)/2 = 2.5
"""


class Solution(object):

    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """

        # FIXME 有序数组没说是什么顺序吧

        # FIXME 我是没想到还能用内置函数 sorted

        # 计算两个数组一共有多少位
        # 按照顺序找到对应的位数，要分 奇数和偶数两种情况

        index,result = 0, []

        length1 = len(nums1)
        length2 = len(nums2)

        if (length1 + length2) % 2 == 0:
            # 是偶数，提取中间两个数字
            mode = [int((length1 + length2)/2), int((length1 + length2)/2) +1]
        else:
            # 是奇数，提取最中间的数字
            mode = [int((length1 + length2)/2) +1]

        while mode:

            if not nums1:
                temp = num2.pop(0)
                index += 1

            elif not nums2:
                temp = nums1.pop(0)
                index += 1

            elif nums1[0] > nums2[0]:
                temp = nums2.pop(0)
                index += 1

            elif nums1[0] <= nums2[0]:
                temp = nums1.pop(0)
                index += 1
            else:
                temp = None

            if index in mode:
                result.append(temp)
                mode.remove(index)

        return sum(result)/float(len(result))



if __name__ == '__main__':

    # num1 = [1,2,3,4,5,6,7]
    # num2 = [2,4,6,8,10,11]

    num1 = [1,2]
    num2 = [3,4]

    a = Solution()
    b = a.findMedianSortedArrays(num1, num2)

    print(b)



