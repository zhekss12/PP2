n = int(input())
nums = input().split()

count = 0
i = 0

while i < n:
    if int(nums[i]) > 0:
        count += 1
    i = i + 1

print(count)