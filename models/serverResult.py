class ServerResult:
    
    response = ''
    ok = True
    message = ''
    
    def __init__(self, response='', ok=True, message=''):
        self.response = response
        self.ok = ok
        self.message = message