%define major 0
%define libname %mklibname %{name}_ %{major}
%define devname %mklibname %{name} -d
%define girname %mklibname udisks-gir 2.0

Summary:	Disk Manager
Name:		udisks
Version:	2.10.90
Release:	3
License:	GPLv2+
Group:		System/Libraries
Url:		https://www.freedesktop.org/wiki/Software/udisks
Source0:	https://github.com/storaged-project/udisks/releases/download/%{name}-%{version}/udisks-%{version}.tar.bz2
Recommends:	%{name}-btrfs = %{EVRD}
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.31.13
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.31.13
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gudev-1.0) >= 186
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(libatasmart) >= 0.19
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.92
BuildRequires:	pkgconfig(polkit-agent-1) >= 0.92
BuildRequires:	pkgconfig(libsystemd) >= 230
BuildRequires:	systemd-rpm-macros
BuildRequires:	pkgconfig(libacl)
BuildRequires:	pkgconfig(blockdev)
BuildRequires:	pkgconfig(mount)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libconfig)
BuildRequires:	pkgconfig(libstoragemgmt)
BuildRequires:	iscsi-initiator-utils-devel
BuildRequires:	bd_mdraid-devel
BuildRequires:	bd_part-devel
BuildRequires:	bd_loop-devel
BuildRequires:	bd_lvm-devel
BuildRequires:	bd_swap-devel
BuildRequires:	bd_fs-devel
BuildRequires:	bd_btrfs-devel
BuildRequires:	bd_crypto-devel
BuildRequires:	bd_nvme-devel
BuildRequires:	%mklibname -d smart
BuildRequires:	intltool
BuildRequires:	gettext-devel
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	chrpath
BuildRequires:	xsltproc
# pull libblockdev plugins
Requires:	libblockdev-mdraid
Requires:	libblockdev-part
Requires:	libblockdev-loop
Requires:	libblockdev-swap
Requires:	libblockdev-fs
Requires:	libblockdev-crypto
Requires:	libblockdev-nvme
# for LUKS devices
Requires:	cryptsetup-luks
# needed to pull in the system bus daemon
Requires:	dbus >= 1.8.0
# for mkfs.vfat
Requires:	dosfstools
# for mkfs.ext3, mkfs.ext3, e2label
Requires:	e2fsprogs
# for partitioning
Requires:	gdisk
Requires:	parted
# for mlabel
Requires:	mtools
Requires:	ntfsprogs
# needed to pull in the udev daemon
Requires:	udev >= 186
# for mount, umount, mkswap
Requires:	util-linux
# for mkfs.xfs, xfs_admin
Requires:	xfsprogs
# flash friendly filesystem
Requires:	f2fs-tools
Requires:	btrfs-progs
Requires:	exfat-utils
# for /proc/self/mountinfo, only available in 2.6.26 or higher
Conflicts:	kernel < 2.6.26
%rename	udisks2
%rename	storaged
%{?systemd_requires}

%description
udisks provides a daemon, D-Bus API and command line tools for
managing disks and storage devices. This package is for the udisks 2.x
series.

%files -f %{name}.lang
%{_datadir}/dbus-1/system.d/org.freedesktop.UDisks2.conf
%{_sysconfdir}/udisks2/udisks2.conf
%{_sysconfdir}/udisks2/mount_options.conf.example
%{_datadir}/bash-completion/completions/udisksctl
%{_udevrulesdir}/80-udisks2.rules
%{_sbindir}/umount.udisks2
%dir %{_libexecdir}/udisks2
%{_libexecdir}/udisks2/udisksd
%{_bindir}/udisksctl
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%doc %{_mandir}/man8/*
%{_datadir}/polkit-1/actions/org.freedesktop.UDisks2.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.UDisks2.service
%{_presetdir}/86-%{name}.preset
%{_unitdir}/udisks2.service
%{_datadir}/zsh/site-functions/_udisks2
%dir %{_sysconfdir}/udisks2
%dir %{_sysconfdir}/udisks2/modules.conf.d
%dir %{_libdir}/udisks2
%dir %{_libdir}/udisks2/modules
# Permissions for local state data are 0700 to avoid leaking information
# about e.g. mounts to unprivileged users
%attr(0700,root,root) %dir %{_localstatedir}/lib/udisks2

#----------------------------------------------------------------------------
%(for i in btrfs iscsi lsm lvm2; do
	cat <<EOF
%package $i
Summary: $i support for udisks
Group: System/Libraries

%description $i
$i support for udisks

%files $i
%{_libdir}/udisks2/modules/libudisks2_$i.so
%{_datadir}/polkit-1/actions/org.freedesktop.UDisks2.$i.policy
EOF
	if [ "$i" = "lsm" ]; then
		cat <<EOF
%{_sysconfdir}/udisks2/modules.conf.d/udisks2_lsm.conf
EOF
	fi
done)

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Dynamic library to access the udisks daemon
License:	LGPLv2+
Group:		System/Libraries
Obsoletes:	%{_lib}udisks20 < 1.90.0-2

%description -n %{libname}
This package contains the dynamic library libudisks2, which provides
access to the udisks daemon. This package is for the udisks 2.x
series.

%files -n %{libname}
%{_libdir}/libudisks2.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
License:	LGPLv2+
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%files -n %{girname}
%{_libdir}/girepository-1.0/UDisks-2.0.typelib

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for libudev
License:	LGPLv2+
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains the development files for the library
libudisks2, a dynamic library, which provides access to the udisks
daemon. This package is for the udisks 2.x series.

%files -n %{devname}
%doc AUTHORS NEWS COPYING HACKING
%{_libdir}/libudisks2.so
%dir %{_includedir}/udisks2
%dir %{_includedir}/udisks2/udisks
%{_includedir}/udisks2/udisks/*.h
%{_datadir}/gir-1.0/UDisks-2.0.gir
%dir %{_datadir}/gtk-doc/html/udisks2
%{_datadir}/gtk-doc/html/udisks2/*
%{_libdir}/pkgconfig/udisks2.pc
%{_libdir}/pkgconfig/udisks2-btrfs.pc
%{_libdir}/pkgconfig/udisks2-iscsi.pc
%{_libdir}/pkgconfig/udisks2-lsm.pc
%{_libdir}/pkgconfig/udisks2-lvm2.pc

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%global optlags %{opflags} -Qunused-arguments

#NOCONFIGURE=yes gnome-autogen.sh
%configure \
	--enable-fhs-media \
	--enable-gtk-doc \
	--enable-btrfs \
	--enable-iscsi \
	--enable-lsm \
	--enable-lvm2 \
	--enable-modules \
	--disable-static \
	--with-udevdir="$(dirname %{_udevrulesdir})" \
	--with-systemdsystemunitdir="%{_unitdir}" \
	--with-tmpfilesdir=%{_tmpfilesdir} \
	--with-modloaddir=%{_modulesloaddir} \
	--with-modprobedir=%{_modprobedir}

%make_build

%install
%make_install

mkdir -p %{buildroot}/%{_localstatedir}/lib/udisks2

chrpath --delete %{buildroot}/%{_sbindir}/umount.udisks2
chrpath --delete %{buildroot}/%{_bindir}/udisksctl
chrpath --delete %{buildroot}/%{_libexecdir}/udisks2/udisksd

# (tpg) disable it by default
# https://github.com/storaged-project/udisks/issues/535
install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
disable udisks2.service
EOF

%find_lang %{name}2 %{name}.lang

%post -n %{name}
%systemd_post udisks2.service
if [ -S /run/udev/control ]; then
    udevadm control --reload
    udevadm trigger
fi

%preun -n %{name}
%systemd_preun udisks2.service

%postun -n %{name}
%systemd_postun_with_restart udisks2.service
