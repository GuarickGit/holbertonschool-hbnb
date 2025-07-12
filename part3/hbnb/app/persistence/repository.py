from abc import ABC, abstractmethod
from app.extensions import db
from sqlalchemy.orm import joinedload

class Repository(ABC):
    """
    Abstract base class defining the contract for a repository.

    This interface supports basic CRUD operations and attribute-based retrieval.
    """
    @abstractmethod
    def add(self, obj):
        """
        Persist a new object.

        Args:
            obj: The object to be added.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by its unique ID.

        Args:
            obj_id: Identifier of the object.

        Returns:
            The object if found, else None.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects.

        Returns:
            List of stored objects.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an object with the given data.

        Args:
            obj_id: ID of the object to update.
            data (dict): Dictionary of fields to update.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Delete an object by its ID.

        Args:
            obj_id: ID of the object to remove.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object matching a specific attribute value.

        Args:
            attr_name (str): The attribute name to search by.
            attr_value: The expected value of the attribute.

        Returns:
            The matching object or None.
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory implementation of the Repository interface using a dictionary.

    Intended for testing or non-persistent environments.
    """

    def __init__(self):
        """Initialize with an empty internal dictionary."""
        self._storage = {}

    def add(self, obj):
        """
        Add an object.

        Args:
            obj: The object (must have a unique 'id' attribute).
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Return the object by ID, or None if not found."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Return all stored objects."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update the object with the given data if it exists.

        Args:
            obj_id: Identifier of the object.
            data (dict): Data to update.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Remove the object if it exists.

        Args:
            obj_id: Identifier of the object to delete.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """
        Return the first object where `attr_name == attr_value`.

        Args:
            attr_name (str): Attribute to compare.
            attr_value: Expected value.

        Returns:
            Matching object or None.
        """
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)


class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy-backed implementation of the Repository interface.

    Provides persistent storage using the configured database session.
    """

    def __init__(self, model):
        """
        Initialize with a SQLAlchemy model.

        Args:
            model: The SQLAlchemy model class to manage.
        """
        self.model = model

    def add(self, obj):
        """Add and persist the object."""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Fetch the object by primary key."""
        return self.model.query.get(obj_id)

    def get_with_options(self, obj_id, options=None):
        query = self.model.query
        if options:
            for option in options:
                query = query.options(option)
        return query.filter(self.model.id == obj_id).first()

    def get_all(self):
        """Return all rows from the table."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """
        Update the fields of an existing object.

        Args:
            obj_id: The object's ID.
            data (dict): Fields and values to apply.
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """
        Delete the object from the database.

        Args:
            obj_id: The object's ID.
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """
        Fetch an object by attribute value.

        Args:
            attr_name (str): Column name.
            attr_value: Value to match.

        Returns:
            The first matching row, or None.
        """
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()

