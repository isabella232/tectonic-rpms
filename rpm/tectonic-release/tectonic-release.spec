%define release_name BlackMaple
%define dist_version 7
%define bug_version prerelease
%define registry_domain quay.io
%define key_fingerprint bff313cdaa560b16a8987b8f72abf5f6799d33bc

Summary:        Tectonic release files and repository configuration
Name:           tectonic-release
Version:        %{dist_version}
Release:        1%{?dist}
License:        ASL 2.0
Group:          System Environment/Base
URL:            https://coreos.com/tectonic
Source0:        mirrors-tectonic
Source1:        RPM-GPG-KEY-Tectonic
Source2:        Tectonic-Legal-README.txt
Source3:        %{registry_domain}-%{key_fingerprint}

BuildArch:      noarch
Requires:       systemd >= 219

%description
Tectonic release files including the /etc/tectonic-version file, signing keys
and RPM repository files.

%prep

%setup -cT
cp -p %{SOURCE0} .
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .
cp -p %{SOURCE3} .
chmod -Rf a+rX,u+w,g-w,o-w .
sed -i 's|@@VERSION@@|%{dist_version}|g' Tectonic-Legal-README.txt

%{__cat} <<-TECTONIC-EOF > tectonic.repo
	[tectonic]
	name=Tectonic distribution of Kubernetes for RHEL \$releasever by CoreOS
	baseurl=https://yum.prod.coreos.systems/repo/tectonic-rhel/\$releasever/\$basearch/
	mirrorlist=https://yum.prod.coreos.systems/repo/\$releasever/mirrorlist
	enabled=1
	gpgcheck=1
	gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-Tectonic
	protect=0
TECTONIC-EOF

%build

%install
install -d %{buildroot}%{_sysconfdir}/{yum.repos.d,pki/rpm-gpg,rkt/trustedkeys/prefix.d/%{registry_domain}}
echo "Tectonic release %{version} (%{release_name})" > %{buildroot}%{_sysconfdir}/tectonic-release
install -p -m 644 tectonic.repo %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/
install -p -m 664 %{SOURCE3} %{buildroot}%{_sysconfdir}/rkt/trustedkeys/prefix.d/%{registry_domain}/%{key_fingerprint}

# Symlink the -release files
ln -s tectonic-release %{buildroot}%{_sysconfdir}/kubernetes-release


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license Tectonic-Legal-README.txt
%config %{_sysconfdir}/yum.repos.d/tectonic.repo
%config %attr(0644,root,root) %{_sysconfdir}/tectonic-release
%{_sysconfdir}/kubernetes-release
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-Tectonic
%attr(0664,root,rkt-admin) %{_sysconfdir}/rkt/trustedkeys/prefix.d/%{registry_domain}/%{key_fingerprint}

%changelog
* Tue Jul 25 2017 Brian 'redbeard' Harrington <brian.harrington@coreos.com> 7-1
- "nit: Gratuitous version bump for readability"

* Wed Jul 12 2017 Brian 'redbeard' Harrington <brian.harrington@coreos.com> 1.6.2-5
- "bug/yum: dist macro used in place of $releasever"

* Fri Jun 02 2017 Brian 'redbeard' Harrington <brian.harrington@coreos.com> 1.6.2-4
- Yum repo URL Update (brian.harrington@coreos.com)
- Automatic commit of package [tectonic-release] release [1.6.2-3].
  (brian.harrington@coreos.com)
- release: Catching up on 1.6.2 release changes (redbeard@dead-city.org)

* Fri Jun 02 2017 Brian 'redbeard' Harrington <brian.harrington@coreos.com> 1.6.2-3
- fix: tectonic-release does not depend on rkt
- fix: Incorrect version in specfile

* Thu May 25 2017 Brian 'redbeard' Harrington <brian.harrington@coreos.com> - 1.6.2-1
- Packaged Tectonic release 1.6.2-1

* Thu Apr 27 2017 Brian 'redbeard' Harrington <brian.harrington@coreos.com> - 1.5.7-1
- Packaged Tectonic release 1.5.7-1
- Includes license definition, repo file, GPG, and an initial mirrorlist.
