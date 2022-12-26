Summary:	A client to update host entries on DynDNS like services
Name:		ddclient
Version:	3.10.0
Release:	1
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		https://ddclient.net
#Source0:	https://downloads.sourceforge.net/ddclient/%{name}-%{version}.tar.gz
Source0:	https://github.com/ddclient/ddclient/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	ddclient.rwtab
Source2:	ddclient.service
Source3:	ddclient.sysconfig
Source4:	ddclient.NetworkManager
Source5:	ddclient-tmpfiles.conf
Patch0:		ddclient-3.8.2-paths.patch
Patch1:		ddclient-3.8.2-be-satisfied-with-group-read-access-for-config.patch

BuildRequires:	rpm-helper

Requires:	perl(Digest::SHA1) perl(IO::Socket::SSL)

Requires(pre):	rpm-helper
Requires(postun):rpm-helper

BuildArch:	noarch


%files
%doc sample* README* COPYRIGHT
%{_bindir}/ddclient
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/NetworkManager/dispatcher.d/50-%{name}
%attr(640,root,%{name}) %config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/rwtab.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(700,%{name},%{name}) %dir %{_localstatedir}/cache/%{name}/
%attr(600,%{name},%{name}) %ghost %{_localstatedir}/cache/%{name}/%{name}.cache
%attr(755, %{name}, %{name}) %dir %{_localstatedir}/run/%{name}
%ghost %{_localstatedir}/run/%{name}/%{name}.pid

#---------------------------------------------------------------------------

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
%autosetup -p1

# Correct permissions for later usage in %doc
chmod 644 sample-*

%build
%configure \
         --prefix=%{_prefix} \
         --sysconfdir=%{_sysconfdir} \
         --localstatedir=/var
%make_build

%install
%make_install

##install -p -m755 %{name} -D %{buildroot}%{_sbindir}/%{name}
##install -p -m600 sample-etc_ddclient.conf -D %{buildroot}%{_sysconfdir}/%{name}.conf
install -p -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/rwtab.d/%{name}
install -p -m644 %{SOURCE2} -D %{buildroot}%{_unitdir}/%{name}.service
install -p -m644 %{SOURCE5} -D %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -p -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -m755 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d/50-%{name}
mkdir -p %{buildroot}%{_localstatedir}/{cache,run}/%{name}
touch %{buildroot}%{_localstatedir}/cache/%{name}/%{name}.cache
touch %{buildroot}%{_localstatedir}/run/%{name}/%{name}.pid

%triggerprein -- %{name} < 3.8.2
if [ -d %{_sysconfdir}/%{name} ]; then
    %_pre_useradd %{name} %{_localstatedir}/cache/%{name} /bin/nologin
    if [ -e %{_sysconfdir}/%{name}/%{name}.conf ]; then
	mv %{_sysconfdir}/%{name}/%{name}.conf %{_sysconfdir}/%{name}.conf
	chown root:%{name} %{_sysconfdir}/%{name}.conf
	chmod 640 %{_sysconfdir}/%{name}.conf
    fi
    if [ -e %{_sysconfdir}/%{name}/%{name}.cache ]; then
	install -m600 -o %{name} -g %{name} -d %{buildroot}%{_localstatedir}/cache/%{name}
	mv %{_sysconfdir}/%{name}/%{name}.cache %{_localstatedir}/cache/%{name}/%{name}.cache
	chown %{name}:%{name}%{_localstatedir}/cache/%{name}/%{name}.cache
	chmod 600 %{_localstatedir}/cache/%{name}/%{name}.cache

    fi
    rmdir --ignore-fail-on-non-empty %{_sysconfdir}/%{name}
fi

%triggerpostun -- %{name} < %{EVRD}
rm -f %{_localstatedir}/cache/%{name}/*

%pre
%_pre_useradd %{name} %{_localstatedir}/cache/%{name} /bin/nologin

%postun
%_postun_userdel %{name}

