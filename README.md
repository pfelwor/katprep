# katprep
**katprep** is a Python toolkit for automating system maintenance and generating patch reports for systems managed with [Foreman](http://www.theforeman.org/)/[Katello](http://www.katello.org/) or [Red Hat Satellite 6.x](http://www.redhat.com/products/enterprise-linux/satellite/).
 
This can be very useful if you need to document software changes due to IT certifications like [ISO/IEC 27001:2005](http://en.wikipedia.org/wiki/ISO/IEC_27001:2005) or many other.

This toolkit is currently under development, it's a complete rewrite of my other toolkit [**satprep**](https://github.com/stdevel/satprep), which did the same job for systems managed with [Spacewalk](http://www.spacewalkproject.org/), [Red Hat Satellite 5.x](http://www.redhat.com/products/enterprise-linux/satellite/) or [SUSE Manager](http://www.suse.com/products/suse-manager/).

So - stay tuned and check-out this site more often.

# Planned features
- Reporting
  - various formats by using **Pandoc** and [**pypandoc**](https://pypi.python.org/pypi/pypandoc)
  - template with variables, automation using **citeproc**?
- Automation
  - (*un-*)scheduling downtimes within popular monitoring solutions such as:
    - Nagios / Icinga 1.x
    - Icinga 2
    - Thruk
    - Shinken
  - creating/removing snapshots for virtual machines using [libvirt](http://www.libvirt.org) supporting multiple hypervisors including:
    - KVM
    - Xen
    - VMware vSphere ESXi
    - Microsoft Hyper-V
  - applying errata after successful preparation
  - rebooting systems if patches require this
- creating inventory snapshots of managed systems before and after maintenance
- creating reports listing relevant information about installed errata (*category, date, affected packages, CVE information*)

# Planned workflow
- Once after the installation and after new systems were registered, Puppet host parameters are set using ``katprep_parameters.py`
- When patch maintenance is needed, a snapshot report is created using ``katprep_snapshot.py``
- Patch maintenance per system is prepared and (*optionally*) executed using ``katprep_maintenance.py``
- After patch maintenance, another snapshot report is created
- Final patch reports per system are created using ``katprep_report.py``
