
# Project Structure

- **`listmonk/__init__.py`**: Main module entry point with public API exports
- **`listmonk/impl/__init__.py`**: Core implementation containing all API functions
- **`listmonk/models/__init__.py`**: Pydantic models for request/response data
- **`listmonk/urls.py`**: API endpoint URL constants
- **`listmonk/errors/__init__.py`**: Custom exception classes

The library uses a simple global state pattern for authentication (username/password stored globally) and builds on httpx for HTTP operations and Pydantic for data validation.

# Import API Documentation

The library supports bulk importing subscribers via the Listmonk Import API.

## Functions

### `import_subscribers`

Bulk import subscribers from a CSV file.

```python
def import_subscribers(
    file_path: Path,
    mode: str = 'subscribe',
    delim: str = ',',
    lists: Optional[list[int]] = None,
    overwrite: bool = True,
    timeout_config: Optional[httpx.Timeout] = None,
) -> bool
```

**Arguments:**
- `file_path`: Path to the CSV file to import.
- `mode`: 'subscribe' or 'blocklist'. Default is 'subscribe'.
- `delim`: CSV delimiter character. Default is ','.
- `lists`: List of list IDs to add subscribers to.
- `overwrite`: Overwrite existing subscribers. Default is True.
- `timeout_config`: Optional timeout configuration.

**Returns:**
- `True` if the import was started successfully.

---

### `get_import_status`

Get the status of the current or last import.

```python
def get_import_status(timeout_config: Optional[httpx.Timeout] = None) -> Optional[models.ImportStatus]
```

**Returns:**
- `ImportStatus` object containing `name`, `total`, `imported`, and `status`. Returns `None` if no import information is available.

---

### `get_import_logs`

Get the logs of the import process.

```python
def get_import_logs(timeout_config: Optional[httpx.Timeout] = None) -> str
```

**Returns:**
- The log content as a string.

---

### `stop_import`

Stop the current import process.

```python
def stop_import(timeout_config: Optional[httpx.Timeout] = None) -> bool
```

**Returns:**
- `True` if successful.

## Models

### `ImportStatus`

```python
class ImportStatus(BaseModel):
    name: Optional[str] = None
    total: int
    imported: int
    status: Optional[str] = None
```
