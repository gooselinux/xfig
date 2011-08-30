%define app_defaults_dir %{_datadir}/X11/app-defaults

Summary: An X Window System tool for drawing basic vector graphics
Name: xfig
Version: 3.2.5
Release: 22.a.1%{?dist}
License: MIT
Group: Applications/Multimedia
URL: http://www.xfig.org/
# The new upstream 3.2.5a release was made available to me (Hans) by the Debian
# maintainer who is in contact with upstream, which appearantly is still
# somewhat alive (but not alive enough to put the tarbal on the homepage ??)
Source0: xfig.%{version}a.tar.gz
Source1: xfig.png
Source2: xfig.desktop
Source3: xfig.sh

Patch0: xfig-3.2.5a-default-apps.patch
Patch1: xfig-3.2.5-fhs.patch
Patch2: xfig-3.2.5-mkstemp.diff
Patch7: xfig.3.2.5-modularX.patch
Patch9: xfig.3.2.5-Xaw3d.patch
Patch10: xfig-3.2.5-enable-Xaw3d.patch
Patch11: xfig-3.2.5-color-resources.patch
Patch13: xfig-3.2.5-urwfonts.patch
Patch14: xfig-3.2.5-zoom-crash.patch
Patch15: xfig-3.2.5-missing-protos.patch
Patch17: xfig-3.2.5-rh490257.patch
Patch18: xfig-3.2.5-rh490259.patch
Patch19: xfig-3.2.5-debian.patch
Patch20: xfig-3.2.5-rh494193.patch

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: imake
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: libX11-devel
BuildRequires: libXaw-devel
BuildRequires: libXext-devel
BuildRequires: libXi-devel
BuildRequires: libXmu-devel
BuildRequires: libXpm-devel
BuildRequires: libXt-devel
BuildRequires: Xaw3d-devel
BuildRequires: desktop-file-utils

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: %{name}-common = %{version}-%{release}
Provides: %{name}-executable = %{version}-%{release}
# Xaw3d used to be the one in a subpackage, now the plain Xaw version is
Obsoletes: %{name}-Xaw3d <= 3.2.5-7.fc8
Provides: %{name}-Xaw3d = %{version}-%{release}

%description
Xfig is an X Window System tool for creating basic vector graphics,
including bezier curves, lines, rulers and more.  The resulting
graphics can be saved, printed on PostScript printers or converted to
a variety of other formats (e.g., X11 bitmaps, Encapsulated
PostScript, LaTeX).

You should install xfig if you need a simple program to create vector
graphics.


%package plain
Summary:        Plain Xaw version of xfig
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Provides:       %{name}-executable = %{version}-%{release}

%description plain
Plain Xaw version of xfig, an X Window System tool for creating basic vector
graphics, including bezier curves, lines, rulers and more. The normal xfig
package uses the more modern / prettier looking Xaw3d toolkit, whereas this
version uses the very basic Xaw toolkit. Unless you really know you want this
version you probably don't want this version.


%package common
Summary:        Common xfig files
Group:          Applications/Multimedia
Requires:       transfig >= 1:3.2.5, xdg-utils, enchant, urw-fonts
Requires:       hicolor-icon-theme
Requires:       xorg-x11-fonts-base
# So that this will get uninstalled together with xfig / xfig-Xaw3d
Requires:       %{name}-executable = %{version}-%{release}
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description common
Files common to both the plain Xaw and the Xaw3d version of xfig.


%prep
%setup -q -n xfig.%{version}a
%patch0 -p1 -b .redhat
%patch1 -p1 -b .fhs
%patch2 -p1 -b .mkstemp
%patch7 -p1 -b .modularX
%patch9 -p1 -b .Xaw3d
%patch10 -p1 -b .no-Xaw3d
%patch11 -p1 -b .color-resources
%patch13 -p1 -b .urw
%patch14 -p1 -b .zoom-crash
%patch15 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
rm Doc/html/images/sav1a0.tmp


%build
# First build the Xaw3d version
xmkmf
# make sure cmdline option parsing still works despite us renaming the binary
sed -i 's/"xfig"/"xfig-Xaw3d"/' main.c
make XFIGDOCDIR=%{_docdir}/%{name}-%{version} \
     CDEBUGFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fno-strength-reduce -fno-strict-aliasing"
mv xfig xfig-Xaw3d
make distclean

# And then build the normal Xaw version
mv Imakefile.no-Xaw3d Imakefile
xmkmf
# make sure cmdline option parsing still works despite us renaming the binary
sed -i 's/"xfig-Xaw3d"/"xfig-plain"/' main.c
make XFIGDOCDIR=%{_docdir}/%{name}-%{version} \
     CDEBUGFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fno-strength-reduce -fno-strict-aliasing"


%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} XFIGDOCDIR=%{_docdir}/%{name}-%{version} \
     INSTALL="install -p" install.all
install -p -m 644 CHANGES README LATEX.AND.XFIG* FIGAPPS \
  %{buildroot}%{_docdir}/%{name}-%{version}

# install the Xaw3d version and the wrapper for the .desktop file
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}-plain
install -p -m 755 %{SOURCE3} %{buildroot}%{_bindir}/%{name}
install -m 755 %{name}-Xaw3d %{buildroot}%{_bindir}

# remove the map generation scripts, these are for xfig developers only
rm %{buildroot}%{_datadir}/%{name}/Libraries/Maps/{USA,Canada}/assemble

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps \
         %{buildroot}%{_datadir}/applications

install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps

desktop-file-install --vendor fedora         \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE2}

# remove app-defaults symlink which gets installed
rm %{buildroot}%{_prefix}/lib*/X11/app-defaults


%clean
rm -rf %{buildroot}


%post common
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun common
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}-Xaw3d

%files plain
%defattr(-,root,root,-)
%{_bindir}/%{name}-plain

%files common
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/*/*
%{app_defaults_dir}/*
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 3.2.5-22.a.1
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-22.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 28 2009 Caolán McNamara <caolanm@redhat.com> 3.2.5-21.a
- Resolves: rhbz#506791 make xfig spellchecking work

* Wed Jun  3 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-20.a
- Fix eps preview (#503911)

* Wed Apr  8 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-19.a
- Fix crash when printing (#494193), thanks to Ian Dall for the patch

* Fri Mar 27 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-18.a
- Rebase to new upstream 3.2.5a release, this was made available to me by
  the Debian maintainer who is in contact with upstream, which appearantly
  is still somewhat alive (but not alive enough to put the tarbal on the
  homepage ??)

* Sun Mar 15 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-17
- Add various patches from Debian (doc updates, new figures in the lib,
  better fix for modepanel resizing)
- Do not crash when inserting a character from the charmap into a text string

* Sun Mar 15 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-16
- Fix Text size field inserts characters on left instead of right (#490257)
- Fix xfig-Xaw3d does not display messages in message panel (#490259)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Hans de Goede <hdegoede@redhat.com> 3.2.5-14
- Add missing Requires: xorg-x11-fonts-base (#486701)

* Mon Nov 10 2008 Stepan Kasal <skasal@redhat.com> - 3.2.5-13
- fix the Obsoletes tag to <= 3.2.5-7.fc8, which is the last
  release with Xaw3d subpackage

* Tue Nov  4 2008 Hans de Goede <hdegoede@redhat.com> 3.2.5-12
- Various small specfile cleanups from merge review

* Mon Jul 14 2008 Ian Hutchinson <ihutch@mit.edu> 3.2.5-11
- Fix incorrect height of modepanel.

* Thu Apr  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.5-10
- Fix missing prototype compiler warnings

* Thu Feb 28 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.5-9
- Fix cmdline parsing (broken by renaming the binary) (bz 435097)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.2.5-8
- Autorebuild for GCC 4.3

* Wed Dec 12 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.5-7
- Fix xfig crashing when zooming in a lot (bz 420411)

* Sat Nov 17 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.5-6
- Put the Xaw3d version in the main xfig package, put the plain Xaw version
  in a -plain subpackage

* Fri Nov 16 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.2.5-5
- Also compile a version against Xaw3d instead of plain Xaw, available in the
  new xfig-Xaw3d package
- Various specfile cleanups for packaging guidelines compliance
- Remove spurious executable permissions on various files (bz 247424)
- Apply patch fixing problems with xfig not finding fonts (bz 210278)

* Thu Nov 15 2007 Than Ngo <than@redhat.com> 3.2.5-4
- fix #201992, xfig crashes in the edit function

* Thu Nov 15 2007 Than Ngo <than@redhat.com> 3.2.5-3
- fix #201992, xfig crashes in the edit function

* Fri Oct 05 2007 Than Ngo <than@redhat.com> - 3.2.5-2
- rh#313321, use xdg-open

* Mon Apr 16 2007 Than Ngo <than@redhat.com> - 3.2.5-1.fc7
- 3.2.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.2.4-21.1
- rebuild

* Tue May 16 2006 Than Ngo <than@redhat.com> 3.2.4-21
- fix #191816, Xaw3d build problem 

* Fri May 05 2006 Than Ngo <than@redhat.com> 3.2.4-20
- fix #169330, wrong docdir
- fix #187902, no parameter negotiation for xfig
- fix #182451, switch xfig's pdf viewer to evince

* Tue Apr 25 2006 Adam Jackson <ajackson@redhat.com> 3.2.4-19
- Rebuild for updated imake build rules

* Tue Apr 04 2006 Than Ngo <than@redhat.com> 3.2.4-18
- no parameter negotiation for xfig, fix #187902

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.2.4-17.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.2.4-17.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 21 2005 Than Ngo <than@redhat.com> 3.2.4-17
- workaround for utf8

* Sun Dec 18 2005 Than Ngo <than@redhat.com> 3.2.4-16
- add correct app-defaults directory

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 15 2005 Than Ngo <than@redhat.com> 3.2.4-15
- fix for modular X 

* Mon Oct 24 2005 Than Ngo <than@redhat.com> 3.2.4-14
- enable xpm support #158422 

* Tue Jul 19 2005 Than Ngo <than@redhat.com> 3.2.4-13
- buildrequires on xorg-x11-devel

* Mon Jul 18 2005 Than Ngo <than@redhat.com> 3.2.4-12
- fix another buffer overflow #163413

* Thu May 19 2005 Than Ngo <than@redhat.com> 3.2.4-11
- apply patch to fix buffer overflow #158088

* Mon Mar 21 2005 Than Ngo <than@redhat.com> 3.2.4-10
- fix font warning #116542

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 3.2.4-9
- cleanup

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 3.2.4-8
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 3.2.4-7
- rebuilt

* Sat Sep 25 2004 Than Ngo <than@redhat.com> 3.2.4-6
- add mimetype spec #131629

* Mon Sep 13 2004 Than Ngo <than@redhat.com> 3.2.4-5
- fix desktop file #131983

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Tue May  6 2003 Than Ngo <than@redhat.com> 3.2.4-1
- 3.2.4

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Nov  7 2002 Than Ngo <than@redhat.com> 3.2.3d-11
- rebuild in new enviroment

* Thu Aug 22 2002 Than Ngo <than@redhat.com> 3.2.3d-10
- close should get fd, not filename

* Wed Jul 31 2002 Than Ngo <than@redhat.com> 3.2.3d-9
- Fixed typo bug (bug #70347)

* Wed Jul 24 2002 Than Ngo <than@redhat.com> 3.2.3d-8
- desktop file issue (bug #69543)

* Tue Jun 25 2002 Than Ngo <than@redhat.com> 3.2.3d-7
- add patch file using mkstemp (bug #67351)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jul 13 2001 Than Ngo <than@redhhat.com> 3.2.3d-3
- fix build dependencies (bug #48910)

* Tue Jul 03 2001 Than Ngo <than@redhat.com>
- fix export to eps when i18n set (bug #45114)
- requires transfig-3.2.3d

* Fri Jun 15 2001 Than Ngo <than@redhat.com>
- update to 3.2.3d release

* Tue Jun 12 2001 Than Ngo <than@redhat.com>
- fix to build against XFree86-4.1.0

* Tue May 29 2001 Than Ngo <than@redhat.com>
- update to 3.2.3d beta2 fixes (Bug #42597, #42556)
- fix bug when LANG is set, launching help gives a spurious error (Bug #42596)
- fix bug in resource setting (Bug #42595)
- remove some patches, which are included in 3.2.3d beta2
- fix wrong version number
- use make install.all
- fix fhs problem

* Wed May  9 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't require Netscape at all - use htmlview (which automatically launches
  Netscape, Mozilla or Konqueror depending on what is installed/running).
  No need to depend on proprietary stuff...

* Thu Apr 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do the same for s390x

* Sat Jan 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- only require /usr/bin/netscape if not on S390

* Tue Dec 20 2000 Yukihiro Nakai <ynakai@redhat.com>
- Delete enable_japanese macro and set i18n default.
- Fix Japanese translation in .desktop file

* Mon Nov 20 2000 Than Ngo <than@redhat.com>
- rebuilt to fix bad dir perms

* Thu Nov 9 2000 Than Ngo <than@redhat.com>
- fixed f_read, which made xfig stop reading the file after
  removing such bad objects.

* Fri Oct 13 2000 Preston Brown <pbrown@redhat.com>
- improved .desktop entry

* Thu Aug 24 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese patch

* Tue Aug 08 2000 Than Ngo <than@redhat.de>
- fixed dependency problem
- fixed starting xpdf

* Mon Aug 07 2000 Than Ngo <than@redhat.de>
- fixed for using xpdf instead acroreader (Bug #15621)
- add requires: netscape, display

* Sat Aug 05 2000 Than Ngo <than@redhat.de>
- update to 3.2.3c (bugs fixed released)
- fix parse_printcap broken (Bug #11147)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 23 2000 Than Ngo <than@redhat.de>
- xfig crash, if a menu item was clicked (Bug #12855)

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- rebuilt in the new build environment
- enable optimization
 
* Sat Jun 03 2000 Than Ngo <than@redhat.de>
- fix requires, xfig-3.2.3a requires transfig-2.2.3 or newer
- disable optimization -O2 (gcc-2.96 Bug) on i386

* Thu May 18 2000 Preston Brown <pbrown@redhat.com>
- fix buildroot issue in Imakefile

* Mon May  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with current libXaw3d
- update to 3.2.3a

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages

* Fri Jan 14 2000 Preston Brown <pbrown@redhat.com>
- upgrade to beta1 of 2.2.3.  Hopefully this fixes outstanding issues.
- no need for vararg fix, commented out

* Thu Sep 23 1999 Preston Brown <pbrown@redhat.com>
- add icon
- don't compile with optimization on alpha

* Mon Aug 30 1999 Preston Brown <pbrown@redhat.com>
- converted to use a .desktop file

* Fri Mar 26 1999 Michael Maher <mike@redhat.com>
- added files that were missing. 

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)
- varargs fix

* Thu Feb 18 1999 Jeff Johnson <jbj@redhat.com>
- correct DESTDIRR typo (#962)

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul  7 1998 Jeff Johnson <jbj@redhat.com>
- updated to 3.2.2.

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- updated for manhattan
- buildroot

* Thu Oct 23 1997 Marc Ewing <marc@redhat.com>
- new version
- messed with config for 5.0
- updated Requires and Copyright
- added wmconfig

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
