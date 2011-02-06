#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
%define		netfilter_snap		20070806
%define		llh_version		7:2.6.22.1
%define		name6			ip6tables
#
%define		rel 0.1
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl.UTF-8):	System filtrowania pakietów oraz system translacji adresów (NAT)
Summary(pt_BR.UTF-8):	Ferramenta para controlar a filtragem de pacotes no kernel-2.6.x
Summary(ru.UTF-8):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk.UTF-8):	Утиліти для керування пакетними фільтрами ядра Linux
Summary(zh_CN.UTF-8):	Linux内核包过滤管理工具
Name:		xtables
Version:	1.5.2.1
Release:	%{rel}
License:	GPL
Group:		Networking/Daemons
Source0:	http://dev.computergmbh.de/files/xtables/%{name}-%{version}.tar.bz2
# Source0-md5:	c120ca709d374bab0696cf5e317d47d9
Source2:	iptables.init
Source3:	ip6tables.init
%if %{with dist_kernel} && %{netfilter_snap} != 0
BuildRequires:	kernel%{_alt_kernel}-headers(netfilter) >= %{netfilter_snap}
%endif
BuildConflicts:	kernel-headers < 2.3.0
Provides:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extensible NAT system, and an extensible packet filtering system.
Replacement of ipchains in 2.6 and higher kernels.

%description -l pl.UTF-8
Wydajny system translacji adresów (NAT) oraz system filtrowania
pakietów. Zamiennik ipchains w jądrach 2.6 i nowszych.

%description -l pt_BR.UTF-8
Esta é a ferramenta que controla o código de filtragem de pacotes do
kernel 2.6, obsoletando ipchains. Com esta ferramenta você pode
configurar filtros de pacotes, NAT, mascaramento (masquerading),
regras dinâmicas (stateful inspection), etc.

%description -l ru.UTF-8
xtables управляют кодом фильтрации сетевых пакетов в ядре Linux. Они
позволяют вам устанавливать межсетевые экраны (firewalls) и IP
маскарадинг, и т.п.

%description -l uk.UTF-8
xtables управляють кодом фільтрації пакетів мережі в ядрі Linux. Вони
дозволяють вам встановлювати міжмережеві екрани (firewalls) та IP
маскарадинг, тощо.

%package devel
Summary:	Libraries and headers for developing xtables extensions
Summary(pl.UTF-8):	Biblioteki i nagłówki do tworzenia rozszerzeń xtables
Group:		Development/Libraries

%description devel
Libraries and headers for developing xtables extensions.

%description devel -l pl.UTF-8
Biblioteki i pliki nagłówkowe niezbędne do tworzenia rozszerzeń dla
xtables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl.UTF-8):	Iptables init (w stylu RedHata)
Release:	%{rel}
Group:		Networking/Admin
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}
Requires:	rc-scripts

%description init
Iptables-init is meant to provide an alternate way than firewall-init
to start and stop packet filtering through xtables(8).

%description init -l pl.UTF-8
Iptables-init ma na celu udostępnienie alternatywnego w stosunku do
firewall-init sposobu włączania i wyłączania filtrów IP jądra poprzez
xtables(8).

%prep
%setup -q

%build
%configure \
	--with-kernel=%{_kernelsrcdir} \
	--enable-libipq \
	--enable-shared
%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/iptables
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/ip6tables

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add %{name}
/sbin/chkconfig --add %{name6}

%preun init
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
	/sbin/chkconfig --del %{name6}
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/iptables-xml
%attr(755,root,root) %{_sbindir}/iptables
%attr(755,root,root) %{_sbindir}/iptables-multi
%attr(755,root,root) %{_sbindir}/iptables-restore
%attr(755,root,root) %{_sbindir}/iptables-save
%attr(755,root,root) %{_sbindir}/ip6tables
%attr(755,root,root) %{_sbindir}/ip6tables-multi
%attr(755,root,root) %{_sbindir}/ip6tables-restore
%attr(755,root,root) %{_sbindir}/ip6tables-save
%dir %{_libdir}/xtables
%attr(755,root,root) %{_libdir}/xtables/*.so
%{_mandir}/man8/ip6tables.8*
%{_mandir}/man8/ip6tables-restore.8*
%{_mandir}/man8/ip6tables-save.8*
%{_mandir}/man8/iptables.8*
%{_mandir}/man8/iptables-restore.8*
%{_mandir}/man8/iptables-save.8*
%{_mandir}/man8/iptables-xml.8*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libipq.a
%{_includedir}/ip6tables.h
%{_includedir}/iptables.h
%{_includedir}/libipq.h
%{_includedir}/xtables.h
%{_includedir}/libiptc
%{_mandir}/man3/ipq_*.3*
%{_mandir}/man3/libipq.3*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/iptables
%attr(754,root,root) /etc/rc.d/init.d/ip6tables
