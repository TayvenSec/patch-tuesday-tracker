# JULY 2026 SECURITY PATCH ROUNDUP – Windows, iOS, macOS, Android, Linux & More

July 2026's patch cycle brings updates across all major platforms. This month's roundup covers Windows, Apple, Android, Ubuntu, Red Hat, Debian, ChromeOS, Palo Alto Networks, and Cisco IOS/IOS XE. Combined, this month addresses approximately **1873+ CVEs** across the ecosystem.

Below is the full breakdown.

---

# Windows Updates – 2026-Jul

Microsoft addressed **354 CVEs** this month — **4 Critical** and **15 Important**.


## Key KB Articles

- **Server Software**

## Critical CVEs

- **CVE-2026-57100** — Microsoft Entra Provisioning Service Elevation of Privilege Vulnerability
- **CVE-2026-45499** — Azure OpenAI Elevation of Privilege Vulnerability
- **CVE-2026-26145** — Microsoft Azure Synapse Elevation of Privilege Vulnerability
- **CVE-2026-41106** — Microsoft 365 Copilot Elevation of Privilege Vulnerability

### Recommended Actions

- Apply Windows and Windows Server updates via Windows Update or WSUS
- Prioritise Critical CVEs — especially any remote code execution or privilege escalation
- Validate Secure Boot and BitLocker configurations post-update


---

# Apple Security Updates – July 2026

No Apple security releases found this month.


---

# Android Security Bulletin – July 2026

Google's July 2026 bulletin addresses **0 CVEs** across Framework, System, Kernel, and vendor components.

- **Critical:** 0
- **High:** 0
- **Moderate:** 0


### Recommended Actions

- Update Android devices to the latest patch level
- Enterprise: enforce patch compliance via MDM
- Check vendor-specific bulletins (Samsung, Pixel, etc.)


---

# Ubuntu Security Notices – July 2026

Canonical published **10 USNs** covering **1519 CVEs** this month.


## Key Security Notices


### USN-8496-2 – USN-8496-2: cifs-utils regression
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8496-2)

### USN-8503-1 – USN-8503-1: ncurses vulnerability
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8503-1)

### USN-8500-1 – USN-8500-1: Vim vulnerabilities
**Severity:** Unknown  **CVEs:** 8
[View USN](https://ubuntu.com/security/notices/USN-8500-1)
**CVE IDs:** CVE-2026-57453, CVE-2026-55693, CVE-2026-55892, CVE-2026-57455, CVE-2026-35177, CVE-2026-55895

### USN-8501-1 – USN-8501-1: Linux kernel vulnerabilities
**Severity:** Low  **CVEs:** 14
[View USN](https://ubuntu.com/security/notices/USN-8501-1)
**CVE IDs:** CVE-2026-31402, CVE-2026-43407, CVE-2026-43011, CVE-2026-43037, CVE-2026-46119, CVE-2026-43503

### USN-8493-2 – USN-8493-2: Linux kernel (Oracle) vulnerabilities
**Severity:** Low  **CVEs:** 64
[View USN](https://ubuntu.com/security/notices/USN-8493-2)
**CVE IDs:** CVE-2025-37822, CVE-2025-68214, CVE-2026-23262, CVE-2026-31478, CVE-2026-43117, CVE-2026-46243

### USN-8499-1 – USN-8499-1: Linux kernel (Xilinx) vulnerabilities
**Severity:** Low  **CVEs:** 516
[View USN](https://ubuntu.com/security/notices/USN-8499-1)
**CVE IDs:** CVE-2026-23095, CVE-2026-23038, CVE-2026-47332, CVE-2026-45904, CVE-2026-23267, CVE-2026-45869

### USN-8498-1 – USN-8498-1: Linux kernel (NVIDIA Tegra) vulnerabilities
**Severity:** Low  **CVEs:** 297
[View USN](https://ubuntu.com/security/notices/USN-8498-1)
**CVE IDs:** CVE-2026-43226, CVE-2026-45856, CVE-2026-45964, CVE-2026-43194, CVE-2026-46270, CVE-2026-43207

### USN-8497-1 – USN-8497-1: Linux kernel (Low Latency) vulnerabilities
**Severity:** Low  **CVEs:** 321
[View USN](https://ubuntu.com/security/notices/USN-8497-1)
**CVE IDs:** CVE-2026-47332, CVE-2026-45904, CVE-2026-23267, CVE-2026-45869, CVE-2026-43271, CVE-2026-43159

### USN-8492-2 – USN-8492-2: Linux kernel vulnerabilities
**Severity:** Low  **CVEs:** 299
[View USN](https://ubuntu.com/security/notices/USN-8492-2)
**CVE IDs:** CVE-2026-43226, CVE-2026-45856, CVE-2026-45964, CVE-2026-43194, CVE-2026-46270, CVE-2026-43207

### USN-8496-1 – USN-8496-1: cifs-utils vulnerability
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8496-1)

### Recommended Actions

- Run `sudo apt update && sudo apt upgrade` on all Ubuntu systems
- Prioritise kernel USNs — may require reboot
- Review USNs affecting your specific Ubuntu LTS version


---

# Debian Security Advisories – July 2026

Debian published **0 DSAs** covering **0 CVEs** this month.


### Recommended Actions

- Run `sudo apt update && sudo apt upgrade` on Debian systems
- Check [Debian Security Tracker](https://security-tracker.debian.org) for package-level detail


---

# Chrome OS Updates – July 2026

Google released **0 ChromeOS updates** covering **0 CVEs** this month.


### Recommended Actions

- ChromeOS updates automatically; verify via Settings → About ChromeOS
- Enterprise: manage rollouts via Google Admin Console


---

# Palo Alto Networks Advisories – July 2026

Palo Alto Networks published **0 advisories** — Critical: 0, High: 0.


### Recommended Actions

- Review advisories at [security.paloaltonetworks.com](https://security.paloaltonetworks.com)
- Update PAN-OS via Panorama or device console
- Apply threat prevention content updates


---

# Cisco IOS / IOS XE Advisories – July 2026

Cisco published **0 IOS/IOS XE advisories** — Critical: 0, High: 0. *(HTML scrape — set CISCO_CLIENT_ID/SECRET for full API data)*


### Recommended Actions

- Review advisories at [sec.cloudapps.cisco.com](https://sec.cloudapps.cisco.com/security/center/publicationListing.x)
- Apply IOS XE updates via `install add file` process
- Use Cisco's Software Checker tool for version impact analysis


---

# Recommended Actions

## For Individuals

- Apply Windows 10/11 and iOS/macOS updates immediately
- Update Android devices to the latest available patch level
- Ensure ChromeOS devices have auto-update enabled


## For Businesses

- Prioritise kernel updates across Windows Server and Linux distributions
- Patch network appliances (Palo Alto, Cisco) — these are high-value targets
- Enforce patch compliance across Android fleets via MDM
- Review Red Hat and Debian advisories relevant to your server stack


## For Admins

- Use WSUS, SCCM, or Intune to validate Windows patch rollout
- Test kernel updates in non-prod before rolling to production Linux hosts
- Check Cisco Software Checker for IOS XE version impact
- Monitor PAN-OS advisories — Critical severity warrants emergency patching


---

# Closing Thoughts

> ✏️ *Writer's note: Add your closing commentary here — key themes from this month, what stood out, and what to watch for next month.*


## Explore the Full Patch Management Series
[View the Patch Management Series](https://tayvensec.com/patch-management/)


---
*Data collected automatically via [patch-tuesday-tracker](https://github.com/YOUR_USERNAME/patch-tuesday-tracker). Generated: 2026-07-04T09:57:49.065053Z*
