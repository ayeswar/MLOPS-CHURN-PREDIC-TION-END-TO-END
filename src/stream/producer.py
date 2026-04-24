import json
import time
import random
import uuid
from confluent_kafka import Producer

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def generate_customer_data():
    """ Generate synthetic customer data for churn prediction """
    return {
        'customer_id': str(uuid.uuid4()),
        'age': random.randint(18, 80),
        'tenure': random.randint(0, 10),
        'balance': round(random.uniform(0, 250000), 2),
        'num_products': random.randint(1, 4),
        'has_cr_card': random.choice([0, 1]),
        'is_active_member': random.choice([0, 1]),
        'estimated_salary': round(random.uniform(20000, 200000), 2),
        'churn': random.choices([0, 1], weights=[0.8, 0.2])[0]  # Imbalanced 80/20
    }

def main():
    # Configure Producer
    conf = {'bootstrap.servers': 'localhost:29092'}
    producer = Producer(conf)
    topic = 'customer_data'

    print(f"Starting simulated data stream to topic '{topic}'...")
    
    try:
        while True:
            # Generate dummy data
            data = generate_customer_data()
            
            # Asynchronously produce a message, the delivery report callback
            # will be triggered from poll() above, or flush() below, when the message has
            # been successfully delivered or failed permanently.
            producer.produce(
                topic, 
                key=data['customer_id'], 
                value=json.dumps(data), 
                callback=delivery_report
            )
            
            # Wait for any outstanding messages to be delivered and delivery report
            # callbacks to be triggered.
            producer.poll(0)
            
            # Sleep to simulate real-time stream
            time.sleep(random.uniform(0.1, 2.0))
            
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        # Wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        producer.flush()

if __name__ == '__main__':
    main()
