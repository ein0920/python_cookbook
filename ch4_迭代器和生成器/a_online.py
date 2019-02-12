




# iterating_in_sorted_order_over_merged_sorted_iterables
if __name__ == '__main__':
    # Iterating over merged sorted iterables

    import heapq

    a = [1, 4, 7, 10]
    b = [2, 5, 6, 11]
    for c in heapq.merge(a, b):
        print(c)




