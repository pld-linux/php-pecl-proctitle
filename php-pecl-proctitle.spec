%define		modname proctitle
Summary:	change current process' name
Summary(pl.UTF-8):	zmiana nazwy bieżącego procesu
Name:		php-pecl-%{modname}
Version:	0.1.1
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	274eb72584b7fc617f191473bcd2ee14
URL:		http://pecl.php.net/package/proctitle/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-pear-%{modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension allows changing the current process'. This is useful
when using pcntl_fork() to identify running processes in process list.

%description -l pl.UTF-8
Rozszerzenie to pozwala na zmianę nazwy bieżącego procesu. Jest to
szcególnie przydante do identyfikacji procesów na liście procesu w
przypadku korzystania z pcntl_fork().

%prep
%setup -q -c
cat <<'EOF' > %{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%build
cd %{modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -D %{modname}-%{version}/modules/proctitle.so $RPM_BUILD_ROOT%{php_extensiondir}/%{modname}.so

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

cp -a %{modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{modname}-%{version}/README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
