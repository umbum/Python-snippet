class Tst:
    var = "Tst, string var"
    def __init__(self, name):
        self.name = name
        self.var = 33
    def functst(self, a, b):
        result = a + b
        print("Tst, " + self.name + " funcTst : "+str(result))


class Bird(Exception):
    def fly(self):
        raise NotImplementedError


class FastBird(Bird):
    def fly(self):
        print("fly")

class Cal4:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def add(self):
        return self.a+self.b
    def sub(self):
        return self.a-self.b
    def mul(self):
        return self.a*self.b
    def div(self):
        return self.a/self.b


class Cal7(Cal4):
    def square(self):
        return self.a**self.b
    def mod(self):
        return self.a%self.b
    def quotient(self):
        return self.a//self.b