# A config file to help speed up match day work.
# For storing the time of the match + IP addresses too potentially.


class BohsConfig:
    def __init__(self):
        self.hour : int = 16
        self.minute : int = 45
        self.second : int = 1
        self.microsecond : int = 1

        assert 0 <= self.hour <= 23, "Hour must be between 0 and 23"
        assert isinstance(self.hour, int), "Hour must be an int"
        assert 0 <= self.minute <= 59 and isinstance(self.minute, int), "Minute must be between 0 and 59"
        assert isinstance(self.minute, int), "Minute must be an int"
        assert 0 <= self.second <= 59, "Second must be between 0 and 59"
        assert isinstance(self.second, int), "Second must be an int"
        assert isinstance(self.microsecond, int), "Microsecond must be an int"

    def __str__(self):
        return f"hour: {self.hour}, minute: {self.minute}, second: {self.second}, microsecond: {self.microsecond}"



def test():
    x = BohsConfig()
    print(x)
    print(x.hour)


if __name__ == "__main__":
    test()
