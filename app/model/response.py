class Response:
    def __init__(self, success: bool = False, message: str = "", data: object = None):
        self.success = success
        self.message = message
        self.data = data

    def get_response(self):
        return {
            'success': self.success,
            'message': self.message,
            'data': self.data
        }
    
    def set_response(self, success, message, data):
        self.success = success
        self.message = message
        self.data = data