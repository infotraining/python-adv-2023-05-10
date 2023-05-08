from collections import defaultdict, Counter
from typing import List, Tuple

def tokenize_file(path: str) -> List[str]:
    with open(path, 'r') as file:
        words = [w.lower() for w in file.read().split()]
    return words

def get_most_common(words: List[str]) -> List[Tuple[str, int]]:
    """TODO"""


print(get_most_common(tokenize_file('holmes.txt')))   