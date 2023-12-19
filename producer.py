async def produce(channel, connection, message_body) -> None:
    exchange_name = 'devices'
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    queue_name = 'devices_queue'
    channel.queue_declare(queue=queue_name)

    routing_key = 'devices_routing_key'
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message_body)
    connection.close()
