#coding=gbk
#降序

def bubble_sort(alist):
    n = len(alist)
    count = 0
    for j in range(n-1):
        #总共遍历n-1次，将每次都将一个最大的元素移动到最后
        for i in range(0, n-1-j):
            #每一次遍历都会将较大的元素向后移动一位
            if alist[i] > alist[i+1]:
                alist[i], alist[i+1] = alist[i+1], alist[i]
                count += 1
        if count == 0:
            break
            #加入if之后，如果最开始就是有序的那么将不会进行接下来的比较


#----------------------------------------------------------------------
def select_sort(alist):
    n = len(alist)
    for i in range(n-1):
        #每次遍历都将最小的元素放在无序列表的第i位
        min_index = i
        for j in range(i+1, n):
            #从i的下一个值开始遍历，如果有比i位置元素小的元素就将该元素下标交换给min_index。
            if alist[j] < alist[min_index]:
                min_index = j
        if min_index != i:
            #如果发现下标被置换过，那就直接将这两个元素交换。
            alist[i], alist[min_index] = alist[min_index],alist[i]
            
#----------------------------------------------------------------------
def insert_sort(alist):
    n = len(alist)
    for i in range(1,n):
        for j in range(i,1,-1):
            if alist[j] < alist[j-1]:
                alist[j-1],alist[j] = alist[j],alist[j-1]
            else:
                break
            
#----------------------------------------------------------------------
def shell_sort(alist):
    n= len(alist)
    gap = n//2
    while gap >0:
        for i in range(gap,n):
            j = i
            while j>=gap and alist[j-gap] > alist[j]:
                alist[j-gap],alist[j] = alist[j],alist[j-gap]
                j -= gap
        gap = gap//2
        
#----------------------------------------------------------------------
def quick_sort(alist):
    n = len(alist)
    if start >= end:
            return
    mid = alist[start]
    left = start
    right = end 
    while left < right:
        while left < right and alist[right] >= mid:
            right -= 1
        while left < right and alist[left]< mid:
            left += 1 
        alist[right],alist[left] = alist[left],alist[right]
    alist[left] = mid 
    quick_sort(alist,start,left-1)
    quick_sort(alist,left+1,end)

#----------------------------------------------------------------------
def merge_sort(alist):
    n = len(alist)
    if 1 == n :
        return alist
    mid = n//2
    left_sorted_li = merge_sort(alist[:mid])
    right_sorted_li = merge_sort(alist[mid:])
    left,right = 0,0
    merge_sorted_li = []
    left_n = len(right_sorted_li)
    
    while left < left_n and right < right_n:
        if left_sorted_li[left] <= right_sorted_li[right]:
            merge_sorted_li.append(left_sorted_li[left])
            left += 1
        else:
            merge_sorted_li.append(right_sorted_li[right])
            right += 1
    merge_sorted_li += left_sorted_li[left:]
    merge_sorted_li += right_sorted_li[right:]
    return merge_sort_li


#堆排序 
def buildMaxHeap(alist):
    import math
    for i in range(math.floor(len(alist)/2),-1,-1):
        heapify(alist,i)

def heapify(alist,i):
    left = 2*i+1
    right = 2*i+2
    largest = i
    if left < alistLen and alist[left] > alist[largest]:
        largest = left
    if right <alistLen and alist[right] >alist[largest]:
        largest = right
    if largest != i:
        swap(alist,i,largest)
        heapify(alist, largest)

def swap(alist,i,j):
    alist[i],alist[j] = alist[j],alist[i]
    
def heapSort(alist):
    global alistLen
    alistLen = len(alist)
    buildMaxHeap(alist)
    for i in range(len(alist)-1,0,-1):
        swap(alist,0,i)
        alistLen -= 1
        heapify(alist,0)
    return alist
    

def Count_Sort(l):
    n = len(l)
    res = [None] * n
    for i in range(n):
        p = 0
        q = 0
        for j in range(n):
            if l[i] >l[j]:
                p += 1
            elif l[i] == l[j]:
                q += 1
        for k in range(p,p+q):
            res[k] = l[i]
    return res
                
    
    
    
                
    
    
    