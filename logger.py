import os
import datetime


class Logger:
    """
    A class for logging messages to a file on disk. This version of the logger
    uses a buffer to collect log messages before writing them to disk, which
    can help reduce the number of writes and improve performance.

    Args:
        log_file_path (str): The path to the log file.
        buffer_size (int, optional): The maximum number of log messages to buffer
            before writing them to disk. Defaults to 100.
    """
    def __init__(self, log_file_path: str, buffer_size: int = 100):
        self.log_file_path = log_file_path
        self.log_file = None
        self.buffer = []
        self.buffer_size = buffer_size

    def log(self, message: str) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp}: {message}\n"

        self.buffer.append(log_message)

        if len(self.buffer) >= self.buffer_size:
            self.flush_buffer()

    def flush_buffer(self) -> None:
        if not self.log_file:
            # If the log file isn't open, try to open it
            try:
                self.log_file = open(self.log_file_path, "a")
            except FileNotFoundError:
                # If the file doesn't exist, create it and try again
                os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
                self.log_file = open(self.log_file_path, "a")

        # If the file is open, write the buffered log messages to it
        if self.log_file:
            self.log_file.writelines(self.buffer)
            self.log_file.flush()
            self.buffer.clear()

    def __del__(self):
        # If the file is open, flush the buffer and close it when the object is deleted
        if self.log_file:
            self.flush_buffer()
            self.log_file.close()


def main():
    import time

    logger = Logger("test.log", buffer_size=10)

    for i in range(100):
        logger.log(f"Test message {i}")
        time.sleep(0.1)

    logger.flush_buffer()
    print("Done")


if __name__ == "__main__":
    main()
