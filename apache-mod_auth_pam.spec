%define		mod_name	auth_pam
%define 	apxs		/usr/sbin/apxs
Summary:	This is the PAM authentication module for Apache
Summary(es):	Este m�dulo proporciona autenticaci�n PAM para Apache
Summary(pl):	Modu� uwierzytelnienia PAM dla Apache
Summary(pt_BR):	Este m�dulo prov� autentica��o PAM para o Apache
Name:		apache-mod_%{mod_name}
Version:	1.1.1
Release:	1
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://pam.sourceforge.net/mod_%{mod_name}/dist/mod_%{mod_name}-2.0-%{version}.tar.gz
# Source0-md5:	ab873520ddd2fee7d480dfd53e464e0a
Source1:	apache-mod_auth_pam.conf
URL:		http://pam.sourceforge.net/mod_auth_pam/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache >= 2.0
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using PAM (pluggable authentication module).

%description -l es
Este m�dulo permite autenticar clientes HTTP usando el directorio PAM.

%description -l pl
To jest modu� uwierzytelnienia dla Apache pozwalaj�cy na
uwierzytelnianie klient�w HTTP przez PAM.

%description -l pt_BR
Este m�dulo permite que voc� autentique clientes HTTP usando o
diret�rio PAM.

%prep
%setup -q -n mod_%{mod_name}

%build
%{apxs} -c mod_%{mod_name}.c	-o mod_%{mod_name}.la	 -lpam
%{apxs} -c mod_auth_sys_group.c -o mod_auth_sys_group.la -lpam

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},/etc/pam.d,%{_sysconfdir}/httpd.conf}

install .libs/mod_*.so $RPM_BUILD_ROOT%{_pkglibdir}
install samples/httpd $RPM_BUILD_ROOT/etc/pam.d/httpd
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%preun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%triggerpostun -- %{name} < 1.1
if [ -f %{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf ]; then
	echo "Saving old configuration as %{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf.rpmsave"
	cp -f %{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf %{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf.rpmsave
	echo "Adjusting configuration for apache-mod_auth_pam >= 1.1"
	sed -i -e '{ s/pam_auth_module/auth_pam_module/g; s/etc_group_auth_module/auth_sys_group_module/g; s/mod_auth_pam2.so/mod_auth_pam.so/g; s/mod_auth_etc_group.so/mod_auth_sys_group.so/g; }' %{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf

	%service -q httpd restart
fi

# This shouldn't be here, but someone has used version 2.0 in spec when real
# version was 1.0a. Since it was built as 2.0 I don't see other way to perform
# clean upgrade. This trigger may be a problem when real 2.0 will be out.
%triggerpostun -- %{name} >= 2.0
if [ -f %{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf ]; then
	echo "Saving old configuration as %{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf.rpmsave"
	cp -f %{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf %{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf.rpmsave
	echo "Adjusting configuration for apache-mod_auth_pam >= 1.1"
	sed -i -e '{ s/pam_auth_module/auth_pam_module/g; s/etc_group_auth_module/auth_sys_group_module/g; s/mod_auth_pam2.so/mod_auth_pam.so/g; s/mod_auth_etc_group.so/mod_auth_sys_group.so/g; }' %{_sysconfdir}/httpd.conf/52_mod_auth_pam.conf

	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc doc/{configure,faq}.html samples/dot-htaccess README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_auth_pam.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%config(noreplace) /etc/pam.d/httpd
