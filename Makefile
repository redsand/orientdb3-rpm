.PHONY:	rpm clean

ORIENTDB_VERSION ?= 3.0.22
INT_VERSION ?= 21000
VERSION = $(shell echo $(ORIENTDB_VERSION) | sed "s/-/_/")
BUILD_NUMBER ?= 1
TARBALL_NAME = orientdb-$(ORIENTDB_VERSION)
TARBALL = $(TARBALL_NAME).tar.gz
TARBALL_URL = https://s3.us-east-2.amazonaws.com/orientdb3/releases/${ORIENTDB_VERSION}/orientdb-${ORIENTDB_VERSION}.tar.gz
TOPDIR = /tmp/orientdb-rpm
PWD = $(shell pwd)

rpm:
	@wget "${TARBALL_URL}" -O ${TARBALL}
	@rpmbuild -v -bb \
			--define "version $(VERSION)" \
			--define "int_version $(INT_VERSION)" \
			--define "orientdb_version $(ORIENTDB_VERSION)" \
			--define "build_number $(BUILD_NUMBER)" \
			--define "tarball $(TARBALL)" \
			--define "tarball_name $(TARBALL_NAME)" \
			--define "_sourcedir $(PWD)" \
			--define "_rpmdir $(PWD)" \
			--define "_topdir $(TOPDIR)" \
			orientdb.spec

clean:
	@rm -rf $(TOPDIR) x86_64
	@rm -f $(TARBALL)

$(TARBALL):
	@spectool \
			--define "version $(VERSION)" \
			--define "int_version $(INT_VERSION)" \
			--define "orientdb_version $(ORIENTDB_VERSION)" \
			--define "tarball $(TARBALL)" \
			-g orientdb.spec
