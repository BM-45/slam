class Config:

    def __init__(self, K):
        self.K = K
        self.focal = float(K[0, 0])
        self.pp = (float(K[0, 2]), float(K[1, 2]))
