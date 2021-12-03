class A:
    def __init__(self, n, m):
        self.n = n
        self.m = m
    def __str__(self) -> str:
        return f"n = {self.n} m = {self.m}"
    
    def __add__(self, other):
        a = self.__init__(self.n + other.n, self.m + other.m)
        return a



# b = str(a) + "a"
# print(b)

a = A(4, 6)
b = A(7, 9)
print(a + b)