from awscrt import mqtt
from awsiot import mqtt_connection_builder
from concurrent import futures
from IOTContext import IOTContext, IOTCredentials
from typing import Optional

class IOTClient:
    _mqtt_connection: mqtt.Connection
    context: IOTContext
    credentials: IOTCredentials

    def __init__(self, context: IOTContext, credentials: IOTCredentials, ca_bytes: Optional[bytes] = None):
        self.context = context
        self.credentials = credentials
        
        self._mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.credentials.endpoint,
            port=self.credentials.port,
            cert_filepath=self.credentials.cert_path,
            pri_key_filepath=self.credentials.priv_key_path,
            client_bootstrap=self.context.client_bootstrap,
            ca_bytes=ca_bytes,
            on_connection_interrupted=self._on_conn_interrupted,
            on_connection_resumed=self._on_conn_resumed,
            client_id=self.credentials.client_id,
            clean_session=False,
            keep_alive_secs=30,
        )

    def connect(self) -> futures.Future:
        print("Connecting to endpoint '{}' with client ID '{}'".format(self.credentials.endpoint, self.credentials.client_id))
        return self._mqtt_connection.connect()

    def disconnect(self) -> futures.Future:
        print("Disconnecting")
        return self._mqtt_connection.disconnect()

    def publish(self, topic: str, payload: str) -> futures.Future:
        print("Publishing message to topic '{}'".format(topic))

        publish_future, packet_id = self._mqtt_connection.publish(
            topic = topic,
            payload = payload,
            qos = mqtt.QoS.AT_MOST_ONCE,
        )

        return publish_future

    def subscribe(self, topic: str, handler) -> futures.Future:
        print("Subscribing to topic '{}'".format(topic))

        subscribe_future, packet_id = self._mqtt_connection.subscribe(
            topic = topic,
            qos = mqtt.QoS.AT_MOST_ONCE,
            callback=handler,
        )

        return subscribe_future

    def _on_conn_resumed(self, connection, return_code, session_present, **kwargs):
        pass

    def _on_conn_interrupted(self, connection, error, **kwargs):
        pass


