from checkers import Board, Utility

b = Board().set_board("..........,.o........,..........,.o........,..x.......,..........,..........,..........,..........,..........")
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

#k = Board()
#print(k)
#k.push(k.legal_moves()[0])
#print(k)
#k.pop()
#print(k)

# DIY TESTI
print("--------------------")
print("Running tests...")

# Test 1
b = Board().set_board("..........,.x........,..........,.x........,..........,..........,..........,..........,........o.,..........")
moves = Utility().moves_to_string(b.legal_moves())
if (moves == "Move[X,f(1, 1),t(0, 0)],Move[X,f(1, 1),t(0, 2)],Move[x,f(3, 1),t(2, 0)],Move[x,f(3, 1),t(2, 2)]"):
    print("OK")
else:
    print("Problem in test 1. Result is: " + moves)

# Test 2
b = Board().set_board("..........,.o........,..........,.o........,..........,..........,..........,..........,........x.,..........")
b.color = False
moves = Utility().moves_to_string(b.legal_moves())
if (moves == "Move[o,f(1, 1),t(2, 0)],Move[o,f(1, 1),t(2, 2)],Move[o,f(3, 1),t(4, 0)],Move[o,f(3, 1),t(4, 2)]"):
    print("OK")
else:
    print("Problem in test 2. Result is: " + moves)

# Test 3
b = Board().set_board("..........,.o........,..........,.o........,..........,..........,..........,..........,..........,..........")
moves = Utility().moves_to_string(b.legal_moves())
if (moves == ""):
    print("OK")
else:
    print("Problem in test 3. Result is: " + moves)

# Test 4
b = Board().set_board("..........,.o.o......,..........,..x.......,..........,..........,..........,..........,..........,..........")
moves = Utility().moves_to_string(b.legal_moves())
if (moves == "Move[x,f(3, 2),t(2, 1)],Move[x,f(3, 2),t(2, 3)]"):
    print("OK")
else:
    print("Problem in test 4. Result is: " + moves)

# Test 5
b = Board().set_board("..........,.o.o......,..x.......,..........,..........,..........,..........,..........,..........,..........")
moves = Utility().moves_to_string(b.legal_moves())
if (moves == "Move[X,f(2, 2),t(0, 0)],Move[X,f(2, 2),t(0, 4)]"):
    print("OK")
else:
    print("Problem in test 4. Result is: " + moves)

# Test 6
b = Board().set_board("..........,.o...o....,..o.o.....,...x......,..........,..........,..........,..........,..........,..........")
moves = Utility().moves_to_string(b.legal_moves())
if (moves == ""):
    print("OK")
else:
    print("Problem in test 6. Result is: " + moves)

# Test 7
b = Board().set_board("..........,...o.o....,..........,...o.o....,....x.....,..........,..........,..........,..........,..........")
moves = Utility().moves_to_string(b.legal_moves())
if (moves == "Move[x,f(4, 4),t(2, 2)]Move[x,f(2, 2),t(0, 4)]Move[x,f(0, 4),t(2, 6)]Move[x,f(2, 6),t(4, 4)],Move[x,f(4, 4),t(2, 6)]Move[x,f(2, 6),t(0, 4)]Move[x,f(0, 4),t(2, 2)]Move[x,f(2, 2),t(4, 4)]"):
    print("OK")
else:
    print("Problem in test 7. Result is: " + moves)

# Test 8
b = Board().set_board("..........,...o.o....,..........,...o......,....x.....,...o......,..........,..........,..........,..........")
moves = Utility().moves_to_string(b.legal_moves())
if (moves == "Move[x,f(4, 4),t(2, 2)]Move[x,f(2, 2),t(0, 4)]Move[x,f(0, 4),t(2, 6)]"):
    print("OK")
else:
    print("Problem in test 8. Result is: " + moves)
