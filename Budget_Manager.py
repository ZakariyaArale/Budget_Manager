# Zakariya Arale 12/24/2024
# Design Plan
'''  Start Program
     Greet user
     Ask for the user's budget
     Provide the following features
     1. Change budget
        Ask for new amount
        Update the new budget
     2. Add Expense
        Ask for the name, amount, and importance level (1-5) of the expense
        Sort the expenses by importance level > amount > alpha
        If expense already in the budget plan, update the amount
     3. Remove Expense
        Ask for the name of expense
        Remove expense without modifying the order
     4. See current budget plan
        Output the plan, stating the budget and a list of expenses
     5. Export plan as txt file
        Do 4. but write the plan in a txt file
     Thank the user for using the program
     End program
'''
import re
def valid_money_amount(amount: str) -> float:
    ''' Return the valid monetary value that is entered by the user (only digits and non-negative)
    '''
    pattern = r'^\d+(\.\d{2})?$'
    while not bool(re.match(pattern, amount)):
        print('Invalid amount, please enter a valid amount')
        amount = input("Enter the amount: $")
    return round(float(amount), 2)


def add_expense(remaining_budget: int, expenses: list) -> float:
    ''' Modify expenses by adding expense in correct order and return the new remaining
    budget if expense is successfully added. Otherwise, return the old remaining budget
    '''
    expense_name = input('Enter the name of expense: ').strip()
    expense_amount = valid_money_amount(input('Enter the expense amount $'))
    if expense_amount > remaining_budget:
        print('Expense exceeds budget, please remove an expense or add a different expense')
        return remaining_budget
    if expense_name in [exp[0] for exp in expenses]:
        print('This expenses already exists, please try again')
        return remaining_budget
    else:
        expense_importance = input('On a scale of 1-5 (1: least important, 5: most important),'
                                   ' how important is the expense?\n' 'Scale: ')
        while not (expense_importance.isdigit() and 1 <= int(expense_importance) <= 5):
            print('Invalid scale level, please enter a valid scale number')
            expense_importance = input('On a scale of 1-5 (1: least important, 5: most important),'
                                       ' how important is the expense?\n' 'Scale: ')
        expense_importance = int(expense_importance)
        expenses.append((expense_name, expense_amount, expense_importance))
        print(f'Expense \'{expense_name}\' with amount ${expense_amount} and importance scale \'{expense_importance}\''
              ' has successfully been added')
        expenses.sort(key=lambda x: (-x[2], -x[1], x[0]))
        return remaining_budget - expense_amount


def remove_expense(expenses: list) -> None:
    ''' Modify expenses by removing the specified expense to be removed while keeping the order
    of expenses
    '''
    remove_expense_name = input('Type the expense name you want to remove: ').strip()
    for expense in expenses:
        if expense[0] == remove_expense_name:
            print(f'The expense \'{expense[0]}\' with amount ${expense[1]} and importance scale \'{expense[2]}\' '
                  'has been removed')
            expenses.remove(expense)
            break
    else:
        print(f'No expense has the name \'{remove_expense_name}\'')


def write_plan(budget: int, name: str, expenses: list, remaining_budget: int) -> str:
    ''' Return a formatted string that incorporates the name of the user, the budget,
    the list of expenses and the remaining budget
    '''
    plan = f'Budget Plan for {name}\n' + ('-' * 34) + (f'\nBudget {" " * (33 - len("Budget") - len(str(budget)) 
                                                                      - 1)}${budget}\n')
    plan += ('-' * 34) + '\n'
    plan += 'Expenses \n'
    for expense in expenses:
        plan += f'{expense[0]} {" " * (33 - len(expense[0]) - len(str(expense[1])) - 1)}${expense[1]}\n'
    plan += ('-' * 34) + '\n'
    plan += f'Remaining Budget {" " * (33 - len("Remaining Budget") - len(str(remaining_budget)) - 1)}${remaining_budget}'
    return plan


def change_budget(expenses: list) -> tuple:
    ''' Return a tuple that has the new budget and new remaining budget if successful.
    Otherwise return None
    '''
    temp_budget = valid_money_amount(input("Enter new budget amount: $"))
    total_expenses = 0
    for expense in expenses:
        total_expenses += expense[1]
    remaining_budget = temp_budget - total_expenses
    if remaining_budget >= 0:
        print(f"Budget now change to ${temp_budget}")
        return (temp_budget, remaining_budget)
    else:
        print(f'Budget will not satisfy expenses, please choose a different budget')


expenses = []
print('Hello, welcome to your personal budgeting manager.')
name = input('Enter your name: ')
budget = valid_money_amount(input("Enter your budget amount: $"))
remaining_budget = budget
print('')
while True:
    feature = (input("Enter the feature number you would like to use\n1. Change budget\n2. Add Expense\n"
                     "3. Remove Expense\n" "4. See current budget plan\n" "5. Export and finalize budget plan\n" 
                     "Feature: "))
    while not (feature.isdigit() and 1 <= int(feature) <= 5):
        print('Invalid feature, please enter a valid feature number')
        feature = input("Enter the feature number you would like to use\n1. Change budget\n2. Add Expense\n"
                        "3. Remove Expense\n" "4. See current budget plan\n" "5. Export and finalize budget plan\n"
                        "Feature: ")
    feature = int(feature)
    print('')
    if feature == 1:
        budget_change = change_budget(expenses)
        if budget_change is not None:
            budget, remaining_budget = budget_change
    elif feature == 2:
        remaining_budget = add_expense(remaining_budget, expenses)
    elif feature == 3:
        remove_expense(expenses)
    elif feature == 4:
        print(write_plan(budget, name, expenses, remaining_budget))
    elif feature == 5:
        break
    print('')
with open('Budget_Plan.txt', 'w') as file:
    file.write(write_plan(budget, name, expenses, remaining_budget))

print('Your budget plan is now ready, please open your file explorer and type \'Budget_Plan.txt\' '
      'to access the budget plan\n' 'Thank you for using budget manager!')