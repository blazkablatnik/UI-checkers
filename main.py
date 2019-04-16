from checkers import Board, Utility

b = Board()
b.set_board("..........,.o........,..........,.o........,..x.......,..........,..........,..........,..........,..........")
print(b)
for move in b.legal_moves():
    print("\n")
    print("-------------------")
    print("\n")
    for m in move:
        print(m)
        print(b.push([m]))
        print("\n")

# for i in range(1000):
#     print("---")
#     b.push(b.legal_moves()[0])
#     print(b)

k = Board()
print(k)
#k.push(k.legal_moves()[0])
#print(k)
#k.pop()
#print(k)