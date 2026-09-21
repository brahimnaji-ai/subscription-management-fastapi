class DomainException(Exception):
    pass


class PlanAlreadyExistsException(DomainException):
    def __init__(self, name: str):
        super().__init__(f"Plan '{name}' already exists")


class PlanNotFoundException(DomainException):
    def __init__(self, plan_id: int):
        super().__init__(f"Plan '{plan_id}' was not found")
