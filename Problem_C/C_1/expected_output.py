def digit_sum(n):
    return sum(int(digit) for digit in str(n))

def find_difference(numbers):
    min_num = float('inf')
    max_num = float('-inf')
    for num in numbers:
        if digit_sum(num) == 30:
            min_num = min(min_num, num)
            max_num = max(max_num, num)
    return max_num - min_num