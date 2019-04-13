from checkers import Board

b = Board()
print(b)
[print(x) for x in b.legal_moves()]

# for i in range(1000):
#     print("---")
#     b.push(b.legal_moves()[0])
#     print(b)

k = Board()
print(k)
k.push(k.legal_moves()[0])
print(k)
k.pop()
print(k)
