class NoGeneratorError(Exception):

    def __init__(self):
        super().__init__(self)

    def __str__(self):
        Msg = "None available generator"
        return Msg
