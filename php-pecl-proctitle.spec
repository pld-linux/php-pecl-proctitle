%define		php_name	php%{?php_suffix}
%define		modname proctitle
Summary:	Change current process' name
Summary(pl.UTF-8):	Zmiana nazwy bieżącego procesu
Name:		%{php_name}-pecl-%{modname}
Version:	0.1.2
Release:	4
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	5ebf52449f50013383f052271b0dc21a
URL:		http://pecl.php.net/package/proctitle/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension allows changing the current process'. This is useful
when using pcntl_fork() to identify running processes in process list.

%description -l pl.UTF-8
Rozszerzenie to pozwala na zmianę nazwy bieżącego procesu. Jest to
szczególnie przydatne do identyfikacji procesów na liście procesów w
przypadku korzystania z pcntl_fork().

%prep
%setup -qc
mv %{modname}-%{version}/* .

cat <<'EOF' > %{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -D -p modules/proctitle.so $RPM_BUILD_ROOT%{php_extensiondir}/%{modname}.so
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cp -p %{modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini

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
%doc README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
