from datetime import datetime
from datetime import timedelta 

import seed

class BadgeAnalyzer:

    login_sequence = []
    final_result = []

    """
    Class constructor.

    Args:
        login_sequence: List of login timestamps.
    Returns: -
    """
    def __init__(self, login_sequence: list) -> None:
        self.login_sequence = login_sequence
    ####### end __init__()


    """
    Main method of the class. Used as a wrapper for all the internal logic.

    Args: -
    Returns: -
    """
    def run(self) -> None:
        # drop the time from the timestamp and keep the date
        # this is because we're only interested in counting consecutive days, not logins
        date_seq = self.convert_datetime_to_date(self.login_sequence)
        
        # drop any duplicates (i.e. multiple logins on the same day)
        date_seq = self.drop_duplicates(date_seq)
        
        # sort date sequence in ascending order
        date_seq = self.sort_sequence(date_seq)
        
        # actually loop through the sequnce counting subsequences
        ret = self.get_longest_subsequence(date_seq)
        
        self.final_result = ret
        
        # output results
        self.tabulate_results(ret)
    ####### end run()


    """
    Method to loop through the date sequence looking for an subsequences

    Args: 
        seq: List of login dates
    Returns: -
    """
    def get_longest_subsequence(self, seq) -> list:
        # create list to store the subsequences
        subsequence_len = [] # format is: [(start, end, count), (start, end, count), ...]
        
        start_dt = end_dt = '' # will be set for each subsequence
        count = 0 # number of consecutive days

        # cater for edge case of only one day in the sequence
        # note that if the length of the sequence is zero, it will simply skip the for loop and return an empty list
        if len(seq) == 1:
            return [(seq[0], seq[0], 1)]

        for i in range(len(seq)):
            # if it's the first element, we consider it a new subsequence
            if i == 0:
                start_dt = seq[0]
                continue
            
            count += 1

            # get current element minus previous element 
            date_diff = self.get_date_diff(seq[i], seq[i-1])
            
            reset_sequence = False
            if i == (len(seq) - 1): # means we're already at the end of the full sequence
                # end current sequence
                end_dt = seq[i]
                count += 1
                reset_sequence = True
            elif date_diff > 1: # means the sequence hasn't started yet or it's broken here
                # end previous sequence
                end_dt = seq[i-1]
                reset_sequence = True
            
            if reset_sequence:
                # push tuple onto the final list
                subsequence_len.append((start_dt, end_dt, count))    
                # reset sequence
                start_dt = seq[i]
                end_dt = ''
                count = 0
        ####### end for i in range(len(seq))

        return self.sort_tuples_descendingly(subsequence_len)
    ####### end get_longest_subsequence()


    """
    Method to convert datetime strings into date strings.

    Args: 
        seq: List of login timestamps (as datetime string).
    Returns:
        date_seq: List of login dates (as date string).
    """
    def convert_datetime_to_date(self, seq: list) -> list:
        date_seq = []
        for item in seq:
            date_seq.append(item.split()[0])
        return date_seq
    ####### end convert_datetime_to_date()


    """
    Method to calculate the difference in days between two date strings.

    Args: 
        date1: Date to subtract from (i.e. left-hand operand).
        date2: Date to be subtracted from (i.e. right-hand operand).
    Returns:
        Number of days between the input dates.
    """
    def get_date_diff(self, date1, date2) -> int:
        try:
            date1_val = datetime.strptime(date1, '%Y-%m-%d')
            date2_val = datetime.strptime(date2, '%Y-%m-%d')
        except ValueError as e:
            raise Exception('Invalid date format')
        return (date1_val - date2_val).days
    ####### end get_date_diff()


    """
    Method to sort a list of elements. This was separated into a method in case 
    we decide to enhace the sorting algorithm later on.

    Args: 
        seq: List of elements to be sorted.
    Returns:
        Sorted list of input elements.
    """
    def sort_sequence(self, seq: list) -> list:
        return sorted(seq)
    ####### end sort_sequence()


    """
    Method to drop any duplicate elements in a list. It was separated into a method 
    in case we want to enhance the logic later on.

    Args: 
        seq: List of elements to be cleaned up.
    Returns:
        List of unique elements in the input list.
    """
    def drop_duplicates(self, seq: list) -> list:
        # convert to set() to drop the duplicates
        return list(set(seq))
    ####### end drop_duplicates()


    """
    Method to sort the list of subsequence tuples in descending order.

    Args: 
        in_list: List of subsequence tuples in the format: (start, end, count).
    Returns:
        input list, sorted by the 'count' element descendingly.
    """
    def sort_tuples_descendingly(self, in_list: list) -> list:
        return sorted(in_list, key=lambda x: x[-1], reverse=True)
    ####### end sort_tuples_descendingly()


    """
    Method to pretty-print the list of subsequence tuples.

    Args: 
        in_list: List of subsequence tuples in the format: (start, end, count).
    Returns: -
    """
    def tabulate_results(self, res_list: list) -> None:
        print(
            '|----------|----------|--------|\n' +
            '|  START   |   END    | LENGTH |\n' +
            '|----------|----------|--------|'
        )
        for record in res_list:
            print("|{}|{}|   {}    |".format(record[0], record[1], record[2]))
    ####### end tabulate_results

####### end class BadgeAnalyzer

###############################################################
# now we actually run the solution code
###############################################################

# get random sequence
seq = seed.res

print('\n')

# run
badge_analyzer_obj = BadgeAnalyzer(seq)
badge_analyzer_obj.run()