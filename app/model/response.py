class Response:
    def __init__(self, success=False, message=""):
        self.success = success
        self.message = message
        self.data = {}
    
    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }