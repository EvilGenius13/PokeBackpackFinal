import enum

class FormEnum(enum.Enum):
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)