# JULY 2026 SECURITY PATCH ROUNDUP – Windows, iOS, macOS, Android, Linux & More

July 2026's patch cycle brings updates across all major platforms. This month's roundup covers Windows, Apple, Android, Ubuntu, Red Hat, Debian, ChromeOS, Palo Alto Networks, and Cisco IOS/IOS XE. Combined, this month addresses approximately **1780+ CVEs** across the ecosystem.

Below is the full breakdown.

---

# Windows Updates – 2026-Jul

Microsoft addressed **25 CVEs** this month — **5 Critical** and **4 Important**.


## Key KB Articles

- **Server Software**

## Critical CVEs

- **CVE-2026-57100** — Microsoft Entra Provisioning Service Elevation of Privilege Vulnerability
- **CVE-2026-45499** — Azure OpenAI Elevation of Privilege Vulnerability
- **CVE-2026-26145** — Microsoft Azure Synapse Elevation of Privilege Vulnerability
- **CVE-2026-41106** — Microsoft 365 Copilot Elevation of Privilege Vulnerability
- **CVE-2026-54998** — Microsoft Exchange Online Elevation of Privilege Vulnerability

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

Canonical published **10 USNs** covering **1755 CVEs** this month.


## Key Security Notices


### USN-8500-1 – USN-8500-1: Vim vulnerabilities
**Severity:** Unknown  **CVEs:** 8
[View USN](https://ubuntu.com/security/notices/USN-8500-1)
**CVE IDs:** CVE-2026-57455, CVE-2026-55895, CVE-2026-55693, CVE-2026-35177, CVE-2026-57453, CVE-2026-57456

### USN-8501-1 – USN-8501-1: Linux kernel vulnerabilities
**Severity:** Low  **CVEs:** 14
[View USN](https://ubuntu.com/security/notices/USN-8501-1)
**CVE IDs:** CVE-2026-43407, CVE-2026-45988, CVE-2026-43038, CVE-2026-43011, CVE-2026-46243, CVE-2026-43503

### USN-8493-2 – USN-8493-2: Linux kernel (Oracle) vulnerabilities
**Severity:** Low  **CVEs:** 64
[View USN](https://ubuntu.com/security/notices/USN-8493-2)
**CVE IDs:** CVE-2026-23256, CVE-2026-23257, CVE-2026-46195, CVE-2026-31685, CVE-2026-43304, CVE-2026-23202

### USN-8499-1 – USN-8499-1: Linux kernel (Xilinx) vulnerabilities
**Severity:** Low  **CVEs:** 516
[View USN](https://ubuntu.com/security/notices/USN-8499-1)
**CVE IDs:** CVE-2026-43196, CVE-2026-23257, CVE-2026-45947, CVE-2026-43167, CVE-2026-47337, CVE-2026-45981

### USN-8498-1 – USN-8498-1: Linux kernel (NVIDIA Tegra) vulnerabilities
**Severity:** Low  **CVEs:** 297
[View USN](https://ubuntu.com/security/notices/USN-8498-1)
**CVE IDs:** CVE-2026-43196, CVE-2026-43201, CVE-2026-45947, CVE-2026-23236, CVE-2026-43167, CVE-2026-43136

### USN-8497-1 – USN-8497-1: Linux kernel (Low Latency) vulnerabilities
**Severity:** Low  **CVEs:** 321
[View USN](https://ubuntu.com/security/notices/USN-8497-1)
**CVE IDs:** CVE-2026-43196, CVE-2026-45947, CVE-2026-43167, CVE-2026-47337, CVE-2026-45981, CVE-2026-43304

### USN-8492-2 – USN-8492-2: Linux kernel vulnerabilities
**Severity:** Low  **CVEs:** 299
[View USN](https://ubuntu.com/security/notices/USN-8492-2)
**CVE IDs:** CVE-2026-43196, CVE-2026-43201, CVE-2026-45947, CVE-2026-23236, CVE-2026-43167, CVE-2026-43136

### USN-8496-1 – USN-8496-1: cifs-utils vulnerability
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8496-1)

### USN-8488-2 – USN-8488-2: Linux kernel (Raspberry Pi) vulnerabilities
**Severity:** Low  **CVEs:** 236
[View USN](https://ubuntu.com/security/notices/USN-8488-2)
**CVE IDs:** CVE-2026-46074, CVE-2026-46316, CVE-2026-31578, CVE-2026-43073, CVE-2026-46059, CVE-2026-46053

### USN-8495-1 – USN-8495-1: nghttp2 vulnerability
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8495-1)

### Recommended Actions

- Run `sudo apt update && sudo apt upgrade` on all Ubuntu systems
- Prioritise kernel USNs — may require reboot
- Review USNs affecting your specific Ubuntu LTS version


---

# Red Hat Security Advisories – July 2026

Red Hat published **0 RHSAs** covering **0 CVEs** — Critical: 0, Important: 0.


### Recommended Actions

- Apply updates via `dnf update` or `yum update`
- Prioritise Critical and Important RHSAs
- RHEL subscribers can use Red Hat Satellite or Insights for fleet management


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
*Data collected automatically via [patch-tuesday-tracker](https://github.com/YOUR_USERNAME/patch-tuesday-tracker). Generated: 2026-07-03T10:24:13.928715Z*
