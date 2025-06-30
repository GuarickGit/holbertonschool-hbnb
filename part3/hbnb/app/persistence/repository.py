from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract base class defining the interface for a repository.
    """
    @abstractmethod
    def add(self, obj):
        """
        Add an object to the repository.

        Args:
            obj: The object to be added.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id: The unique identifier of the object.

        Returns:
            The object if found, else None.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all stored objects.

        Returns:
            A list of all stored objects.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an existing object by ID with provided data.

        Args:
            obj_id: The unique identifier of the object.
            data (dict): Data to update on the object.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Remove an object from the repository by ID.

        Args:
            obj_id: The unique identifier of the object to delete.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute and its value.

        Args:
            attr_name (str): The name of the attribute.
            attr_value: The value to match.

        Returns:
            The matching object if found, else None.
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory implementation of the Repository interface using a dictionary.
    """

    def __init__(self):
        """
        Initialize the repository with an empty internal storage.
        """
        self._storage = {}

    def add(self, obj):
        """
        Add an object to the in-memory storage.

        Args:
            obj: The object to be added. Must have a unique 'id' attribute.
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id: The unique identifier of the object.

        Returns:
            The object if found, else None.
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Retrieve all stored objects.

        Returns:
            List of all stored objects.
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update an existing object with new data.

        Args:
            obj_id: The unique identifier of the object.
            data (dict): Data to update on the object.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Delete an object by ID.

        Args:
            obj_id: The unique identifier of the object to delete.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by matching an attribute value.

        Args:
            attr_name (str): The attribute name to search.
            attr_value: The value of the attribute to match.

        Returns:
            The first matching object, or None if not found.
        """
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
