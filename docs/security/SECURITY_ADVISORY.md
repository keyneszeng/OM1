# Security Advisory: Command Injection Vulnerability

**Date**: 2024  
**Severity**: Critical (CVSS 9.8)  
**Status**: Identified - Fix in Progress

## Summary

A critical command injection vulnerability has been identified in the lifecycle hook command execution functionality. This vulnerability allows remote code execution (RCE) if malicious configuration files are processed.

## Affected Components

- **File**: `src/runtime/multi_mode/hook.py`
- **Function**: `CommandHookHandler.execute()`
- **Line**: ~153
- **Impact**: All versions using lifecycle hooks with command handlers

## Vulnerability Details

### Technical Description

The `CommandHookHandler` class uses `asyncio.create_subprocess_shell()` to execute commands specified in configuration files without proper validation or sanitization:

```python
# Vulnerable code
process = await asyncio.create_subprocess_shell(
    formatted_command,  # Direct shell execution - vulnerable to injection
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
)
```

### Attack Vector

An attacker who can influence the content of JSON5 configuration files (either through file write access or by providing a malicious configuration) can execute arbitrary system commands.

### Potential Impact

1. **Remote Code Execution**: Complete system compromise
2. **Data Exfiltration**: Access to API keys, credentials, and sensitive configuration
3. **Persistence**: Installation of backdoors or malicious services
4. **Physical Safety**: If controlling robots, potential physical harm

## Mitigation (Immediate Actions)

### 1. Restrict Configuration File Access

```bash
# Restrict permissions
chmod 600 config/*.json5
chown root:root config/*.json5  # If running as root

# Review all configuration files
grep -r "handler_type.*command" config/*.json5
```

### 2. Use Environment Variables

Move sensitive data (API keys) to environment variables:

```bash
export OM_API_KEY="your_key_here"
```

### 3. Review Configuration Files

Inspect all `.json5` files for suspicious lifecycle hooks:

```bash
grep -r "global_lifecycle_hooks\|lifecycle_hooks" config/
```

### 4. Monitor Logs

Watch for suspicious command executions:

```bash
grep "Hook command" /var/log/om1/*.log
```

## Planned Fix

The fix will include:

1. **Replace Shell Execution**: Use `asyncio.create_subprocess_exec()` with argument arrays
2. **Command Whitelist**: Only allow approved commands
3. **Input Sanitization**: Clean and validate command inputs
4. **Configuration Validation**: Verify configuration file integrity
5. **Security Flag**: Option to disable command hooks entirely

## Timeline

- **Discovery**: 2024
- **Disclosure**: Coordinated disclosure
- **Fix ETA**: To be determined

## References

- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)

## Contact

For security-related questions, please contact: [security@openmind.org](mailto:security@openmind.org)

