class DomainException(Exception):
    pass


class PlanAlreadyExistsException(DomainException):
    def __init__(self, name: str):
        super().__init__(f"Plan '{name}' already exists")


class PlanNotFoundException(DomainException):
    def __init__(self, plan_id: int):
        super().__init__(f"Plan '{plan_id}' was not found")

# =========================== CUSTOMER ==================================

class CustomerNotFoundException(DomainException):
    def __init__(self, customer_id: int):
        super().__init__(f"Customer '{customer_id}' was not found")


class CustomerAlreadyExistsException(DomainException):
    def __init__(self, email : str):
        super().__init__(f"Customer '{email}' already exists")
