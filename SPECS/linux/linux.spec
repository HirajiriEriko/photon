%global security_hardening none
Summary:        Kernel
Name:           linux
Version:    	4.4.8
Release:    	2%{?dist}
License:    	GPLv2
URL:        	http://www.kernel.org/
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:    	http://www.kernel.org/pub/linux/kernel/v4.x/%{name}-%{version}.tar.xz
%define sha1 linux=78df847edacc6c01cb4dcc89a2b96822d7e8d1e1
Source1:	config-%{version}
Patch0:         double-tcp_mem-limits.patch
Patch1:         linux-4.4-sysctl-sched_weighted_cpuload_uses_rla.patch
Patch2:         linux-4.4-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch3:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch4:         06-sunrpc.patch
Patch5:         vmware-log-kmsg-dump-on-panic.patch
Patch6:         net-Driver-Vmxnet3-set-CHECKSUM_UNNECESSARY-for-IPv6-packets.patch
BuildRequires:  bc
BuildRequires:  kbd
BuildRequires:  kmod
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  xml-security-c-devel
BuildRequires:  libdnet
BuildRequires:  libmspack
BuildRequires:  Linux-PAM
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
Requires:       filesystem kmod coreutils

%description
The Linux package contains the Linux kernel. 


%package dev
Summary:    Kernel Dev
Group:        System Environment/Kernel
Requires:    python2
%description dev
The Linux package contains the Linux kernel dev files

%package drivers-gpu
Summary:    Kernel GPU Drivers
Group:        System Environment/Kernel
Requires:    %{name} = %{version}-%{release}
%description drivers-gpu
The Linux package contains the Linux kernel drivers for GPU

%package sound
Summary:    Kernel Sound modules
Group:        System Environment/Kernel
Requires:    %{name} = %{version}-%{release}
%description sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:    Kernel docs
Group:        System Environment/Kernel
Requires:    python2
%description docs
The Linux package contains the Linux kernel doc files

%package oprofile
Summary:    Kernel driver for oprofile, a statistical profiler for Linux systems
Group:        System Environment/Kernel
Requires:    %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
make mrproper
cp %{SOURCE1} .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
install -vdm 755 %{buildroot}/etc/modprobe.d
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}
make INSTALL_MOD_PATH=%{buildroot} modules_install

cp -v arch/x86/boot/bzImage    %{buildroot}/boot/vmlinuz-%{version}
cp -v System.map        %{buildroot}/boot/system.map-%{version}
cp -v .config            %{buildroot}/boot/config-%{version}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cat > %{buildroot}/boot/%{name}-%{version}-%{release}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet plymouth.enable=0
photon_linux=vmlinuz-%{version}
photon_initrd=initrd.img-no-kmods
EOF

# Restrict the permission on system.map-X file
chmod -v 400 %{buildroot}/boot/system.map-%{version}

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{version}/source
rm -rf %{buildroot}/lib/modules/%{version}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy
find arch/x86/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy
find arch/x86/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{version}-%{release}' copy

cp .config %{buildroot}/usr/src/%{name}-headers-%{version}-%{release} # copy .config manually to be where it's expected to be
ln -sf "/usr/src/%{name}-headers-%{version}-%{release}" "%{buildroot}/lib/modules/%{version}/build"

%post
/sbin/depmod -aq %{version}
ln -sf %{name}-%{version}-%{release}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -aq %{version}

%post sound
/sbin/depmod -aq %{version}

%post oprofile
/sbin/depmod -aq %{version}

%files
%defattr(-,root,root)
/boot/system.map-%{version}
/boot/config-%{version}
/boot/vmlinuz-%{version}
%config(noreplace) /boot/%{name}-%{version}-%{release}.cfg
/lib/firmware/*
/lib/modules/*
%exclude /lib/modules/%{version}/build
%exclude /lib/modules/%{version}/kernel/drivers/gpu
%exclude /lib/modules/%{version}/kernel/sound
%exclude /lib/modules/%{version}/kernel/arch/x86/oprofile/

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{version}/*

%files dev
%defattr(-,root,root)
/lib/modules/%{version}/build
/usr/src/%{name}-headers-%{version}-%{release}

%files drivers-gpu
%defattr(-,root,root)
%exclude /lib/modules/%{version}/kernel/drivers/gpu/drm/cirrus/
/lib/modules/%{version}/kernel/drivers/gpu

%files sound
%defattr(-,root,root)
/lib/modules/%{version}/kernel/sound

%files oprofile
%defattr(-,root,root)
/lib/modules/%{version}/kernel/arch/x86/oprofile/

%changelog
* 	Wed May 18 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-2
-	Enabled CONFIG_UPROBES in config as needed by ktap
*   Wed May 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
-   Added net-Drivers-Vmxnet3-set-... patch
*   Tue May 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-27
-   Compile Intel GigE and VMXNET3 as part of kernel.
*   Tue Apr 28 2016 Nick Shi <nshi@vmware.com> 4.2.0-26
-   Compile cramfs.ko to allow mounting cramfs image
*   Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-25
-   Revert network interface renaming disable in kernel.
*   Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-24
-   Support kmsg dumping to vmware.log on panic
-   sunrpc: xs_bind uses ip_local_reserved_ports
*   Mon Mar 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-23
-   Enabled Regular stack protection in Linux kernel in config
*   Thu Mar 17 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-22
-   Restrict the permissions of the /boot/System.map-X file
*   Fri Mar 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-21
-   Patch: SUNRPC: Do not reuse srcport for TIME_WAIT socket.
*   Wed Mar 02 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-20
-   Patch: SUNRPC: Ensure that we wait for connections to complete
    before retrying
*   Fri Feb 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
-   Disable watchdog under VMware hypervisor.
*   Thu Feb 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
-   Added rpcsec_gss_krb5 and nfs_fscache
*   Mon Feb 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-17
-   Added sysctl param to control weighted_cpuload() behavior
*   Thu Feb 18 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.0-16
-   Disabling network renaming
*   Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
-   veth patch: don’t modify ip_summed
*   Thu Feb 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-14
-   Full tickless -> idle tickless + simple CPU time accounting
-   SLUB -> SLAB
-   Disable NUMA balancing
-   Disable stack protector
-   No build_forced no-CBs CPUs
-   Disable Expert configuration mode
-   Disable most of debug features from 'Kernel hacking'
*   Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
-   Double tcp_mem limits, patch is added.
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-12
-   Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
*   Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 4.2.0-11
-   Revert CONFIG_HZ=250
*   Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
-   Fix for CVE-2016-0728
*   Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
-   CONFIG_HZ=250
*   Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
-   Remove rootfstype from the kernel parameter.
*   Mon Jan 04 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-7
-   Disabled all the tracing options in kernel config.
-   Disabled preempt.
-   Disabled sched autogroup.
*   Thu Dec 17 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-6
-   Enabled kprobe for systemtap & disabled dynamic function tracing in config
*   Fri Dec 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-5
-   Added oprofile kernel driver sub-package.
*   Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-4
-   Change the linux image directory.
*   Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-3
-   Added the build essential files in the dev sub-package.
*   Mon Nov 09 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-2
-   Enable Geneve module support for generic kernel.
*   Fri Oct 23 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
-   Upgraded the generic linux kernel to version 4.2.0 & and updated timer handling to full tickless mode. 
*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.9-5
-   Added driver support for frame buffer devices and ACPI
*   Wed Sep 2 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-4
-   Added mouse ps/2 module.
*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-3
-   Use photon.cfg as a symlink.
*   Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-2
-   Added environment file(photon.cfg) for grub.
*   Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
-   Upgrading kernel version.
*   Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19.2-5
-   Updated OVT to version 10.0.0.
-   Rename -gpu-drivers to -drivers-gpu in accordance to directory structure.
-   Added -sound package/
*   Tue Aug 11 2015 Anish Swaminathan<anishs@vmware.com> 3.19.2-4
-   Removed Requires dependencies. 
*   Fri Jul 24 2015 Harish Udaiya Kumar <hudaiyakumar@gmail.com> 3.19.2-3
-   Updated the config file to include graphics drivers.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.13.3-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version

