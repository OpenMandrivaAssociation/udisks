%define major 0
%define libname %mklibname %{name}_ %{major}
%define devname %mklibname %{name} -d
%define girname %mklibname udisks-gir 2.0

Summary:	Disk Manager
Name:		udisks2
Version:	2.1.7
Release:	1
License:	GPLv2+
Group:		System/Libraries
Url:		http://www.freedesktop.org/wiki/Software/udisks
Source0:	http://udisks.freedesktop.org/releases/udisks-%{version}.tar.bz2
Patch0:		udisks-1.92.0-link.patch
# (tpg) from upstream git
Patch1:		0000-Reread-partition-table-before-wiping-when-creating-n.patch
# Mount to /media
Patch3:		udisks-2.1.4-no-multiseat.patch
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.31.13
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.31.13
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gudev-1.0) >= 186
BuildRequires:	pkgconfig(libatasmart) >= 0.19
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.92
BuildRequires:	pkgconfig(polkit-agent-1) >= 0.92
BuildRequires:	pkgconfig(libsystemd-login) >= 186
BuildRequires:	pkgconfig(libsystemd-daemon) >= 220
BuildRequires:	intltool
BuildRequires:	gnome-common
BuildRequires:	gettext-devel
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	pkgconfig(systemd)
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
# for /proc/self/mountinfo, only available in 2.6.26 or higher
Conflicts:	kernel < 2.6.26

%description
udisks provides a daemon, D-Bus API and command line tools for
managing disks and storage devices. This package is for the udisks 2.x
series.

%files -f %{name}.lang
%doc README AUTHORS NEWS COPYING HACKING
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.UDisks2.conf
%{_datadir}/bash-completion/completions/udisksctl
/lib/udev/rules.d/80-udisks2.rules
%{_sbindir}/umount.udisks2
%dir %{_libexecdir}/udisks2
%{_libexecdir}/udisks2/udisksd
%{_bindir}/udisksctl
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/polkit-1/actions/org.freedesktop.udisks2.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.UDisks2.service
%{_unitdir}/udisks2.service
# Permissions for local state data are 0700 to avoid leaking information
# about e.g. mounts to unprivileged users
%attr(0700,root,root) %dir %{_localstatedir}/lib/udisks2

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
%{_libdir}/libudisks2.so
%dir %{_includedir}/udisks2
%dir %{_includedir}/udisks2/udisks
%{_includedir}/udisks2/udisks/*.h
%{_datadir}/gir-1.0/UDisks-2.0.gir
%dir %{_datadir}/gtk-doc/html/udisks2
%{_datadir}/gtk-doc/html/udisks2/*
%{_libdir}/pkgconfig/udisks2.pc

#----------------------------------------------------------------------------

%prep
%setup -q -n udisks-%{version}
%apply_patches

%build
%global optlags %{opflags} -Qunused-arguments

NOCONFIGURE=yes gnome-autogen.sh
%configure \
	--enable-fhs-media \
	--enable-gtk-doc \
	--disable-static \
	--with-systemdsystemunitdir=%{_unitdir}
%make

%install
%makeinstall_std

mkdir -p %{buildroot}/%{_localstatedir}/lib/udisks2

%find_lang %{name} %{name}.lang
