# Include/loop_closer.py

# from pydbow3 import DBoW3  # Python bindings for DBoW3

# class LoopCloser:
#     """
#     Detect loop closures using a Bag-of-Words database.
#     """
#     def __init__(self, vocab_path):
#         # Load vocabulary and create a database
#         self.vocab = DBoW3.Vocabulary(vocab_path)
#         self.db    = DBoW3.Database(self.vocab, False, 0)
#         self.kf_list = []  # list of (kf_idx, descriptors)

#     def insert_keyframe(self, kf_idx, descriptors):
#         """Add a new keyframe’s descriptors to the DB."""
#         self.db.add(descriptors)
#         self.kf_list.append((kf_idx, descriptors))

#     def detect_loop(self, descriptors, score_thresh=0.1):
#         """
#         Query the database for similar keyframes.
#         Returns: list of candidate kf_idx above the threshold.
#         """
#         results = self.db.query(descriptors, 4)
#         loops = []
#         for (kf_idx, _), score in zip(self.kf_list, results.score):
#             if score > score_thresh:
#                 loops.append(kf_idx)
#         return loops
