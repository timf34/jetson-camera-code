import argparse
from IOTClient import IOTClient
from IOTContext import IOTContext, IOTCredentials
import json

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--endpoint", action="store", required=True, dest="endpoint", help="The AWS endpoint")
	parser.add_argument("--clientid", action="store", required=True, dest="clientid", help="The IOT Thing client ID")
	parser.add_argument("--match", action="store", required=True, dest="match", help="The match to publish to")
	parser.add_argument("--file", action="store", default="./replay.json", dest="file", help="The name of the replay file")
	parser.add_argument("--cert", action="store", default="./cert.pem.crt", dest="cert", help="The IOT Thing cert")
	parser.add_argument("--privkey", action="store", default="./privkey.pem.key", dest="privkey", help="The IOT Thing private key")
	parser.add_argument("--region", action="store", default="eu-west-1", dest="region", help="The AWS region")
	parser.add_argument("--port", action="store", default=443, type=int, dest="port", help="The AWS endpoint port")

	args = parser.parse_args()

	print("Using certificate at '{}' and privkey at '{}'".format(args.cert, args.privkey))

	replay = json.load(open(args.file))

	if isinstance(replay, list) == False:
		raise TypeError("Replay file is not a list")

	context = IOTContext()

	credentials = IOTCredentials(
		cert_path = args.cert,
		client_id = args.clientid,
		endpoint = args.endpoint,
		port=args.port,
		region = args.region,
		priv_key_path = args.privkey,
	)

	iot_client = IOTClient(context, credentials)

	connect_future = iot_client.connect()
	connect_future.result()
	print("Connected to IoT Core, packets will be published to 'tablets/{}'".format(args.match))

	for packet in replay:
		iot_client.publish("tablets/" + args.match, json.dumps(packet)).result()

