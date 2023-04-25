from IOTContext import IOTContext, IOTCredentials
from IOTDiscovery import IOTDiscovery
import json
from os import getcwd
import threading
from time import time

received_event = threading.Event()


def on_message_received(topic, payload, dup, qos, retain, **kwargs):
	print(f"Received message from topic '{topic}' at {time()}: {payload}")
	received_event.set()


if __name__ == "__main__":
	cwd = getcwd()

	iot_context = IOTContext()

	iot_credentials = IOTCredentials(
		ca_path=cwd + "/AmazonRootCA1.pem",
		cert_path=cwd + "/2b149186f8-certificate.pem.crt",
		client_id="Seb_Laptop_Test",
		endpoint="a3lkzcadhi1yzr-ats.iot.eu-west-1.amazonaws.com",
		region="eu-west-1",
		priv_key_path=cwd + "/2b149186f85e8d5439849e473c4334116142923690a58d753b25886b85c56568-private.pem.key",
	)

	iot_discovery = IOTDiscovery(iot_context, iot_credentials)
	discovery_results = iot_discovery.discover("Seb_Laptop_Test").result()
	client = iot_discovery.get_client(discovery_results)

	if client is None:
		print("Failed to retrieve a valid client")
		exit(1)

	subscribe_future = client.subscribe("tablets/test", on_message_received)

	subscribe_result = subscribe_future.result()
	print(f"Subscribed with {str(subscribe_result['qos'])}")

	for i in range(4):
		message = json.dumps({
			"camera": i,
			"message": f"Test Message {str(i + 1)}",
		})

		print(f"Sending message at {time()}")
		client.publish("cameras/test", message)

	if not received_event.is_set(): print("Waiting to receive message.")

	received_event.wait()

	disconnect_future = client.disconnect()
	disconnect_future.result()
	print("Disconnected!")
