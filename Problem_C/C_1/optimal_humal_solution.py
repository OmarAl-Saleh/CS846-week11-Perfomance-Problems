def digit_sum(n):
    total = 0
    while n:
        total += n % 10
        n //= 10
    return total

def find_difference(numbers):
    min_num = float('inf')
    max_num = float('-inf')
    for num in numbers:
        if num < min_num or num > max_num:
            if digit_sum(num) == 30:
                min_num = min(min_num, num)
                max_num = max(max_num, num)
    return max_num - min_num