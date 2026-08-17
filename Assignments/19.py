def unique_list(list):
    list2 = []

    for i in list:
        if i not in list2:
            list2.append(i)

    return list2


numbers = [1,2,2,3,4,5,6,6,7]
print("unique list : " , unique_list(numbers))
