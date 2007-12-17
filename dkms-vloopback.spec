%define module vloopback
%define version 1.0
%define release %mkrel 2

Summary: Video4Linux Loopback Device
Name: dkms-%{module}
Version: %{version}
Release: %{release} 
License: GPL
Group: System/Kernel and hardware
Source0: http://www.lavrsen.dk/twiki/pub/Motion/VideoFourLinuxLoopbackDevice/%{module}-%{version}.tar.bz2
URL: http://www.lavrsen.dk/twiki/bin/view/Motion/VideoFourLinuxLoopbackDevice
Provides: %{module}
Requires: dkms >= 1.00
BuildArch: noarch

%description
The video4linux device is a driver that implements a video pipe using two
video4linux devices.

Jeroen Vreeken wrote this driver for debugging motion realtime, which worked
very nice and he decided to make something usefull of it. You can use this
driver for looking at motion in realtime or for feeding a webcam while still
securing your room.

Note also that vloopback output can be used by several applications at the same time.

%prep
%setup -n %{module}-%{version} -q

%build

%install
if [ "$RPM_BUILD_ROOT" != "/" ]; then
	rm -rf $RPM_BUILD_ROOT
fi

mkdir -p $RPM_BUILD_ROOT/usr/src/%{module}-%{version}-%{release}

cp -rf	Makefile \
	vloopback.c \
	$RPM_BUILD_ROOT/usr/src/%{module}-%{version}-%{release}
cat > %{buildroot}/usr/src/%{module}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_VERSION="%{version}-%{release}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{module}"
MAKE[0]="src=/usr/src/${PACKAGE_NAME}-${PACKAGE_VERSION}/ ; make"
CLEAN="make clean"

BUILT_MODULE_NAME[0]="%{module}"
DEST_MODULE_LOCATION[0]="/kernel/3rdparty/%{module}"

AUTOINSTALL=yes
EOF

%clean
if [ "$RPM_BUILD_ROOT" != "/" ]; then
	rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root,-)
%doc README vloopback.html
/usr/src/%{module}-%{version}-%{release}

%post
dkms add -m	%{module} -v %{version}-%{release} --rpm_safe_upgrade
dkms build -m	%{module} -v %{version}-%{release} --rpm_safe_upgrade
dkms install -m	%{module} -v %{version}-%{release} --rpm_safe_upgrade

%preun
dkms remove -m	%{module} -v %{version}-%{release} --rpm_safe_upgrade --all

