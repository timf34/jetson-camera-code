from IOTClient import IOTClient
from IOTContext import IOTContext, IOTCredentials
import json
import os
import threading
from time import time

NUM_MESSAGES = 4

received_count = 0
received_all_event = threading.Event()

# Start a timer at 0 seconds
start_time = time()


def on_message_received(topic, payload, dup, qos, retain, **kwargs):
	print(f"Received message from topic '{topic}' at {time()}: {payload}")

	global received_count
	received_count += 1

	end_time = time()
	elapsed_time = end_time - start_time
	print(f"Received {received_count} messages in {elapsed_time} seconds")

	if received_count == NUM_MESSAGES:
		received_all_event.set()


if __name__ == "__main__":
	cwd = os.getcwd()

	iot_context = IOTContext()

	iot_credentials = IOTCredentials(
		cert_path=os.path.join(cwd,
							   "certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-certificate.pem.crt"),
		client_id="user5",
		endpoint="a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com",
		region="eu-west-1",
		priv_key_path=os.path.join(cwd,
								   "certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-private.pem.key"),
		ca_path=os.path.join(cwd, "certificates/tims/camera_send_messages/root.pem")
	)

	iot_manager = IOTClient(iot_context, iot_credentials)

	# Note this must be called before calling .connect()
	# iot_manager._mqtt_connection.on_message(on_message_callback)

	connect_future = iot_manager.connect()

	connect_future.result()
	print("Connected!")

	print(iot_manager._mqtt_connection)

	subscribe_future = iot_manager.subscribe(topic="dalymount_IRL/pub", handler=on_message_received)

	subscribe_result = subscribe_future.result()
	print(f"Subscribed with {str(subscribe_result['qos'])}")

	for i in range(NUM_MESSAGES):
		message = json.dumps({
			"camera": i,
			"message": f"Test Message {str(i + 1)}",
		})

		print(f"Sending message at {time()}")
		iot_manager.publish("dalymount_IRL/pub", message)

	if not received_all_event.is_set():
		print("Waiting to receive message.")

	received_all_event.wait()

	disconnect_future = iot_manager.disconnect()
	disconnect_future.result()
	print("Disconnected!")
