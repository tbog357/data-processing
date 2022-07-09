from bson.objectid import ObjectId
from dataclasses import dataclass, field
import datetime
import helper

@dataclass
class TokenId:
    _data: str = field(default=None)

    def __init__(self, _data) -> None:
        self._data = _data


@dataclass
class Ns:
    db: str = field(default=None)
    coll: str = field(default=None)

    def __init__(self, db, coll) -> None:
        self.db = db
        self.coll = coll


@dataclass
class DocumentKey:
    _id: ObjectId = field(default=None)

    def __init__(self, _id) -> None:
        self._id = _id


@dataclass
class UpdateDescription:
    updateFields: dict = field(default=None)

    def __init__(self, updateFields) -> None:
        self.updateFields = updateFields


@dataclass
class ChangeEvent:
    _id: TokenId = field(default=None)
    operationType: str = field(default=None)
    clusterTime: datetime.datetime = field(default=None)
    ns: Ns = field(default=None)
    documentKey: DocumentKey = field(default=None)
    updateDescription: UpdateDescription = field(default=None)
    fullDocument: dict = field(default=None)
    removeFields: list = field(default=None)

    def get_unique_identity(self):
        db = self.ns.db
        coll = self.ns.coll
        doc_id = str(self.documentKey._id)
        return helper.join_strings(db, coll, doc_id)

    def __init__(self, **kwargs) -> None:
        self._id = TokenId(kwargs.get("_id", {}).get("_data", {}))

        self.operationType = kwargs.get("operationType", {})

        db = kwargs.get("ns", {}).get("db", {})
        coll = kwargs.get("ns", {}).get("coll", {})
        self.ns = Ns(db, coll)

        self.documentKey = DocumentKey(
            kwargs.get("documentKey", {}).get("_id", {})
        )

        self.updateDescription = UpdateDescription(
            kwargs.get("updateDescription", {}).get("updateFields", {})
        )

        self.fullDocument = kwargs.get("fullDocument", {})
        self.removeFields = kwargs.get("removeFields", [])
