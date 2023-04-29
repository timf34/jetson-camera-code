### Command line args with certificate paths

Rather than using bash, just going to copy paste the command line commands for running the `camera_send_messages.py`
file with different certs for different cameras in different terminals

---

`user5`:
```
python camera_send_messages.py --camera_id 1 --cert_path ./certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-certificate.pem.crt --priv_key_path ./certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-private.pem.key --root_ca_path ./certificates/tims/camera_send_messages/root.pem  --client_id user5
```

or if running from the root dir of `jetson-camera-code`
```
python aws_iot/camera_send_messages.py --camera_id 1 --cert_path ./aws_iot/certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-certificate.pem.crt --priv_key_path ./aws_iot/certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-private.pem.key --root_ca_path ./aws_iot/certificates/tims/camera_send_messages/root.pem  --client_id user5
```

---

`jetson0`:
```
python camera_send_messages.py --camera_id 0 --cert_path ./certificates/tims/jetson0/a14899325642fe1cad3a4454d45b988752ec93cdf6a5078a6864bec1f6af838f-certificate.pem.crt --priv_key_path ./certificates/tims/jetson0/a14899325642fe1cad3a4454d45b988752ec93cdf6a5078a6864bec1f6af838f-private.pem.key --root_ca_path ./certificates/tims/jetson0/AmazonRootCA1.pem  --client_id jetson0
```

or if running from the root dir of `jetson-camera-code`
```
python aws_iot/camera_send_messages.py --camera_id 0 --cert_path ./aws_iot/certificates/tims/jetson0/a14899325642fe1cad3a4454d45b988752ec93cdf6a5078a6864bec1f6af838f-certificate.pem.crt --priv_key_path ./aws_iot/certificates/tims/jetson0/a14899325642fe1cad3a4454d45b988752ec93cdf6a5078a6864bec1f6af838f-private.pem.key --root_ca_path ./aws_iot/certificates/tims/jetson0/AmazonRootCA1.pem  --client_id jetson0
```