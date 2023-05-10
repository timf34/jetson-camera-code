"""
A config file to help speed up match day work.
For storing the time of the match + IP addresses too potentially.
"""
import os


class BohsConfig:
    def __init__(self):

        if os.name == 'nt':
            self.jetson_name: str = "jetson1"  # If we're on windows, just assume we're on jetson1
        else:
            self.jetson_name: str = os.environ.get('JETSON_NAME')

        self.jetson_number: str = self.jetson_name[-1]
        self.hour: int = 17
        self.minute: int = 1
        self.second: int = 2
        self.microsecond: int = 1

        self.publish_topic: str = "cameras/bohs"
        self.subscribe_topic: str = "devices/bohs"

        # TODO: I need to verify these endpoints!
        if os.name == 'nt':
            # TODO: note these weights aren't being used rn
            self.path_to_weights: str = "data/weights/model_22_11_2022__0202_90.pth.pth"
            self.cert_path: str = "./aws_iot/certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-certificate.pem.crt"  # Cert ending in .pem.crt
            self.private_key_path: str = "./aws_iot/certificates/tims/camera_send_messages/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-private.pem.key"  # Private key ending in .pem.key
            self.root_ca_path: str = "./aws_iot/certificates/tims/camera_send_messages/root.pem"  # Root CA ending in .pem (usually: AmazonRootCA1.pem)
            self.endpoint: str = "a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com"
        if self.jetson_name == "jetson1":
            # TODO: note these are values for my laptop, not the jetson!
            self.path_to_weights: str = "data/weights/model_22_11_2022__0202_90.pth"
            self.cert_path: str = "aws_iot/certificates/tims/jetson1/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-certificate.pem.crt"  # Cert ending in .pem.crt
            self.private_key_path: str = "aws_iot/certificates/tims/jetson1/3da7dc68bfa5d09b723ebb9068a96d54550c1555969088ec7398103e772196d2-private.pem.key"  # Private key ending in .pem.key
            self.root_ca_path: str = "aws_iot/certificates/tims/jetson1/root.pem"  # Root CA ending in .pem (usually: AmazonRootCA1.pem)
            self.endpoint: str = "a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com"
        elif self.jetson_name == "jetson2":
            self.path_to_weights: str = 'data/weights/model_06_03_2023__0757_35.pth'
            self.cert_path: str = "/home/tim/jetson-camera-code/certificates/tims/camera_send_messages/a14899325642fe1cad3a4454d45b988752ec93cdf6a5078a6864bec1f6af838f-certificate.pem.crt"
            self.private_key_path: str = "/home/tim/jetson-camera-code/certificates/tims/camera_send_messages/a14899325642fe1cad3a4454d45b988752ec93cdf6a5078a6864bec1f6af838f-private.pem.key"
            self.root_ca_path: str = "/home/tim/jetson-camera-code/certificates/tims/camera_send_messages/AmazonRootCA1.pem"
            self.endpoint: str = "a13d7wu4wem7v1-ats.iot.eu-west-1.amazonaws.com"

        assert 0 <= self.hour <= 23, "Hour must be between 0 and 23"
        assert isinstance(self.hour, int), "Hour must be an int"
        assert 0 <= self.minute <= 59 and isinstance(self.minute, int), "Minute must be between 0 and 59"
        assert isinstance(self.minute, int), "Minute must be an int"
        assert 0 <= self.second <= 59, "Second must be between 0 and 59"
        assert isinstance(self.second, int), "Second must be an int"
        assert isinstance(self.microsecond, int), "Microsecond must be an int"

    def __str__(self):
        return f"hour: {self.hour}, minute: {self.minute}, second: {self.second}, microsecond: {self.microsecond}"


def _test():
    x = BohsConfig()
    print(x)
    print(x.hour)


if __name__ == "__main__":
    _test()
