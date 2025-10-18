pushed = [1,2,3,4,5]
popped = [4,5,3,2,1]

stack = []
j = 0

for val in pushed:
    stack.append(val)

    while stack and j< len(popped) and stack[-1] == popped[j]:
        stack.pop()
        j +=1

if not stack:
    print(True)
else:
    print(False)