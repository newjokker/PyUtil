# -*- coding: utf-8  -*-
# -*- author: jokker -*-

# https://leetcode-cn.com/problems/3sum/

class Solution:
    def threeSum(self, nums):

        # 个数小于 3 返回空

        if len(nums) < 3:
            return []


        res = []

        # 排序，查找
        nums.sort()

        L, R = 0, len(nums)-1

        while L + 1 < R:

            if nums[R] < 0:
                return

            if nums[L] > 0:
                return

            if nums[L] + nums[L+1] + nums[R] > 0:
                R -= 1
                continue

            elif nums[L] + nums[R-1] + nums[R] < 0:
                L += 1
                continue

            for i in range(L+1, R):
                if nums[L] + nums[R] + nums[i] == 0:
                    if res:
                        if res[-1] != [nums[L], nums[i],  nums[R]]:
                            res.append([nums[L], nums[i], nums[R]])
                            print(nums[L], nums[i], nums[R])
                    else:
                        res.append([nums[L], nums[i], nums[R]])
                        print(nums[L], nums[i],  nums[R])

            if nums[L] + nums[R] < 0:
                L += 1
            else:
                R -= 1


if __name__ == '__main__':

    a = Solution()
    a.threeSum([-4,-2,-2,-2,0,1,2,2,2,3,3,4,4,6,6])