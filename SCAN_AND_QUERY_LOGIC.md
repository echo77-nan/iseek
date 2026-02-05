# Data Scanning and Query Logic Documentation

## I. Overall Architecture Flow

```
User inputs scan path 
  ↓
Frontend sends scan request (POST /api/scan)
  ↓
Backend starts background scan task
  ↓
Clean old records → Scan file system → Save to database
  ↓
Frontend automatically filters and displays
```

## II. Detailed Scan Process

### 2.1 Scan Request Handling (`main.py`)

**Entry:** `POST /api/scan?path=/path/to/scan&recursive=true`

```python
@app.post("/api/scan")
async def scan_directory(path, recursive, background_tasks):
    # 1. Return response immediately, non-blocking
    background_tasks.add_task(scan_and_save_files, path, recursive)
    return {"success": True, "status": "processing"}
```

**Features:**
- ✅ Asynchronous background task, returns response immediately
- ✅ Non-blocking API request
- ✅ Suitable for scanning large numbers of files

### 2.2 Scan Execution Flow (`scan_and_save_files`)

#### Step 1: Path Normalization
```python
from pathlib import Path
scan_path = str(Path(path).resolve())  # Convert to absolute path
# Example: "/home/user/documents" → "/home/user/documents"
```

#### Step 2: Clean Old Records ⚠️ **Critical Step**
```python
deleted_count = db.delete_files_by_path_prefix(scan_path)
```

**Purpose:**
- Delete all historical scan records under this path
- Avoid displaying duplicate historical files
- Ensure only current scan results are displayed

**SQL Logic:**
```sql
DELETE FROM files 
WHERE file_path LIKE '/home/user/documents/%' 
   OR file_path = '/home/user/documents'
```

#### Step 3: Scan File System
```python
scanner = FileScanner(max_file_size=104857600)  # 100MB
files = scanner.scan_directory(scan_path, recursive=True)
```

**Scan Content:**
- File path, file name
- File size, type, extension
- MIME type
- Creation time, modification time
- File hash (for files smaller than 10MB)
- Metadata (is symlink, is readable)

#### Step 4: Batch Save to Database
```python
batch_size = 100
for i in range(0, len(files), batch_size):
    batch = files[i:i + batch_size]
    batch_saved = db.insert_files_batch(batch)
```

**Batch Processing Advantages:**
- Avoid inserting too much data at once
- Improve insertion efficiency
- Reduce database connection pressure

## III. Data Storage Logic

### 3.1 Data Cleaning and Validation (`_sanitize_file_info`)

**Purpose:** Ensure data conforms to database field limits

| Field | Limit | Handling Method |
|-------|-------|-----------------|
| `file_path` | VARCHAR(2000) | Truncate if exceeds |
| `file_name` | VARCHAR(500) | Truncate if exceeds |
| `file_extension` | VARCHAR(50) | Remove leading dot, truncate if exceeds |
| `mime_type` | VARCHAR(200) | Truncate if exceeds |
| `file_hash` | VARCHAR(64) | Truncate if exceeds |
| `metadata` | TEXT | JSON serialization |

### 3.2 Insert/Update Logic (`insert_file`)

**Strategy:** Check-Update/Insert Pattern

```python
# 1. Check if file already exists
SELECT id FROM files WHERE file_path = %s

# 2. If exists → Update
UPDATE files SET 
    file_name = %s,
    file_size = %s,
    file_type = %s,
    scan_time = NOW()  # Update scan time
WHERE id = %s

# 3. If not exists → Insert
INSERT INTO files (...) VALUES (...)
```

**Key Points:**
- ✅ Preserve original `id` and `created_time`
- ✅ Update `scan_time` to current time
- ✅ Update file size, type and other fields that may change

## IV. Query Logic

### 4.1 Query Interface (`GET /api/files`)

**Parameters:**
- `file_type`: File type filter (optional)
- `path_prefix`: Path prefix filter (optional)
- `limit`: Return count limit (default 100)
- `offset`: Offset (default 0)

### 4.2 Query Building (`get_all_files`)

**Dynamic SQL Building:**

```python
conditions = []
params = []

# 1. File type filter
if file_type:
    conditions.append("file_type = %s")
    params.append(file_type)

# 2. Path prefix filter
if path_prefix:
    normalized_prefix = path_prefix.rstrip('/') + '/'
    conditions.append("(file_path LIKE %s OR file_path = %s)")
    params.append(f"{normalized_prefix}%")  # Example: "/home/user/%"
    params.append(path_prefix.rstrip('/'))   # Example: "/home/user"

# 3. Combine query
where_clause = " AND ".join(conditions) if conditions else "1=1"
sql = f"SELECT * FROM files WHERE {where_clause} ORDER BY scan_time DESC LIMIT %s OFFSET %s"
```

**SQL Examples:**

```sql
-- Filter by path only
SELECT * FROM files 
WHERE (file_path LIKE '/home/user/documents/%' OR file_path = '/home/user/documents')
ORDER BY scan_time DESC 
LIMIT 100 OFFSET 0

-- Path + type filter
SELECT * FROM files 
WHERE file_type = 'document' 
  AND (file_path LIKE '/home/user/documents/%' OR file_path = '/home/user/documents')
ORDER BY scan_time DESC 
LIMIT 100 OFFSET 0
```

## V. Frontend Display Logic

### 5.1 State Management

```javascript
const [currentScanPath, setCurrentScanPath] = useState(null)  // Current scan path
const [fileType, setFileType] = useState(null)                // File type filter
```

### 5.2 Auto-filter After Scan

```javascript
const handleScan = async () => {
  const response = await scanDirectory(searchPath, true)
  if (response.success) {
    // Key: Set current scan path
    setCurrentScanPath(searchPath.trim())
    // Auto refresh file list
    loadFiles()
  }
}
```

### 5.3 Query Trigger

```javascript
useEffect(() => {
  loadFiles()  // Auto query when fileType or currentScanPath changes
}, [fileType, currentScanPath])

const loadFiles = async () => {
  // Use current scan path as path prefix filter
  const response = await getFiles(fileType, currentScanPath)
  setFiles(response.files || [])
}
```

## VI. Data Flow Diagram

```
┌─────────────────┐
│  User Input Path│
│ /home/user/docs │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ POST /api/scan  │
│ Start Background│
│     Task        │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ 1. Normalize Path      │
│ /home/user/docs         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 2. Delete Old Records  │
│ DELETE WHERE path LIKE  │
│ '/home/user/docs/%'    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 3. Scan File System     │
│ Found 33 files          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 4. Batch Insert to DB   │
│ INSERT 33 records       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 5. Frontend Set Filter  │
│ currentScanPath =      │
│ '/home/user/docs'      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 6. Auto Filter on Query │
│ WHERE path LIKE         │
│ '/home/user/docs/%'     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 7. Display Results      │
│ Show only 33 files      │
└─────────────────────────┘
```

## VII. Key Design Decisions

### 7.1 Why Delete Old Records Before Scanning?

**Problem:** If only update/insert, historically scanned files will still be displayed

**Solution:** Delete all old records under this path before scanning

**Advantages:**
- ✅ Ensure only current scan results are displayed
- ✅ Avoid historical file interference
- ✅ More accurate data

**Disadvantages:**
- ⚠️ If files are deleted, they will also be deleted from database (as expected)

### 7.2 Why Use Path Prefix Filter?

**Problem:** How to display only files under a specific directory?

**Solution:** Use `LIKE` query for path prefix

**SQL:**
```sql
WHERE file_path LIKE '/home/user/documents/%' 
   OR file_path = '/home/user/documents'
```

**Advantages:**
- ✅ Support subdirectories from recursive scanning
- ✅ Precisely match scan path
- ✅ Frontend automatically applies filter

### 7.3 Why Use Asynchronous Background Tasks?

**Problem:** Scanning large numbers of files will block API requests

**Solution:** FastAPI's `BackgroundTasks`

**Advantages:**
- ✅ Return response immediately
- ✅ No timeout
- ✅ Better user experience

## VIII. Data Consistency Guarantees

### 8.1 Scan Time Update

Each scan updates `scan_time`, used for:
- Sorting (newest first)
- Identifying recently scanned files
- Distinguishing different scan batches

### 8.2 Path Uniqueness

Although there is no unique index in the database (OceanBase limitation), through:
- Delete old records before scanning
- Check existence when inserting
- Ensure same path won't duplicate

## IX. Performance Optimization

### 9.1 Batch Insert
- 100 files per batch
- Reduce database interaction count
- Improve insertion efficiency

### 9.2 Index Usage
- `idx_file_path`: Accelerate path queries
- `idx_file_type`: Accelerate type filtering
- `idx_scan_time`: Accelerate sorting

### 9.3 Connection Management
- Auto-reconnect mechanism
- Connection validity check
- Avoid connection timeout

## X. Usage Examples

### Scan Specific Directory
```bash
POST /api/scan?path=/home/user/documents&recursive=true
```

**Execution Flow:**
1. Delete all old records under `/home/user/documents`
2. Scan the directory, find 33 files
3. Insert 33 new records
4. Frontend automatically sets `currentScanPath`
5. Auto filter on query, display only these 33 files

### Query File List
```bash
GET /api/files?path_prefix=/home/user/documents&file_type=document&limit=100&offset=0
```

**Returns:** Only document type files under this path

## XI. Summary

**Core Logic:**
1. ✅ Clean old records before scanning
2. ✅ Save new records after scanning
3. ✅ Auto path filter on query
4. ✅ Frontend automatically applies filter conditions

**Data Flow:**
```
Scan Path → Clean Old Data → Scan Files → Save to DB → Frontend Filter → Display Results
```

**Key Features:**
- 🎯 Precisely display current scan results
- 🎯 Support path and type dual filtering
- 🎯 Auto update scan time
- 🎯 Asynchronous processing, non-blocking


