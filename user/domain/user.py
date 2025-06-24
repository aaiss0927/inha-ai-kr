from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: str
    name: str
    student_id: str
    department: str
    phone_number: str
    email: str
    password: str
    study: str
    created_at: datetime
    updated_at: datetime