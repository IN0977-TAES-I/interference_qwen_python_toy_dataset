# Semantic Merge Conflicts - Python Scenarios

This archive contains 10 toy merge scenarios demonstrating semantic conflicts
in Python code that can trap merge reviewers.

## Structure

Each folder (S001-S010) contains 4 files:
- `base.py` - Original code before any branch modifications
- `left.py` - Changes from the left branch
- `right.py` - Changes from the right branch  
- `merge.py` - The problematic merge result with semantic conflicts

## Scenarios

- **S001** - Authentication Bypass Trap: Semantic Interference - Security Bypass
- **S002** - Discount Calculation Override: Semantic Interference - Business Logic Error
- **S003** - Variable Shadowing Trap: Semantic Interference - Variable Shadowing
- **S004** - Return Type Inconsistency: Semantic Interference - Type Contract Violation
- **S005** - Shared State Mutation Conflict: Semantic Interference - State Management
- **S006** - Exception Handling Trap: Semantic Interference - Error Handling Strategy
- **S007** - Default Parameter Mutation Trap: Semantic Interference - Mutable Default Arguments
- **S008** - Loop Boundary Off-by-One: Semantic Interference - Boundary Condition
- **S009** - Conditional Logic Precedence Trap: Semantic Interference - Control Flow
- **S010** - Resource Cleanup Race Condition: Semantic Interference - Resource Lifecycle

## Important

The `merge.py` files contain semantic conflicts that are NOT detectable by
automated merge tools (like Git). These conflicts require human review to
identify and resolve properly.

Each merge file has comments marked with "TRAP:" indicating the specific
semantic issues that make these merges dangerous.
