# -*- coding: utf-8  -*-
# -*- author: jokker -*-


def test(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    count, res = 0, nums[0]  # 初始化计数器和结果
    for i in range(len(nums) - 1):  # 遍历数组中每一个数
        print(res)
        if nums[i] == res:  # 如果当前的数和结果变量相同
            count += 1  # 计数器+1
        else:  # 否则
            count -= 1  # 计数器-1
            if count == 0:  # 如果减到了0
                res = nums[i + 1]  # 那么更新结果变量为下一个数
    return res



if __name__ == "__main__":

    print(test( [-2,1,-3,4,-1,4,4,4,4,4,4,2,1,-3,4,-1,4,4,4,4,4,4,4,4,4,2,1,-5,4,133,78]))
