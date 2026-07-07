# JULY 2026 SECURITY PATCH ROUNDUP – Windows, iOS, macOS, Android, Linux & More

July 2026's patch cycle brings updates across all major platforms. This month's roundup covers Windows, Apple, Android, Ubuntu, Red Hat, Debian, ChromeOS, Palo Alto Networks, and Cisco IOS/IOS XE. Combined, this month addresses approximately **720+ CVEs** across the ecosystem.

Below is the full breakdown.

---

# Windows Updates – 2026-Jul

Microsoft addressed **380 CVEs** this month — **5 Critical** and **16 Important**.


## Key KB Articles

- **Server Software**

## Critical CVEs

- **CVE-2026-9547** — SSH improper host validation
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

Canonical published **10 USNs** covering **340 CVEs** this month.


## Key Security Notices


### USN-8514-1 – USN-8514-1: OpenSSH vulnerability
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8514-1)

### USN-8502-1 – USN-8502-1: GnuTLS vulnerabilities
**Severity:** Unknown  **CVEs:** 10
[View USN](https://ubuntu.com/security/notices/USN-8502-1)
**CVE IDs:** CVE-2026-42009, CVE-2026-3833, CVE-2024-0553, CVE-2026-42010, CVE-2024-12243, CVE-2026-5260

### USN-8513-1 – USN-8513-1: PHP vulnerabilities
**Severity:** Unknown  **CVEs:** 3
[View USN](https://ubuntu.com/security/notices/USN-8513-1)
**CVE IDs:** CVE-2025-14179, CVE-2026-6722, CVE-2026-7261

### USN-8512-1 – USN-8512-1: Gzip vulnerabilities
**Severity:** Unknown  **CVEs:** 2
[View USN](https://ubuntu.com/security/notices/USN-8512-1)
**CVE IDs:** CVE-2026-41991, CVE-2026-41992

### USN-8511-1 – USN-8511-1: socat vulnerabilities
**Severity:** Unknown  **CVEs:** 2
[View USN](https://ubuntu.com/security/notices/USN-8511-1)
**CVE IDs:** CVE-2024-54661, CVE-2026-56123

### USN-8510-1 – USN-8510-1: tar vulnerability
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8510-1)

### USN-8509-1 – USN-8509-1: Python vulnerabilities
**Severity:** Low  **CVEs:** 17
[View USN](https://ubuntu.com/security/notices/USN-8509-1)
**CVE IDs:** CVE-2026-9669, CVE-2025-13462, CVE-2026-2297, CVE-2026-6019, CVE-2026-3644, CVE-2026-4786

### USN-8506-1 – USN-8506-1: Request Tracker vulnerabilities
**Severity:** Unknown  **CVEs:** 7
[View USN](https://ubuntu.com/security/notices/USN-8506-1)
**CVE IDs:** CVE-2026-44229, CVE-2026-6841, CVE-2026-41076, CVE-2026-41075, CVE-2026-44231, CVE-2026-41073

### USN-8505-1 – USN-8505-1: Parsl vulnerability
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8505-1)

### USN-8492-3 – USN-8492-3: Linux kernel (Raspberry Pi Real-time) vulnerabilities
**Severity:** Low  **CVEs:** 299
[View USN](https://ubuntu.com/security/notices/USN-8492-3)
**CVE IDs:** CVE-2025-71232, CVE-2026-43269, CVE-2026-43313, CVE-2026-43200, CVE-2026-43264, CVE-2026-43256

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

Google released **1 ChromeOS updates** covering **0 CVEs** this month.


## Stable Channel Update for ChromeOS / ChromeOS Flex
**Date:** 2026-07-06  **CVEs:** 0
**Version(s):** 149.0.7827.232
[View release notes](http://chromereleases.googleblog.com/2026/07/stable-channel-update-for-chromeos.html)

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
*Data collected automatically via [patch-tuesday-tracker](https://github.com/YOUR_USERNAME/patch-tuesday-tracker). Generated: 2026-07-07T10:43:15.913525Z*
