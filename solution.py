import csv

def read_csv(filename: str) -> list[list]:
    with open(filename, 'r') as transactions_file:
        data = [line.strip().split(',') \
            for line in transactions_file.readlines()]
    return data


def cleansed(transactions_data: list[list], users_data: list[list]) -> tuple[list, list]:
    transactions = {}
    users = {}

    for row in transactions_data[1:]:
        if row[3] == 'FALSE':
            transaction_id, date,  user_id,  is_blocked, \
                transaction_amount, transaction_category_id = row
            transactions[transaction_id] = {
                'transaction_category_id': transaction_category_id,
                'transaction_amount': float(transaction_amount),
                'user_id': user_id,
                'is_blocked': is_blocked
            }

    for row in users_data[1:]:
        if row[1] == 'TRUE':
            user_id, is_active = row
            users[user_id] = {
                'is_active': is_active 
            }

    return transactions, users


def merge_and_sort(transactions: list[dict], users: list[dict])-> list[dict]:
    result = {}
    for transaction_id, transaction_data in transactions.items():
        user_id = transaction_data['user_id']
        if user_id in users:
            transaction_category_id = \
                transaction_data['transaction_category_id']
            amount = transaction_data['transaction_amount']
            
            if transaction_category_id not in result:
                result[transaction_category_id] = \
                    {'sum_amount': 0, 'num_users': set()}
            
            result[transaction_category_id]['sum_amount'] =  \
                result[transaction_category_id]['sum_amount'] + amount
            result[transaction_category_id]['num_users'].add(user_id)
    sorted_result = sorted(result.items(), key=lambda x: x[1]['sum_amount'], \
        reverse=True)            
    return sorted_result


if __name__ == '__main__':
    transactions_data = read_csv("./CSV/transactions.csv")
    users_data = read_csv("./CSV/users.csv")

    transactions, users = cleansed(transactions_data, users_data)
    data = merge_and_sort(transactions, users)

    for category_id, category_data in data:
        sum_amount = category_data['sum_amount']
        num_users = len(category_data['num_users'])
        print(f"Category ID: {category_id}, \
            Sum Amount: {sum_amount}, \
            Number of Users: {num_users}")
