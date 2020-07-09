class Parameters:
    def __init__(self, size):
        self.MESSAGE_SIZE = size

    def set_message_size(self, new_msg_size):
        self.MESSAGE_SIZE = new_msg_size


MESSAGE_SIZE = 1024
PARAMS = Parameters(MESSAGE_SIZE)
