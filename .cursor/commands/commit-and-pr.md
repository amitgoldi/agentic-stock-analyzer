# Commit and Create PR

Commit your changes and create a pull request with proper formatting and description.

## What This Command Does

The agent will perform these steps:

1. **Gets the story ID** from the current branch name (e.g., `CN-1768-feature-name` → `CN-1768`)
2. **Stages all changes** in the current working directory
3. **Creates a commit** with proper story ID prefix and descriptive message
4. **Pushes the branch** to the remote repository
5. **Creates a pull request** with comprehensive description of changes

## Usage

When you run this command, the agent will execute all the steps automatically.

## Commit Message Format

Following the project guidelines from `Claude.md`:

- **Always include the story ID** at the beginning
- **Get the story ID from the current branch name**
- Format: `CN-XXXX: Brief description of the change`
- Example: `CN-1768: Fix message filtering for pre-planned task steps`

## PR Description Generation

The command will automatically generate a PR description that includes:

1. **Story ID and Title** - From the branch name
2. **Summary** - Brief overview of changes
3. **Changes Made** - List of modified files and their purposes
4. **Testing** - What was tested and how
5. **Breaking Changes** - Any breaking changes or migrations needed
6. **Screenshots** - If applicable (placeholders for manual addition)

## Branch Name Requirements

Your branch must follow the naming convention:
- Format: `CN-XXXX-feature-description`
- Example: `CN-2305-fix-task-step-message-filtering`

## Agent Workflow

The agent will execute these steps:

1. **Check current branch and extract story ID**
   - Get current branch name using `git branch --show-current`
   - Extract story ID using pattern `CN-[0-9]+`
   - Verify story ID was found, exit with error if not

2. **Verify branch naming convention**
   - Ensure branch follows format: `CN-XXXX-feature-description`
   - Display current branch name for reference

3. **Stage all changes**
   - Run `git add .` to stage all changes
   - Confirm changes are staged

4. **Get commit message from user**
   - Prompt user for commit message (without story ID prefix)
   - Validate that message is not empty

5. **Create commit with proper format**
   - Combine story ID and user message: `"$story_id: $commit_message"`
   - Execute `git commit -m "$story_id: $commit_message"`

6. **Push branch to remote**
   - Run `git push origin "$current_branch"`
   - Handle any push failures gracefully

7. **Create pull request**
   - Use GitHub CLI: `gh pr create --title "$story_id: $commit_message" --body "$(generated_description)"`
   - Generate comprehensive PR description automatically

## Expected Output

The agent will:
- Extract story ID from branch name
- Stage all changes
- Prompt for commit message
- Create properly formatted commit
- Push to remote
- Create PR with generated description
- Show success confirmation

## Prerequisites

1. **GitHub CLI** installed and authenticated
2. **Active branch** following naming convention
3. **Changes staged** or ready to be staged
4. **Remote repository** configured

## Error Handling

The agent will handle these scenarios:

1. **Invalid branch naming**: Stop execution if branch doesn't follow `CN-XXXX-feature-description` format
2. **GitHub CLI issues**: Check authentication with `gh auth status` and provide guidance
3. **Remote issues**: Ensure remote origin is properly configured
4. **PR creation failures**: Provide manual fallback instructions with generated description

## PR Description Template

The agent will automatically generate a PR description including:

```markdown
## Story: CN-XXXX

### Summary
[Commit message description]

### Changes Made
The following files have been modified:
- `file1.py`
- `file2.js`
- etc.

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Code review completed

### Breaking Changes
- [ ] No breaking changes
- [ ] Breaking changes documented below

### Migration Notes
- [ ] No migration required
- [ ] Migration steps documented below

### Screenshots
<!-- Add screenshots if applicable -->

### Additional Notes
<!-- Add any additional context or notes -->
```

## Notes

- This command follows the project's commit message standards from `Claude.md`
- PR descriptions are automatically generated for consistency
- All changes are automatically staged before committing
- The agent validates branch naming conventions before proceeding
