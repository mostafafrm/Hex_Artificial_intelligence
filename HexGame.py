def console(lines):
    count1 = 0
    count2 = 7
    rowSpace = 0
    for i in range(0, 9):
        print("R   ", end=" ")

    for i in range(0, 8):
        for numOfRow in range(0, rowSpace):
            print(" ", end=" ")
        if i != 0:
            print(" ",  end=" ")
            print("B   ", end=" ")
            for line in range(count1, count2):
                print(lines[line] + "  ", end=" ")
            print(" B")
            count1 += 7
            count2 += 7
            rowSpace += 1
        else:
            print("")

    for numOfRowSpaceForRed in range(0, rowSpace+1):
        print(" ", end=" ")

    for i in range(0, 9):
        print("R   ", end=" ")

    print("\nplayer (RED) connects horizontally. ")
    print("CPU (BLUE) connects vertically. ")
    print()


listOfLines = []

for j in range(0, 49):
    if j < 10:
        listOfLines.append(str(j) + " ")
    else:
        listOfLines.append(str(j))
print("Type '1' for starting the game or '2' for CPU to start the game")
count = int(input) % 2
console(listOfLines)

placeOfMove = 0

while True:
    if count % 2 == 1:
        print("player turn\nplease enter your choice : ")
        while True:
            placeOfMove = int(input())
            if cell_list[placeOfMove].color == "white":
                listOfLines[placeOfMove] = "R "
                cell_list[placeOfMove].color = "red"
                break
            else:
                print("Enter a valid number")
        console(listOfLines)
        count += 1
    else:
        print("CPU turn : ")
        # shomareye khoneiy ke entekhab shode ro bedin be placeOfMove
        placeOfMove += 1
        listOfLines[placeOfMove] = "B "
        console(listOfLines)
        count += 1
