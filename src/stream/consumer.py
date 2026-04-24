import json
import pandas as pd
import os
from confluent_kafka import Consumer, KafkaError

def main():
    # Configure Consumer
    conf = {
        'bootstrap.servers': 'localhost:29092',
        'group.id': 'mlops_ingestion_group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    topic = 'customer_data'
    consumer.subscribe([topic])
    
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    output_file = os.path.join(data_dir, 'raw_data.csv')
    
    print(f"Starting consumer. Listening to topic '{topic}'...")
    print(f"Data will be appended to {output_file}")

    batch_size = 10
    batch_data = []

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            # Parse message
            val = msg.value().decode('utf-8')
            data = json.loads(val)
            batch_data.append(data)

            # Write batch to CSV
            if len(batch_data) >= batch_size:
                df = pd.DataFrame(batch_data)
                
                # If file doesn't exist, write header, else append without header
                if not os.path.exists(output_file):
                    df.to_csv(output_file, index=False)
                else:
                    df.to_csv(output_file, mode='a', header=False, index=False)
                
                print(f"Wrote batch of {len(batch_data)} records to {output_file}")
                batch_data = []

    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        # Flush any remaining data
        if batch_data:
            df = pd.DataFrame(batch_data)
            if not os.path.exists(output_file):
                df.to_csv(output_file, index=False)
            else:
                df.to_csv(output_file, mode='a', header=False, index=False)
            print(f"Wrote final batch of {len(batch_data)} records")
            
        consumer.close()

if __name__ == '__main__':
    main()
