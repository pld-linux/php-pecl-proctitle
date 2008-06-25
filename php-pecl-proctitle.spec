%define		snap	36540
%define		_modname	proctitle
Summary:	%{_modname} - show what code is running in process name
Name:		php-pecl-%{_modname}
Version:	0.1
Release:	0.%{snap}.1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://tools.wikimedia.de/~vvv/mw-nightly/pool/ext-pecl-proctitle-nightly-r%{snap}.tar.gz
# Source0-md5:	384facb4e0c59b4e6c499a824ebef3a2
URL:		http://svn.wikimedia.org/viewvc/mediawiki/trunk/extensions/pecl-proctitle/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Proctitle extension to PHP that allows seeing which portion of code is
executed by Apache child at the moment simply using ‘ps’.

%prep
%setup -q -c
cat <<'EOF' > %{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF


%build
cd pecl-%{_modname}
phpize
%configure \
	--%{!?debug:dis}%{?debug:en}able-debug
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -D pecl-%{_modname}/modules/proctitle.so $RPM_BUILD_ROOT%{php_extensiondir}/%{_modname}.so

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

cp -a %{_modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini

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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
