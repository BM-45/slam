import cv2

# Brute force matcher for orb descriptor.
class Matcher:
    def __init__(self):
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def match(self, des1, des2, max_matches=200):
        if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
            return []
        matches = self.bf.match(des1, des2)
        matches = sorted(matches, key=lambda m: m.distance)
        return matches[:max_matches]


class FlannMatcher:
    def __init__(self):
        FLANN_INDEX_LSH = 6
        index_params = dict(
            algorithm=FLANN_INDEX_LSH,
            table_number=12,      
            key_size=20,          
            multi_probe_level=2  
        )
        search_params = dict(checks=50)
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)

    def match(self, des1, des2, ratio=0.7):
        if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
            return []
        raw_matches = self.flann.knnMatch(des1, des2, k=2)
        good = []
        for pair in raw_matches:
        
            if len(pair) < 2:
                continue
            m, n = pair
            if m.distance < ratio * n.distance:
                good.append(m)
        return sorted(good, key=lambda m: m.distance)
