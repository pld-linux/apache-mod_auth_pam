%define		mod_name	auth_pam
%define 	apxs		/usr/sbin/apxs
Summary:	This is the PAM authentication module for Apache
Summary(es):	Este módulo proporciona autenticación PAM para Apache
Summary(pl):	Modu³ uwierzytelnienia PAM dla Apache
Summary(pt_BR):	Este módulo provê autenticação PAM para o Apache
Name:		apache-mod_%{mod_name}
Version:	2.0
Release:	5
License:	GPL
Group:		Networking/Daemons
Source0:	http://pam.sourceforge.net/mod_%{mod_name}/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	561a495f27e6cc810641bd6ce6db3d02
Source1:	apache-mod_auth_pam.conf
Patch0:		%{name}-missing_constant.patch
URL:		http://pam.sourceforge.net/mod_auth_pam/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	pam-devel
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using PAM (pluggable authentication module).

%description -l es
Este módulo permite autenticar clientes HTTP usando el directorio PAM.

%description -l pl
To jest modu³ uwierzytelnienia dla Apache pozwalaj±cy na
uwierzytelnianie klientów HTTP przez PAM.

%description -l pt_BR
Este módulo permite que você autentique clientes HTTP usando o
diretório PAM.

%prep
%setup -q -n mod_%{mod_name}
cd apache-2.0
%patch0 -p0

%build
cd apache-2.0
%{apxs} -c mod_%{mod_name}2.c	-o mod_%{mod_name}2.la	 -lpam
%{apxs} -c mod_auth_etc_group.c -o mod_auth_etc_group.la -lpam

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},/etc/pam.d,%{_sysconfdir}/httpd.conf}

install apache-2.0/.libs/mod_*.so $RPM_BUILD_ROOT%{_pkglibdir}
install samples/httpd- $RPM_BUILD_ROOT/etc/pam.d/httpd
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc doc/{configure,faq}.txt samples/dot-htaccess README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_auth_pam.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%config(noreplace) /etc/pam.d/httpd
