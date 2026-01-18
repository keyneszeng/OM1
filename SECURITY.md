# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in OM1, please report it to us responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Email security concerns to: [security@openmind.org](mailto:security@openmind.org) (if available)
3. Include detailed information about the vulnerability
4. Allow us 90 days to address the vulnerability before public disclosure

## Security Considerations

### Known Security Issues

#### Critical: Command Injection in Lifecycle Hooks

**Status**: ⚠️ **Identified - Fix Pending**

**Description**: 
The lifecycle hook command execution feature in `src/runtime/multi_mode/hook.py` uses `create_subprocess_shell` which allows command injection if malicious configuration files are loaded.

**Affected Code**:
- File: `src/runtime/multi_mode/hook.py`
- Line: ~153
- Component: `CommandHookHandler.execute()`

**Impact**:
- Remote Code Execution (RCE) if malicious configuration files are processed
- Potential data exfiltration
- System compromise

**Mitigation** (Until Fixed):
1. Only load configuration files from trusted sources
2. Restrict write permissions on configuration files: `chmod 600 config/*.json5`
3. Review all configuration files for suspicious lifecycle hooks
4. Consider disabling command hooks if not needed

**Planned Fix**:
- Replace `create_subprocess_shell` with `create_subprocess_exec`
- Implement command whitelist validation
- Add input sanitization
- Add configuration file integrity checks

**CVSS Score**: 9.8 (Critical)

#### Medium: API Key Exposure in Configuration Files

**Description**: 
API keys may be stored in plain text within JSON5 configuration files, which could be exposed if files are committed to version control or shared.

**Mitigation**:
- Use environment variables for API keys: `OM_API_KEY`
- Never commit `.json5` files with real API keys
- Use `.env` files (and ensure they are in `.gitignore`)

#### Medium: Configuration File Hot Reload

**Description**: 
Configuration files can be hot-reloaded without integrity verification, potentially allowing attackers to inject malicious configurations if file write access is obtained.

**Mitigation**:
- Restrict file permissions on configuration files
- Implement configuration file checksum verification
- Monitor configuration file changes

## Security Best Practices

1. **Configuration Files**:
   - Never commit configuration files containing real API keys
   - Use environment variables for sensitive data
   - Restrict file permissions: `chmod 600 config/*.json5`

2. **Network Security**:
   - WebSim should only listen on localhost in production
   - Use HTTPS when exposing services over network
   - Implement authentication for remote access

3. **Robots Safety**:
   - Implement motion safety limits
   - Add emergency stop mechanisms
   - Validate all robot control commands

4. **Dependencies**:
   - Regularly update dependencies
   - Audit third-party packages
   - Use dependency scanning tools

5. **Logging**:
   - Ensure sensitive information (API keys, passwords) is not logged
   - Rotate logs regularly
   - Monitor logs for suspicious activity

## Security Updates

Security updates will be communicated through:
- GitHub Security Advisories
- Release notes for security patches
- Email notifications (if subscribed)

## Acknowledgments

We thank security researchers who responsibly disclose vulnerabilities to help improve the security of OM1.

