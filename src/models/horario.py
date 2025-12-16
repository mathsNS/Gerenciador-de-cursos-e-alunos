class Horario:
    def __init__(self, tempo):
        self.start, self.end = map(int, tempo.split('-'))

    def choca_com(self, outro):
        return max(self.start, outro.start) < min(self.end, outro.end)