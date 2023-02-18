fingers = detector.fingersUp()
def suyketqua(a):
    if a == "ngon cai":
        return fingers[0]==1
    elif a == "ngon tro":
        return fingers[1]==1
    elif a == "ngon giua":
        return fingers[2]==1
    elif a == "ngon ap ut":
        return fingers[3]==1
    elif a == "ngon ut":
        return  fingers[4]==1