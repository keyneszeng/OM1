# Security Fix Guide: Command Injection Vulnerability

This guide provides step-by-step instructions for fixing the command injection vulnerability in lifecycle hooks.

## Overview

The vulnerability exists in `src/runtime/multi_mode/hook.py` where `CommandHookHandler` uses shell execution without proper validation.

## Fix Implementation

### Step 1: Update CommandHookHandler

Replace the vulnerable `create_subprocess_shell` with secure `create_subprocess_exec`:

**File**: `src/runtime/multi_mode/hook.py`

**Before** (Vulnerable):
```python
process = await asyncio.create_subprocess_shell(
    formatted_command,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
)
```

**After** (Secure):
```python
import shlex

# Parse command into argument array (prevents injection)
args = shlex.split(formatted_command)

# Validate against whitelist
ALLOWED_COMMANDS = ["echo", "logger"]  # Add only needed commands
if args and args[0] not in ALLOWED_COMMANDS:
    logging.error(f"Command not allowed: {args[0]}")
    return False

# Use subprocess_exec (no shell interpretation)
process = await asyncio.create_subprocess_exec(
    *args,  # Arguments as array, not shell string
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
)
```

### Step 2: Add Input Validation

Add validation to sanitize context variables:

```python
def _sanitize_context(context: Dict[str, Any]) -> Dict[str, Any]:
    """Remove potentially dangerous characters from context."""
    sanitized = {}
    for key, value in context.items():
        if isinstance(value, str):
            # Remove command separators
            sanitized_value = value.replace(';', '').replace('&&', '').replace('||', '')
            sanitized_value = sanitized_value.replace('`', '').replace('$', '')
            sanitized[key] = sanitized_value
        else:
            sanitized[key] = value
    return sanitized
```

### Step 3: Add Configuration Flag

Allow disabling command hooks entirely:

```python
class CommandHookHandler(LifecycleHookHandler):
    # Environment variable to disable command hooks
    ENABLED = os.getenv("OM1_ENABLE_COMMAND_HOOKS", "false").lower() == "true"
    
    async def execute(self, context: Dict[str, Any]) -> bool:
        if not self.ENABLED:
            logging.warning("Command hooks disabled for security")
            return False
        # ... rest of implementation
```

## Testing

### Test 1: Verify Command Injection is Blocked

```python
# Test malicious command should fail
handler = CommandHookHandler({"command": "echo test; rm -rf /"})
result = await handler.execute({})
assert result == False
```

### Test 2: Verify Whitelisted Commands Work

```python
# Test allowed command should work
handler = CommandHookHandler({"command": "echo test"})
result = await handler.execute({})
assert result == True
```

## Deployment Checklist

- [ ] Code changes reviewed
- [ ] Unit tests added and passing
- [ ] Integration tests passing
- [ ] Configuration files reviewed for malicious hooks
- [ ] File permissions set correctly
- [ ] Logging verified (no sensitive data)
- [ ] Documentation updated
- [ ] Security advisory published

## Rollback Plan

If issues arise, rollback by:
1. Revert code changes
2. Disable command hooks via environment variable
3. Remove any suspicious configuration files

## Additional Security Measures

1. **Configuration File Signing**: Implement digital signatures for configuration files
2. **File Integrity Checks**: Add checksum verification
3. **Monitoring**: Alert on command hook executions
4. **Audit Logging**: Log all command hook executions

