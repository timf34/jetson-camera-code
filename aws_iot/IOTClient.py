from awscrt import mqtt
from awsiot import mqtt_connection_builder
from concurrent import futures
from aws_iot.IOTContext import IOTContext, IOTCredentials
from typing import Optional


class IOTClient:
    _mqtt_connection: mqtt.Connection
    context: IOTContext
    credentials: IOTCredentials

    def __init__(
            self,
            context: IOTContext,
            credentials: IOTCredentials,
            subscribe_topic: str = None,
            publish_topic: Optional[str] = None,
            ca_bytes: Optional[bytes] = None
    ):
        self.context = context
        self.credentials = credentials
        self.subscribe_topic: str = subscribe_topic
        self.publish_topic: Optional[str] = publish_topic

        # Docs: https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/mqtt_connection_builder.html#awsiot.mqtt_connection_builder.mtls_from_path
        self._mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.credentials.endpoint,
            port=self.credentials.port,
            cert_filepath=self.credentials.cert_path,
            pri_key_filepath=self.credentials.priv_key_path,
            ca_filepath=self.credentials.ca_path,
            client_bootstrap=self.context.client_bootstrap,
            ca_bytes=ca_bytes,
            on_connection_interrupted=self._on_conn_interrupted,
            on_connection_resumed=self._on_conn_resumed,
            client_id=self.credentials.client_id,
            clean_session=False,
            keep_alive_secs=30,
        )

    def connect(self) -> futures.Future:
        print(f"Connecting to endpoint '{self.credentials.endpoint}' with client ID '{self.credentials.client_id}'")
        return self._mqtt_connection.connect()

    def disconnect(self) -> futures.Future:
        print("Disconnecting")
        return self._mqtt_connection.disconnect()

    def publish(self, topic: str = None, payload: str = None) -> futures.Future:
        if topic is None:
            topic = self.publish_topic
        if payload is None:
            print("No payload provided! Won't be able to publish anything")
        publish_future, packet_id = self._mqtt_connection.publish(
            topic=topic,
            payload=payload,
            qos=mqtt.QoS.AT_MOST_ONCE,
        )
        print(f"Published message: {payload} to topic: {topic} with packet id: {packet_id}")
        return publish_future

    def subscribe(self, topic: str = None, handler=None) -> futures.Future:
        if topic is None:
            topic = self.subscribe_topic
        print(f"Subscribing to topic '{topic}'")
        if handler is None:
            print("No handler provided! Won't be able to handle incoming messages - only sending them")

        # Docs: https://awslabs.github.io/aws-crt-python/api/mqtt.html#awscrt.mqtt.Connection.subscribe
        subscribe_future, packet_id = self._mqtt_connection.subscribe(
            topic=topic,
            qos=mqtt.QoS.AT_MOST_ONCE,
            callback=handler,
        )

        return subscribe_future

    # TODO: Implement this: https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/pubsub.py
    def _on_conn_resumed(self, connection, return_code, session_present, **kwargs):
        pass

    def _on_conn_interrupted(self, connection, error, **kwargs):
        pass
