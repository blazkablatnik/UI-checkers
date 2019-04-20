from checkers import Board

b = Board()
b.set_board("..........,.o........,..........,.o........,..x.......,..........,..........,..........,..........,..........")
print(b)
while len(b.legal_moves()) > 0:
    print("-------------------")
    m = b.legal_moves()[0]
    b.push(m)
    print(m)
    print(b)