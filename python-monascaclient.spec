%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9
%global pypi_name monascaclient
%global cliname   monasca

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order sphinx openstackdocstheme

%global common_desc \
Python client for monasca REST API. Includes python library for monasca API \
and Command Line Interface (CLI) library.

Name:           python-%{pypi_name}
Version:        2.8.0
Release:        1%{?dist}
Summary:        Python client for monasca REST API

License:        Apache-2.0
URL:            https://github.com/openstack/python-monascaclient
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        Python client for monasca REST API

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description -n python3-%{pypi_name}
%{common_desc}

%package -n     python3-%{pypi_name}-tests
Summary:        Tests for Python client for monasca REST API

Requires:  python3-%{pypi_name} = %{version}-%{release}
Requires:  python3-mock
Requires:  python3-stestr
Requires:  python3-testscenarios
Requires:  python3-testtools

%description -n python3-%{pypi_name}-tests
%{common_desc}

This package contains the unit tests

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cliname} %{buildroot}%{_bindir}/%{cliname}-3

rm -f %{buildroot}%{_datarootdir}/monasca.bash_completion

%check
%tox -e %{default_toxenv}

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-*.dist-info
%{_bindir}/%{cliname}
%{_bindir}/%{cliname}-3
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{pypi_name}/tests

%changelog
* Mon Sep 18 2023 RDO <dev@lists.rdoproject.org> 2.8.0-1
- Update to 2.8.0

