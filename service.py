
class MaintenanceService:
    def __init__(self):
        self.requests = []

    def add_request(self, request):
        self.requests.append(request)

    def get_request(self, request_id):
        for request in self.requests:
            if request.request_id == request_id:
                return request
        return None

    def get_all(self):
        return list(self.requests)

    def by_status(self, status):
        return [r for r in self.requests if r.status == status]

    def by_priority(self, priority):
        return [r for r in self.requests if r.priority == priority]
