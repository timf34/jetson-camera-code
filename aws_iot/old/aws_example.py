# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from awscrt import mqtt
import sys
import threading
import time
from uuid import uuid4
import json

# This sample uses the Message Broker for AWS IoT to send and receive messages
# through an MQTT connection. On startup, the device connects to the server,
# subscribes to a topic, and begins publishing messages to that topic.
# The device should receive those same messages back from the message broker,
# since it is subscribed to that same topic.

# Parse arguments
from camera_utils import command_line_utils

# This is essentially just argeparse, but have a camera_utils file which stores a number of useful commands to add
cmdUtils = command_line_utils.CommandLineUtils("PubSub - Send and recieve messages through an MQTT connection.")
cmdUtils.add_common_mqtt_commands()
cmdUtils.add_common_topic_message_commands()
cmdUtils.add_common_proxy_commands()
cmdUtils.add_common_logging_commands()
cmdUtils.register_command("key", "<path>", "Path to your key in PEM format.", default=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-private.pem.key")
cmdUtils.register_command("cert", "<path>", "Path to your client certificate in PEM format.", default=r"C:\Users\timf3\OneDrive - Trinity College Dublin\Documents\fov\SebsFovWork\fov\fov-net\certificates\tims\3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-certificate.pem.crt")
cmdUtils.register_command("port", "<int>", "Connection port. AWS IoT supports 443 and 8883 (optional, default=auto).", type=int, default="8883")
cmdUtils.register_command("client_id", "tim_testing_mqtt_pub_sub", "Client ID to use for MQTT connection (optional, default='test-*').", default="test-" + str(uuid4()))
cmdUtils.register_command("count", "10", "The number of messages to send (optional, default='10').", default=100, type=int)
cmdUtils.register_command("is_ci", "<str>", "If present the sample will run in CI mode (optional, default='None')")
cmdUtils.register_command("endpoint", "<str", "meh", default="a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com")
# Needs to be called so the command camera_utils parse the commands
cmdUtils.get_args()

# Start a timer at 0 seconds
start_time = time.time()


received_count = 0
received_all_event = threading.Event()
is_ci = cmdUtils.get_command("is_ci", None) != None

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print(f"Connection interrupted. error: {error}")


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(f"Connection resumed. return_code: {return_code} session_present: {session_present}")


    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print(f"Resubscribe results: {resubscribe_results}")

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit(f"Server rejected resubscribe to topic: {topic}")


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print(f"Received message from topic '{topic}': {payload}")
    global received_count
    received_count += 1

    # End the timer
    end_time = time.time()
    print("Time taken: ", end_time - start_time)

    if received_count == cmdUtils.get_command("count"):  # If we have received all the messages we want to send.
        received_all_event.set()  # Set the event to true (finished)


if __name__ == '__main__':
    mqtt_connection = cmdUtils.build_mqtt_connection(on_connection_interrupted, on_connection_resumed)

    if is_ci == False:
        print(f"""Connecting to {cmdUtils.get_command(cmdUtils.m_cmd_endpoint)} with client ID '{cmdUtils.get_command("client_id")}'...""")

    else:
        print("Connecting to endpoint with client ID")
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    message_count = cmdUtils.get_command("count")
    message_topic = cmdUtils.get_command(cmdUtils.m_cmd_topic)
    message_string = cmdUtils.get_command(cmdUtils.m_cmd_message)

    # Subscribe
    print(f"Subscribing to topic '{message_topic}'...")
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=message_topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print(f"Subscribed with {str(subscribe_result['qos'])}")

    # Publish message to server desired number of times.
    # This step is skipped if message is blank.
    # This step loops forever if count was set to 0.
    if message_string:
        if message_count == 0:
            print ("Sending messages until program killed")
        else:
            print(f"Sending {message_count} message(s)")

        publish_count = 1
        while (publish_count <= message_count) or (message_count == 0):
            message = f"{message_string} [{publish_count}]"
            print(f"Publishing message to topic '{message_topic}': {message}")
            message_json = json.dumps(message)
            mqtt_connection.publish(
                topic=message_topic,
                payload=message_json,
                qos=mqtt.QoS.AT_LEAST_ONCE)
            time.sleep(1)
            publish_count += 1

    # Wait for all messages to be received.
    # This waits forever if count was set to 0.
    if message_count != 0 and not received_all_event.is_set():
        print("Waiting for all messages to be received...")

    received_all_event.wait()
    print(f"{received_count} message(s) received.")

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")