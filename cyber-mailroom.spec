Name:		cyber-mailroom
# 1.0.<Build>
Version:	%{!?version:1.0.0}%{?version}
# ${commit_count}_${git_commit}
Release:	%{!?release:1}%{?release}
Summary:	Cyberlife Mailroom API

Group:		Application
License:	GPL
URL:		http://www.cyber-life.cn/
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	python(abi) = 2.7
Requires:	systemd python(abi) = 2.7 nginx

%undefine __check_files

%description

%prep

%build
make

%install
make install DESTDIR=%{buildroot}

%post
/usr/bin/systemctl daemon-reload

for default_config in /etc/cyberlife/*mailroom*.default
do
        config=${default_config%.default}
        if [ ! -f $config ]; then
                cp $default_config $config
        fi
done

systemctl enable cyber-mailroom.service
systemctl restart cyber-mailroom.service
systemctl enable cyber-mailroom-swagger.service
systemctl restart cyber-mailroom-swagger.service
systemctl enable nginx.service
systemctl restart nginx.service

%postun
/usr/bin/systemctl daemon-reload

%files
/etc/cyberlife/*
/etc/nginx/location.d/*
/etc/nginx/conf.d/*
/opt/cyberlife/service/cyber-mailroom/*
/etc/systemd/system/*

%doc

%changelog
