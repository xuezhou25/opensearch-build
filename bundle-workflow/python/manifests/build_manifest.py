# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import yaml

'''
A BuildManifest is an immutable view of the outputs from a build step
The manifest contains information about the product that was built (in the `build` section),
and the components that made up the build in the `components` section.

The format for schema version 1.0 is:
schema-version: 1.0
build:
  name: string
  version: string
  architecture: x64 or arm64
components:
  - name: string
    repository: URL of git repository
    ref: git ref that was built (sha, branch, or tag)
    commitid: The actual git commit ID that was built (i.e. the resolved "ref")
    artifacts:
      maven:
        - maven/relative/path/to/artifact
        - ...
      plugins:
        - plugins/relative/path/to/artifact
        - ...
      libs:
        - libs/relative/path/to/artifact
        - ...
  - ...
'''
class BuildManifest:
    @staticmethod
    def from_file(path):
        with open(path, 'r') as file:
            return BuildManifest(yaml.safe_load(file))

    def __init__(self, data):
        self.version = str(data['schema-version'])
        if self.version != '1.0':
            raise ValueError(f'Unsupported schema version: {self.version}')
        self.build = self.Build(data['build'])
        self.components = list(map(lambda entry: self.Component(entry),
                                   data['components']))

    def to_dict(self):
        return {
            'schema-version': '1.0',
            'build': self.build.to_dict(),
            'components': list(map(lambda component: component.to_dict(),
                                   self.components))
        }

    class Build:
        def __init__(self, data):
            self.name = data['name']
            self.version = data['version']
            self.architecture = data['architecture']

        def to_dict(self):
            return {
                'name': self.name,
                'version': self.version,
                'architecture': self.architecture
            }

    class Component:
        def __init__(self, data):
            self.name = data['name']
            self.repository = data['repository']
            self.ref = data['ref']
            self.commitid = data['commitid']
            self.artifacts = data['artifacts']

        def to_dict(self):
            return {
                'name': self.name,
                'repository': self.repository,
                'ref': self.ref,
                'commitid': self.commitid,
                'artifacts': self.artifacts
            }
