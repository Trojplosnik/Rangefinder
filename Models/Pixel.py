class Pixel:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def to_string(self) -> str:
        return f"({self.x}, {self.y})"

    def print(self):
        print(self.to_string())
