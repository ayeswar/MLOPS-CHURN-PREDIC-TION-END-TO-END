"""
Bypass Kafka and generate synthetic customer churn data directly to CSV.
Use this script to quickly seed data for model training.
"""
import pandas as pd
import numpy as np
import os
import random
import uuid

NUM_RECORDS = 5000
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

data = []
for _ in range(NUM_RECORDS):
    age = random.randint(18, 80)
    tenure = random.randint(0, 10)
    balance = round(random.uniform(0, 250000), 2)
    num_products = random.randint(1, 4)
    has_cr_card = random.choice([0, 1])
    is_active_member = random.choice([0, 1])
    estimated_salary = round(random.uniform(20000, 200000), 2)
    # Weighted toward non-churn (80/20 split)
    churn = random.choices([0, 1], weights=[0.8, 0.2])[0]

    data.append({
        'customer_id': str(uuid.uuid4()),
        'age': age,
        'tenure': tenure,
        'balance': balance,
        'num_products': num_products,
        'has_cr_card': has_cr_card,
        'is_active_member': is_active_member,
        'estimated_salary': estimated_salary,
        'churn': churn
    })

data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(data_dir, exist_ok=True)
output_path = os.path.join(data_dir, 'raw_data.csv')
df = pd.DataFrame(data)
df.to_csv(output_path, index=False)
print(f"Generated {NUM_RECORDS} synthetic customer records -> {output_path}")
print(df.head())
print(f"\nChurn distribution:\n{df['churn'].value_counts()}")
