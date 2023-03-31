import pickle
from typing import Any,  Union
from datetime import datetime


class CacheManager:

    _DataStorageObjs: set[str] = set()

    def __init__(self, path:str = "cache_data"):

        if path not in CacheManager._DataStorageObjs:
            self.path = r"{}".format(path)
            self._catalogue = []
            self._data: dict[str, Any] = {}
            self._setup()

    def _setup(self):
        self._data = self._data_storage_handler()
        self._load_catalogue()
        CacheManager._DataStorageObjs.add(self.path)

    def _data_storage_handler(self, obj_to_store=None) -> Union[dict[str, Any], None]:
        if obj_to_store is not None:
            with open(self.path, "wb") as handle:
                pickle.dump(obj_to_store, handle,
                            protocol=pickle.HIGHEST_PROTOCOL)
        else:
            _data = None
            try:
                with open(self.path, "rb") as handle:
                    _data = pickle.load(handle)
            except FileNotFoundError:
                create_file = {
                    "creation": datetime.today().strftime('%Y-%m-%d')}
                self._data_storage_handler(create_file)
                _data = create_file
            return _data

    def store_object(self, **kwargs):
        for obj in kwargs.items():
            if obj[0] not in self._data.keys():
                self._catalogue.append(obj[0])
            self._data[obj[0]] = obj[1]

        self.save()

    def load_object(self, *access_names):
        if len(access_names) == 1:
            return self._data[access_names[0]]
        else:
            return tuple(self._data.setdefault(access_name, None) for access_name in access_names)

    def _load_catalogue(self):
        self._catalogue = [key for key in self._data.keys()]

    @property
    def catalogue(self) -> list[str]:
        return self._catalogue

    def remove(self, *names):
        for name in names:
            del self._data[name]
        self.save()

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        self._load_catalogue()
        self.save()

    def __delitem__(self, key):
        del self._data[key]
        self.save()

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return "NotImplemented"

    def __str__(self):
        return str(self.catalogue)

    def __call__(self, *args, **kwargs):
        """When called without any arguments returns all data
        When called with positional argument returns the data with the given name
        When called with keyword arguments stores the data with the given name"""

        if not any(args) and not any(kwargs):
            return self._data

        if any(args) and not any(kwargs):
            return self.load_object(*args)

        if any(kwargs) and not any(args):
            return self.store_object(**kwargs)

        if any(args) and any(kwargs):
            return self.load_object(*args), self.store_object(**kwargs)
    
    def items(self):
        return self._data.items()

    def save(self):
        self._data_storage_handler(self._data)
        self._load_catalogue()