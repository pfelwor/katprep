# katprep
**katprep** is a Python toolkit for automating system maintenance and generating patch reports for systems managed with [Foreman](http://www.theforeman.org/)/[Katello](http://www.katello.org/) or [Red Hat Satellite 6.x](http://www.redhat.com/products/enterprise-linux/satellite/).

This can be very useful if you need to document software changes due to IT certifications like [ISO/IEC 27001:2005](http://en.wikipedia.org/wiki/ISO/IEC_27001:2005) or many other.

katprep can automate the following infrastructure tasks:
  - create/remove virtual machine snapshots hypervisor independently (*e.g. VMware vSphere, KVM, XEN, Hyper-V,...*) by utilizing [libvirt](http://www.libvirt.org) and the [VMware vSphere Python API bindings (*pyVmomi*)](https://github.com/vmware/pyvmomi)
  - schedule/remove downtimes within your monitoring system (*Nagios/Icinga, Icinga2*)
  - patch and reboot affected systems
  - document system changes in a customizable report by utilizing [Pandoc](https://pypi.python.org/pypi/pypandoc) (*HTML, Markdown,...*)
  
This software is a complete rewrite of my other toolkit [**satprep**](https://github.com/stdevel/satprep).

# Documentation and contribution
The project documentation is created automatically using [Sphinx](http://www.sphinx-doc.org) - it can be found in the **doc** folder of this repository. Check-out [**this website**](http://katprep.st-devel.net/doc/latest) for an online mirror.

You want to contribute? That's great! Please check-out the [**Issues**](https://github.com/stdevel/katprep/issues) tab of this project and share your thoughts/ideas in a new issue - also, pull requests are welcome!

# How does this work?
katprep uses Puppet host parameters to assign additional meta information to systems managed with Foreman/Katello or Red Hat Satellite such as:
  - monitoring/virtualization system managing the host
  - differing object names within those systems
  - snapshots required before system maintenance

If you plan to execute maintenance tasks, katprep triggers monitoring and virtualization hosts to schedule downtimes and create VM snapshots. Once these tasks have been completed, katprep can automatically trigger the patch installation and system reboot. After verifying your systems, katprep can remove downtimes and snapshots automatically. As a result, patching big system landscapes becomes less time-consuming.

To make the installation even easier, an auto-discover functionality is [currently under development](https://github.com/stdevel/katprep/issues/8). This feature will automatically scan your monitoring systems and hypervisors and link gathered information with Foreman/Katello and Red Hat Satellite.
