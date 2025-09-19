# Plan Feature

Create a comprehensive feature planning document following the project's feature planning guidelines.

## Command

```bash
/plan
```

## What This Command Does

1. **Extracts story ID** from the current branch name (e.g., `CN-1768-feature-name` → `CN-1768`)
2. **Prompts for feature details** including name and description
3. **Creates a feature markdown file** in the `features/` directory
4. **Generates comprehensive documentation** following Claude.md guidelines
5. **Opens the file** for immediate editing

## Usage

Simply run this command in Cursor:

```
/plan
```

## Feature File Structure

Following the guidelines from `Claude.md`, the generated file will include:

### Required Sections
1. **Overview and Purpose** - High-level description of the feature
2. **Implementation Details** - Technical approach and architecture
3. **Business Rules and Requirements** - Functional and technical requirements
4. **Technical Architecture** - System design and integration points
5. **Testing Strategy** - Test scenarios and validation approach
6. **Future Considerations** - Potential enhancements and migration notes

### File Naming Convention
- Format: `CN_XXXX_FEATURE_NAME.md`
- Example: `CN_1768_USER_AUTHENTICATION.md`
- Uses story ID from current branch name
- Feature name converted to uppercase with underscores

## Workflow

```bash
# 1. Extract story ID from current branch
current_branch=$(git branch --show-current)
story_id=$(echo "$current_branch" | grep -o 'CN-[0-9]\+' | head -1)

# 2. Validate story ID
if [[ -z "$story_id" ]]; then
    echo "❌ Error: Could not extract story ID from branch name"
    echo "Branch name must follow format: CN-XXXX-feature-description"
    echo "Current branch: $current_branch"
    exit 1
fi

# 3. Prompt for feature details
echo "Enter feature name (e.g., User Authentication):"
read feature_name

echo "Enter brief feature description:"
read feature_description

# 4. Generate filename
feature_name_upper=$(echo "$feature_name" | tr '[:lower:]' '[:upper:]' | tr ' ' '_')
filename="features/${story_id}_${feature_name_upper}.md"

# 5. Create feature file with template
cat > "$filename" << EOF
# $story_id: $feature_name

## Overview and Purpose

$feature_description

## Implementation Details

### Changes Required

### Technical Approach

### Integration Points

## Business Rules and Requirements

### Functional Requirements

### Technical Requirements

### Constraints and Limitations

## Technical Architecture

### System Design

### Data Models

### API Changes

### Dependencies

## Testing Strategy

### Test Scenarios

### Unit Tests

### Integration Tests

### Manual Testing

## Future Considerations

### Potential Enhancements

### Migration Considerations

### Risk Assessment

## Implementation Summary

*This section will be updated during implementation to document:*
- Files modified with specific changes
- Purpose and impact of each change
- Implementation details and flow
- Benefits and testing results
- Migration considerations and risk assessment

EOF

echo "✅ Feature file created: $filename"
echo "📝 Opening file for editing..."

# 6. Open the file in the editor
code "$filename"
```

## Template Structure

The generated template includes all sections required by Claude.md:

### Header
- Story ID and feature name as title
- Clear identification following naming convention

### Planning Sections
- **Overview and Purpose**: High-level feature description
- **Implementation Details**: Technical approach and changes
- **Business Rules**: Functional and technical requirements
- **Technical Architecture**: System design and integration
- **Testing Strategy**: Comprehensive testing approach
- **Future Considerations**: Enhancements and migration notes

### Implementation Section
- **Implementation Summary**: Placeholder for post-implementation documentation
- Clear guidance on what to document during implementation

## Branch Name Requirements

Your branch must follow the naming convention:
- Format: `CN-XXXX-feature-description`
- Example: `CN-2305-fix-task-step-message-filtering`

## Expected Output

The command will:
- Extract story ID from branch name (e.g., `CN-1768`)
- Prompt for feature name (e.g., "User Authentication")
- Prompt for brief description
- Generate filename: `features/CN_1768_USER_AUTHENTICATION.md`
- Create comprehensive feature template
- Open file in editor for immediate editing

## Integration with Development Workflow

This command integrates with the project's development process:

1. **Feature Planning**: Use `/plan` to create initial feature documentation
2. **Implementation**: Update the "Implementation Summary" section as you build
3. **Documentation**: Keep all feature docs in the same file (no separate docs)
4. **Commit**: Use `/commit-and-pr` to commit with proper story ID formatting

## Prerequisites

1. **Active branch** following naming convention `CN-XXXX-feature-description`
2. **Features directory** exists in the project root
3. **Code editor** available for opening files

## Troubleshooting

If you encounter issues:

1. **Check branch naming**: Ensure branch follows `CN-XXXX-feature-description` format
2. **Verify features directory**: Ensure `features/` directory exists
3. **Check permissions**: Ensure you can write to the features directory
4. **Manual creation**: If command fails, manually create file using the template structure

## Notes

- Follows feature planning guidelines from `Claude.md`
- Maintains consistency with existing feature files
- Includes placeholder for implementation documentation
- Automatically opens file for immediate editing
- Integrates with project's story ID and branch naming conventions
