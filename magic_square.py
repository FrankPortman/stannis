def generate_square(n):
    ''' Generate n x n magic square. A magic square is a square
    where all rows, columns, and diagonals sum to the same thing.
    We specifically fill the values from 1 to n^2 in the square and use this
    as an isomorphism for tic tac toe victory conditions.
    '''

    '''
    Subset sum problem approach for victory determination.
    '''
    magic_square = [[0 for x in range(n)]for y in range(n)]
 
    i = n / 2
    j = n - 1
     
    num = 1
    while num <= (n * n):
        if i == -1 and j == n:
            j = n - 2
            i = 0
        else:
            if j == n:
                j = 0
            if i < 0:
                i = n - 1
        if magic_square[i][j]:
            j = j - 2
            i = i + 1
            continue
        else:
            magic_square[i][j] = num
            num = num+1

        j = j + 1
        i = i - 1

    return magic_square
