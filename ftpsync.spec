#
Summary:	Set of bash scripts for mirroring debian
Summary(pl.UTF-8):	Zestaw skryptów do mirrorowania debiana
Name:		ftpsync
Version:	8086
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://ftp-master.debian.org/ftpsync.tar.gz
# Source0-md5:	b824db81496648d8c298069d8b7bbbe5
URL:		http://www.debian.org/mirror/ftpmirror
Requires:	rsync
Provides:	group(rsync)
Provides:	user(rsync)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Set of bash scripts for mirroring Debian.

%description -l pl.UTF-8
Zestaw skryptów do mirrorowania Debiana.

%prep
%setup -q -c

sed -i 's,${BASEDIR}/etc,/etc/ftpsync,' bin/* etc/*
sed -i 's,${LOGDIR}/log,/var/log/ftpsync,' bin/* etc/*

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/%{name}/secrets,%{_var}/{log,lib}/%{name}}

install etc/common $RPM_BUILD_ROOT/etc/%{name}
install bin/* $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 239 ftpsync %{name}
%useradd -u 239 ftpsync -d /var/lib/%{name} -g %{name} -c "ftpsync user" %{name}

%post

%preun

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc README etc/*.sample
%{_sysconfdir}/%{name}
%{_bindir}/*
%attr(2751,root,ftpsync) %dir /var/log/ftpsync
%attr(2751,ftpsync,ftpsync) %dir /var/lib/ftpsync
