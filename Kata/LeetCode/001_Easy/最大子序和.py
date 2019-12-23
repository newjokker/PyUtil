# -*- coding: utf-8  -*-
# -*- author: jokker -*-


def test(numbs):
    dp = [None for i in range(len(numbs))]

    dp[0] = numbs[0]

    for i in range(1, len(numbs)):
        numb = numbs[i]
        cur_sum = dp[i-1] + numb
        dp[i] = max(cur_sum, numb)
    return max(dp)






if __name__ == "__main__":
    print(test( [-2,1,-3,4,-1,2,1,-5,4]))
