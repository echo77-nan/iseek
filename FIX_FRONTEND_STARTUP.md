# Fix Frontend Startup Script

## Problem
The `package.json` on the server is missing the `start` script, causing `npm start` to fail.

## Solutions

### Method 1: Modify package.json on Server Directly

Execute on the server:

```bash
cd frontend

# Edit package.json, add "start": "vite" in scripts section
nano package.json
# or
vi package.json
```

Add to the `scripts` section:
```json
"start": "vite",
```

The complete scripts section should be:
```json
"scripts": {
  "dev": "vite",
  "start": "vite",
  "build": "vite build",
  "preview": "vite preview"
}
```

### Method 2: Use sed Command to Add Quickly

```bash
cd frontend

# Add "start" script after "dev" line
sed -i '/"dev": "vite",/a\    "start": "vite",' package.json
```

### Method 3: Recreate scripts Section Using cat

```bash
cd frontend

# Backup original file
cp package.json package.json.bak

# Replace scripts section using sed
sed -i 's/"dev": "vite",/"dev": "vite",\n    "start": "vite",/' package.json
```

### Method 4: Sync File from Local

If the local file is updated, sync using scp:

```bash
# Execute on local machine
scp frontend/package.json user@server:/path/to/iseek/frontend/package.json
```

## Verify Fix

After fixing, verify:

```bash
cd frontend

# Check scripts
cat package.json | grep -A 5 "scripts"

# Should see "start": "vite"
```

## Start Service

After fixing, start:

```bash
cd frontend
npm start
```

Or use:

```bash
npm run dev
```

