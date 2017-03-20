
class MulLayer:
    def __init__(self):
        self.x = None
        self.y = None

    def forward(self, x, y):
        self.x = x
        self.y = y
        return x*y

    def backward(self, dout):
        dx = dout * self.y
        dy = dout * self.x

        return dx, dy

class AddLayer:
    def __init__(self):
        pass
    
    def forward(self, x, y):
        return x+y
    
    def backward(self, dout):
        return dout, dout

class ReLU:
    def __init__(self):
        self.x = None
    
    def forward(self, x):
        self.x = x
        if x > 0:
            return x
        else:
            return 0

    def backward(self, dout):
        if self.x > 0:
            return dout
        else:
            return 0


apple_cost = 100
apple_num = 2
tax = 1.1

mul_apple_layer = MulLayer()
mul_tax_layer = MulLayer()

apple_price = mul_apple_layer.forward(apple_cost, apple_num)
price = mul_tax_layer.forward(apple_price, tax)

print(price)

dprice=1
dapple_price, dtax = mul_tax_layer.backward(dprice)
dapple_cost, dapple_num = mul_apple_layer.backward(dapple_price)

print(dapple_cost, dapple_num, dtax)

li = [1, -1]

r = ReLU()
r.forward( )
