%define __jar_repack 0
%define _prefix /opt
%define debug_package %{nil}

Summary: OrientDB is a multi-model datastore
Name: orientdb
Version: %{version}
Release: %{build_number}%{?dist}
License: Apache License, Version 2.0
Group: Applications
Source0: https://s3.us-east-2.amazonaws.com/orientdb3/releases/%{version}/orientdb-%{version}.tar.gz
URL: http://www.orientdb.org
BuildRoot: %{_tmppath}/%{name}-%{orientdb_version}-root
Prefix: /opt
Requires: java >= 1.8
Requires(pre): shadow-utils
Requires: zookeeper >= 3.3.4

Vendor: Apache Software Foundation
Packager: Ivan Dyachkov <ivan.dyachkov@klarna.com>
Provides: orientdb

%description
OrientDB is a multi-model datastore.

%prep
%setup -n %{tarball_name}

%build
rm -f libs/*

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/orientdb-%{version}
mkdir $RPM_BUILD_ROOT%{_prefix}/orientdb-%{version}/bin
cp -rf {bin,config,databases,*.txt,lib,log,plugins,www} $RPM_BUILD_ROOT%{_prefix}/orientdb-%{version}/.
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
sed -i '0,/ORIENTDB_DIR.*/s//ORIENTDB_DIR="\/opt\/orientdb-%{version}"/' bin/orientdb.sh
sed -i '0,/ORIENTDB_USER.*/s//ORIENTDB_USER="orientdb"/' bin/orientdb.sh
install -m 755 bin/orientdb.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/orientdb
%else
mkdir -p $RPM_BUILD_ROOT/etc/systemd/system/
sed -i '0,/User=.*/s//User="orientdb"/' bin/orientdb.service
sed -i '0,/Group.*/s//Group="orientdb"/' bin/orientdb.service
sed -i '0,/$ORIENTDB_HOME/s//\/opt\/orientdb-%{version}/' bin/orientdb.service
install -m 644 bin/orientdb.service $RPM_BUILD_ROOT/etc/systemd/system/
%endif
mkdir -p $RPM_BUILD_ROOT/var/log/orientdb

%clean
rm -rf $RPM_BUILD_ROOT

%pre

# Create user and group
getent group orientdb >/dev/null || groupadd -r orientdb
getent passwd orientdb >/dev/null || \
			 useradd -r -g orientdb -d /opt/orientdb -s /bin/bash \
			  -c "OrientDB Account" orientdb

exit 0

%post
alternatives --install /opt/orientdb orientdbhome /opt/%{name}-%{version} %{int_version}

if [ $1 = 1 ]; then
    /sbin/chkconfig --add orientdb
fi

if [ -d "/opt/orientdb" ]; then
	echo -n "Copying previous configs... "
	cp -rf /opt/orientdb/config/* /opt/%{name}-%{version}/config/
	echo "done."
fi
alternatives --install /opt/orientdb orientdbhome  /opt/%{name}-%{version} %{int_version}

%preun
# When the last version of a package is erased, $1 is 0
if [ $1 = 0 ]; then
    /sbin/service orientdb stop >/dev/null
    /sbin/chkconfig --del orientdb
fi

%postun
# When the last version of a package is erased, $1 is 0
# Otherwise it's an upgrade and we need to restart the service
if [ $1 -ge 1 ]; then
    /sbin/service orientdb stop >/dev/null 2>&1
    sleep 1
    /sbin/service orientdb start >/dev/null 2>&1
fi

alternatives --remove orientdbhome  /opt/%{name}-%{version}



%files
%defattr(-,root,root)
%attr(0755,orientdb,orientdb) %dir /opt/orientdb-%{version}
%attr(0755,orientdb,orientdb) /opt/orientdb-%{version}/bin
%attr(0755,orientdb,orientdb) /opt/orientdb-%{version}/databases
%attr(0755,orientdb,orientdb) /opt/orientdb-%{version}/*.txt
%attr(0755,orientdb,orientdb) /opt/orientdb-%{version}/lib
%attr(0755,orientdb,orientdb) /opt/orientdb-%{version}/log
%attr(0755,orientdb,orientdb) /opt/orientdb-%{version}/plugins
%attr(0755,orientdb,orientdb) /opt/orientdb-%{version}/www
%config(noreplace) %attr(755,orientdb,orientdb) /opt/%{name}-%{version}/config

%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
%attr(0775,root,orientdb) /etc/rc.d/init.d/orientdb
%else
%attr(0775,root,orientdb) /etc/systemd/system/orientdb.service
%endif

%attr(0755,orientdb,orientdb) %dir /var/log/orientdb

%doc readme.txt
%doc license.txt

