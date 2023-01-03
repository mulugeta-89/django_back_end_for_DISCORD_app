class Human:
    def __init__(self, name, age, color):
        self.name = name
        self.age = age
        self.color = color
    def introduce_self(self):
        return "My name is {} and my age is {} and my color is {}".format(self.name, self.age, self.color)

r1 = Human("Mulugeta", 21, "orange")
print(r1.introduce_self())