import pika
from typing import Any
import json



class RabbitMQ:
    def __init__(self,
                 user: str,
                 password: str,
                 host: str = 'localhost',
                 port: int = 5672,
                 queue: str = 'tmp',
                 durable: bool = False,
                 priority: int = None,
                 mq_type: str = 'produce'
                 ):
        credentials = pika.PlainCredentials(username=user, password=password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=credentials, heartbeat=0))
        self.queue = queue
        self.channel = connection.channel()
        if not priority:
            self.channel.queue_declare(queue=self.queue, durable=durable)
        self.channel.queue_declare(queue=self.queue, durable=durable, arguments={'x-max-priority': int(priority)})
        if mq_type.startswith('consume'):
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(queue=queue, on_message_callback=self.callback)

    def produce(self,
                data: Any,
                priority: int = None,
                routing_key: str = None,
                delivery_mode: int = None,
                exchange='',
                ):
        if isinstance(data, dict):
            data = json.dumps(data)
        if not routing_key:
            routing_key = self.queue
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=data,
                                   properties=pika.BasicProperties(
                                               priority=priority,
                                               delivery_mode=delivery_mode
                                   )
                                   )

    def callback(self, channel, method, properties, body):
        """
        poka回调函数，一切皆为默认值（偷偷吐槽pika的设计理念。。。）
        :param channel:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        if isinstance(body, bytes):
            body = body.decode('utf8')
        data = json.loads(body)
        print(data)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        self.channel.start_consuming()


class KafkaMQ:

    def __init__(self):
        pass
        # from kafka import KafkaConsumer
        # #创建一个消费者，指定了topic,group_id,bootstrap_servers
        # #group_id:多个拥有相同group_id的消费者被判定为一组，一条数据记录只会被同一个组中的一个消费者消费
        # #bootstrap_servers：kafka的节点，多个节点使用逗号分隔
        # #这种方式只会获取新产生的数据
        #
        # consumer = KafkaConsumer(
        #     bootstrap_servers = "localhost:9092", # kafka集群地址
        #     group_id = "my.group", # 消费组id
        #     enable_auto_commit = True, # 每过一段时间自动提交所有已消费的消息（在迭代时提交）
        #     auto_commit_interval_ms = 5000, # 自动提交的周期（毫秒）
        # )
        #
        # consumer.subscribe(["my-topic"]) # 消息的主题，可以指定多个
        #
        # for msg in consumer: # 迭代器，等待下一条消息
        #     print(msg) # 打印消息
        #
        #
        #
        # from kafka import KafkaProducer
        # from kafka.errors import KafkaError
        #
        # producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        #
        # # Asynchronous by default
        # future = producer.send('my-topic', b'raw_bytes')
        #
        # try:
        #     record_metadata = future.get(timeout=10)
        # except KafkaError:
        #     pass

