%define _initddir /etc/rc.d/init.d

Summary:	A client to update host entries on DynDNS like services
Name:		ddclient
Version:	3.8.1
Release:	%mkrel 1
License:	GPL
Group:		System/Configuration/Networking
URL:		http://ddclient.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/ddclient/%name-%version.tar.bz2
# (fc) 3.8.0-2mdv add LSB header
Patch0:		ddclient-3.8.0-lsb.patch
Requires:	perl(IO::Socket::SSL)
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
DDclient is a small full featured client requiring only Perl and no
additional modules. It runs under most UNIX OSes and has been tested
under Linux and FreeBSD. Supported features include: operating as a
daemon, manual and automatic updates, static and dynamic updates,
optimized updates for multiple addresses, MX, wildcards, abuse
avoidance, retrying failed updates, and sending update status to
syslog and through e-mail. This release may now obtain your IP address
from any interface, web based IP detection, Watchguard's SOHO router,
Netopia's R910 router, SMC's Barricade broadband router, Netgear's
RT3xx router, Linksys' broadband routers, MaxGate's UGATE-3x00
routers, ELSA's LANCOM DSL/10 routers, Cisco's 2610, 3com 3c886a 56k
Lan Modem, SOHOWare BroadGuard NBG800, almost every other router with
user configurable FW definitions (see the sample-etc_ddclient.conf)
and now provides Full support for DynDNS.org's NIC2 protocol. Support
is also included for other dynamic DNS services. Comes with sample
scripts for use with DHCP, PPP, and cron. See the README for more
information.

%prep
%setup -q
%patch0 -p1 -b .lsb

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_sbindir},%{_sysconfdir}/%{name},%{_initddir}}
mkdir -p %{buildroot}/var/cache/ddclient

install -p ddclient %{buildroot}%{_sbindir}
install -p sample-etc_ddclient.conf %{buildroot}%{_sysconfdir}/%{name}/ddclient.conf
touch %{buildroot}%{_sysconfdir}/%{name}/ddclient.cache
install -p sample-etc_rc.d_init.d_ddclient.redhat %{buildroot}%{_initddir}/ddclient


%clean
rm -rf %{buildroot}

%post
%_post_service privoxy

%preun
%_preun_service privoxy


%files
%defattr(-,root,root)
%doc sample* README* COPYRIGHT COPYING
%{_sbindir}/ddclient
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ddclient.conf
%config(noreplace) %ghost %{_sysconfdir}/%{name}/ddclient.cache
%{_initddir}/ddclient
%dir /var/cache/ddclient




%changelog
* Mon Aug 01 2011 Leonardo Coelho <leonardoc@mandriva.com> 3.8.1-1mdv2012.0
+ Revision: 692695
- bump new version

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 3.8.0-3mdv2011.0
+ Revision: 610205
- rebuild

* Fri Apr 17 2009 Frederic Crozat <fcrozat@mandriva.com> 3.8.0-2mdv2010.1
+ Revision: 367863
- Patch0: add LSB header to initscript
- use macro to add/remove service

* Fri Feb 20 2009 Frederik Himpe <fhimpe@mandriva.org> 3.8.0-1mdv2009.1
+ Revision: 343496
- update to new version 3.8.0

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 3.7.3-5mdv2009.0
+ Revision: 243987
- rebuild

* Thu Mar 13 2008 Andreas Hasenack <andreas@mandriva.com> 3.7.3-3mdv2008.1
+ Revision: 187591
- rebuild for 2008.1

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 04 2007 Emmanuel Andry <eandry@mandriva.org> 3.7.3-1mdv2008.0
+ Revision: 79530
- New version

* Fri May 25 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 3.7.1-3mdv2008.0
+ Revision: 31224
- add explict requirement for perl(IO::Socket::SSL). Without it ddclient
  fails silently when trying to access https servers.
  (automatic requirement not working for this one)

