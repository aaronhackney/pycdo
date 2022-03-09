class DuplicateObjectError(Exception):
    pass


class OnBoardingException(Exception):
    def __init__(self, asa_name: str, asa_ip: str, asa_port: str) -> None:
        self.message = ""
        self.asa_name = asa_name
        self.asa_ip = asa_ip
        self.asa_port = asa_port
        super().__init__(self.message)


class AddDeviceException(OnBoardingException):
    def __str__(self):
        return (
            f"Adding device {self.asa_name} at {self.asa_ip}:{self.asa_port} has failed. "
            "Please check the CDO portal and onboardning workflows for more details"
        )


class AddCredentialsException(OnBoardingException):
    def __str__(self):
        return (
            f"{self.asa_name} at {self.asa_ip}:{self.asa_port} "
            f"We did not get back the expected result from our attempt to add the credentials for "
            f"device {self.asa_name} {self.asa_ip}:{self.asa_port}"
        )
