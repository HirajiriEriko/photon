Summary:	Linux API header files
Name:		linux-api-headers
Version:	4.4.8
Release:	1%{?dist}
License:	GPLv2
URL:		http://www.kernel.org/
Group:		System Environment/Kernel
Vendor:		VMware, Inc.
Distribution: Photon
Source0:    	http://www.kernel.org/pub/linux/kernel/v4.x/linux-4.4.8.tar.xz
%define sha1 linux=78df847edacc6c01cb4dcc89a2b96822d7e8d1e1
BuildArch:	noarch
%description
The Linux API Headers expose the kernel's API for use by Glibc.
%prep
%setup -q -n linux-4.4.8
%build
make mrproper
make headers_check
%install
cd %{_builddir}/linux-%{version}
make INSTALL_HDR_PATH=%{buildroot}%{_prefix} headers_install
find /%{buildroot}%{_includedir} \( -name .install -o -name ..install.cmd \) -delete
%files
%defattr(-,root,root)
%{_includedir}/*
%changelog
*   Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
*   Wed Dec 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
-   Upgrading kernel version to 4.2.0.
*   Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
-   Upgrading kernel version.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version
