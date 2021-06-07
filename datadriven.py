import csv, numpy, glob, itertools
from multiprocessing import Pool

def main():
    csvs = glob.glob("*.csv")
    csvCounts = len(csvs)
    combinations = list(itertools.combinations(csvs, 2))
    
    last = 0
    groupList = []

    for i in range(1,len(combinations) // 5):
        next = 5 * i
        groupList.append(combinations[last : next])
        last = next
    groupList.append(combinations[last:])

    results = []
    with Pool(50) as pool:
        results = pool.map(groupProcess, groupList)
    results = numpy.array(results)
    results = results.ravel()
    results = results.reshape(-1, 3)
    print("results", len(results))
    results.ravel()
    
    matrix = []
    for i in range(30):
        row = []
        for j in range(30):
            row.append(0)
        matrix.append(row)
    matrix = numpy.array(matrix)
    print(matrix)
    
    for element in results:
        if element[2] == 0:
            continue
        rowNumber = 10 * (int(element[0][0:2].strip()) - 1) + int(element[0][2:4].strip()) - 1
        colNumber = 10 * (int(element[1][0:2].strip()) - 1) + int(element[1][2:4].strip()) - 1
        print(rowNumber, colNumber)
        matrix[rowNumber][colNumber] = int(element[2])
        matrix[colNumber][rowNumber] = int(element[2])
        
    print(matrix)
    numpy.savetxt('matrix.txt', matrix, delimiter=',', fmt="%s")
    
    numpy.savetxt('results.csv',results, delimiter=',', fmt="%s")
    print(results)

def groupProcess(dataList):
    tmpResult = []
    for combi in dataList:

        print(combi[0])
        print(combi[1])
        tmpResult.append(calc(combi[0], combi[1]))
    return tmpResult

def calc(data1, data2):
    def readCsv(data):
        with open(str(data)) as file:
            h = next(csv.reader(file))
            body01 = file.read()

        csvData01 = csv.reader(body01.strip().splitlines())
        return numpy.array([row for row in csvData01])

    list01 = readCsv(data1)
    list02 = readCsv(data2)


    score = 0
    tmpScore = 0
    for i in range(len(list01)):
        lower = 0
        upper = 0
        for j in range(60):
            if i+j < len(list01):
                a = float(list01[i+j][2])
                b = float(list02[i+j][2])
                upper += (a-b)**2
                lower += a**2 + b**2
            else:
                break
        if lower >= 5500 and upper / lower <= 0.05:
            tmpScore += 1
            if tmpScore >= 15:
                score += 1
        else:
            tmpScore = 0

    print(score)
    return numpy.array([data1, data2, score])

if __name__ == "__main__":
    main()
