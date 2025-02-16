# fix automatic requires
%global __requires_exclude  ^perl(.*)$

Summary:	A client to update host entries on DynDNS like services
Name:		ddclient
Version:	4.0.0
Release:	1
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		https://ddclient.net
#Source0:	https://downloads.sourceforge.net/ddclient/%{name}-%{version}.tar.gz
Source0:	https://github.com/ddclient/ddclient/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.rwtab
Source2:	%{name}.service
Source3:	%{name}.sysconfig
Source4:	%{name}.NetworkManager
Source5:	%{name}-tmpfiles.conf
Source6:	%{name}.sysusers
Patch0:		ddclient-4.0.0-paths.patch
Patch1:		ddclient-4.0.0-be-satisfied-with-group-read-access-for-config.patch

BuildRequires:	curl
BuildRequires:	rpm-helper
BuildRequires:	perl-generators
BuildRequires:	perl(Sys::Hostname)
BuildRequires:	perl(version)

#Requires:	perl(Data::Validate::IP)
Requires:	perl(Digest::SHA1)
#Requires:	perl(IO::Socket::INET6)
Requires:	perl(IO::Socket::SSL)
#Requires:	perl(JSON::PP)

Requires(pre):	rpm-helper
Requires(postun):rpm-helper

BuildArch:	noarch

%files
%doc sample* README* COPYRIGHT
%{_bindir}/ddclient
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/NetworkManager/dispatcher.d/50-%{name}
%{_sysusersdir}/%{name}.conf
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

# remove executables
find . -name \*exe -delete

# Correct permissions for later usage in %doc
chmod 644 sample-*

%build
%configure \
         --prefix=%{_prefix} \
         --sysconfdir=%{_sysconfdir} \
         --with-confdir=%{_sysconfdir} \
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

# add ddclient user
install -D -pm 0644 %{SOURCE6} %{buildroot}%{_sysusersdir}/%{name}.conf

%triggerprein -- %{name} < 3.8.2
if [ -d %{_sysconfdir}/%{name} ]; then
    if [ -e %{_sysconfdir}/%{name}/%{name}.cache ]; then
	install -m600 -o %{name} -g %{name} -d %{buildroot}%{_localstatedir}/cache/%{name}
	mv %{_sysconfdir}/%{name}/%{name}.cache %{_localstatedir}/cache/%{name}/%{name}.cache
	chown %{name}:%{name}%{_localstatedir}/cache/%{name}/%{name}.cache
	chmod 600 %{_localstatedir}/cache/%{name}/%{name}.cache

    fi
    rmdir --ignore-fail-on-non-empty %{_sysconfdir}/%{name}
1fi

%triggerpostun -- %{name} < %{EVRD}
rm -f %{_localstatedir}/cache/%{name}/*

