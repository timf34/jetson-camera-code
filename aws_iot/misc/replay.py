import argparse
from IOTClient import IOTClient
from IOTContext import IOTContext, IOTCredentials
import json
from time import sleep

# Note: this file is just for sending to the tables MQTT topic

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--endpoint", action="store", required=True, dest="endpoint", help="The AWS endpoint (required)")
	parser.add_argument("--clientid", action="store", required=True, dest="clientid", help="The IOT Thing client ID (required)")
	parser.add_argument("--match", action="store", required=True, dest="match", help="The match to publish to (required)")
	parser.add_argument("--file", action="store", default="./replay.json", dest="file", help="The name of the replay file (default \"./replay.json\")")
	parser.add_argument("--interval", action="store", default=.25, type=float, dest="interval", help="The interval between replay messages (default 0.25)")
	parser.add_argument("--cert", action="store", default="./cert.pem.crt", dest="cert", help="The IOT Thing cert (default \"./cert.pem.crt\")")
	parser.add_argument("--privkey", action="store", default="./privkey.pem.key", dest="privkey", help="The IOT Thing private key (default \"./privekey.pem.key\")")
	parser.add_argument("--region", action="store", default="eu-west-1", dest="region", help="The AWS region (default \"eu-west-1\")")
	parser.add_argument("--port", action="store", default=443, type=int, dest="port", help="The AWS endpoint port (default 443)")

	args = parser.parse_args()

	print(f"Using certificate at '{args.cert}' and privkey at '{args.privkey}'")

	replay = json.load(open(args.file))

	if not isinstance(replay, list):
		raise TypeError("Replay file is not a list")

	context = IOTContext()

	credentials = IOTCredentials(
		cert_path=args.cert,
		client_id=args.clientid,
		endpoint=args.endpoint,
		port=args.port,
		region=args.region,
		priv_key_path=args.privkey,
	)

	iot_client = IOTClient(context, credentials)

	connect_future = iot_client.connect()
	connect_future.result()
	print(f"Connected to IoT Core, packets will be published to 'tablets/{args.match}'")


	for packet in replay:
		iot_client.publish(f"tablets/{args.match}", json.dumps(packet)).result()
		sleep(args.interval)

