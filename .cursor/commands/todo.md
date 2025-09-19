# TODO Command

Find and execute all TODO items in a specified file or class.

## Command

```bash
/todo <file_or_class_name>
```

## What This Command Does

1. **Finds the target file** by searching for:
   - Exact file path matches
   - File name matches (e.g., `service.py` finds all service.py files)
   - Class name matches within Python files
2. **Extracts all TODO items** from the file including:
   - `TODO:` comments
   - `FIXME:` comments
   - `XXX:` comments
3. **Executes each TODO item** by:
   - Analyzing the TODO description
   - Understanding the context around the TODO
   - Implementing the requested change
   - Removing or updating the TODO comment

## Usage Examples

```bash
# Find TODOs in a specific file
/todo src/chat/service.py

# Find TODOs in any file named service.py
/todo service.py

# Find TODOs in files containing a specific class
/todo ChatService

# Find TODOs in a directory
/todo src/chat/
```

## TODO Comment Patterns

The command recognizes these TODO patterns:

```python
# TODO: Implement error handling for this function
# FIXME: This method needs optimization
# XXX: Temporary workaround - needs proper solution
# todo: lowercase also supported
```

## Execution Process

For each TODO found, the command will:

1. **Read the surrounding context** (5-10 lines before/after)
2. **Analyze the TODO description** to understand what needs to be done
3. **Implement the change** using appropriate tools
4. **Update or remove the TODO comment** once completed
5. **Verify the implementation** doesn't break existing functionality

## File Search Strategy

The command searches in this order:

1. **Exact path match** - If the input is a valid file path
2. **Filename search** - Find all files with matching name
3. **Class name search** - Search for class definitions in Python files
4. **Directory search** - If input is a directory, search all files within

## Safety Features

- **Backup creation** - Creates backup of files before modification
- **Syntax validation** - Ensures changes don't break code syntax
- **Test verification** - Runs relevant tests if available
- **Rollback capability** - Can revert changes if issues are detected

## Expected Output

The command will:
- List all TODO items found in the target file(s)
- Show progress as each TODO is being implemented
- Display a summary of changes made
- Indicate any TODOs that couldn't be automatically resolved

## Example Workflow

```bash
$ /todo src/chat/service.py

🔍 Searching for file: src/chat/service.py
✅ Found: /Users/amitgol/git/chat-service/src/chat/service.py

📋 Found 3 TODO items:
1. Line 45: TODO: Add input validation for message content
2. Line 128: FIXME: Optimize database query performance
3. Line 203: TODO: Implement retry logic for failed API calls

🔧 Processing TODO 1/3: Add input validation for message content
   ✅ Added validation logic
   ✅ Updated TODO comment

🔧 Processing TODO 2/3: Optimize database query performance
   ✅ Added database indexing
   ✅ Optimized query structure
   ✅ Removed FIXME comment

🔧 Processing TODO 3/3: Implement retry logic for failed API calls
   ✅ Added retry decorator
   ✅ Configured exponential backoff
   ✅ Updated TODO comment

📊 Summary:
   - 3 TODOs processed
   - 3 successfully implemented
   - 0 requiring manual attention
   - Files modified: 1
```

## Limitations

- **Complex TODOs** may require manual intervention
- **Cross-file dependencies** might not be fully resolved automatically
- **Business logic decisions** may need human input
- **Breaking changes** will be flagged for review

## Integration with Project Standards

The command follows project guidelines:
- Maintains code style and formatting standards
- Preserves existing import patterns
- Follows testing conventions
- Respects commit message formats

## Notes

- Use this command to systematically address technical debt
- Review all changes before committing
- Some TODOs may be converted to GitHub issues if too complex
- The command respects `.gitignore` patterns when searching files
