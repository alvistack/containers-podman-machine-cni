# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: containernetworking-podman-machine
Epoch: 100
Version: 0.2.0
Release: 1%{?dist}
Summary: CNI plugin to provide port information for podman-machine
License: Apache-2.0
URL: https://github.com/containers/dnsname/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.23
BuildRequires: glibc-static
Requires: containernetworking-plugins
Requires: podman
Requires: podman-gvproxy

%description
This plugin collects the port information of the container and sends
information to a server on the host operating system. The information is
used by the server to open and close port mappings on the host. It is
only meant to be used in a podman-machine virtual machine.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
        go build \
            -mod vendor -buildmode pie -v \
            -ldflags "-s -w -X main.gitCommit=0749884b8d1a455c68da30789e37811ec0809d51" \
            -o ./bin/podman-machine github.com/containers/podman-machine-cni/plugins/meta/podman-machine

%install
install -Dpm755 -d %{buildroot}/opt/cni/bin
install -Dpm755 -t %{buildroot}/opt/cni/bin bin/podman-machine

%files
%license LICENSE
%dir /opt/cni
%dir /opt/cni/bin
/opt/cni/bin/*

%changelog
