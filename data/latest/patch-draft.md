# JULY 2026 SECURITY PATCH ROUNDUP – Windows, iOS, macOS, Android, Linux & More

July 2026's patch cycle brings updates across all major platforms. This month's roundup covers Windows, Apple, Android, Ubuntu, Red Hat, Debian, ChromeOS, Palo Alto Networks, and Cisco IOS/IOS XE. Combined, this month addresses approximately **841+ CVEs** across the ecosystem.

Below is the full breakdown.

---

# Windows Updates – 2026-Jul

Microsoft addressed **397 CVEs** this month — **3 Critical** and **17 Important**.


## Key KB Articles

- **Server Software**

## Critical CVEs

- **CVE-2026-9547** — SSH improper host validation
- **CVE-2026-56000** — xorg-x11-server / xwayland GLX contextTags Use-After-Free in CommonMakeCurrent()
- **CVE-2026-38968** — ntopng through 6.6 is vulnerable to Predictable Session Identifier which can lead to Session Hijacking. HTTP session identifiers in src/HTTPserver.cpp use weak time-seeded pseudo-randomness during session creation. As a result, fresh authenticated logins can receive deterministic or colliding session cookies under attacker-controlled timing.

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

Canonical published **10 USNs** covering **394 CVEs** this month.


## Key Security Notices


### USN-8492-4 – USN-8492-4: Linux kernel (Raspberry Pi) vulnerabilities
**Severity:** Low  **CVEs:** 299
[View USN](https://ubuntu.com/security/notices/USN-8492-4)
**CVE IDs:** CVE-2026-43302, CVE-2026-45893, CVE-2026-46247, CVE-2026-31411, CVE-2026-31436, CVE-2026-43406

### USN-8490-2 – USN-8490-2: Linux kernel (Raspberry Pi) vulnerabilities
**Severity:** Low  **CVEs:** 61
[View USN](https://ubuntu.com/security/notices/USN-8490-2)
**CVE IDs:** CVE-2026-43501, CVE-2026-46325, CVE-2026-31436, CVE-2026-31607, CVE-2026-43038, CVE-2026-43406

### USN-8518-1 – USN-8518-1: mailcap vulnerability
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8518-1)

### USN-8517-1 – USN-8517-1: ClamAV vulnerabilities
**Severity:** Unknown  **CVEs:** 7
[View USN](https://ubuntu.com/security/notices/USN-8517-1)
**CVE IDs:** CVE-2026-20244, CVE-2026-20243, CVE-2026-20215, CVE-2026-20217, CVE-2026-20216, CVE-2026-20213

### USN-8516-1 – USN-8516-1: Apache HTTP Server vulnerabilities
**Severity:** Unknown  **CVEs:** 12
[View USN](https://ubuntu.com/security/notices/USN-8516-1)
**CVE IDs:** CVE-2026-43951, CVE-2026-34355, CVE-2026-42535, CVE-2026-29170, CVE-2026-29167, CVE-2026-44186

### USN-8515-1 – USN-8515-1: Addressable vulnerability
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8515-1)

### USN-8514-1 – USN-8514-1: OpenSSH vulnerability
**Severity:** Unknown  **CVEs:** 0
[View USN](https://ubuntu.com/security/notices/USN-8514-1)

### USN-8502-1 – USN-8502-1: GnuTLS vulnerabilities
**Severity:** Unknown  **CVEs:** 10
[View USN](https://ubuntu.com/security/notices/USN-8502-1)
**CVE IDs:** CVE-2025-9820, CVE-2026-33845, CVE-2026-5260, CVE-2024-12243, CVE-2026-42010, CVE-2026-42009

### USN-8513-1 – USN-8513-1: PHP vulnerabilities
**Severity:** Unknown  **CVEs:** 3
[View USN](https://ubuntu.com/security/notices/USN-8513-1)
**CVE IDs:** CVE-2026-6722, CVE-2026-7261, CVE-2025-14179

### USN-8512-1 – USN-8512-1: Gzip vulnerabilities
**Severity:** Unknown  **CVEs:** 2
[View USN](https://ubuntu.com/security/notices/USN-8512-1)
**CVE IDs:** CVE-2026-41992, CVE-2026-41991

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

Google released **5 ChromeOS updates** covering **37 CVEs** this month.


## Long Term Support Channel Update for ChromeOS
**Date:** 2026-07-09  **CVEs:** 10
**Version(s):** 144.0.7559.257
[View release notes](http://chromereleases.googleblog.com/2026/07/long-term-support-channel-update-for.html)

## Stable Channel Update for Desktop
**Date:** 2026-07-08  **CVEs:** 27
**Version(s):** 150.0.7871.114, 150.0.7871.115, 150.0.7871.101
[View release notes](http://chromereleases.googleblog.com/2026/07/stable-channel-update-for-desktop_01162222768.html)

## Dev Channel Update for ChromeOS / ChromeOS Flex
**Date:** 2026-07-07  **CVEs:** 0
**Version(s):** 151.0.7922.14
[View release notes](http://chromereleases.googleblog.com/2026/07/dev-channel-update-for-chromeos.html)

## Stable Channel Update for Desktop
**Date:** 2026-07-07  **CVEs:** 0
**Version(s):** 150.0.7871.101, 150.0.7871.100, 150.0.7871.47
[View release notes](http://chromereleases.googleblog.com/2026/07/stable-channel-update-for-desktop.html)

## Stable Channel Update for ChromeOS / ChromeOS Flex
**Date:** 2026-07-06  **CVEs:** 0
**Version(s):** 149.0.7827.232
[View release notes](http://chromereleases.googleblog.com/2026/07/stable-channel-update-for-chromeos.html)

### Recommended Actions

- ChromeOS updates automatically; verify via Settings → About ChromeOS
- Enterprise: manage rollouts via Google Admin Console


---

# Palo Alto Networks Advisories – July 2026

Palo Alto Networks published **14 advisories** — Critical: 0, High: 2.


## Critical & High Advisories

- **** [High] — CVE-2026-0288 PAN-OS: Buffer Overflow Vulnerabilities in User-ID Terminal Server Agent (Severity: HI
- **PAN-SA-2026-0010** [High] — PAN-SA-2026-0010 Chromium and Prisma Browser: Monthly Vulnerability Update (July 2026) (Severity: HI

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
*Data collected automatically via [patch-tuesday-tracker](https://github.com/YOUR_USERNAME/patch-tuesday-tracker). Generated: 2026-07-09T12:15:24.658768Z*
