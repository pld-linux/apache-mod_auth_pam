%define		mod_name	auth_pam
%define 	apxs		/usr/sbin/apxs
Summary:	This is the PAM authentication module for Apache
Summary(es):	Este módulo proporciona autenticación PAM para Apache
Summary(pl):	Modu³ uwierzytelnienia PAM dla Apache
Summary(pt_BR):	Este módulo provê autenticação PAM para o Apache
Name:		apache-mod_%{mod_name}
Version:	1.1.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://pam.sourceforge.net/mod_auth_pam/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	b1e36b5df18a177e671785f7f4c8001c
Patch0:		%{name}-symbol_fix.patch
URL:		http://pam.sourceforge.net/mod_auth_pam/
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
Requires(post,preun):	%{apxs}
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

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
%setup -q -n mod_%{mod_name}-%{version}
%patch -p1

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so -lpam -ldl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},/etc/pam.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install samples/httpd- $RPM_BUILD_ROOT/etc/pam.d/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc doc/{configure,faq}.txt samples/dot-htaccess README
%config(noreplace) /etc/pam.d/httpd
%attr(755,root,root) %{_pkglibdir}/*
