%define		mod_name	auth_pam
Summary:	This is the PAM authentication module for Apache
Name:		apache-mod_%{mod_name}
Version:	1.0a
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://pam.sourceforge.net/mod_auth_pam/dist/mod_%{mod_name}.tar.gz
BuildRequires:	/usr/sbin/apxs
BuildRequires:	apache(EAPI)-devel
Prereq:		/usr/sbin/apxs
Requires:	apache(EAPI)
URL:		http://pam.sourceforge.net/mod_auth_pam/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using user entries in an samba directory.

%prep 
%setup -q -n mod_%{mod_name}-%{version}

%build
%{_sbindir}/apxs -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%post
/usr/sbin/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
