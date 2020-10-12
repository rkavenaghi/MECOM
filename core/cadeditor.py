from math import sqrt
class Ponto():
    RADIUS_POS_THRESHOLD = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pos(self):
        return self.x, self.y

    def region(self, x, y):
        print(x, y, self.x, self.y)
        if (self.x-self.RADIUS_POS_THRESHOLD < x < self.x+self.RADIUS_POS_THRESHOLD and
            self.y - self.RADIUS_POS_THRESHOLD < y < self.y + self.RADIUS_POS_THRESHOLD):
            return True
        else:
            return False


class Linha():
    def __init__(self, Point_s, Point_f):
        self.p_start = Point_s
        self.p_end = Point_f
        self.length()


    def length(self):
        # Cálculo do comprimento da linha
        self.line_length =  ((self.p_start.x - self.p_end.x)**2 +
                             (self.p_start.y - self.p_end.y)**2)**0.5
        return self.line_length


if __name__ == '__main__':
    p1 = Ponto(4, 5)
    p2 = Ponto(5, 6)
    line = Linha(p1, p2)



