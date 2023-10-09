import argparse
import csv
import datetime
import os
import random
import uuid


def generate_transactions(users):
    num_transactions = 100000
    num_users = len(users['data'])

    header = [
        'transaction_id',
        'date',
        'user_id',
        'is_blocked',
        'transaction_amount',
        'transaction_category_id'
    ]

    data = [[
        uuid.uuid4(),
        (datetime.date.today() - datetime.timedelta(days=random.randint(int(i / num_users), 100))).strftime('%Y-%m-%d'),
        users['data'][random.randint(0, num_users - 1)][0],
        random.random() < 0.99,
        '%.2f' % (random.random() * 100),
        random.randint(0, 10)
    ] for i in range(num_transactions)]

    return {'header': header, 'data': data}


def generate_users():
    num_users = 1000
    header = [
        'user_id',
        'is_active'
    ]

    data = [[
        uuid.uuid4(),
        random.random() < 0.9
    ] for _ in range(num_users)]

    return {'header': header, 'data': data}


def write_data(out, header, data):
    if os.path.exists(out):
        print('File %s already exists!' % out)
        return False

    try:
        with open(out, 'w') as f:
          writer = csv.writer(f)
          writer.writerow(header)
          writer.writerows(data)
    except Exception as err:
        print('Failed to write %s' % out)
        return False
    return True


if __name__ == '__main__':
    users = generate_users()
    transactions = generate_transactions(users)

    write_data('users.csv', users['header'], users['data'])
    write_data('transactions.csv', transactions['header'], transactions['data'])
