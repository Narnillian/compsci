for i in ['./Shalhevet.txt','./North_Shore.txt']:
    print(i)
    stats = open(i,'r')
    while True:
        line = stats.readline()
        if line == '':
            break
        print(line)
    stats.close()
    print()

stats = open('./Shalhevet.txt','r')
while True:
    line = stats.readline()
    if line == '':
        break
    print(line)
stats.close()
