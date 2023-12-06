for x in range(-10, 11, 2):
    for y in range(abs(x)//2): print(" ",end = "")
    for y in range(10-abs(x)): print("@", end = "")
    print()