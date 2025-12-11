

import pytest
import os

# Example: Testing a simple database system
class SimpleDB:
    """Mock database class for demonstration"""
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
    
    def initialize(self):
        """Create the database file"""
        with open(self.filename, 'w') as f:
            f.write("# Database\n")
    
    def insert(self, key, value):
        """Insert data"""
        self.data[key] = value
        return True
    
    def get(self, key):
        """Get data"""
        return self.data.get(key)
    
    def delete(self, key):
        """Delete data"""
        if key in self.data:
            del self.data[key]
            return True
        return False
    
    def close(self):
        """Close database"""
        pass


# CRITICAL: Proper fixture with setup AND teardown
@pytest.fixture
def clean_database():
    """System test fixture - creates and cleans up database"""
    # SETUP: Create clean database
    test_file = "test_system_db.db"
    
    # Remove if exists (defensive programming)
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Create database
    db = SimpleDB(test_file)
    db.initialize()
    
    # Give database to test
    yield db
    
    # TEARDOWN: Always clean up (runs even if test fails!)
    try:
        db.close()
    except:
        pass
    
    if os.path.exists(test_file):
        os.remove(test_file)


def describe_database_system():
    """System tests for database"""
    
    def it_creates_database_file(clean_database):
        """Test that database file is created"""
        db = clean_database
        assert os.path.exists(db.filename)
    
    def it_inserts_data(clean_database):
        """Test inserting data"""
        db = clean_database
        result = db.insert("key1", "value1")
        assert result == True
        assert db.get("key1") == "value1"
    
    def it_retrieves_data(clean_database):
        """Test retrieving data"""
        db = clean_database
        # Set initial state
        db.insert("name", "Alice")
        db.insert("age", "30")
        
        # Test retrieval
        assert db.get("name") == "Alice"
        assert db.get("age") == "30"
    
    def it_returns_none_for_missing_key(clean_database):
        """Test getting non-existent key"""
        db = clean_database
        result = db.get("nonexistent")
        assert result is None
    
    def it_deletes_data(clean_database):
        """Test deleting data"""
        db = clean_database
        # Set initial state
        db.insert("key1", "value1")
        
        # Delete
        result = db.delete("key1")
        assert result == True
        assert db.get("key1") is None
    
    def it_fails_to_delete_missing_key(clean_database):
        """Test deleting non-existent key"""
        db = clean_database
        result = db.delete("nonexistent")
        assert result == False
    
    def it_handles_multiple_inserts(clean_database):
        """Test multiple operations"""
        db = clean_database
        # Set initial state
        db.insert("user1", "Alice")
        db.insert("user2", "Bob")
        db.insert("user3", "Charlie")
        
        # Test state
        assert db.get("user1") == "Alice"
        assert db.get("user2") == "Bob"
        assert db.get("user3") == "Charlie"
    
    def it_overwrites_existing_key(clean_database):
        """Test overwriting data"""
        db = clean_database
        # Initial state
        db.insert("key1", "old_value")
        
        # Overwrite
        db.insert("key1", "new_value")
        
        # Verify
        assert db.get("key1") == "new_value"
    
    def it_persists_after_operations(clean_database):
        """Test data persists"""
        db = clean_database
        # Multiple operations
        db.insert("a", "1")
        db.insert("b", "2")
        db.delete("a")
        db.insert("c", "3")
        
        # Final state check
        assert db.get("a") is None
        assert db.get("b") == "2"
        assert db.get("c") == "3"
    
    def it_starts_with_empty_data(clean_database):
        """Test database starts clean"""
        db = clean_database
        # Should be empty initially
        assert db.get("anything") is None

