# Generated by rust2rpm 13
%bcond_without check
%global __cargo_skip_build 0

%global dracutmodulesdir %(pkg-config --variable=dracutmodulesdir dracut || echo '/usr/lib/dracut/modules.d')

%global crate afterburn

Name:           rust-%{crate}
Version:        4.3.1
Release:        1%{?dist}
Summary:        Simple cloud provider agent

# Upstream license specification: Apache-2.0
License:        ASL 2.0
URL:            https://crates.io/crates/afterburn
Source:         %{crates_source}
# Initial patched metadata
Patch0:         afterburn-fix-metadata.diff
# Use deprecated get_hostname calls so that hostname 0.1 can be used as
# a dependency. TODO: remove patch once at least hostname 0.2 is packaged
# in Fedora.
# https://github.com/svartalf/hostname/blob/master/CHANGELOG.md#020---2019-11-09
Patch1:         0001-Revert-providers-vagrant-fix-deprecated-calls.patch
# Use older request API so reqwest 0.9.24 can be used as a dependency.
# TODO: remove patch once at least reqwest 0.10.0 is packaged in Fedora.
# https://github.com/seanmonstar/reqwest/blob/master/CHANGELOG.md#v0100
Patch2:         0002-Revert-afterburn-update-to-new-reqwest-API.patch

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging
BuildRequires:  systemd

%global _description %{expand:
Simple cloud provider agent.}

%description %{_description}

%package     -n %{crate}
Summary:        %{summary}
%{?systemd_requires}

%description -n %{crate} %{_description}

%files       -n %{crate}
%license LICENSE
%doc README.md
%{_bindir}/afterburn
%{_unitdir}/afterburn.service
%{_unitdir}/afterburn-checkin.service
%{_unitdir}/afterburn-firstboot-checkin.service
%{_unitdir}/afterburn-sshkeys@.service

%post        -n %{crate}
%systemd_post afterburn.service
%systemd_post afterburn-checkin.service
%systemd_post afterburn-firstboot-checkin.service
%systemd_post afterburn-sshkeys@.service

%preun       -n %{crate}
%systemd_preun afterburn.service
%systemd_preun afterburn-checkin.service
%systemd_preun afterburn-firstboot-checkin.service
%systemd_preun afterburn-sshkeys@.service

%postun      -n %{crate}
%systemd_postun afterburn.service
%systemd_postun afterburn-checkin.service
%systemd_postun afterburn-firstboot-checkin.service
%systemd_postun afterburn-sshkeys@.service

%package     -n %{crate}-dracut
Summary:        Dracut modules for afterburn
BuildRequires:  pkgconfig(dracut)
Requires:       %{crate}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       dracut
Requires:       dracut-network

%description -n %{crate}-dracut
Dracut module that enables afterburn and corresponding services
to run in the initramfs on boot.

%files       -n %{crate}-dracut
%{dracutmodulesdir}/30afterburn/

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
# afterburn-sshkeys@.service is by default enabled for the 'core' user in
# Fedora CoreOS.
# Based on https://github.com/coreos/afterburn/blob/master/Makefile.
sed -e 's,@DEFAULT_INSTANCE@,core,' < \
  systemd/afterburn-sshkeys@.service.in > \
  systemd/afterburn-sshkeys@.service
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install
install -Dpm0644 -t %{buildroot}%{_unitdir} \
  systemd/*.service
mkdir -p %{buildroot}%{dracutmodulesdir}
cp -a dracut/* %{buildroot}%{dracutmodulesdir}

%if %{with check}
%check
%cargo_test
%endif

%changelog
* Fri Feb 07 2020 Robert Fairley <rfairley@redhat.com> - 4.3.1-1
- Update to 4.3.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Josh Stone <jistone@redhat.com> - 4.2.0-2
- Bump to nix 0.16, mockito 0.22

* Tue Oct 15 2019 Robert Fairley <rfairley@redhat.com> - 4.2.0-1
- Update to 4.2.0

* Sat Sep 21 13:11:54 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.1.3-1
- Update to 4.1.3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Robert Fairley <rfairley@redhat.com> - 4.1.2-1
- Update to 4.1.2

* Sat Jun 22 11:59:02 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.1.1-3
- Rename dracut subpackage

* Sat Jun 22 11:06:19 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.1.1-2
- Add dracut modules

* Fri Jun 21 2019 Robert Fairley <rfairley@redhat.com> - 4.1.1-1
- Update to 4.1.1
- Regenerate specfile using rust2rpm 10 with DynamicBuildRequires

* Wed Jun 05 2019 Josh Stone <jistone@redhat.com> - 4.1.0-3
- Bump nix to 0.14

* Wed May 22 17:17:00 CEST 2019 Robert Fairley <rfairley@redhat.com> - 4.1.0-2
- Add afterburn-sshkeys@.service patches to enable the unit on supported platfoms only

* Sat Apr 27 09:55:54 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.1.0-1
- Initial package
