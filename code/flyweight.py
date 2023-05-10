from dataclasses import dataclass
import random
from collections import namedtuple
from enum import Enum

TreeSprites = ['pine.bmp', 'chestnut.bmp', 'oak.bmp']

Coord = namedtuple('Coord', 'x,y')


class TreeFlyweight:
    pool = dict()

    def __new__(cls, path):
        self = cls.pool.get(path, None)

        if self is None:
            self = super().__new__(cls)
            cls.pool[path] = self
            self.__bmp = cls.load(path)

        return self

    @classmethod
    def load(cls, path):
        print(f'Loading bitmap from {path}')

        return "***" + path + "***"

    def render(self, coord):
        print(f'Rendering {self.__bmp}#{id(self)} at ({coord.x}, {coord.y})')


@dataclass
class TreeSprite:
    bitmap: TreeFlyweight
    coord: Coord

    def render(self):
        self.bitmap.render(self.coord)


def main():
    t1 = TreeFlyweight(TreeSprites[0])
    t1.render(Coord(10, 20))

    rnd = random.Random()
    min_point, max_point = 0, 100

    forest = []

    # creation of forest
    for _ in range(30):
        rnd_index = rnd.randint(0, len(TreeSprites)-1)
        path = TreeSprites[rnd_index]
        x = rnd.randint(min_point, max_point)
        y = rnd.randint(min_point, max_point)
        forest.append(TreeSprite(TreeFlyweight(path), Coord(x, y)))

    # rendering
    for tree in forest:
        tree.render()


if __name__ == '__main__':
    main()

    tf1 = TreeFlyweight('oak.bmp')
    tf2 = TreeFlyweight('oak.bmp')

    print(tf1 == tf2)

