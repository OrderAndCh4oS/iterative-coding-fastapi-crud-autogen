# filename: database.py

from typing import Dict, Optional
from datetime import datetime
from uuid import uuid4

class InMemoryDB:
    def __init__(self):
        self.db: Dict[str, Dict] = {}

    def get(self, id: str) -> Optional[Dict]:
        return self.db.get(id)

    def get_all(self) -> Dict[str, Dict]:
        return self.db

    def create(self, data: Dict) -> Dict:
        id = str(uuid4())
        data['uuid'] = id
        data['createdAt'] = datetime.now()
        data['updatedAt'] = datetime.now()
        self.db[id] = data
        return self.db[id]

    def update(self, id: str, data: Dict) -> Dict:
        if id in self.db:
            self.db[id].update(data)
            self.db[id]['updatedAt'] = datetime.now()
            return self.db[id]
        else:
            raise ValueError(f"No record found with id: {id}")

    def delete(self, id: str) -> None:
        if id in self.db:
            del self.db[id]
        else:
            raise ValueError(f"No record found with id: {id}")

db = InMemoryDB()