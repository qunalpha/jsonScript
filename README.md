# JSON File Management

A small Python utility for handling JSON configuration files and simple JSON-based databases.

The module provides two classes:

* `jsonFileManagment` — for managing JSON files containing dictionaries.
* `jsonDatabase` — for managing JSON files containing lists of dictionaries.

Both classes support creating missing files, loading and saving data, resetting data, and working with files bundled inside PyInstaller applications.

## Version

`1.2`

## Import

```python
from jsonScript import jsonFileManagment, jsonDatabase
```

## jsonFileManagment

`jsonFileManagment` is designed for JSON files that store configuration or settings in the form of a dictionary.

### Creating an instance

```python
settings = jsonFileManagment(
    "settings.json",
    [
        ("username", "Quna"),
        ("volume", 100),
        ("dark_mode", True)
    ]
)
```

The constructor accepts three parameters:

```python
jsonFileManagment(path, tuple_list, indent=4)
```

| Parameter    | Type   | Description                                                           |
| ------------ | ------ | --------------------------------------------------------------------- |
| `path`       | `str`  | Path to the JSON file.                                                |
| `tuple_list` | `list` | List of key-value tuples used to create the default dictionary.       |
| `indent`     | `int`  | Number of spaces used when formatting the JSON file. Defaults to `4`. |

### load()

Loads the JSON file and returns its contents.

If the file does not exist, it creates the file using the default values.

```python
data = settings.load()

print(data)
```

Example result:

```python
{
    "username": "Quna",
    "volume": 100,
    "dark_mode": True
}
```

If the JSON file contains invalid JSON, the file is replaced with the default data.

### save()

Saves a dictionary to the JSON file.

```python
settings.save({
    "username": "Quna",
    "volume": 75,
    "dark_mode": False
})
```

The method also handles the writable copy of a bundled file when the application is running as a PyInstaller executable.

### reset()

Resets the JSON file to the default values provided when the object was created.

```python
settings.reset()
```

For example, if the original defaults were:

```python
[
    ("volume", 100),
    ("dark_mode", True)
]
```

calling `reset()` will restore those values.

### ensure_writable_resource()

```python
settings.ensure_writable_resource(filename)
```

Makes sure that a writable copy of the specified resource exists in the current working directory.

This is useful when using PyInstaller.

Files included in a PyInstaller executable are normally stored inside the bundled application and should not be modified directly. This method copies the bundled file to the application's working directory when a writable copy does not already exist.

### resource_path()

```python
settings.resource_path(relative_path)
```

Returns the correct path to a resource.

When running normally, the path is based on the Python file's directory.

When running from a PyInstaller executable, it uses `sys._MEIPASS` as the base directory.

This allows the same code to work both during development and after packaging the application.

---

# jsonDatabase

`jsonDatabase` is designed for simple JSON-based databases.

It stores data as a list of dictionaries.

For example:

```json
[
    {
        "name": "Song 1",
        "artist": "Artist 1"
    },
    {
        "name": "Song 2",
        "artist": "Artist 2"
    }
]
```

## Creating an instance

```python
database = jsonDatabase(
    "songs.json",
    ("name", "artist")
)
```

The constructor accepts:

```python
jsonDatabase(path, tuple, indent=4)
```

| Parameter | Type           | Description                                                           |
| --------- | -------------- | --------------------------------------------------------------------- |
| `path`    | `str`          | Path to the JSON database file.                                       |
| `tuple`   | `str \| tuple` | Field names used for each database entry.                             |
| `indent`  | `int`          | Number of spaces used when formatting the JSON file. Defaults to `4`. |

When using only one field, make sure to include the trailing comma:

```python
database = jsonDatabase(
    "data.json",
    ("name",)
)
```

Without the comma, Python treats `("name")` as a string rather than a tuple.

## add()

Adds a new entry to the database.

```python
database.add(("Song 1", "Artist 1"))
```

With:

```python
("name", "artist")
```

the resulting entry will be:

```json
{
    "name": "Song 1",
    "artist": "Artist 1"
}
```

The entry is automatically added to the internal list and saved to the JSON file.

The number and order of values passed to `add()` should match the fields supplied when creating the database.

For example:

```python
database = jsonDatabase(
    "songs.json",
    ("name", "artist", "album")
)

database.add((
    "Song 1",
    "Artist 1",
    "Album 1"
))
```

## remove()

Removes an entry using its list index.

```python
database.remove(0)
```

This removes the first entry in the database.

For example:

```python
database.remove(2)
```

removes the third entry.

The database is automatically saved after removing the entry.

## array

The `array` attribute contains the currently loaded database.

```python
print(database.array)
```

Example:

```python
[
    {
        "name": "Song 1",
        "artist": "Artist 1"
    },
    {
        "name": "Song 2",
        "artist": "Artist 2"
    }
]
```

You can also access individual entries:

```python
print(database.array[0])
```

or individual values:

```python
print(database.array[0]["name"])
```

## load()

Loads the database from the JSON file.

If the file does not exist, an empty database is created:

```json
[]
```

If the JSON file is corrupted or contains invalid JSON, the database is reset to an empty list.

```python
data = database.load()
```

## save()

Saves the provided list of dictionaries to the database file.

```python
database.save(database.array)
```

The method also makes sure that the file is writable when the application is running from a PyInstaller executable.

## reset()

Clears the database and restores it to its initial empty state.

```python
database.reset()
```

After resetting:

```python
database.array
```

will contain:

```python
[]
```

---

# PyInstaller Support

Both classes contain support for applications packaged with PyInstaller.

When a Python application is packaged, resources such as JSON files may be stored inside the bundled application and cannot be modified directly.

The `resource_path()` method determines where bundled resources are located, while `ensure_writable_resource()` creates a writable copy in the current working directory.

For example:

```python
database = jsonDatabase(
    "data.json",
    ("name", "value")
)

database.add(("Example", 100))
```

If `data.json` is bundled with the application but a writable copy does not exist, the class will copy the bundled file to the current working directory before modifying it.

This allows the same code to work during development and in the packaged application.

# Example

A simple configuration file:

```python
from jsonScript import jsonFileManagment

settings = jsonFileManagment(
    "settings.json",
    [
        ("volume", 100),
        ("theme", "dark"),
        ("autoplay", True)
    ]
)

data = settings.load()

data["volume"] = 50

settings.save(data)
```

A simple database:

```python
from jsonScript import jsonDatabase

songs = jsonDatabase(
    "songs.json",
    ("name", "artist")
)

songs.add(("Song 1", "Artist 1"))
songs.add(("Song 2", "Artist 2"))

print(songs.array)

songs.remove(0)
```

# Notes

The module is intended for lightweight configuration and small local databases. It uses JSON directly, so it is not intended to replace a proper database system such as SQLite when working with large amounts of data or many concurrent operations.

The classes also currently use the current working directory for writable files. When distributing an application, make sure the application has permission to create and modify files in that location.

**This whole documentation is AI written**
