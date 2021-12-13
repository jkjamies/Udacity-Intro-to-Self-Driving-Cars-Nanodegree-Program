# File: matrix.py
# Author: jkjamies (GitHub)
# 10/03/2021
# Lab Section: Implement a Matrix Class
# Email: ---
# Description: This program contains various matrix operations, some of which are limited to
#              1x1 and 2x2 matrices. User can create matrices and perform operations on them.
# Collaboration: This was written as an assignment with no collaboration for the
#                Intro to Self-Driving Cars Udacity Nanodegree

import math
from math import sqrt
import numbers

def zeroes(height, width):
    """
    Creates a matrix of zeroes.

    Args:
        height: The height of the zeroes matrix.
        width: The width of the zeroes matrix.

    Returns:
        Zero matrix of height x width size.
    """
    g = [[0.0 for _ in range(width)] for __ in range(height)]
    return Matrix(g)

def identity(n):
    """
    Creates a n x n identity matrix.

    Args:
        n: Size (height and width) of square identity matrix.

    Returns:
        Identity matrix of nxn size.
    """
    I = zeroes(n, n)
    for i in range(n):
        I.g[i][i] = 1.0
    return I

def dot_product(vectorA, vectorB):
    """
    Calculates the dot product of two vectors.

    Args:
        vectorA: First vector to find dot product.
        vectorB: Second vector to find dot product.

    Returns:
        Dot product of two vectors.
    """
    result = 0
    for i in range(len(vectorA)):
        result += vectorA[i] * vectorB[i]
        
    return result

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        
        Returns:
            Determinate of matrix.
            
        Raises:
            ValueError: Raises exception for non-square matrix.
            NotImplementedError: Raises exception for matrix larger than 2x2 size.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1:
            result = self.g[0][0]
        else:
            result = self.g[0][0] * self.g[1][1] - self.g[0][1] * self.g[1][0]
            
        return result

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        
        Returns:
            Sum of diagonal entries of matrix.
            
        Raises:
            ValueError: Raises exception for non-square matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        result = 0
        for i in range(self.h):
            result += self.g[i][i]
            
        return result

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        
        Returns:
            Inverse of the matrix.
        
        Raises:
            ValueError: Raises exception for non-square matrix.
            ValueError: Raises exception for matrix is not invertible.
            NotImplementedError: Raises exception for matrix larger than 2x2 size.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")

        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        
        inverse = []
        if self.h == 1:
            inverse.append([1 / self.g[0][0]])
        elif self.h == 2:
            if self.g[0][0] * self.g[1][1] == self.g[0][1] * self.g[1][0]:
                raise ValueError('The matrix is not invertible.')
            else:
                inverse = 1 / self.determinant() * (self.trace() * identity(self.h) - self)
                        
        return Matrix(inverse)
           
    def T(self):
        """
        Returns a transposed copy of this Matrix.
        
        Returns:
            Transpose of the matrix.
        """
        transpose = zeroes(self.w, self.h)
        for row in range(self.h):
            for col in range(self.w):
                transpose.g[col][row] = self.g[row][col]
                
        return transpose

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.
        
        Args:
            idx: The index to retrieve from the matrix.
        
        Returns:
            Item by index of the matrix.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        
        Returns:
            User-friendly readable string of the matrix.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        
        Args:
            other: The second (other) matrix to add to the matrix.
            
        Returns:
            Matrix of the two added matrices.
        
        Raises:
            ValueError: Raises exception for two matrices not of the same dimensions.
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same")
        
        result = zeroes(self.h, self.w)
        for row in range(self.h):
            for col in range(self.w):
                result[row][col] = self.g[row][col] + other.g[row][col]
                
        return result

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)
        
        Returns:
            Matrix resulting from negating matrix.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        result = zeroes(self.h, self.w)
        for row in range(self.h):
            for col in range(self.w):
                result[row][col] = self.g[row][col] * -1.0
                
        return result

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        
        Args:
            other: The second (other) matrix to subtract from the matrix.
        
        Returns:
            Matrix resulting from a subtraction of two matrices.
        """
        result = zeroes(self.h, self.w)
        for row in range(self.h):
            for col in range(self.w):
                result[row][col] = self.g[row][col] - other.g[row][col]
                
        return result

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        
        Args:
            other: The second (other) matrix to multiply to the matrix.
            
        Returns:
            Matrix resulting in multiplcation of two matrices.
        """
        product = []
        transpose = other.T()
        for row1 in range(self.h):
            new_row = []
            for row2 in range(transpose.h):
                dp = dot_product(self[row1], transpose[row2])
                new_row.append(dp)
            product.append(new_row)
                              
        return Matrix(product)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.
        
        Args:
            other: Second (other) matrix to multiply.
            
        Returns:
            Matrix resulting in multiplication of non-matrix and matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            result = self
            for row in range(self.h):
                for col in range(self.w):
                    result[row][col] *= other
                    
            return result
            