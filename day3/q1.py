def main():

    data = readFiles()

    grid = makeOverlapGrid()
    mapOverlapGrid(data, grid)
    result = countOverlap(grid)

    print(result)

def makeOverlapGrid():
    return [[0 for x in range(1000)] for y in range(1000)]

def mapOverlapGrid(data, grid):

    for datum in data:
        for x in range(datum["startX"], datum["endX"]):
            for y in range(datum["startY"], datum["endY"]):

                if grid[x][y] == 0:
                    grid[x][y] = 1
                elif grid[x][y] == 1:
                    grid[x][y] = 2

def countOverlap(grid):
    count = 0
    for x in range(1000):
        for y in range(1000):
            if grid[x][y] == 2:
                count += 1
    return count

def processFileLine(line):
    datum = {}
    lineSplit = line.split()
    startCoor = lineSplit[2].split(',')
    startCoor[1] = startCoor[1][:-1]
    dim = line.split()[3].split('x')
    datum["startX"] = int(startCoor[0])
    datum["startY"] = int(startCoor[1])
    datum["endX"] = datum["startX"] + int(dim[0])
    datum["endY"] = datum["startY"] + int(dim[1])
    return datum

def readFiles():
    data = []
    file = open("input.txt", "r")
    for line in file:
        data.append(processFileLine(line))
    file.close()
    return data

if __name__ == "__main__":
    main()
