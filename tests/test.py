import sys
import os.path
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from solution import BadgeAnalyzer

class TestBadgeAnalyzer(unittest.TestCase):

    def test_run_valid_results(self):
        login_seq = [
            '2021-03-13 15:13:05', '2021-03-13 23:13:05', '2021-03-16 15:13:05', 
            '2021-03-16 23:13:05', '2021-03-17 07:13:05', '2021-03-17 15:13:05', 
            '2021-03-17 23:13:05', '2021-03-18 07:13:05', '2021-03-18 15:13:05'
        ]

        badge_analyzer_obj = BadgeAnalyzer(login_seq)
        badge_analyzer_obj.run()
        
        self.assertEqual(badge_analyzer_obj.final_result[0][0], '2021-03-16')
        self.assertEqual(badge_analyzer_obj.final_result[0][1], '2021-03-18')
        self.assertEqual(badge_analyzer_obj.final_result[0][2], 3)


    def test_get_longest_subsequence_valid_results(self):
        login_seq = [
            '2021-03-13', '2021-03-16', '2021-03-17', '2021-03-18'
        ]

        badge_analyzer_obj = BadgeAnalyzer([])
        ret = badge_analyzer_obj.get_longest_subsequence(login_seq)

        self.assertEqual(ret[0][0], '2021-03-16')
        self.assertEqual(ret[0][1], '2021-03-18')
        self.assertEqual(ret[0][2], 3)


    def test_get_longest_subsequence_edge_case(self):
        login_seq = [
            '2021-03-13'
        ]

        badge_analyzer_obj = BadgeAnalyzer([])
        ret = badge_analyzer_obj.get_longest_subsequence(login_seq)
        
        self.assertEqual(ret[0][0], '2021-03-13')
        self.assertEqual(ret[0][1], '2021-03-13')
        self.assertEqual(ret[0][2], 1)


    # convert_datetime_to_date() positive case
    def test_convert_datetime_to_date_valid_results(self):
        login_seq = [
            '2021-03-13 15:13:05', '2021-03-13 23:13:05', '2021-03-16 15:13:05', 
            '2021-03-16 23:13:05', '2021-03-17 07:13:05', '2021-03-17 15:13:05', 
            '2021-03-17 23:13:05', '2021-03-18 07:13:05', '2021-03-18 15:13:05'
        ]

        badge_analyzer_obj = BadgeAnalyzer([])
        date_list = badge_analyzer_obj.convert_datetime_to_date(login_seq)
        
        self.assertEqual(date_list[0], '2021-03-13')
        self.assertEqual(date_list[-1], '2021-03-18')


    # get_date_diff() positive case
    def test_get_date_diff_valid_results(self):
        badge_analyzer_obj = BadgeAnalyzer([])

        ret = badge_analyzer_obj.get_date_diff('2021-05-10', '2021-05-07')
        self.assertEqual(ret, 3)
        
        ret = badge_analyzer_obj.get_date_diff('2021-10-10', '2021-10-10')
        self.assertEqual(ret, 0)

        ret = badge_analyzer_obj.get_date_diff('2021-10-20', '2021-10-10')
        self.assertEqual(ret, 10)


    # get_date_diff() negative case
    def test_get_date_diff_invalid_input(self):
        badge_analyzer_obj = BadgeAnalyzer([])
        
        self.assertRaises(
            Exception, 
            badge_analyzer_obj.get_date_diff, 
            '2021-06-05', 
            'ABCDEFG'
        )


    def test_sort_sequence(self):
        in_seq = [
            '2021-03-17', '2021-03-13', '2021-03-18', '2021-03-16', 
        ]

        badge_analyzer_obj = BadgeAnalyzer([])
        out_seq = badge_analyzer_obj.sort_sequence(in_seq)
        
        self.assertEqual(out_seq[0], '2021-03-13')
        self.assertEqual(out_seq[-1], '2021-03-18')
    

    def test_drop_duplicates(self):
        in_seq = [
            '2021-03-13', '2021-03-13', '2021-03-13', '2021-03-13', '2021-03-13', 
            '2021-03-16', '2021-03-17', '2021-03-18', '2021-03-18', '2021-03-18' 
        ]

        badge_analyzer_obj = BadgeAnalyzer([])
        out_seq = badge_analyzer_obj.drop_duplicates(in_seq)
        
        cnt = len([i for i in out_seq if i == '2021-03-13'])
        self.assertEqual(cnt, 1)

        cnt = len([i for i in out_seq if i == '2021-03-18'])
        self.assertEqual(cnt, 1)
        

    def test_sort_tuples_descendingly(self):
        in_seq = [
            ('2021-06-20', '2021-06-22', 3), 
            ('2021-06-26', '2021-06-28', 3), 
            ('2021-06-04', '2021-06-04', 1), 
            ('2021-07-07', '2021-07-09', 3), 
            ('2021-07-29', '2021-08-03', 6), 
            ('2021-06-12', '2021-06-13', 2), 
            ('2021-06-06', '2021-06-10', 5), 
            ('2021-07-21', '2021-07-27', 7), 
            ('2021-06-15', '2021-06-16', 2), 
            ('2021-06-30', '2021-07-01', 2), 
            ('2021-07-14', '2021-07-15', 2), 
            ('2021-06-18', '2021-06-18', 1), 
        ]

        badge_analyzer_obj = BadgeAnalyzer([])
        out_seq = badge_analyzer_obj.sort_tuples_descendingly(in_seq)
        
        self.assertEqual(out_seq[0][0], '2021-07-21')
        self.assertEqual(out_seq[0][1], '2021-07-27')
        self.assertEqual(out_seq[0][2], 7)

        self.assertEqual(out_seq[1][0], '2021-07-29')
        self.assertEqual(out_seq[1][1], '2021-08-03')
        self.assertEqual(out_seq[1][2], 6)


if __name__ == '__main__':
    unittest.main()