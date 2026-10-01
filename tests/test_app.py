import unittest

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"

class TestPomodoroLogic(unittest.TestCase):
    def test_format_time_work(self):
        # 25 phút = 1500 giây
        self.assertEqual(format_time(1500), "25:00")

    def test_format_time_break(self):
        # 5 phút = 300 giây
        self.assertEqual(format_time(300), "05:00")

    def test_format_time_zero(self):
        self.assertEqual(format_time(0), "00:00")

if __name__ == "__main__":
    unittest.main()