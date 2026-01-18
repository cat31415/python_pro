from collections import deque

n = int(input())
    
left = deque()
right = deque()
results = []

for _ in range(n):
    line = input().split()
    cmd = line[0]
    if len(right) == 0:
        right.append(int(line[1]))
        continue
    if cmd == '+':
        if len(right) == len(left):
            right.appendleft(left.pop()) #IndexError: pop from an empty deque
        left.appendleft(int(line[1]))
        
    elif cmd == '*':
        num = int(line[1])
        
        if len(left) < len(right):
            left.append(num)
        else:
            right.appendleft(num)
            
    elif cmd == '-':
        if len(left) == len(right):
            right.appendleft(left.pop())
        results.append(right.pop())
        
    
for a in results:
    print(a)