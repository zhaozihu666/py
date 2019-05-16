def bubble_sort(lists):
    count = len(lists)
    for i in range(0,count):
        for j in range(i+1,count):
            if lists[i]>lists[j]:
                lists[i],lists[j] = lists[j],lists[i]
    return lists

lists = [36,25,48,12,25,65,43,57]
a = bubble_sort(lists)
print(a)