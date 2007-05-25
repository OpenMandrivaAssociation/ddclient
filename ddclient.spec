%define _initddir /etc/rc.d/init.d

Summary: A client to update host entries on DynDNS like services
Name: ddclient
Version: 3.7.1
Release: %mkrel 3
License: GPL
Group: System/Configuration/Networking
URL: http://ddclient.sourceforge.net/
Source0: http://prdownloads.sourceforge.net/ddclient/%name-%version.tar.bz2
Requires: perl(IO::Socket::SSL)
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

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
/sbin/chkconfig --add ddclient

%preun
if [ $1 = 0 ]; then
        /sbin/service ddclient stop > /dev/null 2>&1
        /sbin/chkconfig --del ddclient
fi

%files
%defattr(-,root,root)
%doc sample* README* COPYRIGHT COPYING
%{_sbindir}/ddclient
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ddclient.conf
%config(noreplace) %ghost %{_sysconfdir}/%{name}/ddclient.cache
%{_initddir}/ddclient
%dir /var/cache/ddclient


