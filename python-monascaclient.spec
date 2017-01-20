%global pypi_name monascaclient
%global cliname   monasca

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Python client for monasca REST API

License:        ASL 2.0
URL:            https://github.com/openstack/python-monascaclient
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch

%description
Python client for monasca REST API. Includes python library for monasca API
and Command Line Interface (CLI) library.


%package -n     python2-%{pypi_name}
Summary:        Python client for monasca REST API
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  git
# Required for tests
BuildRequires:  python-fixtures
BuildRequires:  python-keystoneclient
BuildRequires:  python-mock
BuildRequires:  python-mox3
BuildRequires:  python-oslo-serialization
BuildRequires:  python-requests
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  PyYAML

Requires:       python-babel
Requires:       python-iso8601
Requires:       python-keystoneclient >= 3.8.0
Requires:       python-oslo-concurrency >= 3.8.0
Requires:       python-oslo-config >= 3.14.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 1.14.0
Requires:       python-oslo-middleware >= 3.0.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-service >= 1.10.0
Requires:       python-oslo-utils
Requires:       python-pbr
Requires:       python-prettytable
Requires:       python-requests >= 2.10.0
Requires:       PyYAML >= 3.10.0
Requires:       python-six >= 1.9.0

%description -n python2-%{pypi_name}
Python client for monasca REST API. Includes python library for monasca API
and Command Line Interface (CLI) library.


%package -n     python2-%{pypi_name}-tests
Summary:        Tests for Python client for monasca REST API

Requires:  python2-%{pypi_name} = %{version}-%{release}
Requires:  python-fixtures
Requires:  python-mock
Requires:  python-mox3
Requires:  python-testrepository
Requires:  python-testscenarios
Requires:  python-testtools

%description -n python2-%{pypi_name}-tests
Python client for monasca REST API. Includes python library for monasca API
and Command Line Interface (CLI) library.

This package contains the unit tests

# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Python client for monasca REST API
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6
# Required for tests
BuildRequires:  python3-fixtures
BuildRequires:  python3-keystoneclient
BuildRequires:  python3-mock
BuildRequires:  python3-mox3
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-requests
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-PyYAML

Requires:       python3-babel
Requires:       python3-iso8601
Requires:       python3-keystoneclient >= 3.8.0
Requires:       python3-oslo-concurrency >= 3.8.0
Requires:       python3-oslo-config >= 3.14.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-log >= 1.14.0
Requires:       python3-oslo-middleware >= 3.0.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-service >= 1.10.0
Requires:       python3-oslo-utils
Requires:       python3-pbr
Requires:       python3-prettytable
Requires:       python3-requests >= 2.10.0
Requires:       python3-PyYAML >= 3.10.0
Requires:       python3-six >= 1.9.0

%description -n python3-%{pypi_name}
Python client for monasca REST API. Includes python library for monasca API
and Command Line Interface (CLI) library.

%package -n     python3-%{pypi_name}-tests
Summary:        Tests for Python client for monasca REST API

Requires:  python3-%{pypi_name} = %{version}-%{release}
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-mox3
Requires:  python3-testrepository
Requires:  python3-testscenarios
Requires:  python3-testtools

%description -n python3-%{pypi_name}-tests
Python client for monasca REST API. Includes python library for monasca API
and Command Line Interface (CLI) library.

This package contains the unit tests
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/monasca %{buildroot}%{_bindir}/monasca-%{python3_version}
ln -s ./monasca-%{python3_version} %{buildroot}%{_bindir}/monasca-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/monasca %{buildroot}%{_bindir}/monasca-%{python2_version}
ln -s %{_bindir}/monasca-%{python2_version} %{buildroot}%{_bindir}/monasca-2
ln -s %{_bindir}/monasca-2 %{buildroot}%{_bindir}/monasca

# Install bash completion scripts
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
mv  %{buildroot}%{_datarootdir}/monasca.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/python-monascaclient

%check
%if 0%{?with_python3}
%{__python3} setup.py test
rm -rf .testrepository
%endif
%{__python2} setup.py test

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/monasca
%{_bindir}/monasca-2
%{_bindir}/monasca-%{python2_version}
%{_sysconfdir}/bash_completion.d/python-monascaclient
%exclude %{python2_sitelib}/%{pypi_name}/tests

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/%{pypi_name}/tests


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/monasca-%{python3_version}
%{_bindir}/monasca-3
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{pypi_name}/tests
%endif


%changelog
