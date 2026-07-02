# JULY 2026 SECURITY PATCH ROUNDUP – Windows, iOS, macOS, Android, Linux & More

July 2026's patch cycle brings updates across all major platforms. This month's roundup covers Windows, Apple, Android, Ubuntu, Red Hat, Debian, ChromeOS, Palo Alto Networks, and Cisco IOS/IOS XE. Combined, this month addresses approximately **889+ CVEs** across the ecosystem.

Below is the full breakdown.

---

# Windows Updates – 2026-Jul

Microsoft addressed **0 CVEs** this month — **0 Critical** and **0 Important**.


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

Canonical published **7 USNs** covering **889 CVEs** this month.


## Key Security Notices


### USN-8467-2 – USN-8467-2: Perl vulnerabilities
**Severity:** Low  **CVEs:** 2
[View USN](https://ubuntu.com/security/notices/USN-8467-2)
**CVE IDs:** CVE-2026-42496, CVE-2026-8376

### USN-8493-1 – USN-8493-1: Linux kernel vulnerabilities
**Severity:** Low  **CVEs:** 64
[View USN](https://ubuntu.com/security/notices/USN-8493-1)
**CVE IDs:** CVE-2026-43117, CVE-2026-23262, CVE-2026-31607, CVE-2026-31659, CVE-2026-23428, CVE-2025-71222

### USN-8492-1 – USN-8492-1: Linux kernel vulnerabilities
**Severity:** Low  **CVEs:** 299
[View USN](https://ubuntu.com/security/notices/USN-8492-1)
**CVE IDs:** CVE-2026-43117, CVE-2026-23241, CVE-2026-43230, CVE-2026-23233, CVE-2026-31607, CVE-2026-45916

### USN-8488-1 – USN-8488-1: Linux kernel vulnerabilities
**Severity:** Low  **CVEs:** 236
[View USN](https://ubuntu.com/security/notices/USN-8488-1)
**CVE IDs:** CVE-2026-31624, CVE-2026-46286, CVE-2026-31607, CVE-2026-31615, CVE-2026-31603, CVE-2026-46085

### USN-8491-1 – USN-8491-1: Linux kernel (OEM) vulnerabilities
**Severity:** Low  **CVEs:** 62
[View USN](https://ubuntu.com/security/notices/USN-8491-1)
**CVE IDs:** CVE-2026-43117, CVE-2026-31607, CVE-2026-31659, CVE-2026-23428, CVE-2026-43114, CVE-2026-23450

### USN-8490-1 – USN-8490-1: Linux kernel vulnerabilities
**Severity:** Low  **CVEs:** 61
[View USN](https://ubuntu.com/security/notices/USN-8490-1)
**CVE IDs:** CVE-2026-43117, CVE-2026-31607, CVE-2026-31659, CVE-2026-23428, CVE-2026-43114, CVE-2026-23450

### USN-8489-1 – USN-8489-1: Linux kernel (OEM) vulnerabilities
**Severity:** Low  **CVEs:** 165
[View USN](https://ubuntu.com/security/notices/USN-8489-1)
**CVE IDs:** CVE-2026-46286, CVE-2026-46048, CVE-2026-46085, CVE-2026-46099, CVE-2026-46026, CVE-2026-46028

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
*Data collected automatically via [patch-tuesday-tracker](https://github.com/YOUR_USERNAME/patch-tuesday-tracker). Generated: 2026-07-02T10:34:54.508265Z*
