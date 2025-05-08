'''
    Jase Hoffmann
    Benfords Law program
    April 15, 2025
'''
#Constants
BENFORDS_DICT = {1: 0.301, 2: .176, 3: .125, 4: .097, 5: .079, 6: .067, 7: .058, 8: .051, 9: .046}
DEGREES_OF_FREEDOM = 8

#Used to calculate p-value
from scipy.stats import chi2


def csv_to_list(csv_file):
    '''
    This fuction makes a csv file into a list
    Args:
    csv_file = a csv file
    Returns:
    a list only containing the numebers in the csv file
    '''
    list_of_numbers = []
    file = open(csv_file, "r") #opens file in read mode
    for line in file:
        items = line.strip().split(",") #splits based on when a comma occurs
        for item in items:
            if item[0].isnumeric(): 
                #if the number is numeric this accounts for floats and ints
                if int(item[0]) > 0:
                    list_of_numbers.append(item) #add to list
    file.close()
    return list_of_numbers

def count_start_digits(list):
    '''
    This fuction is meant to turn the list into a dictionary 
    Args:
    list = list of all numbers in the csv file
    Returns:
    A dictionary with the counts of each first digit
    '''
    dictionary = {}
    for number in list: #iterates over each index of the list
        first_digit = int(str(number[0]))
        if first_digit in dictionary:
            dictionary[first_digit] += 1
        else:
            dictionary[first_digit] = 1
    return dictionary

def digit_percentages(counts):
    '''
    This fuction is meant to find the percentage of each first digit
    Args:
    counts = the dictioanry with the counts of each first digit
    Returns:
    A dictionary with the percentages of each first digit
    '''
    percentages = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    # Setting up the dictionary ensures that the dictionary starts at 0
    total = 0
    for key in counts:
        value = counts[key]
        total += value 
        # This gives us the total number of first digits
    for key in counts:
        amount = counts[key]
        percentage = (amount/total) * 100
        percentages[key] = round(percentage,2) # Round two decimal places
    return percentages

def create_plot(percentages):
    '''
    This fuction is meant create a plot to visualize how much each
    a first digit occurs
    Args:
    percentages = the dictionary that contains the percentages of each number
    Returns:
    A plot
    '''
    string = ""
    for key in percentages:
       amount = int(percentages[key]) # this rounds down the float into an int
       hashtags = amount * "#" #creates teh number of hashtags
       if int(key) == 1:
        string += f"{key} | {hashtags}"
       else:
        string += f"\n{key} | {hashtags}"
    # made to account for line breaks/formatting
    return string

'''
-Original Function before Chi-squared test was added-
def check_benfords_law(percentages):
    This function decided if benfords law works for the csv file
    Args:
    percentages = the dictionary that contains the percentages of each number
    Returns:
    True or False (if benfords law applies)
    # This dictioanry essentially explains benefords law for each number
    for item in percentages:
        number = percentages[item]
        too_much = BENFORDS_DICT[item] + 10 # 10 and 5 were given in instructions
        too_little = BENFORDS_DICT[item] - 5
        if number > too_much or number < too_little:
            #if outside range benfords law doesn't work
            return False
    return True
'''

def chi_square_test(counts, total_count):
    '''
    In this function the program returns the p_value and test statistic
    from a Chi Sqaured Goodness of Fit test to guage how big the differencethe
    is in number of leading digits between our csv (observed) vs our expected
    '''

    chi_square_test_statistic = 0  
    p_value = 0

    for digit in range(1, 10):
        observed = counts.get(digit,0)  
        expected = BENFORDS_DICT[digit] * total_count
        if expected > 0:
            chi_square_test_statistic += ((observed - expected) ** 2) / expected #Chi squared test statistic equation
    p_value = chi2.sf(chi_square_test_statistic, df=DEGREES_OF_FREEDOM) #chi.sf is use of complement of CDF
    return p_value, chi_square_test_statistic

import csv

def write_results_to_csv(p_value, test_statistic, counts, percentages, total_count, benfords_law_results_file):
    '''
    This function creates a csv file with the p-value, test-statistic, and total count along with the count,
    observed percent, and expected percent for each digit. This csv file would allow the user to furthur 
    investigate the data easily
    '''
    file = open(benfords_law_results_file, "w")

    file.write(f"P-value,{p_value:.4f}\n")
    file.write(f"Test-statistic,{test_statistic:.2f}\n")
    file.write(f"Total Count,{total_count}\n")
    file.write("\n")  # blank line for readability

    # Write header for the table
    file.write("Digit,Observed Count,Observed %,Expected %\n")
    for digit in range(1,10):
        observed_count = counts.get(digit, 0)
        observed_percent = percentages.get(digit, 0)
        expected_percent = BENFORDS_DICT[digit] * 100
        file.write(f"{digit},{observed_count},{observed_percent:.2f},{expected_percent:.2f}\n")

    file.close()


def main():
    csv_file = "sample.csv"
    numbers = csv_to_list(csv_file)
    counts = count_start_digits(numbers)
    percentages = digit_percentages(counts)
    print(create_plot(percentages))
    chi_square_test_statistic, p_value = chi_square_test(counts,len(numbers))
    print(f"Test Statistic: {chi_square_test_statistic:.4f}")
    if p_value <= 0.05:
        print(f"P-value: {p_value:.4f}")
        print("Conclusion: Does not fit Benford's Law (statistically significant difference, p < 0.05)")
    else:
        print(f"P-value: {p_value:.4f}")
        print("Conclusion: Fits Benford's Law (not statistically significant, p > 0.05)")

    write_results_to_csv(p_value, chi_square_test_statistic, counts, percentages, len(numbers), "benfords_law_results.csv")
    
if __name__ == "__main__":
    main()     