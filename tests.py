import unittest

from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_rows = 12
        num_cols = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 20)
        self.assertEqual(
            len(m1._cells),
            num_cols
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows
        )

if __name__ == "__main__":
    unittest.main()
