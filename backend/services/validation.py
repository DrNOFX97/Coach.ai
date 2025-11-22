import json
import hashlib
import shutil
from pathlib import Path
from fastapi import UploadFile

async def validate_dataset_file(file: UploadFile):
    data_dir = Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    file_path = data_dir / file.filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Validation Logic
    stats = {
        "total_examples": 0,
        "valid_format": True,
        "warnings": [],
        "estimated_train": 0,
        "estimated_val": 0,
        "columns": set()
    }
    
    seen_hashes = set()
    duplicates = 0
    empty_fields = 0
    format_errors = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line: continue
                
                try:
                    entry = json.loads(line)
                    stats["total_examples"] += 1
                    
                    # Check columns
                    stats["columns"].update(entry.keys())
                    
                    # Check required fields (prompt/completion OR instruction/output)
                    if not (('prompt' in entry and 'completion' in entry) or 
                            ('instruction' in entry and 'output' in entry) or
                            ('text' in entry)):
                        if line_num <= 5: # Only warn for first few
                            stats["warnings"].append(f"Line {line_num}: Missing standard fields (prompt/completion, instruction/output, or text)")
                    
                    # Check empty
                    if any(not str(v).strip() for v in entry.values()):
                        empty_fields += 1
                        
                    # Check duplicates
                    line_hash = hashlib.md5(line.encode()).hexdigest()
                    if line_hash in seen_hashes:
                        duplicates += 1
                    seen_hashes.add(line_hash)
                    
                except json.JSONDecodeError:
                    format_errors += 1
                    stats["valid_format"] = False
                    if format_errors <= 5:
                        stats["warnings"].append(f"Line {line_num}: Invalid JSON format")
                        
        # Summary Stats
        if duplicates > 0:
            stats["warnings"].append(f"Found {duplicates} duplicate examples")
        if empty_fields > 0:
            stats["warnings"].append(f"Found {empty_fields} examples with empty fields")
        if format_errors > 0:
            stats["warnings"].append(f"Found {format_errors} lines with invalid JSON")
            
        # Estimate splits (80/20)
        stats["estimated_train"] = int(stats["total_examples"] * 0.8)
        stats["estimated_val"] = stats["total_examples"] - stats["estimated_train"]
        
        # Convert sets to list for JSON serialization
        stats["columns"] = list(stats["columns"])
        
        return stats
        
    except Exception as e:
        return {"valid_format": False, "warnings": [f"Error reading file: {str(e)}"]}

async def clean_dataset_file(filename: str):
    data_dir = Path(__file__).parent.parent.parent / "data"
    file_path = data_dir / filename
    
    if not file_path.exists():
        return {"error": "File not found"}
        
    seen_hashes = set()
    cleaned_lines = []
    removed_count = 0
    
    try:
        # Read and filter
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_content = line.strip()
                if not line_content: continue
                
                line_hash = hashlib.md5(line_content.encode()).hexdigest()
                if line_hash not in seen_hashes:
                    seen_hashes.add(line_hash)
                    cleaned_lines.append(line_content)
                else:
                    removed_count += 1
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            for line in cleaned_lines:
                f.write(line + '\n')
                
        return {
            "status": "success",
            "removed": removed_count,
            "remaining": len(cleaned_lines),
            "message": f"Removed {removed_count} duplicate examples"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
