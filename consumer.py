import pika

# RabbitMQ server connection information
connection_params = pika.ConnectionParameters(host='localhost', port=5672)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare an exchange
exchange_name = 'test_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

# Declare a queue
queue_name = 'test_queue'
channel.queue_declare(queue=queue_name)

# Bind the queue to the exchange with a routing key
routing_key = 'test_routing_key'
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


# Set up the consumer and start listening for messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()

print("hello")
